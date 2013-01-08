import re

import colander
import deform
from betahaus.pyracont.decorators import schema_factory
from pyramid.traversal import find_root

from voteit.core.validators import html_string_validator
from voteit.core.schemas.permissions import deferred_autocompleting_userid_widget
from voteit.core.validators import deferred_existing_userid_validator

from voteit.groups import VoteITGroupsMF as _

GROUP_REGEXP = r"[a-z]{1}[a-z0-9-_]{2,30}"
GROUP_PATTERN = re.compile(r'^'+GROUP_REGEXP+r'$')


@colander.deferred
def deferred_new_groupid_validator(node, kw):
    context = kw['context']
    return NewUniqueGroupID(context)


class NewUniqueGroupID(object):
    """ Check if GroupID is unique globally in the site and that GroupID conforms to correct standard. """
    
    def __init__(self, context):
        self.context = context

    def __call__(self, node, value):
        if not GROUP_PATTERN.match(value):
            msg = _('groupid_char_error',
                    default=u"GroupID must be 3-30 chars, start with lowercase a-z and only contain lowercase a-z, numbers, minus and underscore.")
            raise colander.Invalid(node, msg)
        root = find_root(self.context)
        if value in root['groups']:
            msg = _('groupid_already_registered_error',
                    default=u"GroupID already used, pick another!")
            raise colander.Invalid(node, msg)

            
@schema_factory('AddGroupSchema',
                title = _(u"Add group"),)
class AddGroupSchema(colander.Schema):
    name = colander.SchemaNode(colander.String(),
                               description = _(u"add_group_name_description",
                                               default = u"An id for the group, you can't change this later on. Must only contain a-z, 0-9"),
                               validator = deferred_new_groupid_validator,)


class MembersSequence(colander.SequenceSchema):
    userid = colander.SchemaNode(
        colander.String(),
        title = _(u"UserID"),
        validator=deferred_existing_userid_validator,
        widget = deferred_autocompleting_userid_widget,
    )


@schema_factory('EditGroupSchema',
                title = _(u"Group"),)
class EditGroupSchema(colander.Schema):
    title = colander.SchemaNode(colander.String())
    hashtag = colander.SchemaNode(colander.String()) #FIXME: uniqueness within other groups at least!
    members = MembersSequence()
