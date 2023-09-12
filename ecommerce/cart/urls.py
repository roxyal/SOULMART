from django.urls import path

from . import views

urlpatterns = [
    
    # Shopping cart summary view
    path('', views.cart_summary, name='cart-summary'),

    # Add to the cart
    path('add/', views.cart_add, name='cart-add'),

    # Delete from the cart
    path('delete/', views.cart_delete, name='cart-delete'),

    # Update the cart
    path('update/', views.cart_update, name='cart-update'),

]