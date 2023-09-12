from django.contrib import admin

# Register your models here.
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    # This line specifies that the slug field of the Category model should be automatically prepopulated
    # based on the value of the name field. It means that when you enter a value for the name field,
    # the slug field will be automatically filled in using a URL-friendly version of the name.
    prepopulated_fields = {'slug': ('name', )}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    
    prepopulated_fields = {'slug': ('title', )}