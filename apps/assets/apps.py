# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _
# Create your apps here.
class AssetsConfig(AppConfig):
    name = 'assets'
    verbose_name = _("资产管理")
