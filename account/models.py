from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser
from django.core.validators import MinValueValidator

class UserManager(BaseUserManager):
  def createUser(self, email, first_name,password=None, password2=None):
      if not email:
          raise ValueError('User must have an email address')

      user = self.model(
          email=self.normalize_email(email),
          first_name=first_name,
          
      )

      user.set_password(password)
      user.save(using=self._db)
      return user

  def createSuperuser(self, email, first_name, password=None):
      user = self.create_user(
          email,
          password=password,
          first_name=first_name,
      )
      user.is_admin = True
      user.save(using=self._db)
      return user

class User(AbstractBaseUser):
  email = models.EmailField(
      verbose_name='Email',
      max_length=255,
      unique=True,
  )
  ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('merchant', 'Merchant'),
    
  ]
  id = models.BigAutoField(primary_key=True)
  first_name = models.CharField(max_length=50)
  last_name = models.CharField(max_length=50)
  phone = models.CharField(max_length=15, blank=True, null=True)
  address = models.CharField(max_length=255, blank=True, null=True)
  gender = models.CharField(max_length=6, blank=True,)
  password = models.CharField(max_length=255,)
  is_active = models.BooleanField(default=True)
  is_admin = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True,null=True)
  updated_at = models.DateTimeField(auto_now=True,null=True)
  role_type = models.CharField(max_length=20, choices=ROLE_CHOICES)
  
  

  objects = UserManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['first_name']

  def __str__(self):
      return self.email

  def has_perm(self, perm, obj=None):
      "Does the user have a specific permission?"
      return self.is_admin

  def has_module_perms(self, app_label):
      "Does the user have permissions to view the app `app_label`?"
      return True

  @property
  def is_staff(self):
      "Is the user a member of staff?"
     
      return self.is_admin
  
  
  
class Product(models.Model):
    id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    product_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='product_images')
    discount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    color = models.CharField(max_length=50)
    description = models.TextField()
    arrival = models.DateTimeField(auto_now_add=True ,null=True)  # Assuming the arrival datetime is the current datetime
    stock_status = models.CharField(max_length=20, choices=[('in_stock', 'In Stock'), ('out_of_stock', 'Out of Stock')], default='in_stock')

    def save(self, *args, **kwargs):
        if self.quantity > 1:
            self.stock_status = 'in_stock'
        else:
            self.stock_status = 'out_of_stock'
        super().save(*args, **kwargs)
        

class ProductRating(models.Model):
    product_id = models.ForeignKey('Product', on_delete=models.CASCADE, db_column='product_id')
    user_id = models.ForeignKey('User', on_delete=models.CASCADE, db_column='user_id')
    rating = models.IntegerField()
    message = models.TextField(blank=True, null=True)  
    class Meta:
        unique_together = ('product_id', 'user_id') 
        
        

class BuyNow(models.Model):
    PAYMENT_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('paypal', 'PayPal'),
    ]

    user_id = models.ForeignKey(User, on_delete=models.CASCADE,db_column='user_id')
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE,db_column='product_id')
    address = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    payment_type = models.CharField(max_length=20, choices=PAYMENT_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id', related_name='cart_items')
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, db_column='product_id', related_name='cart_items')
    product_price = models.ForeignKey(Product, on_delete=models.CASCADE, db_column='price', related_name='cart_price')
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    added_at = models.DateTimeField(auto_now_add=True)

class OTPModel(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,db_column='user_id')
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)