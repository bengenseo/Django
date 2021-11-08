from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from web.forms import RegisterForm
from web import models


def registerView(request):
    # 注册功能
    if request.method == 'POST':
        forms = RegisterForm(request.POST)
        if forms.is_valid():
            forms.save()
            user = authenticate(username=forms.cleaned_data['username'], password=forms.cleaned_data['password1'])
            user.email = forms.cleaned_data['email']
            models.User(user=user, name=forms.cleaned_data['name'], phone=forms.cleaned_data['phone']).save()
            login(request, user)
            return redirect('web:index')
        return render(request, 'register.html', locals())
    forms = RegisterForm()
    return render(request, 'register.html', locals())
