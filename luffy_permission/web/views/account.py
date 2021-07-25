from django.shortcuts import render, redirect, HttpResponse
# 最好不要从其他app中导入模型类，这是不规范的写法
from rbac import models

from rbac.service.init_permission import init_permission


def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    name = request.POST.get('username')
    pwd = request.POST.get('pwd')

    current_user = models.UserInfo.objects.filter(name=name, password=pwd).first()
    if not current_user:
        return render(request, 'login.html', {'msg': '用户名或者密码错误'})

    init_permission(current_user, request)

    return redirect('/customer/list/')
