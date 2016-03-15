# import deform
from pyramid.view import view_config, view_defaults
from pyramid.httpexceptions import HTTPFound
# from pyramid.httpexceptions import HTTPForbidden
# from betahaus.pyracont.factories import createSchema
# from betahaus.pyracont.factories import createContent
from betahaus.viewcomponent import view_action
# from pyramid.security import effective_principals
# from pyramid.traversal import resource_path
# from pyramid.traversal import find_resource
# from pyramid.response import Response
from pyramid.decorator import reify
# from repoze.catalog.query import Eq
# from repoze.catalog.query import Any
from arche.portlets import PortletType
from arche.views.base import BaseView
from voteit.core.models.interfaces import IAgendaItem
from voteit.core.models.interfaces import IProposal
from voteit.core.models.interfaces import IMeeting
# from voteit.core.models.schemas import add_csrf_token
# from voteit.core.views.base_view import BaseView
from voteit.core import security
from pyramid.renderers import render
from voteit.core import _ as voteit_mf
#
from voteit.core.views.agenda_item import AgendaItemView
from voteit.groups.interfaces import IGroup
from voteit.groups.interfaces import IGroups
from voteit.groups.interfaces import IGroupRecommendations
from voteit.groups import _
# from voteit.groups.fanstaticlib import group_proposals
#
#
@view_config(name="groups", context = IMeeting)
def create_groups_content(context, request):
    """ This view will only be called if there's no groups object. """
    from voteit.groups.models import Groups
    context['groups'] = Groups()
    return HTTPFound(location = request.resource_url(context['groups']))


class GroupsView(BaseView):
    #FIXME: Check permissions for all actions

    @view_config(context = IGroups,
                 permission = security.MODERATE_MEETING,
                 renderer = "voteit.groups:templates/groups.pt")
    def view_groups(self):
        return {}
