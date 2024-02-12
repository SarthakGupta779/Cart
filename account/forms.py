from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm,UserChangeForm
from django.core.exceptions import ValidationError 
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
        fields = ['user_id', 'product_id', 'address', 'quantity', 'payment_type']
        


class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['quantity']


class CartListForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['user_id', 'product_id', 'product_price', 'quantity']
        
       
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password','gender'] 


class EditProfileForm(UserChangeForm):

    def clean_current_password(self):

        if not self.user.check_password(current_password):
            raise ValidationError("Incorrect current password")
        return current_password

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('password')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = '__all__'
        
        
class ForgetForm(forms.Form):
    email = forms.EmailField(label='Email')

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is not associated with any account.")
        return email
    
    
    
class ResetForm(forms.Form):
    otp = forms.CharField(label='OTP', max_length=6)
    new_password = forms.CharField(label='New Password', widget=forms.PasswordInput)

    def clean_otp(self):
        otp = self.cleaned_data['otp']
        if not otp.isdigit() or len(otp) != 6:
            raise forms.ValidationError("Invalid OTP. Please enter a 6-digit OTP.")
        return otp