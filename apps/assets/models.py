# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from usermanager.models import Department,UserProfile
from xadmin.plugins import generic
# Create your models here.
ASSETS_NAME = (
    ('笔记本', u"笔记本"),
    ('台式机', u"台式机"),
    ('显示器', u"显示器"),
    ('手机', u"手机"),
    ('服务器', u"服务器"),
    ('打印机', u"打印机"),
    ('网络设备', u"网络设备"),
    ('电视机', u"电视机"),
    ('iPad', u"iPad"),
    ('其它', u"其它"),
)

ASSETS_STATUS = (
    ('入库', u"入库"),
    ('领用', u"领用"),
    ('归还', u"归还"),
    ('借出', u"借出"),
    ('报废', u"报废"),
    ('丢失', u"丢失"),
    ('维修', u"维修"),
)
class CostTypes(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=True, null=True, verbose_name="名称")
    description = models.TextField(blank=True, null=True, verbose_name="描述")

    def __str__(self):
        return "%s" %(self.name)

    class Meta:
        verbose_name = "费用类型"
        verbose_name_plural = verbose_name

class PurchasingAsset(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=True, null=True, verbose_name="资产名称")
    configuration = models.CharField(max_length=100, blank=True,null=True, verbose_name="规格参数")
    nums = models.DecimalField(max_digits=10, decimal_places=0, default=0, verbose_name="数量")
    cost_types = models.ForeignKey(CostTypes,blank=True,null=True,related_name='purchasingasset_cost_types', verbose_name='费用类型')
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="单价(元)")
    total_prices = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="总价(元)")
    year = models.CharField(max_length=4, blank=True, null=True, verbose_name="保修年份")
    applicaton_department = models.CharField(max_length=100, blank=True,null=True, verbose_name="申请部门")
    applicants = models.CharField(max_length=100, blank=True,null=True, verbose_name="申请人")
    invoice_num = models.CharField(max_length=50, blank=True, null=True, verbose_name='发票号')
    assets_num = models.CharField(max_length=50, blank=True,null=True,verbose_name="资产编号")
    purchase_date = models.DateField(blank=True, null=True, verbose_name="采购日期")
    apply_date = models.DateField(blank=True, null=True, verbose_name="申请日期")
    is_arrival = models.BooleanField(default=False,verbose_name="是否到货")
    is_account = models.BooleanField(default=False,verbose_name="是否报销")
    is_purchase = models.BooleanField(default=True, verbose_name="待采购")
    description = models.TextField(blank=True, null=True, verbose_name="备注")
    create_time = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name="创建时间")
    modified_time = models.DateTimeField(auto_now=True, blank=True,null=True, verbose_name="修改时间")

    def __str__(self):
        return "%s" %(self.name)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.total_prices = self.unit_price * self.nums
        if self.is_arrival == True:
            self.is_purchase = False
        super(PurchasingAsset, self).save(force_insert, force_update, using, update_fields)

    class Meta:
        verbose_name = "采购记录"
        verbose_name_plural = verbose_name

class Partner(models.Model):
    id = models.AutoField(primary_key=True)
    partner = models.CharField(max_length=50, verbose_name='合作伙伴')
    partner_head = models.CharField(max_length=25, verbose_name='负责人')
    partner_tel = models.CharField(max_length=25, verbose_name='联系电话')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    modified_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    def __str__(self):
        return  "%s" %(self.partner)

    class Meta:
        verbose_name = '合作伙伴'
        verbose_name_plural = verbose_name