#
#
# class GroupView(BaseView):
#
#     @view_config(context = IGroup, renderer = "voteit.core.views:templates/base_edit.pt", permission = security.MODERATE_MEETING)
#     def view_group(self):
#         #FIXME: remove once done?
#         schema = createSchema('EditGroupSchema')
#         add_csrf_token(self.context, self.request, schema)
#         schema = schema.bind(context = self.context, request = self.request, api = self.api)
#         form = deform.Form(schema, buttons = ())
#         appstruct = self.context.get_field_appstruct(schema)
#         self.response['form'] = form.render(appstruct = appstruct, readonly = True)
#         return self.response
#
#
# class GroupProposalsView(BaseView):
#
#     @reify
#     def active_group(self):
#         """ Selected group id """
#         group = self.api.user_profile.get_field_value('active_group', None)
#         if group and group not in self.groups:
#             return None
#         return group
#
#     @reify
#     def group(self):
#         """ Group object if selected """
#         return self.groups.get(self.active_group, None)
#
#     @reify
#     def groups(self):
#         """ Groups folder for this meeting. """
#         return self.api.meeting['groups']
#
#     @reify
#     def selectable_group_ids(self):
#         return tuple([x.__name__ for x in self.groups.get_groups_for(self.api.userid)])
#
#     @view_config(name = "group_proposals", context = IAgendaItem, renderer = "templates/group_proposals.pt", permission = security.VIEW)
#     def view_group_proposals(self):
#         group_proposals.need() #js and css
#         self.response['active_group'] = self.active_group
#         self.response['group'] = self.group
#         if not self.active_group:
#             self.response['selectable_groups'] = self.groups.get_groups_for(self.api.userid)
#         self.response['available_hashtags'] = self.get_available_hashtags()
#         self.response['selected_tag'] = self.request.GET.get('tag', '')
#         self.response['inline_propose_button'] = self.inline_propose_button()
#         return self.response
#
#     def get_available_hashtags(self):
#         query = Eq('path', resource_path(self.context)) &\
#                 Any('allowed_to_view', effective_principals(self.request)) &\
#                 Eq('content_type', 'Proposal')
#         hashtags = set()
#         for docid in self.api.root.catalog.query(query)[1]:
#             metadata = self.api.root.catalog.document_map.get_metadata(docid)
#             hashtags.update(metadata.get('tags', ()))
#         return tuple(sorted(hashtags))
#
#     @view_config(name = "set_group_to_work_as", context = IAgendaItem, permission = security.VIEW)
#     def set_group_to_work_as(self):
#         """ Permissions are enforced in code below, so view permission works fine. """
#         picked_group = self.request.GET.get('active_group', None)
#         if picked_group not in self.selectable_group_ids:
#             raise HTTPForbidden(u"You can't select the group with id '%s'. Perhaps you're not a member of that group?" % picked_group)
#         self.api.user_profile.set_field_value('active_group', picked_group)
#         url = self.request.resource_url(self.context, 'group_proposals')
#         return HTTPFound(location = url)
#
#     @view_config(name = "clear_group_to_work_as", context = IAgendaItem, permission = security.VIEW)
#     def clear_group_to_work_as(self):
#         if 'active_group' in self.api.user_profile.field_storage:
#             del self.api.user_profile.field_storage['active_group']
#         url = self.request.resource_url(self.context, 'group_proposals')
#         return HTTPFound(location = url)
#
#     @view_config(name = "group_proposal_listing", context = IAgendaItem, permission = security.VIEW,
#                  renderer = 'templates/proposal_listing.pt', xhr = True)
#     def group_proposal_listing(self):
#
#         def _find_object(path):
#             return find_resource(self.api.root, path)
#         self.response['find_object'] = _find_object
#         self.response['recommendation_for'] = self._recommendation_for
#         self.response['other_group_data'] = self._other_group_data
#         self.response['active_group'] = self.active_group
#         self.response['group'] = self.group
#         try:
#             self.response['show_all'] = int(self.request.GET.get('all', 0))
#         except ValueError:
#             self.response['show_all'] = 0
#
#         query = Eq('path', resource_path(self.context)) & \
#                 Eq('content_type', 'Proposal')
#         total_count = self.api.root.catalog.query(query)[0]
#         tag = self.request.GET.get('tag', None)
#         if tag:
#             query = query & Any('tags', (tag, ))
#         count, docids = self.api.root.catalog.query(query, sort_index='created')
#         get_metadata = self.api.root.catalog.document_map.get_metadata
#         results = []
#         for docid in docids:
#             results.append(get_metadata(docid))
#         self.response['proposals'] = results
#         return self.response
#
#     @view_config(name = "set_recommendation_data", context = IProposal, permission = security.VIEW,
#                  renderer = 'json')
#     def set_recommendation_data(self):
#         active_group = self.api.user_profile.get_field_value('active_group', None)
#         assert active_group in self.selectable_group_ids #Extra safeguard, in case active_group is manipulated
#         #FIXME validation etc
#         data = dict(
#             state = self.request.POST.get('recommend_state'),
#             text = self.request.POST.get('recommend_text'),
#         )
#         recommendations = self.request.registry.getAdapter(self.context, IGroupRecommendations)
#         recommendations.set_group_data(active_group, **data)
#         return data
#
#     def inline_propose_button(self):
#         return u'<button id="add_propsal_button">%s</button>' % self.api.translate(_(u"Add proposal"))
#
#     def inline_proposal_form(self):
#         """ Adjusted so it also adds the groups hashtag.
#             Note that self.context must be an agenda item when using this.
#         """
#         schema = createSchema('ProposalSchema').bind(context = self.context, request = self.request, api = self.api)
#         #FIXME: Add tag to default schema item here
#         form = deform.Form(schema, buttons=('add',), action = '_inline_add_group_proposal')
#         return form
#
#     @view_config(name = "_inline_add_group_proposal", context = IAgendaItem, permission = security.ADD_PROPOSAL,
#                  renderer = 'voteit.core.views:templates/snippets/inline_form.pt')
#     def inline_propose_submit(self):
#         content_type = 'Proposal'
#         form = self.inline_proposal_form()
#         post = self.request.POST
#         if 'add' in post:
#             controls = post.items()
#             try:
#                 appstruct = form.validate(controls)
#             except deform.ValidationFailure, e:
#                 return Response(e.render())
#             kwargs = {}
#             kwargs.update(appstruct)
#             kwargs['creators'] = [self.api.userid]
#             obj = createContent(content_type, **kwargs)
#             name = obj.suggest_name(self.context)
#             self.context[name] = obj
#             return Response(self.inline_propose_button())
#
#         #Note! Registration of form resources has to be in the view that has the javascript
#         #that will include this!
#         self.response['form'] = form.render()
#         self.response['user_image_tag'] = self.api.user_profile.get_image_tag()
#         self.response['content_type'] = content_type
#         return self.response
#
#     def _recommendation_for(self, obj):
#         recommendations = self.request.registry.getAdapter(obj, IGroupRecommendations)
#         res = recommendations.get_group_data(self.active_group)
#         return res and res or {}
#
#     def _other_group_data(self, obj):
#         recommendations = self.request.registry.getAdapter(obj, IGroupRecommendations)
#         res = recommendations.get_other_group_data(self.active_group)
#         return res and res or {}
#
@view_action('participants_menu', 'groups', title = _(u"Groups"))
def groups_moderator_menu_link(context, request, va, **kw):
    url = request.resource_url(request.meeting, 'groups')
    return """<li><a href="%s">%s</a></li>""" % (url, request.localizer.translate(va.title))

