#coding=utf-8
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib import auth
from django.contrib.auth.models import User
from . import forms

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
    if request.method == "POST":
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
#@login_required
#@permission_check
def logout(request):
    auth.logout(request)
    return redirect('/login/')

#商城首页
# @login_required
# @permission_check
def store_index(request):
    if request.method == 'GET':
        form = forms.SearchFruitsForm(request.POST)
        #获取当前用户名
        current_user = request.user
        #前端数据
        # dic1 = {'current_user   ':current_user,'active1':'active','active2':'','active3':'',\
        # 'active4':'','active5':'','current_page_number':1}
        # #查看测试用例数据(一次10条)
        # testcase_info = models.Books.objects.all()[:5]
        # #加入每一行数据的的样式到queryset中
        # for data in book_info:
        #     data.style = random.choice(['success','info','warning','error'])
        # return render(request,'my_testcase.html',{'form':form,'list1':book_info,'dic1':dic1})
        return render(request,'index.html')

def user_info(request):
    if request.method == 'GET':
        return render(request,'user_info.html')


#商城后台管理
def store_management(request):
    pass
