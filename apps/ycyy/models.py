# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from xadmin.plugins import generic
# Create your models here.
ASSETS_TYPE = (
    ('IT资产', u"IT资产"),
    ('办公资产', u"办公资产"),
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

class YcDepartment(models.Model):
    id = models.AutoField(primary_key=True)
    department = models.CharField(max_length=25, verbose_name="部门")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    modified_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")

    def __str__(self):
        return "%s" %(self.department)

    class Meta:
        verbose_name = "银川部门管理"
        verbose_name_plural = verbose_name


class YcUserProfile(models.Model):
    STATUS = (
        ('在职', u"在职"),
        ('离职', u"离职"),
    )
    department = models.ForeignKey(YcDepartment, blank=True, null=True, related_name="ycuserprofile_department", verbose_name='部门')
    name = models.CharField(max_length=25, blank=True, null=True, verbose_name='姓名')
    email = models.CharField(max_length=30, blank=True, null=True, verbose_name='邮件')
    tel = models.CharField(max_length=25, blank=True, null=True, verbose_name='电话')
    status = models.CharField(max_length=25, blank=True, null=True, choices=STATUS, verbose_name='状态')
    entry_date = models.DateField(blank=True, null=True, verbose_name='入职日期')

    def __str__(self):
        return "%s" %(self.name)

    class Meta:
        verbose_name = '银川员工信息'
        verbose_name_plural = verbose_name


class YcPurchasingAsset(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=True, null=True, verbose_name="资产名称")
    configuration = models.CharField(max_length=100, blank=True,null=True, verbose_name="配置参数")
    nums = models.DecimalField(max_digits=10, decimal_places=0, default=0, verbose_name="数量")
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
        super(YcPurchasingAsset, self).save(force_insert, force_update, using, update_fields)

    class Meta:
        verbose_name = "银川采购记录"
        verbose_name_plural = verbose_name


class YcPartner(models.Model):
    id = models.AutoField(primary_key=True)
    partner = models.CharField(max_length=50, verbose_name='合作伙伴')
    partner_head = models.CharField(max_length=25, verbose_name='负责人')
    partner_tel = models.CharField(max_length=25, verbose_name='联系电话')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    modified_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    def __str__(self):
        return  "%s" %(self.partner)

    class Meta:
        verbose_name = '银川合作伙伴'
        verbose_name_plural = verbose_name


class YcAssets(models.Model):
    id = models.AutoField(primary_key=True)
    num = models.CharField(max_length=25, blank=True, null=True, verbose_name='资产编号')
    assets_classes = models.CharField(max_length=25,default= '办公电脑', choices=ASSETS_TYPE, verbose_name='资产分类')
    name = models.CharField(max_length=100, verbose_name='资产名称')
    configuration = models.CharField(max_length=100, verbose_name='配置参数')
    sn = models.CharField(max_length=50, blank=True, null=True, verbose_name='SN')
    position = models.CharField(max_length=50, default='银川医院', verbose_name='存放位置')
    purchaser = models.ForeignKey(YcUserProfile,default=55,related_name='ycassets_purchaser', verbose_name='采购人')
    purchase_date = models.DateField(verbose_name='采购日期')
    partnet = models.ForeignKey(YcPartner, verbose_name='供应商')
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='采购价格(元)')
    applicaton_department = models.ForeignKey(YcDepartment, related_name='ycassets_applicaton_department', verbose_name='申请部门')
    applicants = models.ForeignKey(YcUserProfile, related_name='ycassets_applicants', verbose_name='申请人')
    status = models.CharField(max_length=25, default= '入库',choices=ASSETS_STATUS, verbose_name='资产状态')
    use_department = models.ForeignKey(YcDepartment, related_name='ycassets_use_department', blank=True, null=True, verbose_name='使用部门')
    user = models.ForeignKey(YcUserProfile, related_name='ycassets_user', blank=True, null=True, verbose_name='使用人')
    description = models.TextField(blank=True, null=True, verbose_name='备注')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    modified_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    def __str__(self):
        return "%s" %(self.num)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(YcAssets, self).save(force_insert, force_update, using, update_fields)
        if not self.num:
            self.num = 'YC%06d' % (self.id)
            self.save()

    class Meta:
        verbose_name = '银川资产表'
        verbose_name_plural = verbose_name


class YcAllocate(models.Model):
    id = models.AutoField(primary_key=True)
    num = models.ForeignKey(YcAssets, related_name='ycallocate_num', verbose_name='资产编号')
    status = models.CharField(max_length=25, choices=ASSETS_STATUS, verbose_name='维护类型')
    allocate_date = models.DateField(verbose_name='维护日期')
    use_department = models.ForeignKey(YcDepartment, related_name='ycallocate_use_department', blank=True, null=True, verbose_name='使用部门')
    user = models.ForeignKey(YcUserProfile,related_name='ycallocate_user', blank=True, null=True, verbose_name='使用人')
    description = models.CharField(max_length=300, blank=True, null=True, verbose_name='备注')
    create_time = models.DateTimeField(auto_now_add=True,blank=True, null=True, verbose_name='创建时间')
    modified_time = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name='修改时间')

    def __str__(self):
        return "%s%s" % (self.user, self.status)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(YcAllocate, self).save(force_insert, force_update, using, update_fields)
        if self.status == '归还':
            sql = 'UPDATE ycyy_ycassets SET status = %s, use_department_id = Null, user_id = Null WHERE id=%s'
            params = [self.status, self.num_id]
            generic.update(sql, params)
        elif self.status != '归还':
            sql = 'UPDATE ycyy_ycassets SET status = %s, use_department_id = %s, user_id = %s WHERE id=%s'
            params = [self.status, self.use_department_id, self.user_id, self.num_id]
            generic.update(sql, params)

    class Meta:
        verbose_name = '银川资产记录'
        verbose_name_plural = verbose_name