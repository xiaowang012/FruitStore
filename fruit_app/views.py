#coding=utf-8
import re
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib import messages
from . import forms
from . import models
import random

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
        
#获取水果列表
def get_fruit_info(request):
    if request.method == 'GET':
        fruit_type_id = request.GET.get('code')
        #根据根据fruit_type_id 查询不同的水果
        print(id)
        return render(request,'fruit_list.html')
    

#首页查询水果(模糊查询)
def search_fruit_info(request):
    current_user = request.user
    if request.method == 'GET':
        form = forms.SearchFruitsForm()
        dic1 = {'current_user':current_user}
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
            dic1 = {'current_user':current_user}
            return render(request,'fruit_list_search.html',{'form':form,'dic1':dic1,'fruit_data':search_fruits1})
        else:
            #未通过表单校验
            errors = ''
            for key,value in form.errors.items():
                errors += str(value).replace('<ul class="errorlist"><li>','').replace('</li></ul>','') + '  '
            type = 'alert alert-dismissable alert-danger'
            messages.add_message(request, messages.ERROR, errors)
            print(request.get_full_path())
            return redirect('/getfruitList/')
    
#首页水果翻页(查看更多)
def index_fruit_page(request):
    if request.method == 'GET':
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
            #
            dic1 = {}
            pass


#水果商品详情页面
def fruit_details(request):
    if request.method == 'GET':
        return render(request,'fruit_details.html')

#购物车页面
def shopping_cart(request):
    return render(request,'shopping_cart.html')

#订单付款确认页面
def payment_page(request):
    return render(request,'order_balance_page.html')

#付款(支付宝接口付款)
def ali_pay(request):
    pass

#商城后台管理
def store_management(request):
    return render(request,'management.html')

#权限管理
def permission_management(request):
    pass

#订单管理
def order_management(request):
    pass

#用户管理
def user_management(request):
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
