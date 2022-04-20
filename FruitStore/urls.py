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
    path('delete/message', views.user_delete_message),
    path('morefruits/get', views.index_fruit_page),
    path('userInfo/',views.user_info),
    path('update_user_info/',views.update_user_info),
    path('update_password/',views.update_password),
    path('getfruitList/type',views.get_fruit_info),
    path('getfruitList/type/page',views.get_fruit_info_page),
    path('getfruitList/',views.search_fruit_info),
    path('getfruitList/page',views.search_fruit_info_page),
    path('fruitDetails/search',views.fruit_details),
    path('fruitDetails/add/',views.add_to_shopping_cart),
    path('my_shopping_cart/',views.shopping_cart), 
    path('my_shopping_cart/page',views.shopping_cart_page), 
    path('shopping_cart/fruit/update/',views.update_shopping_cart_fruit_number), 
    path('shopping_cart/fruit/delete',views.delete_shopping_cart__fruit),
    path('settle_accounts/',views.payment_page),
    path('management/',views.user_management), 
    path('management/user',views.user_management_page), 
    path('searchUser/',views.user_management_search_user),
    path('management/user/page',views.user_management_search_user_page),
    path('managementUser/disable',views.user_management_disable_user),
    path('managementUser/enable',views.user_management_enable_user),
    path('managementUser/delete',views.user_management_delete_user),
    path('managementUser/update/',views.user_management_update_user),
    path('managementUser/add/',views.user_management_add_user),
    path('managementUser/import/',views.user_management_import_user),
    path('managementUser/download/',views.user_management_download_import_user_file),
    path('management/permission/',views.permission_management),
    path('management/permission/page',views.permission_management_page),
    path('management/permission/searchPermission/',views.permission_management_search_by_url),
    path('management/permission/searchPermission/page',views.permission_management_search_by_url_page),
    path('management/permission/searchPermission/type',views.permission_management_search_by_user_group),
    path('management/permission/searchPermission/type/page',views.permission_management_search_by_user_group_page),
    path('management/permission/add/',views.permission_management_add_permission),
    path('management/permission/import/',views.permission_management_import_permission),
    path('management/permission/download/',views.permission_management_download_import_permission_file),
    path('management/permission/update',views.permission_management_update_permission),
    path('management/permission/delete',views.permission_management_delete_permission),
]

