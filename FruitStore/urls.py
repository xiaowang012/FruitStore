"""FruitStore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from fruit_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.host),
    path('login/', views.login),
    path('register/', views.register),
    path('logout/', views.logout),
    path('index/', views.store_index),
    path('index_send_message/', views.user_send_message),
    path('userInfo/',views.user_info),
    path('update_user_info/',views.update_user_info),
    path('update_password/',views.update_password),
    path('getfruitList/type',views.fruit_info),
    path('fruitDetails/search',views.fruit_details),
    path('management/',views.store_management), 
    path('my_shopping_cart/',views.shopping_cart), 
    path('settle_accounts/',views.payment_page),
     
]

