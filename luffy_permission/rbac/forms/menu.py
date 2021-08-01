from django import forms
from django.utils.safestring import mark_safe

from rbac import models
from rbac.forms.base import BootStrapModelForm


class MenuModelForm(forms.ModelForm):
    class Meta:
        model = models.Menu
        fields = ['title', 'icon']
        widgets = {
            'icon': forms.RadioSelect(
                choices=[
                    ['fa-user-circle', mark_safe('<i class="fa fa-user-circle" aria-hidden="true"></i>')],
                    ['fa-handshake-o', mark_safe('<i class="fa fa-handshake-o" aria-hidden="true"></i>')],
                    ['fa-window-restore', mark_safe('<i class="fa fa-window-restore" aria-hidden="true"></i>')],
                    ['fa-bell', mark_safe('<i class="fa fa-bell" aria-hidden="true"></i>')],
                    ['fa-bed', mark_safe('<i class="fa fa-bed" aria-hidden="true"></i>')]
                ]
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class SecondMenuModelForm(BootStrapModelForm):
    class Meta:
        model = models.Permission
        fields = ["title", "url", "name", "menu"]


class PermissionMenuModelForm(BootStrapModelForm):
    class Meta:
        model = models.Permission
        fields = ["title", "url", "name"]
