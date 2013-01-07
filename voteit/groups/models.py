from zope.interface import implements
from zope.component import adapts
from betahaus.pyracont.decorators import content_factory
from BTrees.OOBTree import OOBTree
from repoze.folder import unicodify
from voteit.core import security
from voteit.core.models.base_content import BaseContent

from voteit.groups import VoteITGroupsMF as _
from voteit.groups.interfaces import IGroup
from voteit.groups.interfaces import IGroups


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
