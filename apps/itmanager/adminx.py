# -*- coding:utf-8 -*-
from xadmin.layout import Main,Side,Fieldset,Row
import xadmin

from models import ItManager,ItRecord,DhcpBind,WrokOrdersType,WrokOrders

class ItRecordInline(object):
    model = ItRecord
    extra = 1
    style = 'table'

class ItManagerAdmin(object):
    inlines = [ItRecordInline]
    list_display = ['name','ip','username','dep','is_active']
    search_fields = ['name','ip','remarks','dep__two_department','is_active']
    list_filter = ['name','ip','remarks','is_active']
    reversion_enable = True
    form_layout = (
        Main(
            Fieldset('',
                     Row('name', 'model'),
                     Row('ip', 'system'),
                     Row('username', 'password'),
                     Row('link'),
                     Row('tel', 'application'),
                     Row('dep'),
                     Row('remarks'),
                     ),
        ),
        Side(
            Fieldset(('Status'),
                     'is_active'
                     ),
        )
    )
xadmin.site.register(ItManager,ItManagerAdmin)

class DhcpBindAdmin(object):
    list_display = ['scope', 'ip','mac','name','judge','state']
    search_fields = ['ip', 'mac', 'name']
    list_filter =  ['scope','ip', 'mac', 'name','state']
    reversion_enable = True
    form_layout = (
        Main(
            Fieldset('',
                     Row('scope'),
                     Row('ip', 'mac'),
                     Row('name','describe'),
                     Row('cmd'),
                     ),
        ),
        Side(
            Fieldset(('Status'),
                     'state','judge'
                     ),
        )
    )
xadmin.site.register(DhcpBind, DhcpBindAdmin)

class WrokOrdersTypeAdmin(object):
    list_display = ['pro_type']
xadmin.site.register(WrokOrdersType,WrokOrdersTypeAdmin)

class WrokOrdersAdmin(object):
    list_display = ['org_user', 'pro_type','pro_date','is_finish']
    search_fields = []
    readonly_fields = ['creator']
    list_filter =  ['creator','is_finish','create_time','modified_time']
    exclude = ['org_dept']
    reversion_enable = True
    form_layout = (
        Main(
            Fieldset('',
                     Row('creator','org_user'),
                     Row('pro_type', 'pro_date'),
                     Row('pro_desc'),
                     Row('solver', 'solve_len_time'),
                     Row('solve_desc'),
                     ),
        ),
        Side(
            Fieldset(('Status'),
                     'is_finish','is_key_work',
                     ),
        )
    )
    def save_models(self):
        obj = self.new_obj
        request = self.request
        obj.creator = str(request.user.username)
        obj.save()
xadmin.site.register(WrokOrders, WrokOrdersAdmin)