class Assets(models.Model):
    id = models.AutoField(primary_key=True)
    num = models.CharField(max_length=25, blank=True, null=True, verbose_name='资产编号')
    old_num = models.CharField(max_length=25, blank=True, null=True, verbose_name='原资产编号')
    name = models.CharField(max_length=25, choices=ASSETS_NAME, verbose_name='资产名称')
    configuration = models.CharField(max_length=100, verbose_name='配置参数')
    sn = models.CharField(max_length=50, blank=True, null=True, verbose_name='SN')
    mac = models.CharField(max_length=50, blank=True, null=True, verbose_name='MAC地址')
    position = models.CharField(max_length=50, default='欧应信息', verbose_name='存放位置')
    purchaser = models.ForeignKey(UserProfile,default=55,related_name='assets_purchaser', verbose_name='采购人')
    purchase_date = models.DateField(verbose_name='采购日期')
    partnet = models.ForeignKey(Partner, verbose_name='供应商')
    depreciable_lives = models.DecimalField(max_digits=10, decimal_places=0, default=2, verbose_name='折旧年限')
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='采购价格(元)')
    residual_value = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='残余价值(元)')
    applicaton_department = models.ForeignKey(Department, related_name='assets_applicaton_department', verbose_name='申请部门')
    applicants = models.ForeignKey(UserProfile, related_name='assets_applicants', verbose_name='申请人')
    status = models.CharField(max_length=25, default= '入库',choices=ASSETS_STATUS, verbose_name='资产状态')
    use_department = models.ForeignKey(Department, related_name='assets_use_department', blank=True, null=True, verbose_name='使用部门')
    user = models.ForeignKey(UserProfile, related_name='assets_user', blank=True, null=True, verbose_name='使用人')
    description = models.TextField(blank=True, null=True, verbose_name='备注')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    modified_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    def __str__(self):
        return "%s" %(self.num)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(Assets, self).save(force_insert, force_update, using, update_fields)
        if not self.num:
            sql = 'INSERT INTO assets_allocate (status,allocate_date,num_id,use_department_id,user_id,description,create_time,modified_time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'
            params = [self.status, self.purchase_date, self.id, 10, self.purchaser_id, self.description,self.create_time, self.create_time]
            generic.update(sql, params)
            self.num = 'OY%06d' % (self.id)
            self.residual_value = '%s' % self.purchase_price
            self.save()

    class Meta:
        verbose_name = 'IT资产表'
        verbose_name_plural = verbose_name

class Allocate(models.Model):
    id = models.AutoField(primary_key=True)
    num = models.ForeignKey(Assets, related_name='allocate_num', verbose_name='资产编号')
    status = models.CharField(max_length=25, choices=ASSETS_STATUS, verbose_name='维护类型')
    allocate_date = models.DateField(verbose_name='维护日期')
    use_department = models.ForeignKey(Department, related_name='allocate_use_department', blank=True, null=True, verbose_name='使用部门')
    user = models.ForeignKey(UserProfile, related_name='allocate_user', blank=True, null=True, verbose_name='使用人')
    description = models.CharField(max_length=300, blank=True, null=True, verbose_name='备注')
    create_time = models.DateTimeField(auto_now_add=True,blank=True, null=True, verbose_name='创建时间')
    modified_time = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name='修改时间')

    def __str__(self):
        return "%s%s" % (self.user, self.status)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(Allocate, self).save(force_insert, force_update, using, update_fields)
        if self.status == '归还':
            sql = 'UPDATE assets_assets SET status = %s, use_department_id = Null, user_id = Null WHERE id=%s'
            params = [self.status, self.num_id]
            generic.update(sql, params)
        elif self.status != '归还':
            sql = 'UPDATE assets_assets SET status = %s, use_department_id = %s, user_id = %s WHERE id=%s'
            params = [self.status, self.use_department_id, self.user_id, self.num_id]
            generic.update(sql, params)

    class Meta:
        verbose_name = '资产记录'
        verbose_name_plural = verbose_name

class UserPrice(models.Model):
    id = models.AutoField(primary_key=True)
    year = models.CharField(max_length=4, blank=True, null=True, verbose_name='年份')
    month = models.CharField(max_length=2, blank=True, null=True, verbose_name='月份')
    name = models.ForeignKey(Department, related_name='userprice_name', blank=True, null=True, verbose_name='部门')
    price = models.DecimalField(max_digits=10,decimal_places=2, default=0, verbose_name='使用价值')
    create_time = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name='创建时间')
    modified_time = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name='修改时间')

    def __str__(self):
        return "%s" %(self.name)

    class Meta:
        verbose_name = 'IT费用分摊'
        verbose_name_plural = verbose_name

