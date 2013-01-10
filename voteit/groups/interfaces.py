from zope.interface import Interface


class IGroups(Interface):
    """ Folder that contains all Group objects. """


class IGroup(Interface):
    """ A group content type. """


class IGroupRecommendations(Interface):
    """ Adapter that handles proposal recommendations from a specific group. """

    def get_group_data(group, default = None):
        """ Get current group data. Returns an OOBTree object. """

    def set_group_data(group, **kw):
        """ Store group data. """

    def get_other_group_data(group, default = None):
        """ Return a copy of all other groups data, except the one specified.
            Nope that the actual value of the data isn't a copy. """
