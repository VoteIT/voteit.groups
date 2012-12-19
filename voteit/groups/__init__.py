from pyramid.i18n import TranslationStringFactory

PROJECTNAME = 'voteit.groups'
VoteITGroupsMF = TranslationStringFactory(PROJECTNAME)


def includeme(config):
    config.scan(PROJECTNAME)