class LowInventory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=25, verbose_name='资产名称')
    is_recycled = models.BooleanField(verbose_name='可回收')
    inventory = models.DecimalField(max_digits=10, decimal_places=0,default=0, verbose_name='库存')
    recycled = models.DecimalField(max_digits=10, decimal_places=0, default=0, verbose_name='回收')
    lose = models.DecimalField(max_digits=10, decimal_places=0, default=0, verbose_name='丢失')
    broken = models.DecimalField(max_digits=10, decimal_places=0, default=0, verbose_name='报废')
    total_prices = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='总价')
    description = models.TextField(blank=True, null=True, verbose_name='备注')

    def __str__(self):
        return "%s" % (self.name)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(LowInventory, self).save(force_insert, force_update, using, update_fields)
        sql = 'SELECT name_id from assets_lowinventorytmp WHERE name_id = %s'
        params = [self.id]
        if not generic.selectdate(sql, params):
            sql = 'INSERT INTO assets_lowinventorytmp (name_id, is_recycled, inventory, recycled, lose, broken, total_prices, description)' \
                  ' VALUE (%s,%s,%s,%s,%s,%s,%s,%s);'
            params = [self.id,self.is_recycled,self.inventory,self.recycled,self.lose,self.broken,self.total_prices,self.description]
            generic.update(sql, params)

    class Meta:
        verbose_name = '低值库存'
        verbose_name_plural = verbose_name

class LowInventoryTmp(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.ForeignKey(LowInventory, related_name='lowinventorytmp_name', verbose_name='资产名称')
    is_recycled = models.BooleanField(verbose_name='可回收')
    inventory = models.DecimalField(max_digits=10, decimal_places=0,default=0, verbose_name='库存')
    recycled = models.DecimalField(max_digits=10, decimal_places=0, default=0, verbose_name='回收')
    lose = models.DecimalField(max_digits=10, decimal_places=0, default=0, verbose_name='丢失')
    broken = models.DecimalField(max_digits=10, decimal_places=0, default=0, verbose_name='报废')
    total_prices = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='总价')
    description = models.TextField(blank=True, null=True, verbose_name='备注')

    def __str__(self):
        return "%s" % (self.name)

    class Meta:
        verbose_name = '低值库存Tmp'
        verbose_name_plural = verbose_name

class LowPrice(models.Model):
    id = models.AutoField(primary_key=True)
    use_department = models.ForeignKey(Department, related_name='lowprice_use_department', blank=True, null=True,verbose_name='部门')
    year = models.CharField(max_length=4, blank=True, null=True, verbose_name='年份')
    month = models.CharField(max_length=2, blank=True, null=True, verbose_name='月份')
    useful_value = models.DecimalField(max_digits=10,decimal_places=2, default=0, verbose_name='使用价值')

    def __str__(self):
        return "%s" %(self.use_department)

    class Meta:
        verbose_name = '低值费用'
        verbose_name_plural = verbose_name

class LowPriceTmp(models.Model):
    id = models.AutoField(primary_key=True)
    use_department = models.ForeignKey(Department, related_name='lowpricetmp_use_department', blank=True, null=True,verbose_name='部门')
    year = models.CharField(max_length=4, blank=True, null=True, verbose_name='年份')
    month = models.CharField(max_length=2, blank=True, null=True, verbose_name='月份')
    useful_value = models.DecimalField(max_digits=10,decimal_places=2, default=0, verbose_name='使用价值')

    class Meta:
        verbose_name = '低值费用Tmp'
        verbose_name_plural = verbose_name

