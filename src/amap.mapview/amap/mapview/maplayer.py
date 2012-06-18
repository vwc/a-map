from Acquisition import aq_inner
from plone.memoize.instance import memoizedproperty
from collective.geo.mapwidget.maplayers import MapLayer
from collective.geo.mapwidget.browser.widget import MapLayers


class KMLMapLayer(MapLayer):
    name = 'institutionmap'

    @memoizedproperty
    def jsfactory(self):
        context = aq_inner(self.context)
        title = context.Title().replace("'", "\'")
        if isinstance(title, str):
            title = title.decode('utf-8')
        plone_view = context.restrictedTraverse('plone_portal_state')
        plone_url = plone_view.portal_url()
        if not plone_url.endswith('/'):
            plone_url += '/'
        template = context.restrictedTraverse('%s-layer' % self.name)()
        return template % (title, plone_url)


class KMLMapLayers(MapLayers):
    """ Create custom map layers for the institutions map """

    def layers(self):
        layers = super(KMLMapLayers, self).layers()
        layers.append(KMLMapLayer(context=self.context))
        return layers
