# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from usermanager.models import UserProfile,Department
import datetime
from django.utils.html import format_html
# Create your models here.

class AssetApplicationProcess(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(_('编码'), max_length=6, blank=True, null=True)
    assets_name = models.CharField(_('资产名称'), max_length=20, blank=True, null=True)
    department = models.ForeignKey(Department, related_name='AssetApplicationProcess_department_set', blank=True, null=True,verbose_name='使用部门')
    user = models.ForeignKey(UserProfile, related_name='AssetApplicationProcess_user_set', blank=True, null=True, verbose_name='使用人')
    description = models.CharField(_('备注'),max_length=300, blank=True, null=True)
    create_time = models.DateTimeField(_('创建时间'),auto_now_add=True, blank=True, null=True)
    modified_time = models.DateTimeField(_('修改时间'),auto_now=True, blank=True, null=True)

    def __str__(self):
        return "%s" %(self.code)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.code:
            self.code = 'WF%03d' % (self.id)
        super(AssetApplicationProcess, self).save(force_insert, force_update, using, update_fields)

    class Meta:
        verbose_name = u"资产申请流程"
        verbose_name_plural = verbose_name