class LowAllocate(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.ForeignKey(LowInventory, related_name='lowallocate_name', verbose_name='资产名称')
    status = models.CharField(max_length=25, default='入库', choices=ASSETS_STATUS, verbose_name='维护类型')
    use_department = models.ForeignKey(Department, related_name='lowallocate_use_department', blank=True, null=True, verbose_name='部门')
    user = models.ForeignKey(UserProfile, related_name='lowallocate_user', blank=True, null=True, verbose_name='姓名')
    operator = models.ForeignKey(UserProfile, related_name='low_allocate_operator', blank=True, null=True, verbose_name='经办人')
    is_recycled = models.BooleanField(verbose_name='领用库存',default=False)
    nums = models.DecimalField(max_digits=10, decimal_places=0, default=0, verbose_name='数量')
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True, verbose_name='单价(元)')
    partnet = models.ForeignKey(Partner, blank=True, null=True, verbose_name='供应商')
    create_time = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name='创建时间')
    modified_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    def __str__(self):
        return "%s" %(self.name)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(LowAllocate, self).save(force_insert, force_update, using, update_fields)
        if self.status == '入库':
            #库存 = 临时表库存 + 调拨数量
            sql11 = 'UPDATE assets_lowinventory SET ' \
                    'inventory = (SELECT inventory FROM assets_lowinventorytmp WHERE name_id = %s) + %s, ' \
                    'total_prices = ((SELECT total_prices FROM assets_lowinventorytmp WHERE name_id = %s) + %s * %s) ' \
                    'WHERE id = %s'
            params11 = [self.name_id, self.nums, self.name_id, self.unit_price, self.nums, self.name_id ]
            generic.update(sql11, params11)
            # 更新临时表库存、回收、丢失、报废、总价
            sql12 = 'UPDATE assets_lowinventorytmp SET ' \
                  'inventory = (SELECT inventory FROM assets_lowinventory WHERE id = %s), ' \
                  'recycled = (SELECT recycled FROM assets_lowinventory WHERE id = %s), ' \
                  'lose = (SELECT lose FROM assets_lowinventory WHERE id = %s), ' \
                  'broken = (SELECT broken FROM assets_lowinventory WHERE id = %s), ' \
                  'total_prices = (SELECT total_prices FROM assets_lowinventory WHERE id = %s) ' \
                  'WHERE name_id = %s'
            params12 = [self.name_id, self.name_id, self.name_id, self.name_id, self.name_id, self.name_id]
            generic.update(sql12, params12)
        elif self.status == '领用':
            if self.is_recycled == False:
                #条件 回收 = 0
                #库存 = 临时表库存 - 调拨数量
                #总价 = 临时表总价 - （临时表总价/临时表库存）* 调拨数量
                sql21 = 'UPDATE assets_lowinventory SET ' \
                        'inventory = ((SELECT inventory FROM assets_lowinventorytmp WHERE name_id = %s) - %s), ' \
                        'total_prices = ((SELECT total_prices FROM assets_lowinventorytmp WHERE name_id = %s) - ' \
                        '(SELECT total_prices FROM assets_lowinventorytmp WHERE name_id = %s) /' \
                        '(SELECT inventory FROM assets_lowinventorytmp WHERE name_id = %s) * %s) ' \
                        'WHERE id=%s AND recycled = 0'
                params21 = [self.name_id, self.nums, self.name_id, self.name_id, self.name_id, self.nums, self.name_id]
                generic.update(sql21, params21)
                # 条件 回收 > 0
                # 回收 = 临时表回收 - 调拨数量
                sql22 = 'UPDATE assets_lowinventory SET ' \
                        'recycled = ((SELECT recycled FROM assets_lowinventorytmp WHERE name_id = %s) - %s) ' \
                        'WHERE id=%s AND recycled > 0'
                params22 = [self.name_id, self.nums, self.name_id]
                generic.update(sql22, params22)
            elif self.is_recycled == True:
                sql23 = 'UPDATE assets_lowinventory SET ' \
                        'inventory = ((SELECT inventory FROM assets_lowinventorytmp WHERE name_id = %s) - %s), ' \
                        'total_prices = ((SELECT total_prices FROM assets_lowinventorytmp WHERE name_id = %s) - ' \
                        '(SELECT total_prices FROM assets_lowinventorytmp WHERE name_id = %s) /' \
                        '(SELECT inventory FROM assets_lowinventorytmp WHERE name_id = %s) * %s) ' \
                        'WHERE id=%s'
                params23 = [self.name_id, self.nums, self.name_id, self.name_id, self.name_id, self.nums, self.name_id]
                generic.update(sql23, params23)
            # 使用价值 = 原使用价值 + （临时表总价/临时表库存 * 调拨数量)
            import datetime
            year = datetime.datetime.now().year
            month = datetime.datetime.now().month
            sql25 = 'SELECT use_department_id from assets_lowprice WHERE use_department_id = %s AND year =%s AND month = %s '
            params25 = [self.use_department_id, year, month]
            if not generic.selectdate(sql25, params25):
                sql26 = 'INSERT INTO assets_lowprice (use_department_id, year,month,useful_value) VALUE (%s,%s,%s,%s);'
                params26 = [self.use_department_id, year, month, 0]
                generic.update(sql26, params26)
                sql27 = 'INSERT INTO assets_lowpricetmp (use_department_id, year,month,useful_value) VALUE (%s,%s,%s,%s);'
                params27 = [self.use_department_id, year, month, 0]
                generic.update(sql27, params27)
            sql28 = 'UPDATE assets_lowprice SET ' \
                    'useful_value = ((SELECT useful_value FROM assets_lowpricetmp WHERE use_department_id = %s) + ' \
                    '(SELECT total_prices FROM assets_lowinventorytmp WHERE name_id = %s) /' \
                    '(SELECT inventory FROM assets_lowinventorytmp WHERE name_id = %s) * %s) ' \
                    'WHERE use_department_id = %s AND year =%s AND month = %s'
            params28 = [self.use_department_id, self.name_id, self.name_id, self.nums, self.use_department_id, year,
                        month]
            generic.update(sql28, params28)
            sql29 = 'UPDATE assets_lowpricetmp SET ' \
                    'useful_value = (SELECT useful_value FROM assets_lowprice WHERE use_department_id = %s)' \
                    'WHERE use_department_id = %s AND year =%s AND month = %s'
            params29 = [self.use_department_id, self.use_department_id, year, month]
            generic.update(sql29, params29)
            # 更新临时表库存、回收、丢失、报废、总价
            sql24 = 'UPDATE assets_lowinventorytmp SET ' \
                  'inventory = (SELECT inventory FROM assets_lowinventory WHERE id = %s), ' \
                  'recycled = (SELECT recycled FROM assets_lowinventory WHERE id = %s), ' \
                  'lose = (SELECT lose FROM assets_lowinventory WHERE id = %s), ' \
                  'broken = (SELECT broken FROM assets_lowinventory WHERE id = %s), ' \
                  'total_prices = (SELECT total_prices FROM assets_lowinventory WHERE id = %s) ' \
                  'WHERE name_id = %s'
            params24 = [self.name_id, self.name_id, self.name_id, self.name_id, self.name_id, self.name_id]
            generic.update(sql24, params24)
        elif self.status == '归还':
            #库存归还 = 临时表归还 + 调拨数量
            sql31 = 'UPDATE assets_lowinventory SET ' \
                    'recycled = ((SELECT recycled FROM assets_lowinventorytmp WHERE name_id = %s) + %s) ' \
                    'WHERE id = %s'
            params31 = [self.name_id, self.nums, self.name_id]
            generic.update(sql31, params31)
            # 更新临时表库存、回收、丢失、报废、总价
            sql32 = 'UPDATE assets_lowinventorytmp SET ' \
                    'inventory = (SELECT inventory FROM assets_lowinventory WHERE id = %s), ' \
                    'recycled = (SELECT recycled FROM assets_lowinventory WHERE id = %s), ' \
                    'lose = (SELECT lose FROM assets_lowinventory WHERE id = %s), ' \
                    'broken = (SELECT broken FROM assets_lowinventory WHERE id = %s), ' \
                    'total_prices = (SELECT total_prices FROM assets_lowinventory WHERE id = %s) ' \
                    'WHERE name_id = %s'
            params32 = [self.name_id, self.name_id, self.name_id, self.name_id, self.name_id, self.name_id]
            generic.update(sql32, params32)

        elif self.status == '报废':
            #库存报废 = 临时表报废 + 调拨数量
            sql41 = 'UPDATE assets_lowinventory SET ' \
                    'broken = ((SELECT broken FROM assets_lowinventorytmp WHERE name_id = %s) + %s) ' \
                    'WHERE id = %s'
            params41 = [self.name_id, self.nums, self.name_id]
            generic.update(sql41, params41)
            # 更新临时表库存、回收、丢失、报废、总价
            sql42 = 'UPDATE assets_lowinventorytmp SET ' \
                    'inventory = (SELECT inventory FROM assets_lowinventory WHERE id = %s), ' \
                    'recycled = (SELECT recycled FROM assets_lowinventory WHERE id = %s), ' \
                    'lose = (SELECT lose FROM assets_lowinventory WHERE id = %s), ' \
                    'broken = (SELECT broken FROM assets_lowinventory WHERE id = %s), ' \
                    'total_prices = (SELECT total_prices FROM assets_lowinventory WHERE id = %s) ' \
                    'WHERE name_id = %s'
            params42 = [self.name_id, self.name_id, self.name_id, self.name_id, self.name_id, self.name_id]
            generic.update(sql42, params42)
        elif self.status == '丢失':
            #库存丢失=临时表丢失 + 调拨数量
            sql51 = 'UPDATE assets_lowinventory SET ' \
                    'lose = ((SELECT lose FROM assets_lowinventorytmp WHERE name_id = %s) + %s) ' \
                    'WHERE id = %s'
            params51 = [self.name_id, self.nums, self.name_id]
            generic.update(sql51, params51)
            #更新临时表库存、回收、丢失、报废、总价
            sql52 = 'UPDATE assets_lowinventorytmp SET ' \
                    'inventory = (SELECT inventory FROM assets_lowinventory WHERE id = %s), ' \
                    'recycled = (SELECT recycled FROM assets_lowinventory WHERE id = %s), ' \
                    'lose = (SELECT lose FROM assets_lowinventory WHERE id = %s), ' \
                    'broken = (SELECT broken FROM assets_lowinventory WHERE id = %s), ' \
                    'total_prices = (SELECT total_prices FROM assets_lowinventory WHERE id = %s) ' \
                    'WHERE name_id = %s'
            params52 = [self.name_id, self.name_id, self.name_id, self.name_id, self.name_id, self.name_id]
            generic.update(sql52, params52)


    class Meta:
        verbose_name = '低值调拨'
        verbose_name_plural = verbose_name

