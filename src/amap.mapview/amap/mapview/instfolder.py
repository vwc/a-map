from five import grok
from zope.component import getUtility
from plone.directives import dexterity, form
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.i18n.normalizer.interfaces import IIDNormalizer

from Products.CMFPlone.interfaces import IPloneSiteRoot

from collective.geo.geographer.interfaces import IGeoreferenced
from amap.mapview.interfaces import IMapViewLayer
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

    def result_listing(self):
        results = self.institutions()
        data = []
        for item in results:
            obj = item.getObject()
            geo = IGeoreferenced(obj)
            coords = geo.coordinates
            mark = {'location': '%s, %s, 0.000000' % (coords[0], coords[1])}
            mark['title'] = item.Title
            mark['description'] = item.Description
            data.append(mark)
        return data

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

    def keyword_normalizer(self, keyword):
        normalizer = getUtility(IIDNormalizer)
        css_class = 'keyword-%s' % normalizer.normalize(keyword)
        return css_class

    def get_data(self, subject=None):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        query = dict(object_provides=IInstitution.__identifier__,
                     path=dict(query='/'.join(self.context.getPhysicalPath()),
                               depth=1),)
        if subject:
            query['Subject'] = subject
        results = catalog(**query)
        return results


class MapKMLView(grok.View):
    grok.context(IPloneSiteRoot)
    grok.require('zope2.View')
    grok.layer(IMapViewLayer)
    grok.name('institutionmap.kml')

    def title(self):
        return '<![CDATA[%s]]>' % self.context.Title()

    def description(self):
        return '<![CDATA[%s]]>' % self.context.Description()

    def get_institutions(self):
        """ Retrieve all information on contained insitutions """
        results = self.get_data()
        items = []
        for r in results:
            obj = r.getObject()
            geo = IGeoreferenced(obj)
            coords = geo.coordinates
            mark = {'location': '%s, %s, 0.000000' % (coords[0], coords[1])}
            mark['name'] = r.Title
            mark['description'] = r.Description
            items.append(mark)
        return items

    def get_data(self, subject=None):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        query = dict(object_provides=IInstitution.__identifier__,
                     path=dict(query='/'.join(self.context.getPhysicalPath()),
                               depth=1),)
        if subject:
            query['Subject'] = subject
        results = catalog(**query)
        return results
