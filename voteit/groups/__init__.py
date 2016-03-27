from pyramid.i18n import TranslationStringFactory

PROJECTNAME = 'voteit.groups'
_ = VoteITGroupsMF = TranslationStringFactory(PROJECTNAME)


def includeme(config):
    config.add_translation_dirs('%s:locale' % PROJECTNAME)
    config.include('.models')
    config.include('.schemas')
    config.include('.views')
    config.include('.security')
