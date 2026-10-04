from sample.models import Category, Product

class ProductService:
    def create_product(name, category_id):
        name = name.strip()
        if not name:
            raise ValueError("Product name cannot be empty.")
        category = Category.objects.filter(id=category_id).first()
        if not category:
            raise ValueError("Category does not exist.")
        return Product.objects.create(product_name=name, category=category)

    def create_sub_product(name, parent_product_id):
        name = name.strip()
        if not name:
            raise ValueError("Product name cannot be empty.")
        parent_product = Product.objects.filter(id=parent_product_id).first()
        if not parent_product:
            raise ValueError("Parent product does not exist.")
        return Product.objects.create(
            product_name=name,
            category=parent_product.category,
            parent_product=parent_product,
        )

    def update_product(product_id, name):
        name = name.strip()
        if not name:
            raise ValueError("Product name cannot be empty.")
        product = Product.objects.filter(id=product_id).first()
        if not product:
            raise ValueError("Product does not exist.")
        product.product_name = name
        product.save(update_fields=["product_name"])
        return product

    def delete_product(product_id):
        product = Product.objects.filter(id=product_id).first()
        if not product:
            raise ValueError("Product does not exist.")
        product.delete()

    def move_product(product_id, target_category_id=None, target_parent_product_id=None):
        product = Product.objects.filter(id=product_id).first()
        if not product:
            raise ValueError("Product does not exist.")

        if target_parent_product_id is not None:
            if product.id == target_parent_product_id:
                raise ValueError("A product cannot be moved inside itself.")

            target_parent = Product.objects.filter(id=target_parent_product_id).first()
            if not target_parent:
                raise ValueError("Target parent product does not exist.")

            if ProductService.is_descendant(product, target_parent):
                raise ValueError("A product cannot be moved inside its own descendant.")

            if product.category_id != target_parent.category_id:
                raise ValueError("A product and its parent must belong to the same category.")

            product.parent_product = target_parent
        else:
            if target_category_id is None:
                raise ValueError("Target category is required.")

            category = Category.objects.filter(id=target_category_id).first()
            if not category:
                raise ValueError("Target category does not exist.")

            product.category = category
            product.parent_product = None

        product.save(update_fields=["category", "parent_product"])
        ProductService.descendant_categories(product.id, product.category_id)
        return product


    def descendant_categories(product_id, category_id):
        child_ids = list(
            Product.objects.filter(parent_product_id=product_id)
            .values_list("id", flat=True)
        )
        if not child_ids:
            return

        Product.objects.filter(id__in=child_ids).update(category_id=category_id)
        for child_id in child_ids:
            ProductService.descendant_categories(child_id, category_id)

    def is_descendant(product, possible_descendant):
        current = possible_descendant
        while current.parent_product_id is not None:
            if current.parent_product_id == product.id:
                return True
            current = current.parent_product
        return False


    def update_product(product_id, name):
        name = name.strip()
        if not name:
            raise ValueError("Product name cannot be empty")
        product = Product.objects.filter(id=product_id).first()
        if not product:
            raise ValueError("Product does not exist")
        product.product_name = name
        product.save(update_fields=["product_name"])
        return product

    def delete_product(product_id):
        product = Product.objects.filter(id=product_id).first()
        if not product:
            raise ValueError("Product does not exist")
        product.delete()

    def move_product(product_id, target_category_id=None, target_parent_product_id=None):
        product = Product.objects.filter(id=product_id).first()
        if not product:
            raise ValueError("Product does not exist")

        if target_parent_product_id is not None:
            if product.id == target_parent_product_id:
                raise ValueError("A product cannot be moved inside itself")

            target_parent = Product.objects.filter(id=target_parent_product_id).first()
            if not target_parent:
                raise ValueError("Target parent product does not exist")

            if ProductService.is_desc(product, target_parent):
                raise ValueError("A product cannot be moved inside its own sub_child_product")
 
            if product.category_id != target_parent.category_id:
                raise ValueError("A product and its parent must belong to the same category")

            product.parent_product = target_parent
        else:
            if target_category_id is None:
                raise ValueError("Target category is required.")

            category = Category.objects.filter(id=target_category_id).first()
            if not category:
                raise ValueError("Target category does not exist.")

            product.category = category
            product.parent_product = None

        product.save(update_fields=["category", "parent_product"])
        ProductService.desc_categories(product.id, product.category_id)
        return product


    def desc_categories(product_id, category_id):
        child_ids = list(
            Product.objects.filter(parent_product_id=product_id)
            .values_list("id", flat=True)
        )
        if not child_ids:
            return

        Product.objects.filter(id__in=child_ids).update(category_id=category_id)
        for child_id in child_ids:
            ProductService.desc_categories(child_id, category_id)

    def is_desc(product, possible_desc):
        current = possible_desc
        while current.parent_product_id is not None:
            if current.parent_product_id == product.id:
                return True
            current = current.parent_product
        return False
