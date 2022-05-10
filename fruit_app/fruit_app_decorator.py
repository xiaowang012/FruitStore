#coding=utf-8
from functools import wraps
from django.http import HttpResponse
from fruit_app.models import RoutePermission,AppUserGroup
from django.contrib.auth.models import User,Group
from django.shortcuts import render

# 权限缓存
PERMISSION_DICT = {}

#检查路由权限
def routing_permission_check(func):
    @wraps(func)
    def wrapper(request,*args,**kwargs):
        #获取用户名
        user = request.user
        #获取当前访问的url
        current_url = request.path
        if PERMISSION_DICT:
            userinfo = User.objects.filter(username = user).first()
            if userinfo:
                user_id = userinfo.id
                groupinfo = AppUserGroup.objects.filter(user_id = user_id).first()
                if groupinfo:
                    group_id = groupinfo.group_id
                    group_name_info = Group.objects.filter(id = group_id ).first()
                    if group_name_info:
                        group_name = group_name_info.name
                        if group_name in PERMISSION_DICT:
                            if current_url in PERMISSION_DICT[group_name]:
                                return func(request,*args,**kwargs)
                            else:
                                return render(request,'error_403.html')
                        else:
                            return render(request,'error_403.html')
                    else:
                        return render(request,'error_403.html')
                else:
                    return render(request,'error_403.html')
            else:
                return render(request,'error_403.html')
        else:
            user_group_data = Group.objects.all()
            for group in user_group_data:
                group_name = group.name
                permission_info = RoutePermission.objects.filter(group_name = group_name).all()
                url_list = []
                for per in permission_info:
                    url_list.append(per.url)
                PERMISSION_DICT[group_name] = url_list
            userinfo = User.objects.filter(username = user).first()
            if userinfo:
                user_id = userinfo.id
                groupinfo = AppUserGroup.objects.filter(user_id = user_id).first()
                if groupinfo:
                    group_id = groupinfo.group_id
                    group_name_info = Group.objects.filter(id = group_id ).first()
                    if group_name_info:
                        group_name = group_name_info.name
                        if current_url in PERMISSION_DICT[group_name]:
                            return func(request,*args,**kwargs)
                        else:
                            return render(request,'error_403.html')
                    else:
                        return render(request,'error_403.html')
                else:
                    return render(request,'error_403.html')
            else:
                return render(request,'error_403.html')    
    return wrapper

