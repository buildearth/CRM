from collections import OrderedDict

from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse

from rbac import models
from rbac.forms.menu import MenuModelForm, SecondMenuModelForm, PermissionMenuModelForm

from rbac.service.urls import memory_reverse
from rbac.service.routes import get_all_url_dict


def menu_list(request):
    """
    菜单和权限列表
    :param request:
    :return:
    """
    menus = models.Menu.objects.all()
    menu_id = request.GET.get('mid')
    second_menu_id = request.GET.get('sid')

    # 检查menu_id的正确性
    if not models.Menu.objects.filter(pk=menu_id).exists():
        menu_id = None
    # 检查second_menu_id在Permission表中是否存在
    if not models.Permission.objects.filter(pk=second_menu_id).exists():
        second_menu_id = None

    second_menus = []
    permissions = []
    if menu_id:
        # 获取一级菜但下的二级菜单
        second_menus = models.Permission.objects.filter(menu=menu_id)
    if second_menu_id:
        # 获取二级菜单下的所有权限
        permissions = models.Permission.objects.filter(pid_id=second_menu_id)

    return render(
        request,
        'rbac/menu_list.html',
        {
            'menus': menus,
            'mid': menu_id,
            'second_menus': second_menus,
            'sid': second_menu_id,
            'permissions': permissions,
        }
    )


def menu_add(request):
    """
    新增一级菜单
    :param request:
    :return:
    """
    if request.method == 'GET':
        form = MenuModelForm()
        return render(request, 'rbac/change.html', {'form': form})

    form = MenuModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(memory_reverse(request, 'rbac:menu_list'))

    # 验证失败的返回
    return render(request, 'rbac/change.html', {'form': form})


def menu_edit(request, pk):
    """
    修改一级菜单
    :param request:
    :return:
    """
    obj = models.Menu.objects.filter(id=pk).first()
    if not obj:
        return HttpResponse('角色不存在')

    if request.method == 'GET':
        form = MenuModelForm(instance=obj)
        return render(request, 'rbac/change.html', {'form': form})

    form = MenuModelForm(instance=obj, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(memory_reverse(request, 'rbac:menu_list'))
    return render(request, 'rbac/change.html', {'form': form})


def menu_del(request, pk):
    """
    一级菜单删除
    :param request:
    :param pk:要被删除的菜单id
    :return:
    """
    basic_url = memory_reverse(request, 'rbac:menu_list')

    if request.method == "GET":
        return render(request, 'rbac/delete.html', {'cancel_url': basic_url})

    models.Menu.objects.filter(id=pk).delete()
    return redirect(basic_url)


def second_menu_add(request, menu_id):
    """
    增加二级菜单
    :param request:
    :param menu_id: 已选择的一级菜单id,用于设置默认值
    :return:
    """
    menu_obj = models.Menu.objects.filter(pk=menu_id).first()
    if request.method == 'GET':
        # 给设置默认值
        form = SecondMenuModelForm(initial={'menu': menu_obj})
        return render(request, 'rbac/change.html', {'form': form})

    form = SecondMenuModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(memory_reverse(request, 'rbac:menu_list'))

    # 验证失败的返回
    return render(request, 'rbac/change.html', {'form': form})


def second_menu_edit(request, pk):
    """
    修改二级菜单
    :param request:
    :return:
    """
    obj = models.Permission.objects.filter(id=pk).first()
    if not obj:
        return HttpResponse('菜单不存在')

    if request.method == 'GET':
        form = SecondMenuModelForm(instance=obj)
        return render(request, 'rbac/change.html', {'form': form})

    form = SecondMenuModelForm(instance=obj, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(memory_reverse(request, 'rbac:menu_list'))
    return render(request, 'rbac/change.html', {'form': form})


def second_menu_del(request, pk):
    """
    二级菜单删除
    :param request:
    :param pk:要被删除的菜单id
    :return:
    """
    basic_url = memory_reverse(request, 'rbac:menu_list')

    if request.method == "GET":
        return render(request, 'rbac/delete.html', {'cancel_url': basic_url})

    models.Permission.objects.filter(id=pk).delete()
    return redirect(basic_url)


def permission_add(request, second_menu_id):
    """
    二级菜单下的权限增加
    :param request:
    :param second_menu_id:
    :return:
    """
    second_menu_obj = models.Permission.objects.filter(pk=second_menu_id).first()
    # 判断二级菜单是否存在
    if not second_menu_obj:
        return HttpResponse('二级菜单不存在')

    if request.method == "GET":
        form = PermissionMenuModelForm()
        return render(request, 'rbac/change.html', {'form': form})

    form = PermissionMenuModelForm(request.POST)
    if form.is_valid():
        # 将二级菜单传入到用户传入的对象中

        '''
            form.instance中包含用户提交的所有值,其机制是：
            1. instance = models.Permission(title='xx', name='xx', url='xx')
            2. instance.pid = second_menu_obj  给用户传入的数据添加值
            3. instance.save() 保存数据
        '''
        form.instance.pid = second_menu_obj
        form.save()
        return redirect(memory_reverse(request, 'rbac:menu_list'))

    # 验证失败的返回
    return render(request, 'rbac/change.html', {'form': form})


def permission_edit(request, pk):
    """
    二级菜单下的权限编辑
    :param request:
    :param second_menu_id:
    :return:
    """
    permission_obj = models.Permission.objects.filter(pk=pk).first()
    # 判断二级菜单是否存在
    if not permission_obj:
        return HttpResponse('二级菜单不存在')

    if request.method == "GET":
        form = PermissionMenuModelForm(instance=permission_obj)
        return render(request, 'rbac/change.html', {'form': form})

    form = SecondMenuModelForm(instance=permission_obj, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(memory_reverse(request, 'rbac:menu_list'))

    # 验证失败的返回
    return render(request, 'rbac/change.html', {'form': form})


def permission_del(request, pk):
    """
    二级菜单下权限删除
    :param request:
    :param pk:
    :return:
    """
    basic_url = memory_reverse(request, 'rbac:menu_list')

    if request.method == "GET":
        return render(request, 'rbac/delete.html', {'cancel_url': basic_url})

    models.Permission.objects.filter(id=pk).delete()
    return redirect(basic_url)


def multi_permissions(request):
    """
    批量操作权限
    :param request:
    :return:
    """
    # 获取项目中所有的url
    url_ordered_dict = get_all_url_dict()
    router_name_set = set(url_ordered_dict.keys())
    # 获取数据库中所有的url
    permissions = models.Permission.objects.all().values('id', 'title', 'name', 'url', 'menu_id', 'pid_id')
    permissions_dict = OrderedDict()
    for row in permissions:
        permissions_dict[row.name] = row
    permission_name_set = set(permissions_dict.keys())

    # 应该添加、删除、修改的权限有哪些？
    # 添加
    generate_name_list = router_name_set - permission_name_set
    # 删除
    delete_name_list = permission_name_set - router_name_set
    # 更新
    update_name_list = permission_name_set & router_name_set
    # 差集 判断那些需要删除，增加




    return HttpResponse('xx')