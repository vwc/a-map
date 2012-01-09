from five import grok
from plone.directives import dexterity, form

from zope.interface import Interface, Invalid
from zope import schema
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from zope.interface import invariant, Invalid

from z3c.form import group, field

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile

from plone.app.textfield import RichText

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder

from amap.mapview import MessageFactory as _

from collective.z3cform.datagridfield import DataGridFieldFactory, DictRow

# Interface class; used to define content-type schema.

class ITableRowSchema(form.Schema, Interface):
    one = schema.TextLine(title=u"Ansprechpartner")
    two = schema.TextLine(title=u"Strasse")
    three = schema.TextLine(title=u"sontiges")

                                 
class IInstitution(form.Schema, IImageScaleTraversable):
    """
    single institution
    """

    form.widget(table=DataGridFieldFactory) 
 
    table = schema.List(title=_(u"My Table"), value_type=DictRow(title=_(u"The tablerow"), schema=ITableRowSchema))   

    form.model("models/institution.xml")


class Institution(dexterity.Item):
    grok.implements(IInstitution)
    
    # Add your class methods and properties here


class SampleView(grok.View):
    grok.context(IInstitution)
    grok.require('zope2.View')
    fields = field.Fields(IInstitution)
    fields['table'].widgetFactory = DataGridFieldFactory
    
    #grok.name('view')