class VideoAssets(models.Model):
    VIDEO_NAME = (
        ('固定资产', u"固定资产"),
        ('耗材', u"耗材"),
    )
    id = models.AutoField(primary_key=True)
    num = models.CharField(max_length=25, blank=True, null=True, verbose_name="资产编号")
    asset_classes = models.CharField(max_length=25, choices=VIDEO_NAME, verbose_name='资产分类')
    name = models.CharField(max_length=50, blank=True, null=True, verbose_name="资产名称")
    configuration = models.CharField(max_length=100, blank=True, null=True, verbose_name='规格参数')
    sn = models.CharField(max_length=50, blank=True, null=True, verbose_name='SN序列号')
    description = models.TextField(blank=True, null=True, verbose_name='备注')
    purchaser = models.CharField(max_length=20, blank=True, null=True, verbose_name='采购人')
    purchase_date = models.DateField(blank=True, null=True, verbose_name='采购日期')
    partnet = models.CharField(max_length=50, blank=True, null=True, verbose_name='供应商')
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='采购价格(元)')
    applicaton_department = models.CharField(max_length=20, default="视频部", verbose_name='申请部门')
    applicants = models.CharField(max_length=20, blank=True, null=True, verbose_name="申请人")
    status = models.CharField(max_length=25, default='入库', choices=ASSETS_STATUS, verbose_name='资产状态')
    use_department = models.CharField(max_length=20, default="视频部", verbose_name='使用部门')
    user = models.CharField(max_length=20, blank=True, null=True, verbose_name="使用人")
    asset_num = models.DecimalField(max_digits=10, decimal_places=0, default=1, verbose_name="资产数量")
    create_time = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name='创建时间')
    modified_time = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name='修改时间')

    def __str__(self):
        return "%s" % (self.name)

    class Meta:
        verbose_name = "视频资产"
        verbose_name_plural = verbose_name
