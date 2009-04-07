# this module will be populated by ``alchemist.catalyst``

from zope import component
from zope import interface
from zope.location.interfaces import ILocation
from zope.publisher.browser import BrowserView
from zope.app.publisher.browser import queryDefaultViewName
from zope.security.checker import getCheckerForInstancesOf
from zope.security.checker import defineChecker
from zope.proxy import sameProxiedObjects

from ore.alchemist import Session
from ore.alchemist.container import contained
from ore.alchemist.container import stringKey

from bungeni.core.proxy import LocationProxy
from bungeni.models import domain

class ProxyView(BrowserView):
    """Proxy-view.

    Queries for an alternative context and renders the default view of
    this object.
    """

    def __new__(cls, context, request):
        new_context = cls.get_context(context)
        assert not sameProxiedObjects(new_context, context)
        
        # look up default view for the current parliament
        default_view_name = queryDefaultViewName(new_context, request)
        view = component.getMultiAdapter(
            (new_context, request), name=default_view_name)

        # create custom view class which combines these two views
        view_cls = type(view)
        cls = type(view_cls.__name__, (cls, view_cls), dict(view_cls.__dict__))

        # share attributes
        new_view = object.__new__(cls, new_context, request)
        new_view.__dict__ = view.__dict__

        # set up view security
        checker = getCheckerForInstancesOf(view_cls)
        defineChecker(cls, checker)

        return new_view

    def __init__(self, context, request):
        pass

    @classmethod
    def get_context(cls, context):
        raise NotImplementedError("Must be implemented by subclass.")
            
class CurrentParliamentView(ProxyView):
    @classmethod
    def get_context(cls, context):
        return context['current']
