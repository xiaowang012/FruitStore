#coding=utf-8
from django.db import models
from django.db.models.base import Model
from django.db.models.fields import CharField, IntegerField, TextField, TimeField

# Create your models here.
#商品表表
class Fruits(models.Model):
    fruit_name = CharField(max_length=50)
    book_type = CharField(max_length=50)
    book_introduction = TextField(max_length=200)
    issue_year = CharField(max_length=50)
    number_of_downloads = IntegerField()
    book_file_name = CharField(max_length=100)
    add_book_time = CharField(max_length=100)

# #用户视图的权限表
class App1Permission(models.Model):
    user_group = CharField(max_length=50)
    views_func = CharField(max_length=50)
    description = CharField(max_length=50)