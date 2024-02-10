from django import forms
from .models import User,Product,ProductRating,BuyNow,CartItem
from django.contrib.auth.forms import AuthenticationForm,UserChangeForm


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone', 'address', 'gender', 'password']
        widgets = {
            'password': forms.PasswordInput(), 
        }

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Email' 
        self.fields['username'].widget = forms.EmailInput(attrs={'class': 'form-control'})  
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control'})  

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'image', 'discount', 'price', 'quantity', 'color', 'description', 'stock_status']

class ProductRatingForm(forms.ModelForm):
    class Meta:
        model = ProductRating
        fields = ['user_id','product_id', 'rating', 'message']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        

class BuyNowForm(forms.ModelForm):
    class Meta:
        model = BuyNow
        fields = ['address', 'quantity', 'payment_type']
        
        
class OrderListForm(forms.ModelForm):
    class Meta:
        model = BuyNow
        fields = ['first_name', 'name', 'address', 'quantity', 'payment_type']
        


class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['quantity']

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['quantity'].widget.attrs.update({'class': 'form-control', 'min': '1'})

class CartListForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['user', 'product_name', 'product_price', 'quantity']
        
    
    
# class ProfileForm(UserChangeForm):
#     class Meta:
#         model = User
#         fields = ('email', 'phone', 'password') 