_STATES = ('approved', 'denied', 'unhandled', '')
_STATE_TITLES = {'approved': voteit_mf("Approved"),
                  'denied': voteit_mf("Denied"),
                  'unhandled': voteit_mf("Unhandled"),
                  '': _("<Not set>")}
_STATE_ICONS = {'approved': 'approved',
                  'denied': 'denied',
                  'unhandled': 'unhandled',
                  '': 'minus',}

#@view_action('metadata_listing', 'group_recommendation', interface = IProposal)
#def render_group_recommendation(context, request, va, **kw):
#    recommendations = request.registry.getAdapter(context, IGroupRecommendations)
#    if len(recommendations):
#        response = {'recommendations': recommendations,
#                    'choices': _CHOICES,
#                    'choice_titles': _CHOICE_TITLES,
#                    'choice_icons': _CHOICE_ICONS}
#        return render('voteit.groups:templates/group_recommendation.pt', response, request = request)


@view_action('metadata_listing', 'group_recommendation', interface = IProposal)
def render_group_recommendation(context, request, va, **kw):
    recommendations = request.registry.getAdapter(context, IGroupRecommendations)
    if len(recommendations):
        response = {'state_icons': _STATE_ICONS, 'states': _STATES,
                    'state_count': recommendations.count_states(),
                    'context': context}
        return render('voteit.groups:templates/group_summary.pt', response, request = request)



class GroupControlsPortlet(PortletType):
    name = "voteit_groups_controls"
    title = _("Group recommendations")

    def render(self, context, request, view, **kwargs):
        groups = request.meeting.get('groups', None)
        if not groups:
            return
        response = {'title': _("Group recommendations"),
                    'groups': groups,
                    'portlet': self.portlet,
                    'view': view,}
        return render("voteit.groups:templates/group_controls.pt",
                      response,
                      request = request)

#FIXME: Permission
@view_defaults(context = IAgendaItem)
class ManageGroupRecommendationView(AgendaItemView):


    @view_config(name = 'group_recommendations', renderer = 'voteit.groups:templates/recommendation_main.pt')
    def main(self):
        return {'groups': self.request.meeting.get('groups', {}).values()}


#FIXME: Permission
@view_defaults(context = IProposal)
class ProposalGroupRecommendationView(BaseView):

    @view_config(name = '_recommendation_popover',
                 renderer = 'voteit.groups:templates/recommendation_popover.pt')
    def popover(self):
        return dict(recommendations = self.request.registry.getAdapter(self.context, IGroupRecommendations),
                    state_icons = _STATE_ICONS)


def includeme(config):
#    config.add_portlet(GroupControlsPortlet)
    config.scan()
