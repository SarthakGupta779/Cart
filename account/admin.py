from django.contrib import admin
from account.models import User,Product,ProductRating,BuyNow,CartItem
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


admin.site.register(User)
admin.site.register(Product)
admin.site.register(ProductRating)
admin.site.register(BuyNow)
admin.site.register(CartItem)