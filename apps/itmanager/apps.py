# -*- coding:utf-8 -*-
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _
# Create your apps here.
class ItManagerConfig(AppConfig):
    name = 'itmanager'
    verbose_name = _("IT管理")
