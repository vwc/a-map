from Acquisition import aq_inner, aq_parent

from zope.interface import implements
from zope.component import getUtility
from zope.component import getMultiAdapter
from zope.annotation.interfaces import IAnnotations
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from plone.memoize import instance
from plone.registry.interfaces import IRegistry

from plone.i18n.normalizer.interfaces import IIDNormalizer
from collective.geo.geographer.interfaces import IGeoreferenced
from amap.mapview.interfaces import IInstitutionsMapView
from amap.mapview.instfolder import IInstFolder
from amap.mapview.institution import IInstitution


DESC_TEMPLATE = """<![CDATA[<div
class='user-description'
dir="ltr">%s</div>]]>
"""
KEY = 'amap.mapview.filters'


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

    def filter_params(self):
        annotations = IAnnotations(self.request)
        value = annotations.get(KEY, None)
        if value is None:
            annotations[KEY] = self.request.get('subject')
        else:
            annotations[KEY] = value

    def wrapped_view(self):
        context = aq_inner(self.context)
        return self.get_base_view(context, self.request, 'institutionmap_view')

    def wrapped_view_parent(self):
        context = aq_inner(self.context)
        base_view = self.get_base_view(context, self.request,
                    'institutionmap_view')
        return base_view.__parent__

    def get_base_view(self, context, request, name):
        context = aq_inner(context)
        view = getMultiAdapter((context, request), name=name)
        view = view.__of__(context)
        return view


class InstitutionsMapView(InstitutionsMapMixin):
    """Kml Users Map View
    """
    implements(IInstitutionsMapView)

    def __init__(self, context, request):
        super(InstitutionsMapView, self).__init__(context, request)
        self.filter = self.request.get('subject', None)
        self.base_context = aq_inner(self.context)
        self.request.set('disable_border', True)

    def placemarks(self):
        annotations = IAnnotations(self.request)
        filter_by = annotations[KEY]
        return self._get_placemarks(subject=filter_by)

    def _get_placemarks(self, subject=None):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        base_view = self.wrapped_view()
        view_context = aq_inner(base_view)
        canonical = getattr(base_view, '__parent__', None)
        #base_path = '/'.join.getPhysicalPath(self.base_context())
        query = dict(object_provides=IInstitution.__identifier__,
                     path=dict(query='/'.join(self.context.getPhysicalPath()),
                               depth=1),)
        if subject:
            query['Subject'] = subject
        results = catalog(**query)
        import pdb; pdb.set_trace( )
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


class InstitutionsMapKMLView(InstitutionsMapMixin):

    _user_properties = ['fullname', 'description']

    def __call__(self):
        return super(InstitutionsMapKMLView, self).__call__()

    @property
    def description(self):
        return "<![CDATA[%s]]>" % self.context.Description()

    def get_institutions(self):
        """ Retrieve all information on contained insitutions """
        base_view = self.wrapped_view()
        results = base_view.placemarks()
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
