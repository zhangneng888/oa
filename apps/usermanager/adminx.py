# -*- coding:utf-8 -*-
from models import Department, UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import (UserCreationForm, UserChangeForm)
from django.utils.translation import ugettext as _
from django.forms import ModelMultipleChoiceField
from xadmin.layout import Fieldset, Main, Side, Row
from xadmin import views
import xadmin
# Register your models here.
@xadmin.sites.register(views.BaseAdminView)
class BaseSetting(object):
    enable_themes = False
    use_bootswatch = True

@xadmin.sites.register(views.CommAdminView)
class GlobalSetting(object):
    global_search_models = []
    global_models_icon = {}
    #menu_style = 'accordion'  #收起菜单 'accordion'
    site_title = '唯医网-运维管理系统'
    site_footer = '唯医网-运维管理系统'

class DepartmentAdmin(object):
    list_display = ['first_department', 'two_department', 'first_leader', 'two_leader']
    search_fields = ['first_department', 'two_department', 'first_leader', 'two_leader']
    list_filter = ['first_department', 'two_department', 'first_leader', 'two_leader']
    reversion_enable = True
xadmin.site.register(Department, DepartmentAdmin)

ACTION_NAME = {
    'add': _('Can add %s'),
    'change': _('Can change %s'),
    'edit': _('Can edit %s'),
    'delete': _('Can delete %s'),
    'view': _('Can view %s'),
}

def get_permission_name(p):
    action = p.codename.split('_')[0]
    if action in ACTION_NAME:
        return ACTION_NAME[action] % str(p.content_type)
    else:
        return p.name

class PermissionModelMultipleChoiceField(ModelMultipleChoiceField):

    def label_from_instance(self, p):
        return get_permission_name(p)

class ProfileInline(object):
    model = UserProfile
    form_layout = (
        Row('department', 'name'),
        Row('tel', 'email'),
        Row('status', 'entry_date'),
    )
    max_num = 1
    can_delete = False

class UserAdmin(object):
    change_user_password_template = None
    list_display = ['username', 'first_name', 'email',  'is_staff', 'is_active', 'is_superuser']
    list_filter = ['is_staff', 'is_superuser', 'is_active']
    search_fields = ['username', 'first_name', 'last_name', 'email']
    exclude = ['first_name', 'email', 'last_name', 'last_login', 'date_joined',]
    ordering = ['-is_staff', 'username']
    style_fields = {'groups': 'm2m_transfer', 'user_permissions': 'm2m_transfer'}
    model_icon = 'fa fa-user'
    relfield_style = 'fk-ajax'
    inlines = [ProfileInline]

    def get_field_attrs(self, db_field, **kwargs):
        attrs = super(UserAdmin, self).get_field_attrs(db_field, **kwargs)
        if db_field.name == 'user_permissions':
            attrs['form_class'] = PermissionModelMultipleChoiceField
        return attrs

    def get_model_form(self, **kwargs):
        if self.org_obj is None:
            self.form = UserCreationForm
        else:
            self.form = UserChangeForm
        return super(UserAdmin, self).get_model_form(**kwargs)

    def get_form_layout(self):
        if self.org_obj:
            self.form_layout = (
                Main(
                    Fieldset('',
                             'username', 'password',
                             css_class='unsort no_title'
                             ),
                    Fieldset(_('Permissions'),
                             'groups', 'user_permissions'
                             ),
                ),
                Side(
                    Fieldset(_('Status'),
                             'is_active', 'is_staff', 'is_superuser',
                             ),
                )
            )
        return super(UserAdmin, self).get_form_layout()


xadmin.site.unregister(User)
xadmin.site.register(User, UserAdmin)
