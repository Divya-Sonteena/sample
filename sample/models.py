from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255,unique=True)
    parent = models.ForeignKey('self', null=True, blank=True,on_delete=models.CASCADE, related_name='children' )
    def __str__(self):
        return self.name

class Product(models.Model): 
    product_name = models.CharField(max_length=255,unique=True)
    category = models.ForeignKey(Category, null=True, blank=True,on_delete=models.CASCADE, related_name='products')
    def __str__(self):
        return self.product_name
    parent_product = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE, related_name='sub_products'
    )
    def __str__(self):
        return self.product_name
