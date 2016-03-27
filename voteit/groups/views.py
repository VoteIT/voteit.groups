from arche.views.base import BaseView
from betahaus.viewcomponent import view_action
from pyramid.traversal import resource_path
from pyramid.view import view_config, view_defaults
from pyramid.httpexceptions import HTTPFound, HTTPBadRequest, HTTPForbidden
from pyramid.renderers import render
from pyramid.decorator import reify
from voteit.core.models.interfaces import IAgendaItem
from voteit.core.models.interfaces import IProposal
from voteit.core.models.interfaces import IMeeting
from voteit.core import security
from voteit.core import _ as voteit_mf
from voteit.core.views.agenda_item import AgendaItemView

from voteit.groups.interfaces import IGroups
from voteit.groups.interfaces import IGroupRecommendations
from voteit.groups import _
from voteit.groups.fanstaticlib import group_proposals


def _in_any_group(request):
    groups = request.meeting.get('groups', {})
    return bool([x for x in groups.values() if request.authenticated_userid in x.members])


@view_config(name="groups", context = IMeeting)
def create_groups_content(context, request):
    """ This view will only be called if there's no groups object. """
    from voteit.groups.models import Groups
    context['groups'] = Groups()
    return HTTPFound(location = request.resource_url(context['groups']))


class GroupsView(BaseView):

    @view_config(context = IGroups,
                 permission = security.MODERATE_MEETING,
                 renderer = "voteit.groups:templates/groups.pt")
    def view_groups(self):
        return {}


@view_action('participants_menu', 'groups', title = _(u"Groups"))
def groups_moderator_menu_link(context, request, va, **kw):
    if request.is_moderator:
        url = request.resource_url(request.meeting, 'groups')
        return """<li><a href="%s">%s</a></li>""" % (url, request.localizer.translate(va.title))

_STATES = ('approved', 'denied', 'neutral', '')
_STATE_TITLES = {'approved': voteit_mf("Approved"),
                  'denied': voteit_mf("Denied"),
                  'neutral': voteit_mf("Neutral"),
                  '': _("<Not set>")}
_STATE_ICONS = {'approved': 'glyphicon glyphicon-approved',
                  'denied': 'glyphicon glyphicon-denied',
                  'neutral': 'glyphicon glyphicon-minus',
                  '': 'glyphicon glyphicon-question-sign',}


@view_action('metadata_listing', 'group_recommendation', interface = IProposal)
def render_group_recommendation(context, request, va, **kw):
    recommendations = request.registry.getAdapter(context, IGroupRecommendations)
    if len(recommendations):
        response = {'state_icons': _STATE_ICONS, 'states': _STATES,
                    'state_count': recommendations.count_states(),
                    'context': context}
        return render('voteit.groups:templates/group_summary.pt', response, request = request)


@view_defaults(context = IAgendaItem)
class ManageGroupRecommendationView(AgendaItemView):

    @view_config(name = 'group_recommendations',
                 renderer = 'voteit.groups:templates/recommendation_main.pt')
    def main(self):
        if not (self.request.is_moderator or _in_any_group(self.request)):
            raise HTTPForbidden("Access to groups requires that you're a moderator or a member of a group.")
        group_proposals.need()
        query = "type_name == 'Proposal' and path == '%s' and " % resource_path(self.context)
        query += "workflow_state in any(['published','approved','denied'])"
        proposals = tuple(self.catalog_query(query, resolve=True, sort_index = 'created')) #Generator
        return {'proposals': proposals,
                'state_icons': _STATE_ICONS,
                'state_titles': _STATE_TITLES,
                'states': _STATES}

    @view_config(context = IProposal,
                 name = '_set_group_recommendation',
                 renderer = 'json')
    def set_group_recommendation(self):
        state = self.request.GET.get('state','')
        if state not in _STATES:
            raise HTTPBadRequest("No such state: %r" % state)
        recommendations = self.get_rec(self.context)
        recommendations.update(self.gname, state = state)
        if self.request.is_xhr:
            return {'success': True}
        return HTTPFound(location = self.request.resource_url(self.context.__parent__,
                                                              'group_recommendations',
                                                              query = {'group': self.gname}))

    @view_config(context = IProposal,
                 name = '_set_group_recommendation_text',
                 renderer = 'json')
    def set_group_recommendation_text(self):
        text = self.request.POST.get('text','')
        recommendations = self.get_rec(self.context)
        if text != recommendations.get(self.gname, {}).get('text', ''):
            recommendations.update(self.gname, text = text)
        if self.request.is_xhr:
            return {'success': True}
        return HTTPFound(location = self.request.resource_url(self.context.__parent__,
                                                              'group_recommendations',
                                                              query = {'group': self.gname}))

    def get_rec(self, proposal):
        return self.request.registry.getAdapter(proposal, IGroupRecommendations)

    @reify
    def groups(self):
        return self.request.meeting.get('groups', {})

    @reify
    def user_groups(self):
        return [x for x in self.groups.values() if self.request.authenticated_userid in x.members]

    @reify
    def gname(self):
        name = self.request.GET.get('group', '')
        if name:
            if name not in self.groups:
                raise HTTPBadRequest("No such group")
        else:
            return None
        if self.request.authenticated_userid not in self.groups[name].members:
            raise HTTPForbidden("You're not a member of that group")
        return name


@view_defaults(context = IProposal)
class ProposalGroupRecommendationView(BaseView):

    @view_config(name = '_recommendation_popover',
                 renderer = 'voteit.groups:templates/recommendation_popover.pt')
    def popover(self):
        recommendations = self.request.registry.getAdapter(self.context, IGroupRecommendations)
        return dict(recommendations = recommendations,
                    state_icons = _STATE_ICONS,
                    show_link = _in_any_group(self.request) or self.request.is_moderator,
                    rec_url = self.request.resource_url(self.context.__parent__, 'group_recommendations'))


def includeme(config):
    config.scan()
