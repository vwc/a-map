from zope.interface import Interface

from plone.theme.interfaces import IDefaultPloneLayer


class IMapViewLayer(IDefaultPloneLayer):
    """ Marker interface defining a zope 3 browser layer """


class IInstitutionMapView(Interface):
    """ Custom layer for our instutution maps view """


class IInstitutionsMapView(Interface):
    """Marker interface for InstitutionsMapView
    """
