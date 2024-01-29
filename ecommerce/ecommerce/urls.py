"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from myapp import views

urlpatterns = [
    
    # main pages
    path('admin/', admin.site.urls),
    path('',views.index,name='home'),
    path('categories',views.categories,name='categories'),
    path('allproducts',views.allproducts,name='allproducts'),
    path('about',views.about,name='about'),
    path('contact',views.contact,name='contact'),    
    path("loginpage",views.loginpage,name="loginpage"),
    path('searchfn',views.searchfn,name='searchfn'),


    #account pages
    path('signup',views.signup,name='signup'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),


    # categories
    path('laptops',views.laptops,name='laptops'),
    path('mobiles',views.mobiles,name='mobiles'),
    path('cameras',views.cameras,name='cameras'),
    path('powerbanks',views.powerbanks,name='powerbanks'),
    path('headphones',views.headphones,name='headphones'),
    path('accessories',views.accessories,name='accessories'),
    
    
    # cart sections
    path('single/addcart/<wal>',views.addcart,name='addcart'),
    path('cartt',views.cartt,name='cartt'),
    path('minuscart/<de>',views.minuscart,name='minuscart'),
    path('pluscart/<de>',views.pluscart,name='pluscart'),
    path('deletecart/<de>',views.deletecart,name='deletecart'),
    path('single/<wal>',views.single,name='single'),


    # admin dashboard
    path('adminindex',views.adminindex,name='adminindex'),
    path('adminpro',views.adminpro,name='adminpro'),
    path('bs',views.bs,name='bs'),
    path('addproduct',views.addproduct,name='addproduct'),
    path('adsingle/editproduct/<wal>',views.editproduct,name='editproduct'),
    path('adsingle/editproduct/editproduct2/<wal>',views.editproduct2,name='editproduct2'),
    path('adsingle/deleteproduct/<wal>',views.deleteproduct,name='deleteproduct'),
    path('userss',views.userss,name='userss'),
    path('userbooking',views.userbooking,name='userbooking'),
    path('adsingle/<wal>',views.adsingle,name='adsingle'),

    #passwordreset
    path("forgot",views.forgot_password,name="forgot"), 
    path("reset/<token>",views.reset_password,name="reset"), 
    path("reset/reset2/<token>",views.reset_password2,name="reset2"),
    path('proedit',views.profileedit,name='proedit'),


    #order sections
    path('place-order', views.placeorder, name='placeorder'),
    path('proceed-to-pay', views.razorpaycheck, name='proceed-to-pay'),
    path('myorder', views.orderss, name='myorder'),
    path('checkout',views.checkout,name='checkout'),

    
    #emailreply
    path('messages',views.mess1,name='messages'),
    path('reply/<em>',views.reply,name='reply'),
    path('reply/replymail/<em>',views.replymail,name='replymail'),


] + static(settings.STATIC_URL,document_root = settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
