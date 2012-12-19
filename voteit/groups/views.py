import deform
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from betahaus.pyracont.factories import createSchema
from betahaus.pyracont.factories import createContent
from voteit.core.models.interfaces import ISiteRoot
from voteit.core.views.base_view import BaseView
from voteit.core import security

from voteit.groups.interfaces import IGroup
from voteit.groups.interfaces import IGroups
from voteit.groups import VoteITGroupsMF as _


@view_config(name="groups", context = ISiteRoot)
def create_groups_content(context, request):
    """ This view will only be called if there's no groups object. """
    from voteit.groups.models import Groups
    context['groups'] = Groups()
    return HTTPFound(location = request.resource_url(context['groups']))


class GroupsView(BaseView):
    #FIXME: Check permissions for all actions

    @view_config(context = IGroups, renderer = "templates/groups.pt", permission = security.VIEW)
    def view_groups(self):
        if self.api.show_moderator_actions:
            add_groups_schema = createSchema('AddGroupSchema').bind(context = self.context, request = self.request, api = self.api)
            add_groups_form = deform.Form(add_groups_schema, buttons = (deform.Button('add', _(u"Add")),))

        if 'add' in self.request.POST:
            controls = self.request.POST.items()
            try:
                appstruct = add_groups_form.validate(controls)
            except deform.ValidationFailure, e:
                self.response['add_groups_form'] = e.render()
                return self.response
            group = self.context[appstruct['name']] = createContent('Group', creators = [self.api.userid])
            url = self.request.resource_url(group, 'edit')
            return HTTPFound(location = url)

        self.response['add_groups_form'] = add_groups_form.render()
        return self.response


class GroupView(BaseView):
    
    @view_config(context = IGroup, renderer = "templates/group.pt", permission = security.VIEW)
    def view_group(self):
        #FIXME: remove once done?
        schema = createSchema('EditGroupSchema').bind(context = self.context, request = self.request, api = self.api)
        form = deform.Form(schema, buttons = ())
        appstruct = self.context.get_field_appstruct(schema)
        self.response['form'] = form.render(appstruct = appstruct, readonly = True)
        return self.response

