from five import grok
from plone.directives import dexterity, form
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName

from plone.namedfile.interfaces import IImageScaleTraversable

from plone.app.contentlisting.interfaces import IContentListing

from amap.mapview.institution import IInstitution

from amap.mapview import MessageFactory as _


# Interface class; used to define content-type schema.

class IInstFolder(form.Schema, IImageScaleTraversable):
    """
    Folder for Institutions
    """


class InstFolder(dexterity.Container):
    grok.implements(IInstFolder)


class View(grok.View):
    grok.context(IInstFolder)
    grok.require('zope2.View')
    grok.name('view')

    def update(self):
        self.has_subitems = len(self.subitems()) > 0

    def institutions(self):
        subjects = self.request.get('subject', None)
        return self.get_data(subject=subjects)

    def subitems(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        results = catalog(object_provides=IInstitution.__identifier__,
                          path='/'.join(context.getPhysicalPath()),
                          sort_on='sortable_title')
        return results

    def keywords(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        subjects = catalog.uniqueValuesFor('Subject')
        #keywords = [unicode(k, 'utf-8') for k in keywords]
        return subjects

    def get_data(self, subject=None):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        obj_provides = IInstitution.__identifier__
        path = '/'.join(context.getPhysicalPath())
        query = dict(object_provides=IInstitution.__identifier__,
                     path=dict(query='/'.join(self.context.getPhysicalPath()),
                               depth=1),)
        if subject:
            query['Subject'] = subject
        results = catalog(**query)
        return results
