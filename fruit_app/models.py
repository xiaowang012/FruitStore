#coding=utf-8
from django.db import models
from django.db.models.base import Model
from django.db.models.fields import CharField, IntegerField, TextField,AutoField,DecimalField,BooleanField
from django.db.models import DateTimeField
from django.utils import timezone

#商品表
class Fruits(models.Model):
    id = AutoField(primary_key = True)
    fruit_type_id = IntegerField (default = 0)
    fruit_name = CharField(max_length = 50,default = '')
    fruit_description = CharField(max_length = 200,default = '')
    fruit_price = DecimalField(max_digits = 5,decimal_places = 2)
    transportation_price = DecimalField(max_digits = 5,decimal_places = 2)
    fruit_weight = CharField(max_length = 100,default = '')
    Sales = IntegerField (default = 0)
    fruit_pic_file_name = CharField(max_length = 200,default = '')
    add_fruit_time = DateTimeField(default = timezone.now)

#商品评论信息表
class FruitComments(models.Model):
    id = AutoField(primary_key = True)
    fruit_id = IntegerField(default = 0)
    commenting_user = CharField(max_length = 50,default = '')
    commenting_content = CharField(max_length = 200,default = '')
    anonymous = BooleanField()
    commenting_time = DateTimeField(default = timezone.now)

#首页用户留言信息表
class UserMessage(models.Model):
    id = AutoField(primary_key = True)
    commenting_user = CharField(max_length = 50,default = '')
    commenting_content = CharField(max_length = 200,default = '')
    anonymous = BooleanField()
    commenting_time = DateTimeField(default = timezone.now)

#个人信息表
class UserInfo(models.Model):
    id = AutoField(primary_key = True)
    user_id = IntegerField()
    chinese_name = CharField(max_length= 50 ,default = '')
    sex = CharField(max_length = 10,default = '')
    birthday = CharField(max_length= 50,default = '' )
    constellation = CharField(max_length = 50 ,default = '')
    phone_number = CharField(max_length = 50,default = '')
    address1 = CharField(max_length = 200,default = '')
    address2 = CharField(max_length = 200,default = '')
    address3 = CharField(max_length = 200,default = '')
    add_userinfo_time = DateTimeField(default = timezone.now)

#购物车表
class ShoppingCart(models.Model):
    id = AutoField(primary_key = True)
    customer_id =  IntegerField()
    fruit_id = IntegerField()
    fruit_number = IntegerField()
    add_fruit_time = DateTimeField(default = timezone.now)

#订单表
class FruitOrder(models.Model):
    id = AutoField(primary_key = True)
    customer =  CharField(max_length = 100,default = '')
    order_number = CharField(max_length = 100,default = '')
    money = DecimalField(max_digits = 8,decimal_places = 2)
    add_order_time = DateTimeField(default = timezone.now)


#路由权限表
class RoutePermission(models.Model):
    id = AutoField(primary_key = True)
    group_name = CharField(max_length = 50,default = '')
    url = CharField(max_length = 100,default = '')
    description = CharField(max_length = 100,default = '')
    add_route_permission_time = DateTimeField(default = timezone.now)

