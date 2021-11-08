from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from web.forms import RegisterForm
from web import models
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def loginView(request):
    # 登陆功能
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if not user:
            msg = {'code': 1004, 'message': '用户不存在或密码错误'}
            return render(request, 'login.html', locals())
        login(request, user)
        return redirect('web:index')
    return render(request, 'login.html', locals())


def quitView(request):
    # 退出功能
    logout(request)
    return redirect('web:index')



