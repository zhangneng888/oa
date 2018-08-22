# -*- coding:utf-8 -*-
from models import YcDepartment, YcUserProfile,YcPurchasingAsset,YcPartner,YcAssets,YcAllocate
from xadmin.layout import Fieldset, Main, Side, Row
import xadmin
from django.contrib import admin
# Register your models here.

class YcDepartmentAdmin(object):
    list_display = ['department']
    reversion_enable = True
xadmin.site.register(YcDepartment, YcDepartmentAdmin)

class YcUserProfileAdmin(object):
    list_display = ['department','name','status','entry_date']
    list_filter = ['status']
    search_fields = ['name', 'email']
    reversion_enable = True
xadmin.site.register(YcUserProfile, YcUserProfileAdmin)

class YcPartnerAdmin(object):
    list_display = ['partner', 'partner_head', 'partner_tel']
    search_fields = ['partner', 'partner_head', 'partner_tel']
    list_filter = ['partner', 'partner_head']
    ordering = ['id']
    reversion_enable = True
xadmin.site.register(YcPartner, YcPartnerAdmin)

class YcPurchasingAssetAdmin(object):
    list_display = ["name", "configuration", "nums", "unit_price", "total_prices", "year", "applicaton_department",
                    "applicants", "purchase_date"]
    search_fields = ['name']
    list_filter = ['name','is_arrival', 'is_account', 'is_purchase']
    readonly_fields = ['total_prices']
    reversion_enable = True
    form_layout = (
        Main(
            Fieldset("基本信息",
                     Row("applicaton_department", "applicants"),
                     Row("name", "apply_date"),
                     Row("configuration","nums"),
                     Row("description"),
                     ),
            Fieldset("扩展信息",
                     Row("year","total_prices"),
                     Row("invoice_num", "assets_num", ),
                     Row("purchase_date", "unit_price"),
                     ),
            Fieldset("",)
        ),
        Side(
            Fieldset(('Status'),
                     'is_arrival', 'is_account', 'is_purchase'
                     ),
        )
    )
    actions = ['set_is_account']

    def set_is_account(modeladmin, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        YcPurchasingAsset.objects.filter(id__in=selected).update(is_account=True)

    set_is_account.short_description = "设置所选内容为已报销"
xadmin.site.register(YcPurchasingAsset, YcPurchasingAssetAdmin)

class YcAllocateInline(object):
    model = YcAllocate
    extra = 1
    style = 'table'

class YcAssetsAdmin(object):
    list_display = ['num', 'assets_classes','name', 'get_accests_state', 'use_department', 'user']
    search_fields = ['num','name', 'status','user__name']
    list_filter = ['num', 'name', 'user', 'use_department', 'status']
    readonly_fields = ['num', 'status']
    inlines = [YcAllocateInline]
    reversion_enable = True

    form_layout = (
        Main(
            Fieldset("基本信息",
                     Row("num", "status"),
                     Row("assets_classes","name"),
                     Row("configuration", "sn"),
                     Row("purchaser", "purchase_date"),
                     Row("applicaton_department", "applicants"),
                     Row("use_department", "user"),
                     Row("purchase_price","purchase_date"),
                     Row("partnet","position"),
                     Row("description"),
                     ),
        ),
    )
    actions = ['set_is_account']

    def get_accests_state(self, obj):
        if obj.status == '入库':
            return u'<span style="color:green;font-weight:bold">%s</span>' % (u"入库",)
        elif obj.status == '领用':
            return u'<span style="color:green;font-weight:bold">%s</span>' % (u"领用",)
        elif obj.status == '归还':
            return u'<span style="color:green;font-weight:bold">%s</span>' % (u"归还",)
        elif obj.status == '借出':
            return u'<span style="color:violet;font-weight:bold">%s</span>' % (u"借出",)
        elif obj.status == '报废':
            return u'<span style="color:red;font-weight:bold">%s</span>' % (u"报废",)
        elif obj.status == '丢失':
            return u'<span style="color:orange;font-weight:bold">%s</span>' % (u"丢失",)
    get_accests_state.short_description = u'资产状态'
    get_accests_state.allow_tags = True
xadmin.site.register(YcAssets, YcAssetsAdmin)