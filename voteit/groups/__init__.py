from pyramid.i18n import TranslationStringFactory

from .interfaces import IGroupRecommendations

PROJECTNAME = 'voteit.groups'
VoteITGroupsMF = TranslationStringFactory(PROJECTNAME)


def includeme(config):
    from .models import GroupRecommendations
    config.scan(PROJECTNAME)
    config.registry.registerAdapter(GroupRecommendations)
