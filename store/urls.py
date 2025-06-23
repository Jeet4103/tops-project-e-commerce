
from django.contrib import admin
from . import views 
from django.urls import path
from .views import upload_product_images

urlpatterns = [
   path('', views.home, name='home'),
   path('about/', views.about, name='about'),
   path('login/', views.login_user, name='login'),
   path('logout/', views.logout_user, name='logout'),
   path('SignUp/', views.SignUp, name='SignUp'),
   path('Product_Detail/<int:pk>', views.product_detail, name='product_detail'),
   path('upload-images/', views.upload_product_images, name='upload_product_images'),
   path('category/<str:category_name>/', views.category, name='category'),
   path('Profile_update/',views.Profile_update,name='Profile'),
   path('Password_update/',views.Password_update,name='Password_update')
]
   