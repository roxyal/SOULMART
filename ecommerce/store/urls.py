from django.urls import path

# we are in the same directory thus, put .
from . import views

urlpatterns = [

    # Store main page
    path('', views.store, name='store'),
    
    # Individual Product
    path('product/<slug:product_slug>/', views.product_info, name='product-info'),

    # Individual Category
    # <slug:category_slug>/ must be the same name in the views.py
    path('search/<slug:category_slug>/', views.list_category, name='list-category'),


]