from five import grok
from plone.directives import dexterity, form

from zope import schema
from plone.indexer.decorator import indexer


from z3c.form import field

from plone.namedfile.interfaces import IImageScaleTraversable

from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from amap.mapview import MessageFactory as _


KEYWORD_VOCAB = SimpleVocabulary(
    [SimpleTerm(value=u'church', title=_(u'Kirche')),
     SimpleTerm(value=u'sport', title=_(u'Sport')),
     SimpleTerm(value=u'institution', title=_(u'Einrichtung'))]
    )


class IInstitution(form.Schema, IImageScaleTraversable):
    """
    single institution
    """

    title = schema.TextLine(
        title=u"Einrichtung",
    )
    description = schema.Text(
        title=u"Einleittext bei Kartenansicht",
        required=False,
    )
    summary = schema.Text(
        title=u"Aufgaben:",
        required=False,
    )
    job1 = schema.Text(
        title=u"Voraussetzungen zur Mitarbeit:",
        required=False,
    )
    job2 = schema.TextLine(
        title=u"Was du an Wochenstunden mitbringen solltest",
        required=False,
    )
    partner = schema.TextLine(
        title=u"Ansprechpartner:",
    )
    street = schema.TextLine(
        title=u"Strasse:",
    )
    organizer = schema.Choice(
            title=_(u"Art der Einrichtung"),
            vocabulary=KEYWORD_VOCAB,
    )
    location = schema.TextLine(
        title=u"Plz und Ort:",
    )
    phone = schema.TextLine(
        title=u"Tel.:",
        required=False,
    )
    fax = schema.TextLine(
        title=u"Fax:",
        required=False,
    )
    email = schema.TextLine(
        title=u"E-Mail:",
        required=False,
    )
    website = schema.TextLine(
        title=u"Website:",
        required=False,
    )


class View(grok.View):
    grok.context(IInstitution)
    grok.require('zope2.View')
    grok.name('view')


class AddressList(list):
    pass


class Institution(dexterity.Item):
    grok.implements(IInstitution)



class EditForm(form.EditForm):

    grok.context(IInstitution)
    grok.require('zope2.View')
    fields = field.Fields(IInstitution)
    label = u"Demo Usage of DataGridField"

#    fields['contactdetails'].widgetFactory = DataGridFieldFactory


@indexer(IInstitution)
def searchableIndexer(context):
    keywords = " ".join(context.keywords)
    return "%s %s %s" % (context.title, context.description, keywords)

grok.global_adapter(searchableIndexer, name="SearchableText")
