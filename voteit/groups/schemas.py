import colander
from arche.schemas import userid_hinder_widget
from arche.schemas import existing_userids

from voteit.groups import VoteITGroupsMF as _


class MembersSequence(colander.SequenceSchema):
    userid = colander.SchemaNode(
        colander.String(),
        title = _(u"UserID"),
        validator = existing_userids,
        widget = userid_hinder_widget,)


class GroupSchema(colander.Schema):
    title = colander.SchemaNode(colander.String())
    hashtag = colander.SchemaNode(colander.String(),
                                  missing = "") #FIXME: uniqueness within other groups at least!
    members = MembersSequence(title = _(u"Group members"))


def includeme(config):
    config.add_content_schema('VoteITGroup', GroupSchema, ('add', 'edit', 'view'))
