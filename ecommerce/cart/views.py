from django.shortcuts import render

from .cart import Cart

from store.models import Product
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

# Create your views here.
def cart_summary(request):

    cart = Cart(request)
    
    return render(request, 'cart/cart-summary.html', {'cart': cart})

def cart_add(request):

    cart = Cart(request)

    # *TAKENOTE* the 'action' must be the same word as you use in product-info.html which is 
    # small letter post
    if request.POST.get('action') == 'post':

        # The .get must be the same name as the one u wrote in product-info.html
        product_id = int(request.POST.get('product_id'))
        product_quantity = int(request.POST.get('product_quantity'))

        # Check to see if the product_id is valid anot
        product = get_object_or_404(Product, id=product_id)

        cart.add(product=product, product_qty=product_quantity)

        # Obtain the latest length of the cart quantity at that time
        cart_quantity = cart.__len__()

        response = JsonResponse({'qty': cart_quantity})

        return response

def cart_delete(request):
    
    cart = Cart(request)

    # *TAKENOTE* the 'action' must be the same word as you use in product-info.html which is 
    # small letter post
    if request.POST.get('action') == 'post':

        # The .get must be the same name as the one u wrote in product-info.html
        product_id = int(request.POST.get('product_id'))

        cart.delete(product=product_id)

        # Obtain the latest length of the cart quantity at that time
        cart_quantity = cart.__len__()

        # Update the new total sum
        cart_total = cart.get_total()

        # Pass the updated total cart sum and new cart quantity
        response = JsonResponse({'qty': cart_quantity, 'total': cart_total})

        return response

def cart_update(request):
    
    cart = Cart(request)

    # *TAKENOTE* the 'action' must be the same word as you use in product-info.html which is 
    # small letter post
    if request.POST.get('action') == 'post':

        # The .get must be the same name as the one u wrote in product-info.html
        product_id = int(request.POST.get('product_id'))
        product_quantity = int(request.POST.get('product_quantity'))
        
        cart.update(product=product_id, qty=product_quantity)

        # Obtain the latest length of the cart quantity at that time
        cart_quantity = cart.__len__()

        # Update the new total sum
        cart_total = cart.get_total()

        # Pass the updated total cart sum and new cart quantity
        response = JsonResponse({'qty': cart_quantity, 'total': cart_total})

        return response