from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse

from rbac import models
from rbac.forms.role import RoleModelForm


def role_list(request):
    """
    角色列表
    :param request:
    :return:
    """
    role_queryset = models.Role.objects.all()
    return render(request, 'rbac/role_list.html', {'roles': role_queryset})


def role_add(request):
    """
    增加角色
    :param request:
    :return:
    """
    if request.method == 'GET':
        form = RoleModelForm()
        return render(request, 'rbac/change.html', {'form': form})

    form = RoleModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('rbac:role_list'))

    # 验证失败的返回
    return render(request, 'rbac/change.html', {'form': form})


def role_edit(request, pk):
    """
    修改角色
    :param request:
    :return:
    """
    obj = models.Role.objects.filter(id=pk).first()
    if not obj:
        return HttpResponse('角色不存在')

    if request.method == 'GET':
        form = RoleModelForm(instance=obj)
        return render(request, 'rbac/change.html', {'form': form})

    form = RoleModelForm(instance=obj, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('rbac:role_list'))
    return render(request, 'rbac/change.html', {'form': form})


def role_del(request, pk):
    """
    角色删除
    :param request:
    :param pk:要被删除的角色id
    :return:
    """
    origin_url = reverse('rbac:role_list')
    if request.method == "GET":
        return render(request, 'rbac/delete.html', {'cancel_url': origin_url})

    models.Role.objects.filter(id=pk).delete()
    return redirect(origin_url)