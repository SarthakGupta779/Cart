from django.contrib import admin
from django.urls import path
from account import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken import views as v

urlpatterns = [
    path('api-token-auth/', v.obtain_auth_token),
    path('admin/', admin.site.urls),
    path('home/', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('forget/',views.forget,name='forget'),
    path('reset/',views.reset,name='reset'), 
    path('register/', views.user_registration, name='register'),
    path('product-rating/',views.product_rating,name="productrating"),
    path('buy-now/', views.buynow, name='buynow'), 
    path('orders/',views.orderlist,name='orders'),
    path('add-to-cart/',views.add_to_cart, name='addtocart'),
    path('cart/', views.cart_view, name='cart'),
    path('delete-from-cart/<int:cart_item_id>/',views.delete_from_cart, name='deletefromcart'),
    path('view-profile',views.view_profile,name='profile'),
    path('logout/',views.user_logout,name='logout'),
    path('edit-profile/',views.edit_profile, name='edit_profile'),
    path('change-password',views.change_password,name='change_password'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)