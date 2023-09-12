from django.shortcuts import redirect, render

from .forms import CreateUserForm, LoginForm, UpdateUserForm

from payment.forms import ShippingForm # ShippingForm
from payment.models import ShipppingAddress # ShippingAddress
from payment.models import Order, OrderItem

from django.contrib.auth.models import User

# Getting the current website (for example (testing): 127.1...)
from django.contrib.sites.shortcuts import get_current_site
from .token import user_tokenizer_generate

from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from django.contrib.auth.models import auth # Provided us with authentication

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

from django.contrib import messages

def register(request):
    
    form = CreateUserForm()

    if request.method == 'POST':
        
        form = CreateUserForm(request.POST)

        if form.is_valid(): # Check if the form is valid

            user = form.save()

            user.is_active = False #Deactivated by default when created successfully

            user.save()

            # Email verification setup (template)

            current_site = get_current_site(request)
            # Header of the email
            subject = 'Account verification email'

            message = render_to_string('account/registration/email-verification.html', {

                'user': user,
                'domain': current_site, # localhost / website
                'uid': urlsafe_base64_encode(force_bytes(user.pk)), # encrypt 
                'token': user_tokenizer_generate.make_token(user), # generate the token

            })

            user.email_user(subject=subject, message=message)

            # Successful user will be sent to this page
            return redirect('email-verification-sent')
        
    context = {'form': form}
        
    return render(request, 'account/registration/register.html', context=context)

def email_verification(request, uidb64, token):
    
    unique_id = force_text(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=unique_id)

    # Success (if he click on the generate token link)
    if user and user_tokenizer_generate.check_token(user, token):

        user.is_active = True

        user.save()

        return redirect('email-verification-success')
    else:
    # Failed
        return redirect('email-verification-failed')

def email_verification_sent(request):

    return render(request, 'account/registration/email-verification-sent.html')

def email_verification_success(request):

    return render(request, 'account/registration/email-verification-success.html')

def email_verification_failed(request):

    return render(request, 'account/registration/email-verification-failed.html')

def my_login(request):

    form = LoginForm()

    if request.method == 'POST':

        form = LoginForm(request, data=request.POST) # pass in the .POST data

        if form.is_valid():

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None: # If user exist

                auth.login(request, user)

                return redirect('dashboard')

    context = {'form': form}

    return render(request, 'account/my-login.html', context=context)

# Logout
def user_logout(request):

    try:

        for key in list(request.session.keys()):
            
            if key == 'session_key':

                continue
            
            else:

                del request.session[key]
    
    except KeyError:

        pass

    messages.success(request, "Logout Success")

    return redirect('store')


# The login_required decorator checks if the user is authenticated. If the user is not authenticated,
# it redirects them to the specified login URL, which in this case is 'my-login'

@login_required(login_url='my-login')
def dashboard(request):

    return render(request, 'account/dashboard.html')

@login_required(login_url='my-login')
def profile_management(request):
    
    # THIS MUST BE add at the top here, Updating our user's username and email
    # So that we can see the validation error
    user_form = UpdateUserForm(instance=request.user)

    if request.method == 'POST':

        # Get the instance data of the current user
        user_form = UpdateUserForm(request.POST, instance=request.user)

        if user_form.is_valid():

            user_form.save()

            messages.info(request, "Account updated")

            return redirect('dashboard')

    context = {'user_form': user_form}

    return render(request, 'account/profile-management.html', context=context)

@login_required(login_url='my-login')
def delete_account(request):

    # request.user.id -> current user that is accessing the website
    user = User.objects.get(id=request.user.id)

    if request.method == 'POST':

        user.delete()

        messages.error(request, "Account deleted")

        return redirect('store')
    
    return render(request, 'account/delete-account.html')

# Shipping View
@login_required(login_url='my-login')
def manage_shipping(request):

    try:
        # Account user with shipment information

        shipping = ShipppingAddress.objects.get(user=request.user.id)

    except ShipppingAddress.DoesNotExist:

        # Account user with no shipment information

        shipping = None

    form = ShippingForm(instance=shipping) # Prefill the form with their old info

    if request.method == 'POST':
        
        form = ShippingForm(request.POST, instance=shipping)

        if form.is_valid():

            # Assign the user Foreign Key on the object

            shipping_user = form.save(commit=False)

            # Adding the Foreign Key itself
            shipping_user.user = request.user

            shipping_user.save()
 
            return redirect('dashboard')
        
    context = {'form': form}

    return render(request, 'account/manage-shipping.html', context=context)


@login_required(login_url='my-login')
def track_orders(request):

    try: # If that user place the order

        orders = Order.objects.filter(user=request.user)
         
        # orders = OrderItem.objects.filter(user=request.user)

        context = {'orders': orders}

        return render(request, 'account/track-orders.html', context=context)

    except: # Guest user place order

        return render(request, 'account/track-orders.html')

