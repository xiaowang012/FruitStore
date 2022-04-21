#coding=utf-8
from django.http import HttpResponse,FileResponse
from django.shortcuts import render,redirect
from django.contrib import auth
from django.contrib.auth.models import User,Group
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib import messages
from . import forms
from . import models
import random
import time
import os
import xlrd

# Create your views here.
# 127.0.0.1:5001
def host(request):
    if request.session.get('is_login',None) == True:
        return redirect('/index/')
    else:
        return redirect('/login/')
    
#用户登录
def login(request):
    if request.session.get('is_login',None) == True:
        return redirect('/index/')
    if request.method == "GET":
        form = forms.UserForm
        return render(request, "login.html",{"form":form})
    elif request.method == "POST":
        form = forms.UserForm(request.POST)
        if form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")
            #密码认证
            login_user_obj = auth.authenticate(username = username, password = password)
            if not login_user_obj:
                #定义密码错误信息
                dic1 = {}
                dic1['message'] = '用户名或密码错误!'
                return render(request, "login.html", {"form": form,"dic1":dic1})
            else:
                request.session["is_login"] = True
                auth.login(request,login_user_obj)
                return redirect('/index/')
                
        else:
            return render(request, "login.html", {"form": form})

#用户注册
def register(request):
    if request.method == 'GET':
        form = forms.RegisterForm()
        return render(request,'register.html',{'form':form})
    elif request.method == "POST":
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")
            password1 = request.POST.get("password1")
            #创建用户
            if password == password1:
                if not User.objects.filter(username = username).first():
                    #用户名查重,如果查不到，正常创建用户
                    try:
                        User.objects.create_user(username = username,password = password)
                    except:
                        #返回对应的错误提示信息到页面
                        message = ' 注册: ' + username +' Failed!'
                        dic2 = {'frame_type':'alert alert-dismissable alert-danger','title':'ERROR ','message':message}
                        return render(request,'register.html',{'form':form,'dic2':dic2})
                    else:
                        #返回对应的注册成功提示信息到页面
                        message = ' 注册: ' + username +' SUCCESS!'
                        dic2 = {'frame_type':'alert alert-success alert-dismissable','title':'SUCCESS ','message':message}
                        return render(request,'register.html',{'form':form,'dic2':dic2})
                else:
                    error = '用户: '+ username + ' 已存在! 请不要重复注册!'
                    dic1 = {}
                    dic1['message'] = error
                    return render(request, "register.html", {"form": form,"dic1":dic1})
            else:
                error_msg = '两次输入的密码不一致!'
                dic1 = {}
                dic1['message'] = error_msg
                return render(request, "register.html", {"form": form,"dic1":dic1})
        else:
            #未通过表单验证
            dic1 = {}
            clear_err = form.errors.get('__all__')
            if clear_err:
                clear_err = str(clear_err).replace('<ul class="errorlist nonfield"><li>','').replace('</li></ul>','')
                dic1['message'] = clear_err
            return render(request, "register.html", {"form": form,'dic1':dic1})
            
#用户登出
# @login_required
#@permission_check
def logout(request):
    auth.logout(request)
    return redirect('/login/')

#商城首页
# @login_required
# @permission_check
def store_index(request):
    if request.method == 'GET':
        form = forms.SearchFruitsForm()
        #获取当前用户名
        current_user = request.user
        #前端数据
        dic1 = {'current_user':current_user,'page_number':1}
        #查水果数据,-负号表示降序排列(最新时间)
        fruits_data = models.Fruits.objects.order_by('-add_fruit_time')[0:4]
        for i in fruits_data:
            picture_file_name = str(i.fruit_pic_file_name)
            if ';' in picture_file_name:
                pictures_list = picture_file_name.split(';')
                i.pic_html = '/static/imgs/' + pictures_list[0]
            else:
                i.pic_html = '/static/imgs/' + picture_file_name
        #查询留言板数据，最新时间排序限制10条
        comments_data = models.UserMessage.objects.order_by('-commenting_time')[0:10]
        for j in comments_data:
            #根据anonymous字段(True/False)判断是否匿名，是否使用 *替换部分字符串
            anonymous = j.anonymous
            commenting_user = str(j.commenting_user)
            if anonymous == 1:
                num = int(len(commenting_user)/2)
                str1 = commenting_user[0:num]
                str2 = commenting_user[num:]
                commenting_user = str1.replace(str1,'*'*num) + str2 
                #更新到queryset中
                j.commenting_user = commenting_user
            #加入表格的随机样式
            j.type = random.choice(['error','info','success','warning']) 
        return render(request,'index.html',{'form':form,'list1':fruits_data,'list2':comments_data,'dic1':dic1})

#用户信息
def user_info(request):
    if request.method == 'GET':
        current_user = request.user
        #根据当前用户查询userinfo的数据
        #print(current_user)
        info =  User.objects.filter(username = current_user).first()
        if info:
            user_id = info.id
            current_user_info =  models.UserInfo.objects.filter(user_id = user_id).first()
            #前端数据字典
            dic1 = {'current_user':current_user}
            return render(request,'user_info.html',{'dic1':dic1,'user_dic':current_user_info})
        else:
            return render(request,'error_404.html')

#修改密码
def update_password(request):
    current_user = request.user
    if request.method == 'GET':
        form = forms.ChangeUserPassword()
        dic1 = {'current_user':current_user}
        return render(request,'update_password.html',{'form':form,'dic1':dic1})
    elif request.method == 'POST':
        form = forms.ChangeUserPassword(request.POST)
        if form.is_valid():
            username = request.POST.get("username")
            old_password = request.POST.get("old_password")
            password = request.POST.get("new_password1")
            password1 = request.POST.get("new_password2")
            #检查当前用户和post里面的用户是否一致 注:current_user 为User类型， username为字符串
            if str(current_user) == username:
                if password == password1:
                    #密码认证
                    login_user_obj = auth.authenticate(username = username, password = old_password)
                    if not login_user_obj:
                        #错误提示信息
                        type = 'alert alert-dismissable alert-danger'
                        title = ' 错误!'
                        message = ' 原密码错误! 请重试!'
                    else:
                        #修改密码
                        login_user_obj.set_password(password1)
                        login_user_obj.save()
                        type = 'alert alert-success alert-dismissable'
                        title = ' 成功!'
                        message = ' 修改密码成功!'     
                else:
                    type = 'alert alert-dismissable alert-danger'
                    title = ' 错误!'
                    message = ' 新密码两次输入不一致!'
            else:
                return render(request,'error_403.html')        
        else:
            clear_err = form.errors.get('__all__')
            clear_err = str(clear_err).replace('<ul class="errorlist nonfield"><li>','').replace('</li></ul>','')
            type = 'alert alert-dismissable alert-danger'
            title = ' 错误!'
            message = clear_err
        
        #渲染页面
        dic1 = {'current_user':current_user}
        dic2 = {'type':type,'title':title,'message':message}
        return render(request,'update_password.html',{'form':form,'dic1':dic1,'dic2':dic2})   
           
