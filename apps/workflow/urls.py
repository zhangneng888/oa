# -*- coding:utf-8 -*-
from django.conf.urls import include, url,static
import workflow.views

urlpatterns = [
    url(r"^workflow/history/add/$", workflow.views.add_history,name="add_history"),
    url(r'^workflow/history.html', workflow.views.HistoryView.as_view(), name="history"),
]
