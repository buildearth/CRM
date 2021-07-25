from django.conf.urls import url
from django.contrib import admin

from rbac.views import role

urlpatterns = [
    url(r'^role/list/$', role.role_list),
]