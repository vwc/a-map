from five import grok
from plone.directives import dexterity, form
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName

from zope import schema
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from zope.interface import invariant, Invalid

from z3c.form import group, field

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile

from plone.app.textfield import RichText

from plone.app.contentlisting.interfaces import IContentListing
from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder

from amap.mapview.institution import IInstitution

from amap.mapview import MessageFactory as _


# Interface class; used to define content-type schema.

class IInstFolder(form.Schema, IImageScaleTraversable):
    """
    Folder for Institutions
    """
    
    # If you want a schema-defined interface, delete the form.model
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/instfolder.xml to define the content type
    # and add directives here as necessary.
    
    form.model("models/instfolder.xml")


# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class InstFolder(dexterity.Container):
    grok.implements(IInstFolder)
    
    # Add your class methods and properties here


# View class
# The view will automatically use a similarly named template in
# instfolder_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class View(grok.View):
    grok.context(IInstFolder)
    grok.require('zope2.View')
    grok.name('view')

    def hasSubitems(self):
        return len(self.subitems()) > 0

    def subitems(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        results = catalog(object_provides=IInstitution.__identifier__,
                          path= '/'.join(context.getPhysicalPath()),
                          sort_on='sortable_title')
        return results

    def keywords(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        folder_path = '/'.join(context.getPhysicalPath())
        keywords = context.portal_catalog.searchResults(searchableText = 'welcome')
        #keywords = [unicode(k, 'utf-8') for k in keywords]
        return keywords
    
    def archive_url(self, subject):
        # Get the path of where the portlet is created. That's the blog.
        assignment_context = find_assignment_context(self.data, self.context)
        self.folder_url = assignment_context.absolute_url()
        return '%s/%s?category=%s' % (self.folder_url,
                                      self.data.archive_view,
                                      subject)
