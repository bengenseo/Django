from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm

from web import models
from web.forms import EditForm


@login_required(login_url='web:login')
def userCenter(request):
    info = {'user': request.user}
    return render(request, 'userinfo.html', locals())


@login_required(login_url='web:login')
def editProfile(request):
    # 编辑功能
    if request.method == 'POST':
        forms = EditForm(request.POST, instance=request.user)
        if forms.is_valid():
            forms.save()
            request.user.userinfo.phone = forms.cleaned_data['phone']
            request.user.userinfo.name = forms.cleaned_data['name']
            request.user.userinfo.save()
            return redirect('web:user')
        return render(request, 'editprofile.html', locals())
    forms = EditForm(instance=request.user)
    return render(request, 'editprofile.html', locals())


@login_required(login_url='web:login')
def changePassword(request):
    # 编辑功能
    if request.method == 'POST':
        forms = PasswordChangeForm(data=request.POST, user=request.user)
        if forms.is_valid():
            forms.save()
            return redirect('web:login')
        return render(request, 'changepwd.html', locals())
    forms = PasswordChangeForm(user=request.user)
    return render(request, 'changepwd.html', locals())
