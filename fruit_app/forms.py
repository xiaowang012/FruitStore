#coding-utf-8
from django import forms
from django.core.exceptions import ValidationError
from django.forms.widgets import  PasswordInput

#登录表单
class UserForm(forms.Form):
    username = forms.CharField(min_length=3,max_length=10,error_messages={"required":"用户名不能为空!","min_length":"用户名长度不能小于3!","max_length":"用户名长度不能大于10!"})
    password = forms.CharField(widget=PasswordInput,min_length=3,max_length=10,error_messages={"required":"密码不能为空!","min_length":"密码长度不能小于3!","max_length":"密码长度不能大于10!"})

#注册表单  
class RegisterForm(forms.Form):
    username = forms.CharField(min_length=3,max_length=10,error_messages={"required":"用户名不能为空!","min_length":"用户名长度不能小于3!","max_length":"用户名长度不能大于10!"})
    password = forms.CharField(widget=PasswordInput,min_length=3,max_length=10,error_messages={"required":"密码不能为空!","min_length":"密码长度不能小于3!","max_length":"密码长度不能大于10!"})
    password1 = forms.CharField(widget=PasswordInput,min_length=3,max_length=10,error_messages={"required":"密码不能为空!","min_length":"密码长度不能小于3!","max_length":"密码长度不能大于10!"})
    def clean(self):  # 全局钩子 确认两次输入的密码是否一致。
        val = self.cleaned_data.get("password")
        r_val = self.cleaned_data.get("password1")
        if val == r_val:
            return self.cleaned_data
        else:
            raise ValidationError("两次输入的密码不一致!")

#修改密码表单
class ChangeUserPassword(forms.Form):
    username = forms.CharField(min_length=3,max_length=10,error_messages={"required":"用户名不能为空!","min_length":"用户名长度不能小于3!","max_length":"用户名长度不能大于10!"})
    old_password = forms.CharField(widget=PasswordInput,min_length=3,max_length=10,error_messages={"required":"密码不能为空!","min_length":"密码长度不能小于3!","max_length":"密码长度不能大于10!"})
    new_password1 = forms.CharField(widget=PasswordInput,min_length=3,max_length=10,error_messages={"required":"密码不能为空!","min_length":"密码长度不能小于3!","max_length":"密码长度不能大于10!"})
    new_password2 = forms.CharField(widget=PasswordInput,min_length=3,max_length=10,error_messages={"required":"密码不能为空!","min_length":"密码长度不能小于3!","max_length":"密码长度不能大于10!"})
    def clean(self):  # 全局钩子 确认两次输入的密码是否一致。
        val = self.cleaned_data.get("new_password1")
        r_val = self.cleaned_data.get("new_password2")
        if val == r_val:
            return self.cleaned_data
        else:
            raise ValidationError("两次输入的密码不一致!")

#修改个人信息表单
class UpdateUserInfo(forms.Form):
    username = forms.CharField(min_length=3,max_length=10,error_messages={"required":"用户名不能为空!","min_length":"用户名长度不能小于3!","max_length":"用户名长度不能大于10!"})
    chinese_name = forms.CharField(min_length=1,max_length=50,error_messages={"required":"姓名不能为空!","min_length":"姓名长度不能小于1!","max_length":"姓名长度不能大于50!"})
    sex = forms.CharField(min_length=1,max_length=10,error_messages={"required":"性别不能为空!","min_length":"性别长度不能小于1!","max_length":"性别长度不能大于10!"})
    birthday = forms.CharField(min_length=1,max_length=50,error_messages={"required":"生日不能为空!","min_length":"生日长度不能小于1!","max_length":"生日长度不能大于50!"})
    constellation = forms.CharField(min_length=1,max_length=50,error_messages={"required":"星座不能为空!","min_length":"星座长度不能小于1!","max_length":"星座长度不能大于50!"})
    phone_number = forms.CharField(min_length=1,max_length=50,error_messages={"required":"电话号码不能为空!","min_length":"电话号码长度不能小于1!","max_length":"电话号码长度不能大于50!"})
    address1 = forms.CharField(min_length=1,max_length=200,error_messages={"required":"收货地址1不能为空!","min_length":"收货地址1长度不能小于1!","max_length":"姓名长度不能大于200!"})
    address2 = forms.CharField(min_length=1,max_length=200,error_messages={"required":"收货地址2不能为空!","min_length":"收货地址2长度不能小于1!","max_length":"姓名长度不能大于200!"})
    address3 = forms.CharField(min_length=1,max_length=200,error_messages={"required":"收货地址3不能为空!","min_length":"收货地址3长度不能小于1!","max_length":"姓名长度不能大于200!"})

