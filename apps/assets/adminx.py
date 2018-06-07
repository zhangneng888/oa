# -*- coding:utf-8 -*-
from xadmin.layout import Fieldset, Main, Side, Row
from models import Assets, Partner, Allocate,UserPrice,LowInventory,LowPrice,LowAllocate,VideoAssets,PurchasingAsset
import xadmin
# Register your models here.

class PurchasingAssetAdmin(object):
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
xadmin.site.register(PurchasingAsset, PurchasingAssetAdmin)

class PartnerAdmin(object):
    list_display = ['partner', 'partner_head', 'partner_tel']
    search_fields = ['partner', 'partner_head', 'partner_tel']
    list_filter = ['partner', 'partner_head']
    ordering = ['id']
    reversion_enable = True
xadmin.site.register(Partner, PartnerAdmin)

class AllocateInline(object):
    model = Allocate
    extra = 0
    style = 'table'

class AssetsAdmin(object):
    list_display = ['num', 'name', 'get_accests_state', 'use_department', 'user']
    search_fields = ['num','name', 'status','user__name']
    list_filter = ['num', 'name', 'user', 'use_department', 'status']
    readonly_fields = ['num', 'old_num', 'status', 'residual_value']
    inlines = [AllocateInline]
    reversion_enable = True

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
xadmin.site.register(Assets, AssetsAdmin)

class UserPriceAdmin(object):
    list_display = ['name', 'year', 'month', 'price']
    search_fields = ['year', 'month', 'price']
    list_filter = ['name', 'year', 'month', 'price']
    readonly_fields = ['name', 'year', 'month', 'price']
    reversion_enable = True
xadmin.site.register(UserPrice, UserPriceAdmin)

class LowInventoryAdmin(object):
    list_display = ['name', 'inventory', 'is_recycled', 'recycled', 'lose','broken','total_prices']
    search_fields = ['name', 'inventory', 'is_recycled', 'recycled', 'lose','broken','total_prices']
    list_filter = ['name', 'inventory', 'is_recycled', 'recycled', 'lose','broken','total_prices']
    reversion_enable = True
xadmin.site.register(LowInventory, LowInventoryAdmin)

class LowAllocateAdmin(object):
    list_display = [ 'name', 'status', 'use_department', 'user', 'operator','nums']
    search_fields = ['name__name', 'status', 'user__name', 'operator__name']
    list_filter = ['name', 'status', 'use_department', 'user', 'operator','nums']
    reversion_enable = True
xadmin.site.register(LowAllocate, LowAllocateAdmin)

class LowPriceAdmin(object):
    list_display = ['use_department', 'year', 'month', 'useful_value']
    search_fields = []
    list_filter = ['use_department', 'year', 'month', 'useful_value']
    reversion_enable = True
xadmin.site.register(LowPrice, LowPriceAdmin)

class VideoAssetsAdmin(object):
    list_display = ['id','num', 'name','status','asset_num']
    search_fields = ['name', 'status','asset_classes']
    list_filter = ['name', 'status','asset_classes']
    reversion_enable = True
xadmin.site.register(VideoAssets, VideoAssetsAdmin)
