# -*- coding:utf-8 -*-
from xadmin.layout import Main,Side,Fieldset,Row
import xadmin
from models import Modal,Node,NodeBranch,History
# Register your models here.
class NodeInline(object):
    model = Node
    exclude = ['code','notice_type','handler_type','handler_role','handler_department','handler_position']
    extra = 1
    style = 'table'


class ModalAdmin(object):
    inlines = [NodeInline]
    list_display = ['name','app_name','model_name']
    readonly_fields = ['app_name','model_name']
    raw_id_fields = ['content_type']
    form_layout = (
        Row('name','content_type'),
        Row('app_name','model_name'),
        Row('description'),
    )
xadmin.site.register(Modal, ModalAdmin)

class NodeBranchInline(object):
    model = NodeBranch
    form_layout = (
        Row('name','handler_type'),
        Row('handler_user','handler_role'),
        Row('handler_department','handler_position'),
        Row('branch_condition', 'branch_field'),
    )
    extra = 1
    style = 'accordion'

class NodeAdmin(object):
    inlines = [NodeBranchInline]
    form_layout = (
        Main(
            Fieldset('',
                Row('modal','name'),
                Row('code','notice_type'),
                Row('handler_type'),
                Row('handler_user','handler_role'),
                Row('handler_department', 'handler_position'),
                     ),
        ),
        Side(
            Fieldset(('Status'),
                     'code_branch','start','stop','can_approve','can_deny','can_transfer','can_reject',
                     'can_finish','can_not_finish','can_delete'
                     ),
        )
    )
    list_display = ['modal','code','name','start','stop','can_approve','can_deny','can_transfer','can_reject',
                    'can_finish','can_not_finish','can_delete']
    list_filter = ['modal']
    readonly_fields = ['modal','code','name']
    search_fields = ['modal__name']
xadmin.site.register(Node, NodeAdmin)

class HistoryAdmin(object):
    list_display = ['modal','instance','submit_time','submit_user','submit_type','description']
xadmin.site.register(History, HistoryAdmin)

# class ApprovalAdmin(object):
#     list_display = ['code','name','des']
# xadmin.site.register(Approval, ApprovalAdmin)
#
# class InstanceAdmin(object):
#     list_display = ['code','modal','starter','start_time','status']
#     style_fields = {'current_nodes': 'm2m_transfer'}
# xadmin.site.register(Instance, InstanceAdmin)
#
#
#
# class TodoListAdmin(object):
#     list_display = ['code_link','modal_dsc','href','node_dsc','is_read','status','submitter','arrived_time']
#     list_filter = ['status']
# xadmin.site.register(TodoList, TodoListAdmin)