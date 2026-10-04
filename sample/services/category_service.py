from sample.models import Category

class CategoryService:
    def create_root_category(name):
        name = name.strip()
        if not name:
            raise ValueError("Category name cannot be empty.")
        return Category.objects.create(name=name)

    def create_sub_category(name, parent_id):
        name = name.strip()
        if not name:
            raise ValueError("Category name cannot be empty.")
        parent = Category.objects.filter(id=parent_id).first()
        if not parent:
            raise ValueError("Parent category does not exist.")
        return Category.objects.create(name=name, parent=parent)

    def update_category(category_id, name):
        name = name.strip()
        if not name:
            raise ValueError("Category name cannot be empty.")
        category = Category.objects.filter(id=category_id).first()
        if not category:
            raise ValueError("Category does not exist.")
        category.name = name
        category.save(update_fields=["name"])
        return category

    def delete_category(category_id):
        category = Category.objects.filter(id=category_id).first()
        if not category:
            raise ValueError("Category does not exist.")
        category.delete()

    def move_category(category_id, target_parent_id=None):
        category = Category.objects.filter(id=category_id).first()
        if not category:
            raise ValueError("Category does not exist.")

        if target_parent_id is None:
            category.parent = None
            category.save(update_fields=["parent"])
            return category
        target_parent = Category.objects.filter(id=target_parent_id).first()
        if not target_parent:
            raise ValueError("Target parent Category does not exist.")

        if category.id == target_parent.id:
            raise ValueError("A category cannot be moved inside itself.")

        if CategoryService.is_descendant(category, target_parent):
            raise ValueError("A category cannot be moved inside its own descendant.")

        category.parent = target_parent
        category.save(update_fields=["parent"])
        return category

    def is_descendant(category, possible_descendant):
        current = possible_descendant
        while current.parent_id is not None:
            if current.parent_id == category.id:
                return True
            current = current.parent
        return False
