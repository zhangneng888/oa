# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from xadmin.plugins import generic
from usermanager.models import Department,UserProfile

# Create your models here.
class ItManager(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name="名称")
    model = models.CharField(max_length=30,null=True,blank=True,verbose_name="型号")
    ip = models.CharField(max_length=50,null=True,blank=True,verbose_name="IP")
    system = models.CharField(max_length=15,null=True,blank=True,verbose_name="系统")
    username = models.CharField(max_length=20,null=True,blank=True,verbose_name="用户名")
    password = models.CharField(max_length=30,null=True,blank=True,verbose_name="密码")
    link = models.URLField(max_length=200,null=True,blank=True,verbose_name="链接")
    tel = models.CharField(max_length=80, null=True, blank=True, verbose_name="联系电话")
    application = models.CharField(blank=True, null=True, max_length=200, verbose_name="应用")
    dep = models.ForeignKey(Department, related_name='itmanager_dep_set', verbose_name="使用部门")
    remarks = models.TextField(max_length=200,null=True,blank=True,verbose_name="备注")
    is_active = models.BooleanField(default=True,verbose_name="使用中")
    create_time = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    modified_time = models.DateTimeField(auto_now=True,verbose_name="修改时间")

    def __str__(self):
        return  "%s" %(self.name)

    class Meta:
        verbose_name = "IT运维信息"
        verbose_name_plural = verbose_name

class ItRecord(models.Model):
    id = models.AutoField(primary_key=True)
    ip = models.CharField(max_length=24,null=True,blank=True,verbose_name="IP")
    name = models.ForeignKey(ItManager,related_name='itrecord_name_set',verbose_name="系统")
    system = models.CharField(max_length=15,null=True, blank=True, verbose_name="系统")
    username = models.CharField(max_length=20,null=True,blank=True,verbose_name="用户名")
    password = models.CharField(max_length=30,null=True,blank=True,verbose_name="密码")
    application = models.CharField(blank=True, null=True, max_length=200, verbose_name="应用")
    remarks = models.CharField(max_length=200,null=True,blank=True,verbose_name="备注")
    create_time = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    modified_time = models.DateTimeField(auto_now=True,verbose_name="修改时间")

    def __str__(self):
         return "%s%s" % (self.ip, self.application)

    class Meta:
        verbose_name = "IT运维详情记录"
        verbose_name_plural = verbose_name

class DhcpBind(models.Model):
    SCOPE_IPTABLES = (
        ('10.0.0.0', "10.0.0.0-10.0.7.254"),
        ('10.1.0.0', "10.1.0.0-10.1.1.254"),
        ('10.1.6.0', "10.1.6.0-10.1.7.254"),
        ('10.1.8.0', "10.1.8.0-10.1.9.254"),
    )
    DESCRIBE_IPTABLES = (
        ('phone', "phone"),
        ('pc', "pc")
    )
    id = models.AutoField(primary_key=True)
    scope = models.CharField(max_length=30, choices=SCOPE_IPTABLES, verbose_name="范围")
    ip = models.GenericIPAddressField(verbose_name="IP")
    mac = models.CharField(max_length=20,verbose_name="MAC")
    describe = models.CharField(max_length=20,choices=DESCRIBE_IPTABLES,verbose_name="描述")
    name = models.CharField(max_length=20,verbose_name="姓名")
    judge = models.BooleanField(verbose_name="办公设备")
    state = models.BooleanField(verbose_name="使用中")
    cmd = models.TextField(max_length=150,blank=True,null=True,verbose_name="命令")

    def __str__(self):
         return "%s" % (self.ip)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.cmd = 'netsh dhcp server 192.168.1.222 scope %s add reservedip %s %s %s %s BOTH' \
                   % (self.scope,self.ip,self.mac,self.describe,self.name)
        super(DhcpBind, self).save(force_insert, force_update, using, update_fields)

    class Meta:
        verbose_name = "DHCP绑定"
        verbose_name_plural = verbose_name

class WrokOrdersType(models.Model):
    id = models.AutoField(primary_key=True)
    pro_type = models.CharField(max_length=50,blank=True,null=True,verbose_name="问题类型")
    description = models.TextField(blank=True, null=True,verbose_name="描述")

    def __str__(self):
        return "%s" % self.pro_type

    class Meta:
        verbose_name = "工单类型"
        verbose_name_plural = verbose_name

class WrokOrders(models.Model):
    id = models.AutoField(primary_key=True)
    org_dept = models.ForeignKey(Department,blank=True,null=True,related_name='workorders_org_dept',verbose_name="发起部门")
    org_user = models.ForeignKey(UserProfile,related_name='workorders_org_user',verbose_name="发起人")
    pro_type = models.ForeignKey(WrokOrdersType,related_name="workorders_pro_type",verbose_name="问题类型")
    pro_date = models.DateField(verbose_name="问题日期")
    pro_desc = models.TextField(blank=True, null=True,verbose_name="问题描述")
    solver = models.CharField(max_length=100,blank=True,null=True,verbose_name="解决人",help_text="多个解决人时用英文逗号分隔")
    solve_len_time = models.DecimalField(max_digits=10,decimal_places=2,default=0,verbose_name='工时(小时)',help_text="最小单位0.25即15分钟")
    solve_desc = models.TextField(blank=True,null=True,verbose_name="解决方法")
    is_finish = models.BooleanField(default=False,verbose_name="已完成",help_text="不需要IT运维部再进行处理的问题即为已完成")
    is_key_work = models.BooleanField(default=False, verbose_name="重点工作", help_text="耗时较长或比较重要的工作内容即为重点工作")
    creator = models.CharField(max_length=50,blank=True,null=True,verbose_name="创建者")
    create_time = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    modified_time = models.DateTimeField(auto_now=True,verbose_name="修改时间")

    def __str__(self):
         return "%s" % self.pro_type

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(WrokOrders, self).save(force_insert, force_update, using, update_fields)
        if not self.org_dept:
            sql = 'UPDATE itmanager_wrokorders SET org_dept_id = (SELECT department_id from usermanager_userprofile WHERE user_id = %s) WHERE id=%s'
            params = [self.org_user_id,self.id]
            generic.update(sql, params)

    class Meta:
        verbose_name = "工单记录"
        verbose_name_plural = verbose_name
