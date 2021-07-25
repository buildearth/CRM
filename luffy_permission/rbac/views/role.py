from django.shortcuts import render

from rbac.models import Role


def role_list(request):
    """
    角色列表
    :param request:
    :return:
    """
    role_queryset = Role.objects.all()
    return render(request, 'rbac/role_list.html', {'roles': role_queryset})
