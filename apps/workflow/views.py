# -*- coding:utf-8 -*-
from django.core.checks import messages
from django.template.response import TemplateResponse
from django.views.generic.base import View
from django.shortcuts import render,redirect
from django.contrib.contenttypes.models import ContentType
from models import History,Modal
from xadmin import site
from xadmin.views.edit import ModelAdminView,ModelFormAdminView
from xadmin.views.base import CommAdminView
from django.utils.encoding import force_text
from django.forms import ModelForm
from django.http import HttpRequest,HttpResponseRedirect,HttpResponse
from workorder.models import AssetApplicationProcess
from django.views.generic.detail import SingleObjectMixin
import datetime

class ActiveUserView(View):
    def get(self,request,app,model,object_id):
        pass

class HistoryView(View):
    def get(self,request):
        history_list = History.objects.all().filter()
        return render(request, "xadmin/workflow/history.html", {"history_list":history_list})

def start(request,app,model,object_id):
    """

    :param request:
    :return:
    """
    import datetime
    content_type = ContentType.objects.get(app_label=app,model=model)
    obj = content_type.get_object_for_this_type(id=int(object_id))
    title = ("Are you sure?")
    opts = obj._meta
    objects_name = force_text(opts.verbose_name)
    has_workflow = False
    queryset = Modal.objects.filter(content_type=content_type,end__gt=datetime.date.today()).order_by('-end')
    cnt = queryset.count()
    workflow_modal = None
    next_node = None
    next_users = []
    has_next_user = False
    if cnt > 0:
        has_workflow = True
        workflow_modal = queryset[0]
        query_start_node = workflow_modal.node_set.filter(start=1)
        query_first_node = workflow_modal.node_set.order_by('id')
        if query_start_node.count() > 0:
            next_node = query_start_node[0]
        elif query_first_node.count()>0:
            next_node = query_first_node[0]
        if next_node:
            next_users = 'admin'
            if len(next_users) > 0:
                has_next_user = True
    else:
        title = ("No workflow model was found")


    if request.POST.get("post"):
        return HttpResponseRedirect("/%s/%s/%s"%(app,model,object_id))

    context = dict(
        site.each_context(request),
        title=title,
        opts=opts,
        objects_name=objects_name,
        object=obj,
        has_workflow = has_workflow,
        workflow_modal = workflow_modal,
        next_node = next_node,
        has_next_user = has_next_user,
        next_users = next_users,
        checkbox_name = "admin",
    )
    request.current_app = site.name

    return TemplateResponse(request,'xadmin/workflow/workflow_start_confirmation.html', context)



# class ApprovalView(View):
#     def get(self,request):
#         approval_form = ApprovalForm()
#         return render(request, "xadmin/workflow/model_form.html", {'approval_form': approval_form})
#
#     def post(self, request):
#         # 实例化form
#         approval_form = ApprovalForm(request.POST)
#         if approval_form.is_valid():
#             # 这里注册时前端的name为email
#             approval_code = request.POST.get("code", "")
#             approval_name = request.POST.get("name", "")
#             approval_des = request.POST.get("des", "")
#             # 实例化一个user_profile对象，将前台值存入
#             app_roval = Approval()
#             app_roval.code = approval_code
#             app_roval.name = approval_name
#             app_roval.des = approval_des
#             app_roval.save()
#             return render(request, "xadmin/workflow/model_form.html", )
