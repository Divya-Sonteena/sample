from django.contrib import admin
from .models import Category,Product
class MyAdmin(admin.ModelAdmin):
    def log_addition(self,request,object,message):pass
    def log_change(self,request,object,message):pass
    def log_deletion(self,request,object,message):pass
admin.site.register(Category,MyAdmin)
admin.site.register(Product,MyAdmin)

