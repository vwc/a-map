import json
from Acquisition import aq_inner
from five import grok
from plone.directives import dexterity, form
from zope import schema
from plone.indexer.decorator import indexer
from plone.namedfile.interfaces import IImageScaleTraversable
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from collective.geo.geographer.interfaces import IGeoreferenced

from amap.mapview.vocabulary import color_codes

from amap.mapview import MessageFactory as _


marker_types = SimpleVocabulary(
    [SimpleTerm(value=u'seniors', title=_(u'Seniors')),
     SimpleTerm(value=u'sport', title=_(u'Sport')),
     SimpleTerm(value=u'education', title=_(u'Education and Job')),
     SimpleTerm(value=u'neighborhood', title=_(u"Neighborhood")),
     SimpleTerm(value=u'social', title=_(u"Social")),
     SimpleTerm(value=u'culture', title=_(u"Culture and Arts")),
     SimpleTerm(value=u'services', title=_(u"Services")),
     SimpleTerm(value=u'youth', title=_(u"Youth")),
     SimpleTerm(value=u'family', title=_(u"Family"))])


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
        vocabulary=marker_types,
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


class Institution(dexterity.Item):
    grok.implements(IInstitution)


class View(grok.View):
    grok.context(IInstitution)
    grok.require('zope2.View')
    grok.name('view')


class GeoJsonView(grok.View):
    grok.context(IInstitution)
    grok.require('zope2.View')
    grok.name('geojson-view')

    def render(self):
        self.request.response.setHeader('Content-Type',
                                        'application/json; charset=utf-8')
        return json.dumps(self.geojson_data(), indent=4)

    def geojson_data(self):
        context = aq_inner(self.context)
        markers = list()
        marker = {}
        geodata = IGeoreferenced(context)
        coords = geodata.coordinates
        geometry = {'coordinates': [coords[0], coords[1]]}
        marker_color = self.color_code(context.organizer)
        properties = {
            'marker-color': marker_color,
            'marker-symbol': 'circle',
            'image': '/++theme++amap.sitetheme/images/icon_hand.png',
            'title': context.Title(),
            'description': context.Description(),
            'url': context.absolute_url()
        }
        marker['type'] = 'Feature'
        marker['geometry'] = geometry
        marker['properties'] = properties
        markers.append(marker)
        geojson = {'type': 'FeatureCollection',
                   'features': markers}
        return geojson

    def color_code(self, key):
        vocabulary = color_codes()
        code = '#545454'
        if key is not None and vocabulary[key]:
            code = vocabulary[key]
        return code


@indexer(IInstitution)
def searchableIndexer(context):
    keywords = " ".join(context.keywords)
    return "%s %s %s" % (context.title, context.description, keywords)

grok.global_adapter(searchableIndexer, name="SearchableText")
