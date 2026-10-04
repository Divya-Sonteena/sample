from rest_framework import serializers
from .models import Category, Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'parent']
        {
            'name': {
                'error_messages': {'A category with this name already exists try'}
            }
        }
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'product_name', 'category', 'parent_product']
        {
            'product_name': {
                'error_messages': {'A product with this name already exists'}
            }
        }
        
