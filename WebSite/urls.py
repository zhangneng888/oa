# -*- coding: utf-8 -*-
from django.conf.urls import include, url

# Uncomment the next two lines to enable the admin:
import xadmin
xadmin.autodiscover()

# version模块自动注册需要版本控制的 Model
from xadmin.plugins import xversion
xversion.register_models()

from django.contrib import admin
from workflow.views import ActiveUserView
import workflow.views
urlpatterns = [
    #url(r'^workorder/(?P<model_name>.*)/(?P<object_id>.*)/(?P<action>.*)/$', ActiveUserView.as_view(),name="workorder"),
    #url(r"^(?P<app>\w+)/(?P<model>\w+)/(?P<object_id>\d+)/start", ActiveUserView.as_view()),
    url(r"^(?P<app>\w+)/(?P<model>\w+)/(?P<object_id>\d+)/start", workflow.views.start),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(xadmin.site.urls)),
]