from time import time
from Acquisition import aq_inner

from zope.interface import implements
from zope.component import getUtility
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from plone.memoize import ram
from plone.registry.interfaces import IRegistry

from collective.geo.geographer.interfaces import IGeoreferenced
from amap.mapview.interfaces import IInstitutionsMapView
from amap.mapview.institution import IInstitution


DESC_TEMPLATE = """<![CDATA[<div
class='user-description'
dir="ltr">%s</div>]]>
"""


class InstitutionsMapMixin(BrowserView):

    @property
    def portal_registry(self):
        return getUtility(IRegistry)

    @property
    def title(self):
        return self.context.Title()

    @property
    def description(self):
        return self.context.Description()


class InstitutionsMapView(InstitutionsMapMixin):
    """Kml Users Map View
    """
    implements(IInstitutionsMapView)

    def __init__(self, context, request):
        super(InstitutionsMapView, self).__init__(context, request)
        self.request.set('disable_border', True)


class InstitutionsMapKMLView(InstitutionsMapMixin):

    _user_properties = ['fullname', 'description']

    @property
    def description(self):
        return "<![CDATA[%s]]>" % self.context.Description()

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
            desc = r.Description
            mark['description'] = DESC_TEMPLATE % desc
            items.append(mark)
        return items

    def get_data(self, subject=None):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        query = dict(object_provides=IInstitution.__identifier__,
                     path=dict(query='/'.join(self.context.getPhysicalPath()),
                               depth=4),)
        if subject:
            query['Subject'] = subject
        results = catalog(**query)
        return results
