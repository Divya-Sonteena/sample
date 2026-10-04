from django.shortcuts import render, redirect
from django.db import IntegrityError, transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Category, Product
from .services.category_service import CategoryService
from .services.product_service import ProductService

def loop(product):
    return {
        "id": product.id,
        "product_name": product.product_name,
        "sub_products": [loop(sub) for sub in product.sub_products.all()]
    }

def Add(category):
    return {
        "id": category.id,
        "name": category.name,
        "children": [Add(child) for child in category.children.all()],
        "products": [
            loop(p)
            for p in category.products.filter(parent_product__isnull=True)
        ]
    }

class CategoryView(APIView):
    def get(self, request):
        root = Category.objects.filter(parent__isnull=True).prefetch_related(
            'children__products', 'products', 'products__sub_products'
        )
        cat_data = [Add(cat) for cat in root]
        uncategorized_products = [
            loop(product)
            for product in Product.objects.filter(
                category__isnull=True,
                parent_product__isnull=True,
            )
        ]
        return render(request, "store.html", {
            "categories": cat_data,
            "uncategorized_products": uncategorized_products,
            "all_categories": Category.objects.order_by("name"),
            "all_products": Product.objects.select_related("category").order_by("product_name"),
        })
       
    def post(self, request):
        action = request.data.get('action')
        name = request.data.get('name')
        if action in {"create_root", "create_sub", "update"}:
            if not isinstance(name, str) or not name.strip():
                return Response({"error": "Enter a category name."}, status=400)
            name = name.strip()

        try:
            with transaction.atomic():
                if action == "create_root":
                    Category.objects.create(name=name)
                elif action == "create_sub":
                    parent_cat = Category.objects.filter(id=request.data.get('parent_id')).first()
                    if not parent_cat:
                        return Response({"error": "Parent category does not exist."}, status=400)
                    Category.objects.create(name=name, parent=parent_cat)
                elif action == "update":
                    category = Category.objects.filter(id=request.data.get('category_id')).first()
                    if not category:
                        return Response({"error": "Category does not exist."}, status=400)
                    if category.name == name:
                        return Response({"message": "No changes to save."})
                    category.name = name
                    category.save(update_fields=["name"])
                elif action == "delete":
                    category = Category.objects.filter(id=request.data.get('category_id')).first()
                    if not category:
                        return Response({"error": "Category does not exist."}, status=400)
                    category.delete()
                else:
                    return Response({"error": "Unknown category action."}, status=400)
        except IntegrityError:
            return Response({"error": "A category with this name already exists."}, status=400)
        return Response({"message": "Saved.", "reload": True})

class ProductView(APIView):
    def post(self, request):
        action = request.data.get('action')
        name = request.data.get('name')
        if action in {"create_product", "create_sub_product", "update"}:
            if not isinstance(name, str) or not name.strip():
                return Response({"error": "Enter a product name."}, status=400)
            name = name.strip()

        if action in {"create_product", "create_sub_product"} and Product.objects.filter(product_name=name).exists():
            return Response({"error": "A product with this name already exists."}, status=400)
        if action == "update" and Product.objects.filter(product_name=name).exclude(
            id=request.data.get('product_id')
        ).exists():
            return Response({"error": "A product with this name already exists."}, status=400)

        try:
            with transaction.atomic():
                if action == "create_product":
                    category = Category.objects.filter(id=request.data.get('category_id')).first()
                    if not category:
                        return Response({"error": "Category does not exist."}, status=400)
                    Product.objects.create(product_name=name, category=category)
                elif action == "create_sub_product":
                    parent_prod = Product.objects.filter(id=request.data.get('parent_product_id')).first()
                    if not parent_prod:
                        return Response({"error": "Parent product does not exist."}, status=400)
                    Product.objects.create(
                        product_name=name,
                        category=parent_prod.category,
                        parent_product=parent_prod
                    )
                elif action == "update":
                    product = Product.objects.filter(id=request.data.get('product_id')).first()
                    if not product:
                        return Response({"error": "Product does not exist."}, status=400)
                    if product.product_name == name:
                        return Response({"message": "No changes to save."})
                    product.product_name = name
                    product.save(update_fields=["product_name"])
                elif action == "delete":
                    product = Product.objects.filter(id=request.data.get('product_id')).first()
                    if not product:
                        return Response({"error": "Product does not exist."}, status=400)
                    product.delete()
                else:
                    return Response({"error": "Unknown product action."}, status=400)
        except IntegrityError:
            return Response({"error": "Could not save the product because of a database constraint."}, status=400)
        return Response({"message": "Saved.", "reload": True})
class MoveCategoryView(APIView):
    def post(self, request):
        try:
            CategoryService.move_category(
                request.data.get("category_id"),
                request.data.get("target_parent_id")
            )
            return redirect("/store/")
        except ValueError as e:
            return Response({"error": str(e)}, status=400)

class MoveProductView(APIView):
    def post(self, request):
        try:
            ProductService.move_product(
                request.data.get("product_id"),
                request.data.get("target_category_id"),
                request.data.get("target_parent_product_id")
            )
            return redirect("/store/")
        except ValueError as e:
            return Response({"error": str(e)}, status=400)
