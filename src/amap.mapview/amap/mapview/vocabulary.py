from five import grok
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.schema.interfaces import IVocabularyFactory

from amap.mapview import MessageFactory as _

COLOR_CODES = {'seniors': u'#4a5f21',
               'sport': u'#910f1e',
               'education': u'#97be0d',
               'neighborhood': u"#584e98",
               'social': u"#f8b334",
               'culture': u"#92117e",
               'services': u"#dd0b1a",
               'youth': u"#025e5c",
               'family': u"#dd6aa2"}


class InstitutionTypeVocabulary(object):
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
        TYPES = {_(u'Seniors'): 'seniors',
                 _(u'Sport'): 'sport',
                 _(u'Education and Job'): 'education',
                 _(u"Neighborhood"): 'neighborhood',
                 _(u"Social"): 'social',
                 _(u"Culture and Arts"): 'culture',
                 _(u"Services"): 'services',
                 _(u"Youth"): 'youth',
                 _(u"Family"): 'family'}

        return SimpleVocabulary([SimpleTerm(value, title=title)
                                 for title, value in TYPES.itertypes()])

grok.global_utility(InstitutionTypeVocabulary,
                    name=u"amap.mapview.InstitutionTypes")


def color_codes():
    codes = dict({'seniors': u'#4a5f21',
                  'sport': u'#910f1e',
                  'education': u'#97be0d',
                  'neighborhood': u"#584e98",
                  'social': u"#f8b334",
                  'culture': u"#92117e",
                  'services': u"#dd0b1a",
                  'youth': u"#025e5c",
                  'family': u"#dd6aa2"})
    return codes
