from pyramid.i18n import TranslationStringFactory

from .interfaces import IGroupRecommendations

PROJECTNAME = 'voteit.groups'
VoteITGroupsMF = TranslationStringFactory(PROJECTNAME)


def includeme(config):
    return
    #FIXME: Refactor package - it's currently not compatible with VoteIT
    from .models import GroupRecommendations
    config.scan(PROJECTNAME)
    config.registry.registerAdapter(GroupRecommendations)
    config.add_translation_dirs('%s:locale' % PROJECTNAME)
