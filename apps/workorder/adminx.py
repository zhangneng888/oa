# -*- coding:utf-8 -*-
import xadmin
from xadmin.layout import Main,Side,TabHolder,Tab,Fieldset,Row
from models import AssetApplicationProcess
#Register your models here.


class AssetApplicationProcessAdmin(object):
    list_display = ['code','assets_name','department','user','description']
    add_form_template = 'xadmin/workflow/model_form.html'
    change_form_template = 'xadmin/workflow/model_form.html'
xadmin.site.register(AssetApplicationProcess, AssetApplicationProcessAdmin)
