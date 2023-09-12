from django.shortcuts import render
from .models import ShipppingAddress, Order, OrderItem
from cart.cart import Cart
from django.utils import timezone

from django.http import JsonResponse

from django.core.mail import send_mail

from django.conf import settings

def checkout(request):

    # Users with accounts -- Pre-fill the form
    if request.user.is_authenticated:

        try:
            # Authenticated users WITH Shipping Information
            shipping_address = ShipppingAddress.objects.get(user=request.user.id)

            context = {'shipping': shipping_address}

            return render(request, 'payment/checkout.html', context=context)
        
        except:

            # Authenticated users, but WITH NO Shipping information

            return render(request, 'payment/checkout.html')
    else:
        # Guest Users (No Account)

        return render(request, 'payment/checkout.html')
    

def complete_order(request):

    if request.POST.get('action') == 'post':

        name = request.POST.get('name')
        email = request.POST.get('email')

        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        city = request.POST.get('city')

        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')

        # Style user's shipping address
        shipping_address = (address1 + "\n" + address2 + "\n" + city +
                             "\n" + state + "\n" + zipcode)
        
        # Shopping Cart Information

        cart = Cart(request)

        # Get the total price of items

        total_cost = cart.get_total()

        """
            Order variations
            
            1) Create order -> Account users WITH + WITHOUT shipping information

            2) Create order -> Guest users without an account
        
        """
        date_ordered = timezone.now()
        product_list = []

        # 1) Create order -> Account users WITH + WITHOUT shipping information
        if request.user.is_authenticated:

            order = Order.objects.create(full_name=name, email=email, shipping_address=shipping_address,
                                         amount_paid=total_cost, user=request.user, date_ordered=date_ordered)
            
            # The primary key of the created order
            order_id = order.pk

            for item in cart:

                OrderItem.objects.create(order_id=order_id, product=item['product'], quantity=item['qty'],
                                         price=item['price'], user=request.user)
                
                product_list.append(str(item['product']) + ' Quantity: ' + str(item['qty']))
        

        # 2) Create order -> Guest users without an account
        else:

            order = Order.objects.create(full_name=name, email=email, shipping_address=shipping_address,
                                         amount_paid=total_cost, date_ordered=date_ordered)
            
            # The primary key of the created order
            order_id = order.pk

            for item in cart:

                OrderItem.objects.create(order_id=order_id, product=item['product'], quantity=item['qty'],
                                         price=item['price'])
        
                product_list.append(str(item['product']) + ', Quantity: ' + str(item['qty']))

        all_products = ', '.join(product_list)
        # For every successful Complete Order, we will send an email to the user that made the purchase

        send_mail('Order received', 'Hi! ' + '\n\n' + 'Thank you for placing your oder' + '\n\n' +
                   'Please see your order below' + '\n\n' + str(all_products) + '\n\n' + 'Total Price: $' +
                    str(cart.get_total()), settings.EMAIL_HOST_USER, [email], fail_silently=False)

        order_success = True
        
        response = JsonResponse({'success': order_success})
        
        return response

def payment_success(request):
    
    # Clear shopping cart

    for key in list(request.session.keys()):

        if key == 'session_key':

            del request.session[key]

    return render(request, 'payment/payment-success.html')

def payment_failed(request):

    return render(request, 'payment/payment-failed.html')
    