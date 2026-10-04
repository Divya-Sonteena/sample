"""
URL configuration for sample project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic.base import RedirectView

from .views import (
    CategoryView,
    ProductView,
    MoveCategoryView,
    MoveProductView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/store/', permanent=False)),
    path('store/', CategoryView.as_view(), name='store_view'),
    path('api/categories/', CategoryView.as_view(), name='api_categories'),
    path('api/product/', ProductView.as_view(), name='api_product'),
    path('api/move-category/', MoveCategoryView.as_view(), name='api_move_category'),
    path('api/move-product/', MoveProductView.as_view(), name='api_move_product'),
]
