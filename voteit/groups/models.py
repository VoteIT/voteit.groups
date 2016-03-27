from UserDict import IterableUserDict

from pyramid.traversal import find_interface
from zope.interface import implementer
from zope.component import adapter
from BTrees.OOBTree import OOBTree
from voteit.core.models.base_content import BaseContent
from voteit.core.models.interfaces import IProposal
from voteit.core.models.interfaces import IMeeting

from voteit.groups import VoteITGroupsMF as _
from voteit.groups.interfaces import IGroup
from voteit.groups.interfaces import IGroups
from voteit.groups.interfaces import IGroupRecommendations
from voteit.groups.security import PERM_ADD_GROUP


@implementer(IGroups)
class Groups(BaseContent):
    """ Groups content type
        See :mod:`voteit.groups.interfaces.IGroups`.
        All methods are documented in the interface of this class.
    """
    title = _("Groups")
    type_name = 'VoteITGroups'
    type_title = _(u"Groups")
    add_permission = "Add %s" % type_name
    recommendation_visiblity = ""

    def get_groups_for(self, userid):
        groups = []
        for obj in self.get_content(iface = IGroup, sort_on = 'title'):
            if userid in obj.members:
                groups.append(obj)
        return groups


@implementer(IGroup)
class Group(BaseContent):
    """ Group content type.
        See :mod:`voteit.groups.interfaces.IGroup`.
        All methods are documented in the interface of this class.
    """
    type_name = 'VoteITGroup'
    type_title = _(u"Group")
    add_permission = PERM_ADD_GROUP
    custom_mutators = {'members': '_set_members'}
    naming_attr = 'uid'
    default_view = 'dynamic_view'

    @property
    def members(self):
        return self.get_field_value('members', ())
    @members.setter
    def members(self, value):
        self.field_storage['members'] = frozenset(value)

    def _set_members(self, value, key=None): #b/c compat "custom_mutators"
        self.members = value

    @property
    def hashtag(self):
        return self.get_field_value('hashtag', '')
    @hashtag.setter
    def hashtag(self, value):
        self.set_field_value('hashtag', value)


@implementer(IGroupRecommendations)
@adapter(IProposal)
class GroupRecommendations(IterableUserDict):

    def __init__(self, context):
        self.context = context

    @property
    def data(self):
        return self.context.get_field_value('group_recommendations', {})
    @data.setter
    def data(self, value):
        if not isinstance(value, OOBTree):
            value = OOBTree(value)
        self.context.set_field_value('group_recommendations', value)

    def update(self, key, **kwargs):
        if key not in self:
            self[key] = {}
        self.data[key].update(kwargs)

    def __setitem__(self, key, item):
        if not isinstance(self.data, OOBTree):
            self.data = OOBTree()
        self.data[key] = OOBTree(item)

    def group_title(self, group_name, request = None):
        if request and IMeeting.providedBy(request.meeting):
            meeting = request.meeting
        else:
            meeting = find_interface(self.context, IMeeting)
        groups = meeting.get('groups', {})
        group = groups.get(group_name, None)
        return group and group.title or group_name

    def count_states(self):
        results = {'comments': 0}
        for v in self.values():
            name = v.get('state', '')
            if name in results:
                results[name] += 1
            else:
                results[name] = 1
            if v.get('text', False):
                results['comments'] += 1
        return results

    def get_state_sorted(self):
        results = {}
        for (k, v) in self.items():
            state = v.get('state', '')
            if state not in results:
                results[state] = []
            results[state].append(k)
        return results

    def __nonzero__(self):
        """ Make sure empty adapters are treated as bool true
        """
        return True

    def __repr__(self): #pragma: no coverage
        klass = self.__class__
        classname = '%s.%s' % (klass.__module__, klass.__name__)
        return '<%s object with %s entries at %#x>' % (classname,
                                                       len(self),
                                                       id(self))


def includeme(config):
    config.registry.registerAdapter(GroupRecommendations)
    config.add_content_factory(Group, addable_to = 'VoteITGroups')
    config.add_content_factory(Groups)
