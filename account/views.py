import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserForm,UserLoginForm,ProductRatingForm, BuyNowForm,CartItemForm,CartListForm
from django.contrib.auth import authenticate, login
from .models import Product,User,BuyNow,CartItem
from django.contrib import messages
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
# from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.decorators import login_required


def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }


def user_registration(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            token = get_tokens_for_user(user)
            print(token)
    
            return redirect('login')
    else:
        form = UserForm()   
    return render(request, 'registration_form.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(username=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                print(token)
                return redirect('home')
            else:
                return render(request, 'login.html', {'form': form, 'error_message': 'Invalid email or password'})
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})  

def home(request):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return redirect('login')
        
        products = Product.objects.all()
        return render(request, 'home.html', {'products': products})

def product_rating(request):
    if request.method == 'POST':
        form = ProductRatingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home') 
    else:
        form = ProductRatingForm()
    return render(request, 'productrating.html', {'form': form})


def buynow(request):
    if not request.user.is_authenticated:
        return redirect('login')

    product = Product.objects.get()

    if request.method == 'POST':
        form = BuyNowForm(request.POST)
        if form.is_valid():
            address = form.cleaned_data['address']
            quantity = form.cleaned_data['quantity']
            payment_type = form.cleaned_data['payment_type']

            buy_now = BuyNow.objects.create(
                first_name=request.user,
                name=product,
                address=address,
                quantity=quantity,
                payment_type=payment_type
            )
            product.save()

            messages.success(request, 'Product bought successfully!')
            return redirect('home')
    else:
        form = BuyNowForm()

    return render(request, 'buynow.html', {'form': form, 'product': product})

def orderlist(request):
    orders = BuyNow.objects.all()
    return render(request, 'orderlist.html', {'orders': orders})


def add_to_cart(request):
    product = get_object_or_404(Product)

    if request.method == 'POST':
        form = CartItemForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            cart_item = CartItem.objects.create(user=request.user,product_name=product,product_price=product,quantity=quantity)
            cart_item.save()
            return redirect('cart') 
    else:
        form = CartItemForm()

    return render(request, 'add_to_cart.html', {'form': form, 'product': product})

def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    cart_item_forms = []
    for cart_item in cart_items:
        cart_item_form = CartListForm(instance=cart_item)
        cart_item_forms.append(cart_item_form)

    return render(request, 'cartlist.html', {'cart_item_forms': cart_item_forms})

def delete_from_cart(request, cart_item_id):
    cart_items = CartItem.objects.filter(pk=cart_item_id, user=request.user)
    if cart_items.exists():
        cart_items.delete()
    return redirect('cart') 



# @login_required
# def edit_profile(request):
#     if request.method == 'POST':
#         form = ProfileForm(request.POST, instance=request.user)
#         if form.is_valid():
#             form.save()
#             return redirect('home')  # Redirect to profile page after successful form submission
#     else:
#         form = ProfileForm(instance=request.user)
#     return render(request, 'edit_profile.html', {'form': form})
    
    
def forget(request):
    if request.method=='POST':
        email=request.POST.get('email')
        if User.objects.filter(email=email).exists():
             send_mail(
                  "Testing mail",
                  "Here is the message.",
                  "sarthakgupta779@gmail.com",
                  ["guptasarthak868@gmail.com"],
                  fail_silently=False,
                  )
             return redirect('reset')
    return render(request,'forget.html')

def reset(request):
     
    return render(request,'reset.html')
