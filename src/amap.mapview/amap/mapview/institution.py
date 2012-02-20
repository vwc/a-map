from five import grok
from plone.directives import dexterity, form

from zope.interface import Interface
from zope import schema
from plone.indexer.decorator import indexer


from z3c.form import field

from plone.namedfile.interfaces import IImageScaleTraversable

from z3c.form.interfaces import IDataConverter, NO_VALUE
from z3c.form.converter import BaseDataConverter
from zope.schema import getFieldsInOrder

from amap.mapview import MessageFactory as _

# from collective.z3cform.datagridfield import DictRow
# from collective.z3cform.datagridfield import DataGridFieldFactory, IDataGridField


class ITableRowSchema(form.Schema, Interface):
    one = schema.TextLine(title=u"Ansprechpartner", required=False)
    two = schema.TextLine(title=u"Strasse", required=False)
    three = schema.TextLine(title=u"Ort", required=False)
    four = schema.TextLine(title=u"Tel.", required=False)
    five = schema.TextLine(title=u"Fax", required=False)
    six = schema.TextLine(title=u"Email", required=False)


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


#    form.widget(contactdetails=DataGridFieldFactory)
#    contactdetails = schema.List(
#        title=_(u"Kontakt"),
#        value_type=DictRow(title=_(u"The tablerow"),
#                           schema=ITableRowSchema,
#                           )
#    )


class View(grok.View):
    grok.context(IInstitution)
    grok.require('zope2.View')
    grok.name('view')


class AddressList(list):
    pass


class Institution(dexterity.Item):
    grok.implements(IInstitution)


#class GridDataConverter(grok.MultiAdapter, BaseDataConverter):
    """Convert between the AddressList object and the widget. 
       If you are using objects, you must provide a custom converter
    """

#    grok.adapts(IDataGridField)
#    grok.implements(IDataConverter)

#    def toWidgetValue(self, value):
#        """Simply pass the data through with no change"""
#        rv = list()
#        for row in value:
#            d = dict()
#            for name, field in getFieldsInOrder(IInstitution):
#                d[name] = getattr(row, name)
#            rv.append(d)

#        return rv

#    def toFieldValue(self, value):
#        rv = AddressList()
#        for row in value:
#            d = dict()
#            for name, field in getFieldsInOrder(IInstitution):
#                if row.get(name, NO_VALUE) != NO_VALUE:
#                    d[name] = row.get(name)
#            rv.append(Institution(**d))

#        return rv



class EditForm(form.EditForm):

    grok.context(IInstitution)
    grok.require('zope2.View')
    fields = field.Fields(IInstitution)
    label=u"Demo Usage of DataGridField"

#    fields['contactdetails'].widgetFactory = DataGridFieldFactory
    
@indexer(IInstitution)
def searchableIndexer(context):
    keywords = " ".join(context.keywords)
    return "%s %s %s" % (context.title, context.description, keywords)

grok.global_adapter(searchableIndexer, name="SearchableText")
