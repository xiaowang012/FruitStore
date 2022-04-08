#coding=utf-8
from django.db import models
from django.db.models.base import Model
from django.db.models.fields import CharField, IntegerField, TextField, TimeField,AutoField

# Create your models here.
#商品表表
class Fruits(models.Model):
    id = AutoField(primary_key = True)
    fruit_name = CharField(max_length=50)
    book_type = CharField(max_length=50)
    book_introduction = TextField(max_length=200)
    issue_year = CharField(max_length=50)
    number_of_downloads = IntegerField()
    book_file_name = CharField(max_length=100)
    add_book_time = CharField(max_length=100)
