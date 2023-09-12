from django.shortcuts import render

# Create your views here.
from . models import Category, Product

from django.shortcuts import get_object_or_404

def store(request):

    # Obtain all the objects of Product
    all_products = Product.objects.all()

    context = {'my_products': all_products}

    # The context dictionary is created to hold the data that you want to pass to the template.
    return render(request, 'store/store.html', context)

def categories(request):

    all_categories = Category.objects.all()

    return {'all_categories': all_categories}


def list_category(request, category_slug=None):

    category = get_object_or_404(Category, slug=category_slug)

    products = Product.objects.filter(category=category)

    return render(request, 'store/list-category.html', {'category': category, 'products': products})

def product_info(request, product_slug):

    # Check to see if the product and slug is found
    product = get_object_or_404(Product, slug=product_slug)

    context = {'product': product}

    return render(request, 'store/product-info.html', context)