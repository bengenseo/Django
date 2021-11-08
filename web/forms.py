from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django import forms
import re


class RegisterForm(UserCreationForm):
    name = forms.CharField(max_length=20, required=False)
    phone = forms.CharField(max_length=11)

    class Meta:
        model = User
        fields = ['name', 'username', 'phone', 'password1', 'password2', 'email']

    # def __init__(self, *args, **kwargs):
    #     # 自定义表单错误
    #     super().__init__(*args, **kwargs)
    #     self.fields['username'].error_messages = {'unique': '555', }

    def clean_phone(self):  # 函数必须以clean_开头
        """
        通过正则表达式验证手机号码是否合法
        """
        mobile = self.cleaned_data['phone']
        mobile_regex = r'^1[345789]\d{9}$'
        p = re.compile(mobile_regex)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError('手机号码格式错误', code='invalid mobile')


class EditForm(UserChangeForm):
    name = forms.CharField(max_length=20, required=False)
    phone = forms.CharField(max_length=11)

    class Meta:
        model = User
        fields = ['name', 'username', 'phone', 'password', 'email']