#添加/修改个人信息
def update_user_info(request):
    current_user = request.user
    if request.method == 'POST':
        form = forms.UpdateUserInfo(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            chinese_name = request.POST.get('chinese_name')
            sex = request.POST.get('sex')
            birthday = request.POST.get('birthday')
            constellation = request.POST.get('constellation')
            phone_number = request.POST.get('phone_number')
            address1 = request.POST.get('address1')
            address2 = request.POST.get('address2')
            address3 = request.POST.get('address3')
            #判断当前用户是否为提交修改的用户名
            if str(current_user) == username:
                #查询用户id
                user_info = User.objects.filter(username = username).first()
                if user_info:
                    user_id =  user_info.id
                    search_userinfo = models.UserInfo.objects.filter(user_id = user_id).first()
                    if not search_userinfo:
                        #没有该用户id的数据就新增
                        test1 = models.UserInfo(id = None,user_id = user_id,chinese_name = chinese_name,sex = sex,birthday = birthday,constellation = constellation,\
                            phone_number = phone_number,address1 = address1,address2 = address2,address3 = address3)
                        test1.save()
                        #提示信息
                        type = 'alert alert-success alert-dismissable'
                        title = ' 成功!'
                        message = ' 添加个人信息成功!'
                    else:
                        #查到就修改
                        if search_userinfo.chinese_name != chinese_name:
                            search_userinfo.chinese_name = chinese_name
                        if search_userinfo.sex != sex:
                            search_userinfo.sex = sex
                        if search_userinfo.birthday != birthday:
                            search_userinfo.birthday = birthday
                        if search_userinfo.constellation != constellation:
                            search_userinfo.constellation = constellation
                        if search_userinfo.phone_number != phone_number:
                            search_userinfo.phone_number = phone_number
                        if search_userinfo.address1 != address1:
                            search_userinfo.address1 = address1
                        if search_userinfo.address2 != address2:
                            search_userinfo.address2 = address2
                        if search_userinfo.address3 != address3:
                            search_userinfo.address3 = address3
                        #保存
                        search_userinfo.save()
                        #提示信息
                        type = 'alert alert-success alert-dismissable'
                        title = ' 成功!'
                        message = ' 修改个人信息成功!'
                else:
                    #alert alert-dismissable alert-danger 
                    type = 'alert alert-dismissable alert-danger'
                    title = ' 错误!'
                    message = ' 用户不存在!'        
            else:
                type = 'alert alert-dismissable alert-danger'
                title = ' 错误!'
                message = ' 权限错误!'
        else:
            #未通过表单校验
            errors = ''
            for key,value in form.errors.items():
                errors += str(value).replace('<ul class="errorlist"><li>','').replace('</li></ul>','') + '  '
            type = 'alert alert-dismissable alert-danger'
            title = ' 错误!'
            message = errors
        #渲染页面  
        dic1 = {'current_user':current_user}
        dic2 = {'type':type,'title':title,'message':message}
        return render(request,'user_info.html',{'form':form,'dic1':dic1,'dic2':dic2})

#首页给我留言
def user_send_message(request):
    current_user = request.user
    if request.method == 'POST':
        form = forms.UserSendMessage(request.POST)
        commenting_user = request.POST.get('commenting_user')
        commenting_content = request.POST.get('message_content')
        anonymous = request.POST.get('anonymous')
        if form.is_valid():
            if commenting_user == str(current_user):
                if anonymous == 'on':
                    anonymous = True
                elif anonymous == None:
                    anonymous = False
                #添加到数据库
                comment_object = models.UserMessage(id = None,commenting_user = commenting_user,\
                    commenting_content = commenting_content,anonymous = anonymous)
                comment_object.save()
                #添加成功信息
                messages.add_message(request, messages.SUCCESS, '留言成功!')
            else:
                #添加错误信息
                messages.add_message(request, messages.ERROR, '权限错误! 无法评论!')
        else:
            #未通过表单校验,将错误提示添加到messages中
            errors = ''
            for key,value in form.errors.items():
                errors += str(value).replace('<ul class="errorlist"><li>','').replace('</li></ul>','') + '  '
            type = 'alert alert-dismissable alert-danger'
            messages.add_message(request, messages.ERROR, errors)
        return redirect('/index/')
        
#首页删除留言板留言
def user_delete_message(request):
    current_user = request.user
    if request.method == 'GET':
        delete_comment_id = request.GET.get('id')
        try:
            delete_comment_id = int(delete_comment_id)
        except:
            messages.add_message(request,messages.ERROR,'错误!  参数错误!')
        else:
            comments_info = models.UserMessage.objects.filter(id = delete_comment_id).first()
            if comments_info:
                if str(current_user) == comments_info.commenting_user:
                    #判断当前操作用户是否为评论用户
                    comments_info.delete()
                    messages.add_message(request,messages.SUCCESS,' 删除成功!')
                else:
                    messages.add_message(request,messages.ERROR,'错误! 无法删除别人的评论!')
            else:
                messages.add_message(request,messages.ERROR,'错误!  删除失败!')
        return redirect('/index/')

#获取水果列表(第一页)
def get_fruit_info(request):
    current_user = request.user
    if request.method == 'GET':
        fruit_type_id = request.GET.get('code')
        try:
            fruit_type_id = int(fruit_type_id)
        except:
            messages.add_message(request,messages.ERROR,' 错误! 参数错误!')
        else:
            #根据根据fruit_type_id水果
            fruits_res = models.Fruits.objects.filter(fruit_type_id = fruit_type_id)[0:6]
            for i in fruits_res:
                picture_file_name = str(i.fruit_pic_file_name)
                if ';' in picture_file_name:
                    pictures_list = picture_file_name.split(';')
                    i.pic_html = '/static/imgs/' + pictures_list[0]
                else:
                    i.pic_html = '/static/imgs/' + picture_file_name
            #数据为空给个消息提示
            if len(fruits_res) == 0:
                messages.add_message(request,messages.ERROR,' 未查询到任何满足条件水果!')
            #渲染页面
            dic1 = {'current_user':current_user,'page_number':1,'fruit_type_id':fruit_type_id}
            return render(request,'fruit_list.html',{'dic1':dic1,'fruit_data':fruits_res})

#获取水果列表翻页
def get_fruit_info_page(request):
    if request.method == 'GET':
        current_user = request.user
        fruit_type_id = request.GET.get('type')
        page_number = request.GET.get('code')
        try:
            fruit_type_id = int(fruit_type_id)
            page_number = int(page_number)
        except:
            messages.add_message(request,messages.ERROR,' 错误! 参数错误!')
        else:
            #根据根据fruit_type_id 和页码查询不同的水果
            search_start_num = (page_number-1)*6
            search_end_num = page_number*6
            fruits_res = models.Fruits.objects.filter(fruit_type_id = fruit_type_id)[search_start_num:search_end_num]
            for i in fruits_res:
                picture_file_name = str(i.fruit_pic_file_name)
                if ';' in picture_file_name:
                    pictures_list = picture_file_name.split(';')
                    i.pic_html = '/static/imgs/' + pictures_list[0]
                else:
                    i.pic_html = '/static/imgs/' + picture_file_name
            #数据为空给个消息提示
            if len(fruits_res) == 0:
                messages.add_message(request,messages.ERROR,' 未查询到任何满足条件水果!')
            #渲染页面
            dic1 = {'current_user':current_user,'page_number':page_number,'fruit_type_id':fruit_type_id}
            return render(request,'fruit_list.html',{'dic1':dic1,'fruit_data':fruits_res})
    
#首页查询水果(模糊查询)
def search_fruit_info(request):
    current_user = request.user
    if request.method == 'GET':
        form = forms.SearchFruitsForm()
        dic1 = {'current_user':current_user,'page_number':1}
        return render(request,'fruit_list_search.html',{'form':form,'dic1':dic1})
    elif request.method == 'POST':
        form = forms.SearchFruitsForm(request.POST)
        if form.is_valid():
            fruit_name = request.POST.get('fruitname')
            #模糊查询水果
            search_fruits1 = models.Fruits.objects.filter(fruit_name__contains = fruit_name).order_by('-add_fruit_time')[0:6]
            for i in search_fruits1:
                picture_file_name = str(i.fruit_pic_file_name)
                if ';' in picture_file_name:
                    pictures_list = picture_file_name.split(';')
                    i.pic_html = '/static/imgs/' + pictures_list[0]
                else:
                    i.pic_html = '/static/imgs/' + picture_file_name

            #数据为空给个消息提示
            if len(search_fruits1) == 0:
                messages.add_message(request,messages.ERROR,' 未查询到任何满足条件水果!')
            #渲染页面
            dic1 = {'current_user':current_user,'page_number':1,'fruit_name':fruit_name}
            return render(request,'fruit_list_search.html',{'form':form,'dic1':dic1,'fruit_data':search_fruits1})
        else:
            #未通过表单校验
            errors = ''
            for key,value in form.errors.items():
                errors += str(value).replace('<ul class="errorlist"><li>','').replace('</li></ul>','') + '  '
            type = 'alert alert-dismissable alert-danger'
            messages.add_message(request, messages.ERROR, errors)
            #print(request.get_full_path())
            return redirect('/getfruitList/')
    
#首页查询水果(模糊查询)翻页
def search_fruit_info_page(request):
    current_user = request.user
    if request.method == 'GET':
        form = forms.SearchFruitsForm()
        fruit_name = request.GET.get('kw')
        page_number = request.GET.get('code')
        if fruit_name:
            try:
                page_number = int(page_number)
            except:
                messages.add_message(request,messages.ERROR,' 参数错误!')
            else:
                #模糊查询水果
                #根据页码查询分页数据,设置限制返回的起始值和结束值
                search_start_num = (page_number-1)*6
                search_end_num = page_number*6
                search_fruits1 = models.Fruits.objects.filter(fruit_name__contains = fruit_name).order_by('-add_fruit_time')[search_start_num:search_end_num]
                for i in search_fruits1:
                    picture_file_name = str(i.fruit_pic_file_name)
                    if ';' in picture_file_name:
                        pictures_list = picture_file_name.split(';')
                        i.pic_html = '/static/imgs/' + pictures_list[0]
                    else:
                        i.pic_html = '/static/imgs/' + picture_file_name

                #数据为空给个消息提示
                if len(search_fruits1) == 0:
                    messages.add_message(request,messages.ERROR,' 未查询到任何满足条件水果!')
                #渲染页面
                dic1 = {'current_user':current_user,'page_number':page_number,'fruit_name':fruit_name}
                return render(request,'fruit_list_search.html',{'form':form,'dic1':dic1,'fruit_data':search_fruits1})
        else:
            messages.add_message(request,messages.ERROR,' 参数错误!')

#首页水果翻页(查看更多)
def index_fruit_page(request):
    if request.method == 'GET':
        current_user = request.user
        form = forms.SearchFruitsForm()
        page_number = request.GET.get('page_number')
        try:
            page_number = int(page_number)
        except:
            messages.add_message(request,messages.ERROR,'参数错误!')
        else:
            #根据页码查询分页数据,设置限制返回的起始值和结束值
            search_start_num = (page_number-1)*4
            search_end_num = page_number*4
            #根据页码查询指定数据
            fruits_data = models.Fruits.objects.order_by('-add_fruit_time')[search_start_num:search_end_num]
            for i in fruits_data:
                picture_file_name = str(i.fruit_pic_file_name)
                if ';' in picture_file_name:
                    pictures_list = picture_file_name.split(';')
                    i.pic_html = '/static/imgs/' + pictures_list[0]
                else:
                    i.pic_html = '/static/imgs/' + picture_file_name
            #渲染页面
            dic1 = {'current_user':current_user,'page_number':page_number}
            #查询留言板数据，最新时间排序限制10条
            comments_data = models.UserMessage.objects.order_by('-commenting_time')[0:10]
            for j in comments_data:
                #根据anonymous字段(True/False)判断是否匿名，是否使用 *替换部分字符串
                anonymous = j.anonymous
                commenting_user = str(j.commenting_user)
                if anonymous == 1:
                    num = int(len(commenting_user)/2)
                    str1 = commenting_user[0:num]
                    str2 = commenting_user[num:]
                    commenting_user = str1.replace(str1,'*'*num) + str2 
                    #更新到queryset中
                    j.commenting_user = commenting_user
                #加入表格的随机样式
                j.type = random.choice(['error','info','success','warning']) 
            return render(request,'index.html',{'form':form,'list1':fruits_data,'list2':comments_data,'dic1':dic1})

#水果商品详情页面
def fruit_details(request):
    current_user = request.user
    if request.method == 'GET':
        fruit_id = request.GET.get('id')
        try:
            fruit_id = int(fruit_id)
        except:
            messages.add_message(request,messages.ERROR,' 参数错误!')
        else:
            #查询指定水果和对应的评论信息
            fruit_data = models.Fruits.objects.filter(id = fruit_id).first()
            if fruit_data:
                pictures_list1 = []
                picture_file_name = str(fruit_data.fruit_pic_file_name)
                if ';' in picture_file_name:
                    pictures_list = picture_file_name.split(';')
                    k = 0
                    for j in pictures_list:
                        k += 1
                        pic_html = 'pic_html_' + str(k)
                        pictures_list1.append('/static/imgs/' + j)
                    fruit_data.pic_html = pictures_list1
                else:
                    pictures_list1.append('/static/imgs/' + picture_file_name)
                    fruit_data.pic_html = pictures_list1
            else:
                messages.add_message(request,messages.ERROR,' 未查询到任何满足条件水果!')
            #查询评论信息
            comments_data = models.FruitComments.objects.filter(fruit_id = fruit_id).order_by('-commenting_time')[0:5]
            for j in comments_data:
                #根据anonymous字段(True/False)判断是否匿名，是否使用 *替换部分字符串
                anonymous = j.anonymous
                commenting_user = str(j.commenting_user)
                if anonymous == 1:
                    num = int(len(commenting_user)/2)
                    str1 = commenting_user[0:num]
                    str2 = commenting_user[num:]
                    commenting_user = str1.replace(str1,'*'*num) + str2 
                    #更新到queryset中
                    j.commenting_user = commenting_user
                j.type = random.choice(['error','info','success','warning'])
            #渲染页面
            dic1 = {'current_user':current_user}
            return render(request,'fruit_details.html',{'dic1':dic1,'fruit_data':fruit_data,'comments_data':comments_data})

#水果商品详情页面添加水果到购物车
def add_to_shopping_cart(request):
    current_user = request.user
    if request.method == 'POST':
        form = forms.AddFruitsToShoppingcart(request.POST)
        if form.is_valid():
            fruit_id = request.POST.get('fruit_id')
            fruit_number = request.POST.get('fruit_number')
            try:
                fruit_number = int(fruit_number)
                fruit_id = int(fruit_id)
            except:
                messages.add_message(request,messages.ERROR,'参数错误!')
            else:
                #判断数量是否大于0，小于等于0不操作
                if fruit_number > 0:
                    #获取用户ID
                    user_1 = User.objects.filter(username = current_user).first()
                    if user_1:
                        user_id = user_1.id
                        test1 = models.ShoppingCart(id = None,customer_id = user_id,fruit_id = fruit_id,fruit_number = fruit_number)
                        test1.save() 
                        messages.add_message(request,messages.SUCCESS,' 加购成功!') 
                    else:
                        messages.add_message(request,messages.ERROR,' 用户不存在!') 

                    #重定向到详情页面 
                    last_url = '/fruitDetails/search?id=' + str(fruit_id)
                    return redirect(last_url)     
        else:
            return render(request,'error_404.html')

#购物车页面
def shopping_cart(request):
    current_user = request.user
    if request.method == 'GET':
        #通过user查ID
        user_1 =  User.objects.filter(username = current_user).first()
        if user_1:
            #定义一个字典
            list_shopping_cart_data = []
            user_id = user_1.id
            shopping_cart_datas =  models.ShoppingCart.objects.filter(customer_id = user_id).order_by('-add_fruit_time')[0:5]
            for data in shopping_cart_datas:
                #使用data里的fruit_id查询商品信息
                if data.order_number == '0':
                    fruit_data = models.Fruits.objects.filter(id = data.fruit_id).first()
                    if fruit_data:
                        picture_file_name = str(fruit_data.fruit_pic_file_name)
                        if ';' in picture_file_name:
                            pictures_list = picture_file_name.split(';')
                            fruit_data.pic_html = '/static/imgs/' + pictures_list[0]
                        else:
                            fruit_data.pic_html = '/static/imgs/' + picture_file_name
                        dic_data = {'shopping_cart_id':data.id,'fruit_number':data.fruit_number,'pic_html':fruit_data.pic_html,'fruit_name':fruit_data.fruit_name,\
                            'fruit_description':fruit_data.fruit_description,'fruit_price':fruit_data.fruit_price,'fruit_weight':fruit_data.fruit_weight}
                        list_shopping_cart_data.append(dic_data)
            #渲染页面
            dic1 = {'current_user':current_user,'page_number':1}
            return render(request,'shopping_cart.html',{'shopping_cart_data':list_shopping_cart_data,'dic1':dic1})
        else:    
            return render(request,'error_404.html')

#购物车页面翻页
def shopping_cart_page(request):
    current_user = request.user
    if request.method == 'GET':
        page_number = request.GET.get('code')
        try:
            page_number = int(page_number)
        except:
            messages.add_message(request,messages.ERROR,' 参数错误!')
        else:
            #根据页码查询数据
            search_start_num = (page_number-1)*5
            search_end_num = page_number*5
            #通过user查ID
            user_1 =  User.objects.filter(username = current_user).first()
            if user_1:
                #定义一个字典
                list_shopping_cart_data = []
                user_id = user_1.id
                shopping_cart_datas =  models.ShoppingCart.objects.filter(customer_id = user_id).order_by('-add_fruit_time')[search_start_num:search_end_num]
                for data in shopping_cart_datas:
                    #使用data里的fruit_id查询商品信息
                    if data.order_number == '0':
                        fruit_data = models.Fruits.objects.filter(id = data.fruit_id).first()
                        if fruit_data:
                            picture_file_name = str(fruit_data.fruit_pic_file_name)
                            if ';' in picture_file_name:
                                pictures_list = picture_file_name.split(';')
                                fruit_data.pic_html = '/static/imgs/' + pictures_list[0]
                            else:
                                fruit_data.pic_html = '/static/imgs/' + picture_file_name
                            dic_data = {'shopping_cart_id':data.id,'fruit_number':data.fruit_number,'pic_html':fruit_data.pic_html,'fruit_name':fruit_data.fruit_name,\
                                'fruit_description':fruit_data.fruit_description,'fruit_price':fruit_data.fruit_price,'fruit_weight':fruit_data.fruit_weight}
                            list_shopping_cart_data.append(dic_data)
                #渲染页面
                dic1 = {'current_user':current_user,'page_number':page_number}
                return render(request,'shopping_cart.html',{'shopping_cart_data':list_shopping_cart_data,'dic1':dic1})
            else:    
                return render(request,'error_404.html')

#购物车修改商品数量
def update_shopping_cart_fruit_number(request):
    current_user = request.user
    if request.method == 'POST':
        form = forms.UpdateFruitsNumberInShoppingcart(request.POST)
        if form.is_valid():
            shopping_cart_id = request.POST.get('shopping_cart_id')
            fruit_number = request.POST.get('fruit_number')
            try:
                shopping_cart_id = int(shopping_cart_id)
                fruit_number = int(fruit_number)
            except:
                messages.add_message(request,messages.ERROR,' 参数错误!')
            else:
                #更新数据到数据库中
                shopping_info =  models.ShoppingCart.objects.filter(id = shopping_cart_id).first()
                if shopping_info:
                    shopping_info.fruit_number = fruit_number
                    shopping_info.save()
                    messages.add_message(request,messages.SUCCESS,' 修改数据成功!')
                else:
                    messages.add_message(request,messages.ERROR,' 参数错误!')
        else:
            #未通过表单校验
            errors = ''
            for key,value in form.errors.items():
                errors += str(value).replace('<ul class="errorlist"><li>','').replace('</li></ul>','') + '  '
            messages.add_message(request,messages.ERROR,errors)
        #重定向购物车
        return redirect('/my_shopping_cart/')
    
#购物车删除条目
def delete_shopping_cart__fruit(request):
    current_user = request.user
    if request.method == 'GET':
        delete_fruit_id = request.GET.get('id')
        try:
            delete_fruit_id = int(delete_fruit_id)
        except:
            messages.add_message(request,messages.ERROR,' 参数错误!')
        else:
            shopping_cart_info =  models.ShoppingCart.objects.filter(id = delete_fruit_id).first()
            if shopping_cart_info:
                shopping_cart_info.delete()
                messages.add_message(request,messages.SUCCESS,'  删除成功!')
            else:
                messages.add_message(request,messages.ERROR,' 数据不存在!')
        return redirect('/my_shopping_cart/')

#订单付款确认页面
def payment_page(request):
    current_user = request.user
    if request.method == 'GET':
        #通过user查ID
        user_1 =  User.objects.filter(username = current_user).first()
        if user_1:
            #定义需付总金额
            total_amount = 0.00
            #定义一个字典
            list_shopping_cart_data = []
            user_id = user_1.id
            shopping_cart_datas =  models.ShoppingCart.objects.filter(customer_id = user_id).order_by('-add_fruit_time').all()
            for data in shopping_cart_datas:
                #使用data里的fruit_id查询商品信息
                if data.order_number == '0':
                    fruit_data = models.Fruits.objects.filter(id = data.fruit_id).first()
                    if fruit_data:
                        picture_file_name = str(fruit_data.fruit_pic_file_name)
                        if ';' in picture_file_name:
                            pictures_list = picture_file_name.split(';')
                            fruit_data.pic_html = '/static/imgs/' + pictures_list[0]
                        else:
                            fruit_data.pic_html = '/static/imgs/' + picture_file_name
                        
                        #计算单品的需付金额(保留两位小数)
                        #c = '%.2f'%a
                        amount = data.fruit_number*2*fruit_data.fruit_price
                        fruit_amount = float('%.2f'%amount)
                        total_amount += fruit_amount
                        
                        dic_data = {'shopping_cart_id':data.id,'fruit_number':data.fruit_number,'pic_html':fruit_data.pic_html,'fruit_name':fruit_data.fruit_name,\
                            'fruit_description':fruit_data.fruit_description,'fruit_price':fruit_data.fruit_price,'fruit_weight':fruit_data.fruit_weight,'fruit_amount':fruit_amount}
                        list_shopping_cart_data.append(dic_data)
            
            #总金额保留两位小数
            total_amount = float('%.2f'%total_amount)
            #查询收货地址
            address1 = None
            address2 = None
            address3 = None
            address_info = models.UserInfo.objects.filter(user_id = user_id).first()
            if address_info:
                address1 = address_info.address1
                address2 = address_info.address2
                address3 = address_info.address3
            
            if len(list_shopping_cart_data) != 0:
                #生成订单号
                order_number = 'F' + str(time.time()).replace('.','')
                #将订单号更新到购物车表数据中
                for j in shopping_cart_datas:
                    if j.order_number == '0':
                        j.order_number = order_number
                        j.save()
                
                #添加数据到订单表中
                test1 = models.FruitOrder(id = None,customer = user_id,order_number = order_number,money = total_amount,pay_status = '0', order_status= '0')
                test1.save()
            else:
                order_number = None
            #渲染页面
            dic1 = {'current_user':current_user,'address1':address1,'address2':address2,'address3':address3,'total_amount':total_amount,'order_number':order_number}
            return render(request,'order_balance_page.html',{'shopping_cart_data':list_shopping_cart_data,'dic1':dic1})
        else:
            messages.add_message(request,messages.ERROR,' 数据不存在!')
            return redirect('/settle_accounts/')
            
#付款(支付宝接口付款)
def ali_pay(request):
    pass

#用户管理
def user_management(request):
    current_user = request.user
    if request.method == 'GET':
        user_info = User.objects.all().order_by('-date_joined')[0:10]
        for j in user_info:
            #给表格加style
            j.style = random.choice(['error','info','success','warning']) 
            time_last_login = j.last_login
            if time_last_login:
                j.last_login = time_last_login.strftime("%Y-%m-%d %H:%M:%S")
            else:
                j.last_login = None
        dic1 = {'current_user':current_user,'page_number':1}
        return render(request,'management.html',{'dic1':dic1,'user_data':user_info})

#用户管理翻页
def user_management_page(request):
    current_user = request.user
    if request.method == 'GET':
        page_number = request.GET.get('page_number')
        try:
            page_number = int(page_number)
        except:
            messages.add_message(request,messages.ERROR,' 参数错误!')
        else:
            #根据页码查询数据
            search_start_num = (page_number-1)*10
            search_end_num = page_number*10
            user_info = User.objects.all().order_by('-date_joined')[search_start_num:search_end_num]
            for j in user_info:
                #给表格加style
                j.style = random.choice(['error','info','success','warning']) 
                time_last_login = j.last_login
                if time_last_login:
                    j.last_login = time_last_login.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    j.last_login = None
            dic1 = {'current_user':current_user,'page_number':page_number}
            return render(request,'management.html',{'dic1':dic1,'user_data':user_info})

#用户管理查询用户
def user_management_search_user(request):
    current_user = request.user
    form = forms.SearchUserForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            username = request.POST.get('username')
            if username:
                user_info = User.objects.filter(username__contains = username).order_by('-date_joined')[0:10]
                for j in user_info:
                    #给表格加style
                    j.style = random.choice(['error','info','success','warning']) 
                    time_last_login = j.last_login
                    if time_last_login:
                        j.last_login = time_last_login.strftime("%Y-%m-%d %H:%M:%S")
                    else:
                        j.last_login = None
                dic1 = {'current_user':current_user,'page_number':1,'username':username}
                return render(request,'management_search.html',{'dic1':dic1,'user_data':user_info})
            else:
                messages.add_message(request,messages.ERROR,' 参数错误!')
                return redirect('/management/')
        else:
            #未通过表单校验
            errors = ''
            for key,value in form.errors.items():
                errors += str(value).replace('<ul class="errorlist"><li>','').replace('</li></ul>','') + '  '
            messages.add_message(request,messages.ERROR,errors)
            return redirect('/management/')

#用户管理查询用户翻页
def user_management_search_user_page(request):
    current_user = request.user
    if request.method == 'GET':
        username = request.GET.get('search')
        page_number = request.GET.get('page_number')
        if username:
            try:
                page_number = int(page_number)
            except:
                messages.add_message(request,messages.ERROR,' 参数错误!')
            else:
                #根据页码查询数据
                search_start_num = (page_number-1)*10
                search_end_num = page_number*10
                user_info = User.objects.filter(username__contains = username).order_by('-date_joined')[search_start_num:search_end_num]
                for j in user_info:
                    #给表格加style
                    j.style = random.choice(['error','info','success','warning']) 
                    time_last_login = j.last_login
                    if time_last_login:
                        j.last_login = time_last_login.strftime("%Y-%m-%d %H:%M:%S")
                    else:
                        j.last_login = None
                dic1 = {'current_user':current_user,'page_number':page_number,'username':username}
                return render(request,'management_search.html',{'dic1':dic1,'user_data':user_info})
        else:
            messages.add_message(request,messages.ERROR,' 参数错误!')

#用户管理停用账号
def user_management_disable_user(request):
    current_user = request.user
    if request.method == 'GET':
        user_id = request.GET.get('id')
        try:
            user_id = int(user_id)
        except:
            messages.add_message(request,messages.ERROR,' 参数错误!')
        else:
            userinfo = User.objects.filter(id = user_id).first()
            if userinfo:
                if userinfo.is_active == True:
                    userinfo.is_active = False
                    userinfo.save()
                    messages.add_message(request,messages.ERROR,' 停用成功!')
                else:
                    messages.add_message(request,messages.ERROR,' 此账号已经处于停用状态!')
            else:
                messages.add_message(request,messages.ERROR,' 用户不存在!')
        return redirect('/management/')

#用户管理启用账号
def user_management_enable_user(request):
    current_user = request.user
    if request.method == 'GET':
        user_id = request.GET.get('id')
        try:
            user_id = int(user_id)
        except:
            messages.add_message(request,messages.ERROR,' 参数错误!')
        else:
            userinfo = User.objects.filter(id = user_id).first()
            if userinfo:
                if userinfo.is_active == False:
                    userinfo.is_active = True
                    userinfo.save()
                    messages.add_message(request,messages.ERROR,' 启用成功!')
                else:
                    messages.add_message(request,messages.ERROR,' 此账号已经处于启用状态!')
            else:
                messages.add_message(request,messages.ERROR,' 用户不存在!')
        return redirect('/management/')

#用户管理删除账号
def user_management_delete_user(request):
    current_user = request.user
    if request.method == 'GET':
        user_id = request.GET.get('id')
        try:
            user_id = int(user_id)
        except:
            messages.add_message(request,messages.ERROR,' 参数错误!')
        else:
            userinfo = User.objects.filter(id = user_id).first()
            if userinfo:
                userinfo.delete()
                userinfo.save()
                messages.add_message(request,messages.SUCCESS,' 删除成功!')
            else:
                messages.add_message(request,messages.ERROR,' 删除失败!')
        return redirect('/management/')


#用户管理修改账号
def user_management_update_user(request):
    current_user = request.user
    if request.method == 'POST':
        form = forms.ManagementUserUpdate(request.POST)
        if form.is_valid():
            update_id = request.POST.get('update_id')
            update_email = request.POST.get('update_email')
            #print(update_id,update_email)
            userinfo = User.objects.filter(id = update_id).first()
            if userinfo:
                if userinfo.email != update_email:
                    userinfo.email = update_email
                    userinfo.save()
                    messages.add_message(request,messages.SUCCESS,' 更新成功!')
                else:
                    messages.add_message(request,messages.SUCCESS,' 无需更新!')
            else:
                messages.add_message(request,messages.ERROR,' 用户不存在!')
        else:
            #未通过表单校验
            errors = ''
            for key,value in form.errors.items():
                errors += str(value).replace('<ul class="errorlist"><li>','').replace('</li></ul>','') + '  '
            messages.add_message(request,messages.ERROR,errors)
        return redirect('/management/')

#用户管理添加账号
def user_management_add_user(request):
    current_user = request.user
    if request.method == 'POST':
        form = forms.ManagementUserAdd(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            email = request.POST.get('email')
            group_id = request.POST.get('group_id')
            if username and password and email and group_id:
                if not User.objects.filter(username = username).first():
                    User.objects.create_user(username = username,password = password)
                    user_info = User.objects.filter(username = username).first()
                    if user_info:
                        user_info.email = email
                        user_info.save()
                        #根据不同的group_id 分配不同的用户组
                        if group_id == '1':
                            group1 = Group.objects.get(name = 'admin')
                            group1.user_set.add(user_info)
                        elif group_id == '2': 
                            group1 = Group.objects.get(name = 'customer')
                            group1.user_set.add(user_info)
                         
                        messages.add_message(request,messages.SUCCESS,'添加用户 ' + username + ' 成功!')
                    else:
                        messages.add_message(request,messages.ERROR,'添加用户 ' + username + ' 失败!')
                else:
                    messages.add_message(request,messages.ERROR,'添加用户 ' + username + ' 失败! 重复注册!')
            else:
                messages.add_message(request,messages.ERROR,' 参数错误!')
        else:
            ##未通过表单校验
            errors = ''
            for key,value in form.errors.items():
                errors += str(value).replace('<ul class="errorlist"><li>','').replace('</li></ul>','') + '  '
            messages.add_message(request,messages.ERROR,errors)
    return redirect('/management/')

#用户管理导入账号
def user_management_import_user(request):
    current_user = request.user
    if request.method == 'POST':
        form = forms.ManagementUserImport(request.POST,request.FILES)
        if form.is_valid():
            user_file = request.FILES.get('user_file')
            if user_file:
                file_extension = os.path.splitext(user_file.name)[-1]
                if '.xlsx' == file_extension or '.xls' == file_extension:
                    file_name =  str(time.time()) + file_extension
                    user_file_dir = os.getcwd() + os.path.join(os.sep,'temp', file_name)
                    #保存文件到临时文件目录temp
                    with open(user_file_dir,'wb') as f:
                        for chunk in user_file.chunks():
                            f.write(chunk)
                    #读取excel写入数据库
                    work_book = xlrd.open_workbook (user_file_dir)
                    ws = work_book.sheet_by_name('Sheet1')
                    #读取第一行数据
                    if ws.nrows != 0:
                        line_1_values = ws.row_values(0)
                        if line_1_values == ['用户名','密码','邮箱','用户组ID']:
                            message_list = []
                            for i in range(1,ws.nrows):
                                try:
                                    values_list = ws.row_values(i)
                                    username = values_list[0]
                                    password = values_list[1]
                                    email = values_list[2]
                                    group_id = values_list[3]
                                
                                    if not User.objects.filter(username = username).first():
                                        User.objects.create_user(username = username,password = password)
                                        user_info = User.objects.filter(username = username).first()
                                        if user_info:
                                            user_info.email = email 
                                            user_info.save()
                                            #根据不同的group_id 分配不同的用户组
                                            if int(group_id) == 1:
                                                group1 = Group.objects.get(name = 'admin')
                                                group1.user_set.add(user_info)
                                            elif int(group_id) == 2: 
                                                group1 = Group.objects.get(name = 'customer')
                                                group1.user_set.add(user_info)
                                            message = '导入用户: ' + username + ' 成功!'
                                            message_list.append(message)
                                        else:
                                            message= '更新' + username + '邮箱,用户组失败!'
                                            message_list.append(message)
                                    else:
                                        message = '用户: ' + username +' 已存在，导入失败! '
                                        message_list.append(message)
                                except:
                                    pass
                            msgs = ''
                            for msg in message_list:
                                msgs += msg
                            messages.add_message(request,messages.ERROR,msgs)
                        else:
                            messages.add_message(request,messages.ERROR,' 数据格式错误!')
                    else:
                        messages.add_message(request,messages.ERROR,' 空数据!')
                else:
                    messages.add_message(request,messages.ERROR,' 请上传excel文件!')

            else:
                messages.add_message(request,messages.ERROR,' 文件不存在!')
        else:
            #未通过表单校验
            errors = ''
            for key,value in form.errors.items():
                errors += str(value).replace('<ul class="errorlist"><li>','').replace('</li></ul>','') + '  '
            messages.add_message(request,messages.ERROR,errors)
        return redirect('/management/')

#用户管理导入账号模板下载
def user_management_download_import_user_file(request):
    if request.method == 'GET':
        user_template_file = os.getcwd() + os.path.join(os.sep,'media','template_import_user.zip')
        if os.path.isfile(user_template_file) == True:
            try:
                f = open(user_template_file,'rb')
                response = FileResponse(f)
                response['Content-Type'] = 'application/octet-stream'
                response['Content-Disposition'] = 'attachment;filename=' + 'template_import_user.zip'
                return response
            except:
                messages.add_message(request,messages.ERROR,' 下载失败!')
                return redirect('/management/')
        else:
            messages.add_message(request,messages.ERROR,' 模板文件不存在!')
            return redirect('/management/')

#权限管理
def permission_management(request):
    current_user = request.user
    if request.method == 'GET':
        permission_info = models.RoutePermission.objects.all().order_by('-add_route_permission_time')[0:10]
        for j in permission_info:
            #给表格加style
            j.style = random.choice(['error','info','success','warning']) 
        dic1 = {'current_user':current_user,'page_number':1}
        return render(request,'management_permission.html',{'dic1':dic1,'permission_data':permission_info})

#权限管理翻页
def permission_management_page(request):
    current_user = request.user
    if request.method == 'GET':
        page_number = request.GET.get('page_number')
        try:
            page_number = int(page_number)
        except:
            messages.add_message(request,messages.ERROR,' 参数错误!')
        else:
            #根据页码限制返回权限数据
            search_start_num = (page_number-1)*10
            search_end_num = page_number*10
            permission_info = models.RoutePermission.objects.all().order_by('-add_route_permission_time')[search_start_num:search_end_num]
            for j in permission_info:
                #给表格加style
                j.style = random.choice(['error','info','success','warning']) 
            dic1 = {'current_user':current_user,'page_number':page_number}
            return render(request,'management_permission.html',{'dic1':dic1,'permission_data':permission_info})

#权限管理按url模糊查询
def permission_management_search_by_url(request):
    current_user = request.user
    if request.method == 'POST':
        form = forms.ManagementPermissionSearch (request.POST)
        if form.is_valid():
            url = request.POST.get('url')
            #模糊查询URL
            if url:
                search_permissions = models.RoutePermission.objects.filter(url__contains = url).order_by('-add_route_permission_time')[0:10]
                for i in search_permissions:
                    #给表格加style
                    i.style = random.choice(['error','info','success','warning'])
                #数据为空给个消息提示
                if len(search_permissions) == 0:
                    messages.add_message(request,messages.ERROR,' 未查询到任何满足条件的权限条目!')  
                #渲染页面
                dic1 = {'current_user':current_user,'page_number':1,'url':url}
                return render(request,'management_permission_search.html',{'form':form,'dic1':dic1,'permission_data':search_permissions}) 
            else:
                messages.add_message(request,messages.ERROR,' 未收到url数据!')     
        else:
            #未通过表单校验
            errors = ''
            for key,value in form.errors.items():
                errors += str(value).replace('<ul class="errorlist"><li>','').replace('</li></ul>','') + '  '
            type = 'alert alert-dismissable alert-danger'
            messages.add_message(request, messages.ERROR, errors)
        return redirect('/management/permission/')

#权限管理按url模糊查询翻页
def permission_management_search_by_url_page(request):
    current_user = request.user
    if request.method == 'GET':
        url = request.GET.get('url')
        page_number = request.GET.get('page_number')
        if url:
            try:
                page_number = int(page_number)
            except:
                messages.add_message(request,messages.ERROR,' 参数错误!')
                return redirect('/management/permission/')
            else:
                #根据页码限制返回权限数据
                search_start_num = (page_number-1)*10
                search_end_num = page_number*10
                permission_info = models.RoutePermission.objects.filter(url__contains = url).order_by('-add_route_permission_time')[search_start_num:search_end_num]
                for j in permission_info:
                    #给表格加style
                    j.style = random.choice(['error','info','success','warning']) 
                dic1 = {'current_user':current_user,'page_number':page_number,'url':url}
                return render(request,'management_permission_search.html',{'dic1':dic1,'permission_data':permission_info})
        else:
            messages.add_message(request,messages.ERROR,' url参数错误!')
            return redirect('/management/permission/')

#权限管理按用户组查询
def permission_management_search_by_user_group(request):
    current_user = request.user
    if request.method == 'GET':
        code = request.GET.get('code')
        try:
            code = int(code)
        except:
            messages.add_message(request,messages.ERROR,' code参数错误!')
            return redirect('/management/permission/')
        else:
            #根据code查询数据
            group_name = None
            if code == 1:
                group_name = 'admin'
            elif code == 2:
                group_name = 'customer'
            if group_name:
                permission_info = models.RoutePermission.objects.filter(group_name = group_name).order_by('-add_route_permission_time').all()[0:10]
                for i in permission_info:
                    #给表格加style
                    i.style = random.choice(['error','info','success','warning']) 
                dic1 = {'current_user':current_user,'page_number':1,'code':code}
                return render(request,'management_permission_type.html',{'dic1':dic1,'permission_data':permission_info})
            else:
                messages.add_message(request,messages.ERROR,' group_name参数错误!')
                return redirect('/management/permission/')

#权限管理按用户组查询翻页
def permission_management_search_by_user_group_page(request):
    current_user = request.user
    if request.method == 'GET':
        code = request.GET.get('code')
        page_number = request.GET.get('page_number')
        try:
            page_number = int(page_number)
            code = int(code)
        except:
            messages.add_message(request,messages.ERROR,' 参数错误!')
            return redirect('/management/permission/')
        else:
            #根据页码限制返回权限数据
            search_start_num = (page_number-1)*10
            search_end_num = page_number*10
            group_name = None
            if code == 1:
                group_name = 'admin'
            elif code == 2:
                group_name = 'customer'
            if group_name:
                permission_info = models.RoutePermission.objects.filter(group_name = group_name).order_by('-add_route_permission_time')[search_start_num:search_end_num]
                for j in permission_info:
                    #给表格加style
                    j.style = random.choice(['error','info','success','warning']) 
                dic1 = {'current_user':current_user,'page_number':page_number,'code':code}
                return render(request,'management_permission_type.html',{'dic1':dic1,'permission_data':permission_info})
            else:
                messages.add_message(request,messages.ERROR,' group_name参数错误!')
                return redirect('/management/permission/')
    
#权限管理添加权限数据
def permission_management_add_permission(request):
    current_user = request.user
    if request.method == 'POST':
        form = forms.ManagementPermissionAdd(request.POST)
        if form.is_valid():
            url = request.POST.get('url')
            description = request.POST.get('description')
            group_id = request.POST.get('group_id')
            if url and description:
                try:
                    group_id = int(group_id)
                except:
                    messages.add_message(request,messages.ERROR,' group_id参数错误!')
                else:
                    #根据group_id 判断是哪个角色
                    group_name = None
                    if group_id == 1:
                        group_name = 'admin'
                    elif group_id == 2:
                        group_name = 'customer'
                    #add data
                    test1 = models.RoutePermission(id = None,group_name = group_name,url = url,description = description)
                    test1.save()
                    messages.add_message(request,messages.SUCCESS,' 添加权限: '+ str((group_name,url,description)) + ' 成功!' )
            else:
                messages.add_message(request,messages.ERROR,' url,description参数错误!')
        else:
            #未通过表单校验
            errors = ''
            for key,value in form.errors.items():
                errors += str(value).replace('<ul class="errorlist"><li>','').replace('</li></ul>','') + '  '
            messages.add_message(request, messages.ERROR, errors)
    return redirect('/management/permission/')

#权限管理导入权限数据
def permission_management_import_permission(request):
    current_user = request.user
    if request.method == 'POST':
        form = forms.ManagementPermissionImport(request.POST,request.FILES)
        if form.is_valid():
            permission_file = request.FILES.get('permission_file')
            if permission_file:
                file_extension = os.path.splitext(permission_file.name)[-1]
                if '.xlsx' == file_extension or '.xls' == file_extension:
                    file_name =  str(time.time()) + file_extension
                    permission_file_dir = os.getcwd() + os.path.join(os.sep,'temp', file_name)
                    #保存文件到临时文件目录temp
                    with open(permission_file_dir,'wb') as f:
                        for chunk in permission_file.chunks():
                            f.write(chunk)
                    #读取excel写入数据库
                    work_book = xlrd.open_workbook (permission_file_dir)
                    ws = work_book.sheet_by_name('Sheet1')
                    #读取第一行数据
                    if ws.nrows != 0:
                        line_1_values = ws.row_values(0)
                        print(line_1_values)
                        if line_1_values == ['URL','描述信息','用户组ID']:
                            message_list = []
                            for i in range(1,ws.nrows):
                                try:
                                    values_list = ws.row_values(i)
                                    url = values_list[0]
                                    description = values_list[1]
                                    group_id = values_list[2]
                                    #根据不同的group_id 分配不同的用户组
                                    group_name = None
                                    if int(group_id) == 1:
                                        group_name = 'admin'
                                    elif int(group_id) == 2: 
                                        group_name = 'customer'
                                    #加入数据库
                                    test1 = models.RoutePermission(id = None,group_name = group_name,url = url,description = description)
                                    test1.save()
                                    #加入消息列表
                                    msg = ' 导入权限 ' +str((group_name,url,description)) +' 成功!'
                                    message_list.append(msg)
                                except:
                                    #加入消息列表
                                    msg = ' 导入权限 ' +str((group_name,url,description)) +' 失败!'
                                    message_list.append(msg)
                            #从message_list 取提示
                            msgs = ''
                            for msg in message_list:
                                msgs += msg
                            messages.add_message(request,messages.ERROR,msgs)
                        else:
                            messages.add_message(request,messages.ERROR,' 数据格式错误!')
                    else:
                        messages.add_message(request,messages.ERROR,' 空数据!')
                else:
                    messages.add_message(request,messages.ERROR,' 请上传excel文件!')

            else:
                messages.add_message(request,messages.ERROR,' 文件不存在!')
        else:
            #未通过表单校验
            errors = ''
            for key,value in form.errors.items():
                errors += str(value).replace('<ul class="errorlist"><li>','').replace('</li></ul>','') + '  '
            messages.add_message(request,messages.ERROR,errors)
        return redirect('/management/permission/')

#权限管理导入权限数据下载模板
def permission_management_download_import_permission_file(request):
    if request.method == 'GET':
        permission_template_file = os.getcwd() + os.path.join(os.sep,'media','template_import_permission.zip')
        if os.path.isfile(permission_template_file) == True:
            try:
                f = open(permission_template_file,'rb')
                response = FileResponse(f)
                response['Content-Type'] = 'application/octet-stream'
                response['Content-Disposition'] = 'attachment;filename=' + 'template_import_permission.zip'
                return response
            except:
                messages.add_message(request,messages.ERROR,' 下载失败!')
                return redirect('/management/permission/')
        else:
            messages.add_message(request,messages.ERROR,' 模板文件不存在!')
            return redirect('/management/permission/')

#权限管理修改权限数据
def permission_management_update_permission(request):
    current_user = request.user
    if request.method == 'POST':
        form = forms.ManagementPermissionUpdate(request.POST)
        if form.is_valid():
            update_id = request.POST.get('update_id')
            update_url = request.POST.get('update_url')
            update_description = request.POST.get('update_description')
            update_group_id = request.POST.get('update_group_id')
            permission_info = models.RoutePermission.objects.filter(id = update_id).first()
            if permission_info:
                message1 = ''
                message2 = ''
                message3 = ''
                if permission_info.url != update_url:
                    permission_info.url = update_url
                    permission_info.save()
                    message1 = 'URL'
                if permission_info.description != update_description:
                    permission_info.description = update_description
                    permission_info.save()
                    message2 = '描述信息'
                #通过group_id 确定group_name
                group_name = None
                if update_group_id == '1':
                    group_name = 'admin'
                elif update_group_id == '2':
                    group_name = 'customer'
                if permission_info.group_name != group_name:
                    permission_info.group_name = group_name
                    permission_info.save()
                    message3 = '用户组ID'
                messages.add_message(request,messages.SUCCESS,'修改字段: ' + message1 +' '+ message2 +' '+ message3 +' 成功!')
            else:
                messages.add_message(request,messages.ERROR,' 权限不存在!')
        else:
            #未通过表单校验
            errors = ''
            for key,value in form.errors.items():
                errors += str(value).replace('<ul class="errorlist"><li>','').replace('</li></ul>','') + '  '
            messages.add_message(request,messages.ERROR,errors)
        return redirect('/management/permission/')

#权限管理删除权限数据
def permission_management_delete_permission(request):
    current_user = request.user
    if request.method == 'GET':
        delete_permission_id = request.GET.get('id')
        try:
            delete_permission_id = int(delete_permission_id)
        except:
            messages.add_message(request,messages.ERROR,' delete_permission_id参数错误!')
        else:
            permission_info = models.RoutePermission.objects.filter(id = delete_permission_id).first()
            if permission_info:
                permission_info.delete()
                permission_info.save()
                messages.add_message(request,messages.SUCCESS,' 删除成功!')
            else:
                messages.add_message(request,messages.ERROR,' 删除失败!')
        return redirect('/management/permission/')

#订单管理
def order_management(request):
    pass

#商品管理
def goods_management(request):
    pass

#账目管理
def account_management(request):
    pass

#退货管理
def returngoods_management(request):
    pass