#首页给我留言
class UserSendMessage(forms.Form):
    commenting_user = forms.CharField(min_length=3,max_length=10,error_messages={"required":"用户名不能为空!","min_length":"用户名长度不能小于3!","max_length":"用户名长度不能大于10!"})
    message_content = forms.CharField(min_length=1,max_length=200,error_messages={"required":"留言信息不能为空!","min_length":"留言信息长度不能小于1!","max_length":"留言信息长度不能大于200!"})
    anonymous = forms.CharField(required = False,min_length=1,max_length=10,error_messages={"min_length":"是否匿名长度不能小于1!","max_length":"是否匿名长度不能大于10!"})

#主页查询商品信息(水果)
class SearchFruitsForm(forms.Form):
    fruitname = forms.CharField(min_length=1,max_length=100,error_messages={"required":"商品名称不能为空!","min_length":"商品名长度不能小于1!","max_length":"商品名长度不能大于100!"})

# #查询书本的表单
# class SearchBookForm(forms.Form):
#     book_name = forms.CharField(min_length=3,max_length=100,error_messages={"required":"输入框不能为空!","min_length":"搜索内容长度不能小于3!","max_length":"搜索内容长度不能大于100!"})
     
# #导入用户表单
# class AddUserForm(forms.Form):
#     user_file = forms. FileField(required = True,allow_empty_file = False,error_messages={"required":"文件不能为空!","empty":"不允许上传空文件!"})

# #修改书本信息的表单
# class UpdateBooksForm(forms.Form):
#     bookname = forms.CharField(min_length=1,max_length=50,error_messages={"min_length":"bookname长度不能小于1!","max_length":"bookname长度不能大于50!"})
#     booktype =forms.CharField(min_length=1,max_length=50,error_messages={"min_length":"booktype长度不能小于1!","max_length":"booktype长度不能大于50!"})
#     book_description = forms.CharField(max_length=200,error_messages={"max_length":"book_description长度不能大于200!"})
#     issue_year = forms.CharField(min_length=1,max_length=50,error_messages={"min_length":"issue_year长度不能小于1!","max_length":"issue_year长度不能大于50!"})
#     file_name = forms.CharField(min_length=1,max_length=100,error_messages={"min_length":"file_name长度不能小于1!","max_length":"file_name长度不能大于50!"})

# #添加permission表单
# class AddPermissionForm(forms.Form):
#     group_name = forms.CharField(min_length=1,max_length=50,error_messages={"required":"用户组不能为空!","min_length":"用户组长度不能小于1!","max_length":"用户组长度不能大于50!"})
#     url = forms.CharField(min_length=1,max_length=50,error_messages={"required":"URL不能为空!","min_length":"URL长度不能小于1!","max_length":"URL长度不能大于50!"})
#     description = forms.CharField(min_length=1,max_length=50,error_messages={"required":"description不能为空!","min_length":"description长度不能小于1!","max_length":"description长度不能大于50!"})

# #修改permission表单
# class UpdatePermissionForm(forms.Form):
#     group_name1 = forms.CharField(min_length=1,max_length=50,error_messages={"min_length":"用户组长度不能小于1!","max_length":"用户组长度不能大于50!"})
#     url1 = forms.CharField(min_length=1,max_length=50,error_messages={"min_length":"URL长度不能小于1!","max_length":"URL长度不能大于50!"})
#     description1 = forms.CharField( min_length=1,max_length=50,error_messages={"min_length":"description长度不能小于1!","max_length":"description长度不能大于50!"})

# #批量导入permission
# class UploadPermissionForm(forms.Form):
#     permission_file = forms.FileField(required = True,allow_empty_file = False,error_messages={"required":"文件不能为空!","empty":"不允许上传空文件!"})