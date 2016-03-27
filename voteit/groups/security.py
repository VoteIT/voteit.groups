from voteit.core import security

from voteit.groups import _


PERM_ADD_GROUP = "Add VoteITGroup"

def includeme(config):
    meeting_default_acl = config.registry.acl['Meeting:default']
    meeting_default_acl.add(security.ROLE_ADMIN, PERM_ADD_GROUP)
    meeting_closed_acl = config.registry.acl['Meeting:closed']
    meeting_closed_acl.add(security.ROLE_ADMIN, PERM_ADD_GROUP)
