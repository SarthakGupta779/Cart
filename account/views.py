import jwt
import string
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
import random
from django.db import IntegrityError
from django.contrib.auth.forms import PasswordChangeForm
from datetime import datetime, timedelta
from rest_framework.decorators import api_view
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserForm,UserLoginForm,ProductRatingForm, BuyNowForm,CartItemForm,CartListForm, EditProfileForm, ChangePasswordForm,ProfileForm,ForgetForm,ResetForm
from django.contrib.auth import authenticate, login, logout
from .models import Product,User,BuyNow,CartItem,OTPModel
from django.contrib import messages
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required


def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }

# @api_view(['POST'])
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
        # if not request.user.is_authenticated:
        #     return redirect('login')
        
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
    product = get_object_or_404(Product)

    if request.method == 'POST':
        form = BuyNowForm(request.POST)
        if form.is_valid():
            address = form.cleaned_data['address']
            quantity = form.cleaned_data['quantity']
            payment_type = form.cleaned_data['payment_type']

            BuyNow.objects.create(
                user_id=request.user,
                product_id=product,
                address=address,
                quantity=quantity,
                payment_type=payment_type
            )

            messages.success(request, 'Product purchased successfully!')
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

            try:
               
                cart_item = CartItem.objects.create(
                    user_id=request.user,
                    product_id=product,
                    product_price=product,  
                    quantity=quantity
                )
                messages.success(request, 'Product added to cart successfully!')
                return redirect('cart')
            except IntegrityError:
                
                messages.error(request, 'Error adding product to cart. Please try again.')
                return redirect('add_to_cart', product_id=product_id)
    else:
        form = CartItemForm()

    return render(request, 'add_to_cart.html', {'form': form, 'product': product})

def cart_view(request):
    # if request.user.is_authenticated:
    #     user_id = request.user.id
    cart_items = CartItem.objects.filter()
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
        
# def forget(request):
#     if request.method=='POST':
#         email=request.POST.get('email')
#         if User.objects.filter(email=email).exists():
#             send_mail(
#                 "Testing mail",
#                 "786493",
#                 "sarthakgupta779@gmail.com",
#                 ["guptasarthak868@gmail.com"],
#                 fail_silently=False,
#                 )
#             return redirect('reset')
#     return render(request,'forget.html')





def reset(request):
     
    return render(request,'reset.html')

# @login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')  # Assuming 'profile' is the URL name for viewing the profile
    else:
        form = EditProfileForm()
    
    return render(request, 'edit_profile.html', {'form': form})

def view_profile(request):
    user = request.user 
    return render(request, 'view_profile.html', {'user': user})


# @login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            user = form.save()
        
            update_session_auth_hash(user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')  
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})



def forget(request):
    if request.method == 'POST':
        form = ForgetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email=email).first()
            if user:
                otp = generate_otp()
                OTPModel.objects.create(user=user, otp=otp)
                send_mail(
                    'Password Reset OTP',
                    f'Your OTP for password reset is: {otp}',
                    'sarthak778@gmail.com',
                    [guptasarthal868@gmail.com],
                    fail_silently=False,
                )
                return redirect('reset')  
    else:
        form = ForgetForm()
    return render(request, 'forget.html', {'form': form})

def generate_otp(length=6):
    return ''.join(random.choices(string.digits, k=length))


def reset_view(request):
    if request.method == 'POST':
        form = ResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            otp_entered = form.cleaned_data['otp']
            new_password = form.cleaned_data['new_password']

        
            user = User.objects.filter(email=email).first()

           
            otp_object = OTPModel.objects.filter(user=user, otp=otp_entered).first()
            if otp_object:
                
                user.set_password(new_password)
                user.save()
                
                otp_object.delete()
                return redirect('/login/')  
    else:
        form = ResetForm()
    return render(request, 'reset.html', {'form': form})
def user_logout(request):
    logout(request)
    return render(request,'logout.html')