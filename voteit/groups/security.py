from voteit.core import security

from voteit.groups import _


PERM_ADD_GROUP = "Add VoteITGroup"

RECOMMENDATION_VISIBILITY = (
    ('any', _("Any")),
    ('members', _("Members of any group")),
    ('moderators', _("Only moderators")),
)

def allow_access(request):
    if request.is_moderator:
        return True
    if hasattr(request, '_groups_cached_access'):
        return request._groups_cached_access
    groups = request.meeting.get('groups', {})
    if not groups:
        request._groups_cached_access = False
        return request._groups_cached_access
    if groups.recommendation_visiblity == 'members':
        request._groups_cached_access = bool([x for x in groups.values() if request.authenticated_userid in x.members])
    elif groups.recommendation_visiblity == 'any':
        request._groups_cached_access = True
    else:
        request._groups_cached_access = False
    return request._groups_cached_access

def includeme(config):
    meeting_default_acl = config.registry.acl['Meeting:default']
    meeting_default_acl.add(security.ROLE_ADMIN, PERM_ADD_GROUP)
    meeting_closed_acl = config.registry.acl['Meeting:closed']
    meeting_closed_acl.add(security.ROLE_ADMIN, PERM_ADD_GROUP)
