import deform
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.httpexceptions import HTTPForbidden
from betahaus.pyracont.factories import createSchema
from betahaus.pyracont.factories import createContent
from pyramid.security import effective_principals
from pyramid.traversal import resource_path
from pyramid.traversal import find_resource
from pyramid.response import Response
from pyramid.renderers import render
from pyramid.decorator import reify
from repoze.catalog.query import Eq
from repoze.catalog.query import Any
from voteit.core.models.interfaces import IAgendaItem
from voteit.core.models.interfaces import IProposal
from voteit.core.models.interfaces import ISiteRoot
from voteit.core.views.base_view import BaseView
from voteit.core import security

from voteit.groups.interfaces import IGroup
from voteit.groups.interfaces import IGroups
from voteit.groups.interfaces import IGroupRecommendations
from voteit.groups import VoteITGroupsMF as _
from voteit.groups.fanstaticlib import group_proposals


@view_config(name="groups", context = ISiteRoot)
def create_groups_content(context, request):
    """ This view will only be called if there's no groups object. """
    from voteit.groups.models import Groups
    context['groups'] = Groups()
    return HTTPFound(location = request.resource_url(context['groups']))


class GroupsView(BaseView):
    #FIXME: Check permissions for all actions

    @view_config(context = IGroups, renderer = "templates/groups.pt", permission = security.MODERATE_MEETING)
    def view_groups(self):
        if self.api.show_moderator_actions:
            add_groups_schema = createSchema('AddGroupSchema').bind(context = self.context, request = self.request, api = self.api)
            add_groups_form = deform.Form(add_groups_schema, buttons = (deform.Button('add', _(u"Add")),))

        if 'add' in self.request.POST:
            controls = self.request.POST.items()
            try:
                appstruct = add_groups_form.validate(controls)
            except deform.ValidationFailure, e:
                self.response['add_groups_form'] = e.render()
                return self.response
            group = self.context[appstruct['name']] = createContent('Group', creators = [self.api.userid])
            url = self.request.resource_url(group, 'edit')
            return HTTPFound(location = url)

        self.response['add_groups_form'] = add_groups_form.render()
        return self.response


class GroupView(BaseView):
    
    @view_config(context = IGroup, renderer = "templates/group.pt", permission = security.MODERATE_MEETING)
    def view_group(self):
        #FIXME: remove once done?
        schema = createSchema('EditGroupSchema').bind(context = self.context, request = self.request, api = self.api)
        form = deform.Form(schema, buttons = ())
        appstruct = self.context.get_field_appstruct(schema)
        self.response['form'] = form.render(appstruct = appstruct, readonly = True)
        return self.response

class GroupProposalsView(BaseView):

    @reify
    def active_group(self):
        group = self.api.user_profile.get_field_value('active_group', None)
        if group and group not in self.api.root['groups']:
            return None
        return group
    
    @view_config(name = "group_proposals", context = IAgendaItem, renderer = "templates/group_proposals.pt", permission = security.MODERATE_MEETING)
    def view_group_proposals(self):
        group_proposals.need() #js and css
        groups = self.api.root['groups']
        self.response['active_group'] = self.active_group
        self.response['group'] = groups.get(self.active_group, None)
        if not self.active_group:
            self.response['selectable_groups'] = groups.get_groups_for(self.api.userid)
        self.response['available_hashtags'] = self.get_available_hashtags()
        self.response['selected_tag'] = self.request.GET.get('tag', '')
        return self.response

    def get_available_hashtags(self):
        query = Eq('path', resource_path(self.context)) &\
                Any('allowed_to_view', effective_principals(self.request)) &\
                Eq('content_type', 'Proposal')
        hashtags = set()
        for docid in self.api.root.catalog.query(query)[1]:
            metadata = self.api.root.catalog.document_map.get_metadata(docid)
            hashtags.update(metadata.get('tags', ()))
        return tuple(sorted(hashtags))

    @view_config(name = "set_group_to_work_as", context = IAgendaItem)
    def set_group_to_work_as(self, permission = security.VIEW):
        selectable_group_ids = [x.__name__ for x in self.api.root['groups'].get_groups_for(self.api.userid)]
        picked_group = self.request.GET.get('active_group', None)            
        if picked_group not in selectable_group_ids:
            raise HTTPForbidden(u"You can't select the group with id '%s'. Perhaps you're not a member of that group?" % picked_group)
        self.api.user_profile.set_field_value('active_group', picked_group)
        url = self.request.resource_url(self.context, 'group_proposals')
        return HTTPFound(location = url)

    @view_config(name = "clear_group_to_work_as", context = IAgendaItem, permission = security.VIEW)
    def clear_group_to_work_as(self):
        if 'active_group' in self.api.user_profile.field_storage:
            del self.api.user_profile.field_storage['active_group']
        url = self.request.resource_url(self.context, 'group_proposals')
        return HTTPFound(location = url)

    @view_config(name = "group_proposal_listing", context = IAgendaItem, permission = security.MODERATE_MEETING,
                 renderer = 'templates/proposal_listing.pt') #xhr = True
    def group_proposal_listing(self):

        def _find_object(path):
            return find_resource(self.api.root, path)
        self.response['find_object'] = _find_object

        self.response['recommendation_for'] = self._recommendation_for
        self.response['active_group'] = self.api.user_profile.get_field_value('active_group', None)

        query = Eq('path', resource_path(self.context)) & \
                Eq('content_type', 'Proposal')
        total_count = self.api.root.catalog.query(query)[0]
        tag = self.request.GET.get('tag', None)
        if tag:
            query = query & Any('tags', (tag, ))
        count, docids = self.api.root.catalog.query(query, sort_index='created', reverse=True)
        get_metadata = self.api.root.catalog.document_map.get_metadata
        results = []
        for docid in docids:
            #Insert the resolved docid first, since we need to reverse order again.
            results.insert(0, get_metadata(docid))
        self.response['proposals'] = results
        return self.response

    @view_config(name = "set_recommendation_data", context = IProposal, permission = security.MODERATE_MEETING,
                 renderer = 'json') #FIXME: Permisisons
    def set_recommendation_data(self):
        active_group = self.api.user_profile.get_field_value('active_group', None)
        #FIXME validation etc
        data = dict(
            state = self.request.POST.get('recommend_state'),
            text = self.request.POST.get('recommend_text'),
        )
        recommendations = self.request.registry.getAdapter(self.context, IGroupRecommendations)
        recommendations.set_group_data(active_group, **data)
        return data

    def _recommendation_for(self, obj):
        recommendations = self.request.registry.getAdapter(obj, IGroupRecommendations)
        res = recommendations.get_group_data(self.active_group)
        return res and res or {}
