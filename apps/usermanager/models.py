# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User,AbstractUser
from django.db import models
from xadmin.plugins import generic
# Create your models here.
class Department(models.Model):
    id = models.AutoField(primary_key=True)
    first_department = models.CharField(max_length=25, verbose_name='一级部门')
    two_department = models.CharField(max_length=25, verbose_name='二级部门')
    first_leader = models.CharField(max_length=25, verbose_name='一级领导')
    two_leader = models.CharField(max_length=25, verbose_name='二级领导')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    modified_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    def __str__(self):
        return "%s" %(self.two_department)

    class Meta:
        verbose_name = '部门管理'
        verbose_name_plural = verbose_name

class UserProfile(models.Model):
    STATUS = (
        ('试用期', u"试用期"),
        ('已转正', u"已转正"),
        ('已离职', u"已离职"),
    )
    user = models.OneToOneField(User,related_name='userprofile_user',verbose_name='用户名')
    department = models.ForeignKey(Department, blank=True, null=True, related_name='userprofile_department', verbose_name='部门')
    name = models.CharField(max_length=25, blank=True, null=True, verbose_name='姓名')
    email = models.CharField(max_length=30, blank=True, null=True, verbose_name='邮件')
    tel = models.CharField(max_length=25, blank=True, null=True, verbose_name='电话')
    status = models.CharField(max_length=25, blank=True, null=True, choices=STATUS, verbose_name='状态')
    entry_date = models.DateField(blank=True, null=True, verbose_name='入职日期')

    def __str__(self):
        return "%s" %(self.name)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(UserProfile, self).save(force_insert, force_update, using, update_fields)
        sql = 'UPDATE auth_user SET first_name = %s,email = %s WHERE id=%s'
        params = [self.name, self.email, self.user_id]
        generic.update(sql, params)

    class Meta:
        verbose_name = '员工信息'
        verbose_name_plural = verbose_name

def create_user_profile(sender, instance, created, **kwargs):
    """Create the UserProfile when a new User is saved"""
    if created:
        profile = UserProfile()
        profile.user = instance
        profile.save()
