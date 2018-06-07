# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from usermanager.models import UserProfile,Department
import datetime
from django.utils.html import format_html
# Create your models here.

HANDLER_TYPE = (
    (1, u"用户"),
    (2, u"角色"),
    (3, u"部门"),
    (4, u"岗位"),
)

class Modal(models.Model):
    """
    工作流模型：关联流程表单
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(u"工作流名称",max_length=40,null=True)
    content_type = models.ForeignKey(ContentType,verbose_name=u"关联表单",null=True)
    description = models.TextField(u"描述信息",blank=True,null=True)
    app_name = models.CharField(u"应用名称",max_length=60,blank=True,null=True)
    model_name = models.CharField(u"模型名称",max_length=60,blank=True,null=True)

    def __str__(self):
        return "%s" % self.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.app_name = self.content_type.app_label
        self.model_name = self.content_type.model
        super(Modal, self).save(force_insert, force_update, using, update_fields)

    class Meta:
        verbose_name = u"工作流模型"
        verbose_name_plural = verbose_name

class Node(models.Model):
    """
    工作流节点：设置基础的流程流转
    """
    NOTICE_TYPE = (
        (1, u"邮件通知"),
        (2, u"短信通知"),
    )
    id = models.AutoField(primary_key=True)
    modal = models.ForeignKey(Modal,verbose_name=u"工作流模型",related_name="node_modal_set")
    name = models.CharField(u"节点名称", max_length=80, blank=True, null=True)
    code = models.CharField(u"节点编号",max_length=10,blank=True,null=True)
    notice_type = models.IntegerField(u"通知类型", choices=NOTICE_TYPE, default=1, blank=True, null=True)
    handler_type = models.IntegerField(u"管理者类型", choices=HANDLER_TYPE, default=1,blank=True,null=True)
    handler_user = models.ForeignKey(UserProfile,verbose_name=u"指定用户",related_name="node_handler_user_set",blank=True,null=True)
    handler_role = models.ForeignKey(UserProfile, verbose_name=u"指定角色", related_name="node_handler_roles_set",blank=True,null=True)
    handler_department = models.ForeignKey(Department, verbose_name=u"指定部门", related_name="node_handler_department_set",blank=True,null=True)
    handler_position = models.ForeignKey(UserProfile, verbose_name=u"指定岗位", related_name="node_handler_position_set",blank=True,null=True)
    code_branch = models.BooleanField(u"分支", default=False)
    start = models.BooleanField(u"开始", default=False)
    stop = models.BooleanField(u"结束", default=False)
    can_approve = models.BooleanField(u"同意", default=False)
    can_deny = models.BooleanField(u"拒绝", default=False)
    can_transfer = models.BooleanField(u"转交", default=False)
    can_reject = models.BooleanField(u"驳回", default=False)
    can_finish = models.BooleanField(u"完成", default=False)
    can_not_finish = models.BooleanField(u"未完成", default=False)
    can_delete = models.BooleanField(u"删除", default=False)

    def __str__(self):
        return "%s" % self.name

    def save(self, force_insert=False, force_update=False, using=None,update_fields=None):
        if not self.code:
            fmt = 'N%02d'
            self.code = fmt % (self.modal.node_modal_set.count()+1)
        super(Node,self).save(force_insert,force_update,using,update_fields)

    class Meta:
        verbose_name = '工作流节点'
        verbose_name_plural = verbose_name

class NodeBranch(models.Model):
    """
    工作流节点分支：用于添加该节点下的流转条件
    """
    id = models.AutoField(primary_key=True)
    node = models.ForeignKey(Node,verbose_name=u"节点分支",related_name="node_modal_set")
    name = models.CharField(u"分支名称", max_length=80, blank=True, null=True)
    branch_condition = models.CharField(u"分支条件", max_length=50, blank=True, null=True)
    branch_field = models.CharField(u"分支字段", max_length=50, blank=True, null=True)
    handler_type = models.IntegerField(u"管理者类型", choices=HANDLER_TYPE, default=1, blank=True, null=True)
    handler_user = models.ForeignKey(UserProfile, verbose_name=u"指定用户", related_name="nodebranch_handler_user_set",blank=True, null=True)
    handler_role = models.ForeignKey(UserProfile, verbose_name=u"指定角色", related_name="nodebranch_handler_roles_set",blank=True, null=True)
    handler_department = models.ForeignKey(Department, verbose_name=u"指定部门", related_name="nodebranch_handler_department_set",blank=True, null=True)
    handler_position = models.ForeignKey(UserProfile, verbose_name=u"指定岗位", related_name="nodebranch_handler_position_set",blank=True, null=True)

    def __str__(self):
        return "%s" % self.name

    class Meta:
        verbose_name = '工作流节点分支'
        verbose_name_plural = verbose_name

class History(models.Model):
    """
    工作流历史：
    """
    modal = models.CharField(u"工作流模型",max_length=25,blank=True,null=True)
    instance = models.CharField(u"工作流实例", max_length=25, blank=True, null=True)
    submit_time = models.DateTimeField(u"提交时间", auto_now_add=True)
    submit_user = models.ForeignKey(UserProfile,verbose_name=u"提交人",related_name="history_submit_user_set")
    submit_type = models.CharField(u"动作",max_length=25,blank=True,null=True)
    description = models.CharField(u"描述",max_length=200,blank=True,null=True)

    class Meta:
        verbose_name = u"工作流历史"
        verbose_name_plural = verbose_name

# class Approval(models.Model):
#     code = models.CharField(_("编码"),max_length=6,blank=True,null=True)
#     name = models.CharField(_("工作流名称"),blank=True,null=True,max_length=40)
#     des = models.TextField(_("描述信息"),blank=True,null=True)
#
#     def __str__(self):
#         return "%s" %(self.name)
#
#     class Meta:
#         verbose_name = '工作流记录'
#         verbose_name_plural = verbose_name
#
#
#
#
# class Instance(models.Model):
#     STATUS = (
#         (1, _("NEW")),
#         (2, _("IN PROGRESS")),
#         (3, _("DENY")),
#         (4, _("TERMINATED")),
#         (9, _("APPROVED")),
#         (99, _("COMPLETED"))
#     )
#     index_weight = 3
#     code = models.CharField(_("code"),blank=True,null=True,max_length=10)
#     modal = models.ForeignKey(Modal,verbose_name=_("workflow model"))
#     object_id = models.PositiveIntegerField("object id")
#     starter = models.ForeignKey(UserProfile,verbose_name=_("start user"),related_name="starter")
#     start_time = models.DateTimeField(_("start time"),auto_now_add=True)
#     approved_time = models.DateTimeField(_("approved time"),blank=True,null=True)
#     status = models.IntegerField(_("status"),default=1,choices=STATUS)
#     current_nodes = models.ManyToManyField(Node,verbose_name=_("current node"),blank=True)
#
#     def __str__(self):
#         return '%s' % self.code
#
#     def save(self, force_insert=False, force_update=False, using=None,update_fields=None):
#         super(Instance,self).save(force_insert,force_update,using,update_fields)
#         if not self.code:
#             self.code = 'S%05d'%self.id
#             self.save()
#
#     class Meta:
#         verbose_name = '工作流实例'
#         verbose_name_plural = verbose_name
#
#
#
# class TodoList(models.Model):
#     index_weight = 4
#     code = models.CharField(_("code"),max_length=10,blank=True,null=True)
#     inst = models.ForeignKey(Instance,verbose_name=_("workflow instance"))
#     node = models.ForeignKey(Node,verbose_name=_("current node"),blank=True,null=True)
#     app_name = models.CharField(_("app name"),max_length=60,blank=True,null=True)
#     model_name = models.CharField(_("model name"),max_length=60,blank=True,null=True)
#     user = models.ForeignKey(UserProfile,verbose_name=_("handler"))
#     arrived_time = models.DateTimeField(_("arrived time"),auto_now_add=True)
#     is_read = models.BooleanField(_("is read"),default=False)
#     read_time = models.DateTimeField(_("read time"),blank=True,null=True)
#     status = models.BooleanField(_("is done"),default=False)
#
#     def save(self, force_insert=False, force_update=False, using=None,update_fields=None):
#         super(TodoList,self).save(force_update,force_update,using,update_fields)
#         if not self.code:
#             self.code = 'TD%05d' % self.id
#             self.save()
#
#     def node_dsc(self):
#         if self.node:
#             return u'%s'%self.node.name
#         else:
#             return u'启动'
#
#     def code_link(self):
#         return format_html("<a href='/admin/{}/{}/{}'>{}</a>",
#                            self.app_name,self.model_name,self.inst.object_id,self.code)
#     code_link.allow_tags = True
#     code_link.short_description = _("code")
#
#     def href(self):
#         import sys
#         reload(sys)
#         sys.setdefaultencoding("utf-8")
#         ct = ContentType.objects.get(app_label=self.app_name,model=self.model_name)
#         obj = ct.get_object_for_this_type(id=self.inst.object_id)
#         title = u"%s" % (obj)
#         return format_html("<a href='/admin/{}/{}/{}'>{}</a>",
#                            self.app_name,self.model_name,self.inst.object_id,title)
#     def modal_dsc(self):
#         return u'%s'%(self.inst.modal.name)
#     modal_dsc.short_description = u'业务流程'
#
#     def start_time(self):
#         return self.inst.start_time.strftime('%Y-%m-%d %H:%M')
#
#     href.allow_tags = True
#     href.short_description = _("description")
#     node_dsc.short_description = _('current node')
#
#     def submitter(self):
#         return "%s" % (self.inst.starter)
#     submitter.short_description = _("submitter")
#
#     class Meta:
#         verbose_name = '待办任务'
#         verbose_name_plural = verbose_name
#
# def get_modal(app_label,model_name):
#     try:
#         return Modal.objects.get(app_name=app_label,model_name=model_name)
#     except Exception,e:
#         return None
#
# def get_instance(obj):
#     if obj and obj._meta:
#         modal = get_modal(obj._meta.app_label,obj._meta.model_name)
#         if modal:
#             try:
#                 return Instance.objects.get(modal=modal,object_id=obj.id)
#             except Exception,e:
#                 return None
#     else:
#         return None
