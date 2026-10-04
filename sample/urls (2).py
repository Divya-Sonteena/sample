from django.urls import path
from . import views

urlpatterns = [
    path('store/', views.CategoryView.as_view(), name='store_view'),
    path('api/categories/', views.CategoryView.as_view(), name='api_categories'),
    path('api/product/', views.ProductView.as_view(), name='api_product'),
    path('api/move-category/', views.MoveCategoryView.as_view(), name='api_move_category'),
    path('api/move-product/', views.MoveProductView.as_view(), name='api_move_product'),
]
