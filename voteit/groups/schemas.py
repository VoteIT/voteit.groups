# import re
#
# import colander
# from betahaus.pyracont.decorators import schema_factory
# from pyramid.traversal import find_interface
# from voteit.core.schemas.permissions import deferred_autocompleting_userid_widget
# from voteit.core.validators import deferred_existing_userid_validator
# from voteit.core.models.interfaces import IMeeting
#
# from voteit.groups import VoteITGroupsMF as _
#
#
# GROUP_REGEXP = r"[a-z]{1}[a-z0-9-_]{2,30}"
# GROUP_PATTERN = re.compile(r'^'+GROUP_REGEXP+r'$')
#
#
# @colander.deferred
# def deferred_new_groupid_validator(node, kw):
#     context = kw['context']
#     return NewUniqueGroupID(context)
#
#
# class NewUniqueGroupID(object):
#     """ Check if GroupID is unique globally in the site and that GroupID conforms to correct standard. """
#
#     def __init__(self, context):
#         self.context = context
#
#     def __call__(self, node, value):
#         if not GROUP_PATTERN.match(value):
#             msg = _('groupid_char_error',
#                     default=u"GroupID must be 3-30 chars and only numbers, lowercase letters (a-z), minus and underscore.")
#             raise colander.Invalid(node, msg)
#         meeting = find_interface(self.context, IMeeting)
#         if value in meeting['groups']:
#             msg = _('groupid_already_registered_error',
#                     default=u"GroupID already used, pick another!")
#             raise colander.Invalid(node, msg)
#
#
# @schema_factory('AddGroupSchema',
#                 title = _(u"Add group"),)
# class AddGroupSchema(colander.Schema):
#     name = colander.SchemaNode(colander.String(),
#                                title = _(u"Name"),
#                                description = _(u"add_group_name_description",
#                                                default = u"An id for the group, you can't change this later on. OK chars are a-z, 0-9, minus and underscore."),
#                                validator = deferred_new_groupid_validator,)
#
#
# class MembersSequence(colander.SequenceSchema):
#     userid = colander.SchemaNode(
#         colander.String(),
#         title = _(u"UserID"),
#         validator=deferred_existing_userid_validator,
#         widget = deferred_autocompleting_userid_widget,
#     )
#
#
# @schema_factory('EditGroupSchema',
#                 title = _(u"Group"),)
# class EditGroupSchema(colander.Schema):
#     title = colander.SchemaNode(colander.String())
#     hashtag = colander.SchemaNode(colander.String()) #FIXME: uniqueness within other groups at least!
#     members = MembersSequence(title = _(u"Group members"))
#
