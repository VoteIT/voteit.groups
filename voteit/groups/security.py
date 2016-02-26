from arche.security import Role
from voteit.core import security
from voteit.core.models.interfaces import IMeeting


PERM_ADD_GROUP = "Add VoteITGroup"
#PERM_ADD_RECOMMENDATION = "Add recommendation"


# ROLE_RECOMMEND = Role('role:Recommend',
#                       title = _("Recommend"),
#                       inheritable = True,
#                       assignable = True,
#                       required = IMeeting)


def includeme(config):
    #config.register_roles(ROLE_RECOMMEND)
    meeting_default_acl = config.registry.acl['Meeting:default']
    meeting_default_acl.add(security.ROLE_ADMIN, PERM_ADD_GROUP)
    #meeting_default_acl.add(ROLE_RECOMMEND, PERM_ADD_RECOMMENDATION)
