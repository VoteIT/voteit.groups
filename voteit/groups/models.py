from zope.interface import implements
from zope.component import adapts
from betahaus.pyracont.decorators import content_factory
from BTrees.OOBTree import OOBTree
from repoze.folder import unicodify
from voteit.core import security
from voteit.core.models.base_content import BaseContent
from voteit.core.models.interfaces import IProposal

from voteit.groups import VoteITGroupsMF as _
from voteit.groups.interfaces import IGroup
from voteit.groups.interfaces import IGroups
from voteit.groups.interfaces import IGroupRecommendations


@content_factory('Groups', title=_(u"Groups"))
class Groups(BaseContent):
    """ Groups content type
        See :mod:`voteit.groups.interfaces.IGroups`.
        All methods are documented in the interface of this class.
    """
    implements(IGroups)
    content_type = 'Groups'
    display_name = _(u"Groups")
    allowed_contexts = ()
    add_permission = None

    def get_groups_for(self, userid):
        groups = []
        for obj in self.get_content(iface = IGroup, sort_on = 'title'):
            if userid in obj.get_field_value('members'):
                groups.append(obj)
        return tuple(groups)


@content_factory('Group', title=_(u"Group"))
class Group(BaseContent):
    """ Group content type.
        See :mod:`voteit.groups.interfaces.IGroup`.
        All methods are documented in the interface of this class.
    """
    implements(IGroup)
    content_type = 'Group'
    display_name = _(u"Group")
    allowed_contexts = ('Groups',)
    add_permission = '' #FIXME
    schemas = {'edit': 'EditGroupSchema'}
    custom_mutators = {'members': '_set_members'}

    def _set_members(self, value, key=None):
        self.field_storage['members'] = frozenset(value)


class GroupRecommendations(object):
    implements(IGroupRecommendations)
    adapts(IProposal)

    def __init__(self, context):
        self.context = context

    def get_group_data(self, group, default = None):
        storage = self.context.get_field_value('group_recommendations', default)
        if storage is default:
            return default
        #FIXME: Convert to dict to avoid accidental modification?
        return storage.get(group, default)

    def set_group_data(self, group, **kw):
        storage = self.context.get_field_value('group_recommendations', None)
        if storage is None:
            storage = OOBTree()
            self.context.set_field_value('group_recommendations', storage)
        storage[group] = OOBTree(kw)

    def get_other_group_data(self, group, default = None):
        storage = self.context.get_field_value('group_recommendations', default)
        if storage is default:
            return default
        result = {}
        for (gid, data) in storage.items():
            if gid == group:
                continue
            result[gid] = {}
            for (k, v) in data.items():
                result[gid][k] = v
        return result
