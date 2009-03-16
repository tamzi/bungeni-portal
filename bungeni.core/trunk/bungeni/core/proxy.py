import zope.interface

from zope.proxy import ProxyBase, getProxiedObject, non_overridable
from zope.proxy.decorator import DecoratorSpecificationDescriptor
from zope.security.checker import getCheckerForInstancesOf
from zope.location.interfaces import ILocation

class ClassAndInstanceDescr(object):

    def __init__(self, *args):
        self.funcs = args

    def __get__(self, inst, cls):
        if inst is None:
            return self.funcs[1](cls)
        return self.funcs[0](inst)

class LocationProxy(ProxyBase):
    """Location-object proxy

    This is a non-picklable proxy that can be put around objects that
    don't implement `ILocation`.
    """

    zope.interface.implements(ILocation)

    __slots__ = '__parent__', '__name__'
    __safe_for_unpickling__ = True

    def __new__(self, ob, container=None, name=None):
        checker = getCheckerForInstancesOf(type(ob))
        ob = ProxyBase.__new__(self, ob)
        ob.__Security_checker__ = checker
        return ob

    def __init__(self, ob, container=None, name=None):
        ProxyBase.__init__(self, ob)
        self.__parent__ = container
        self.__name__ = name

    @non_overridable
    def __reduce__(self, proto=None):
        raise TypeError("Not picklable")

    __doc__ = ClassAndInstanceDescr(
        lambda inst: getProxiedObject(inst).__doc__,
        lambda cls, __doc__ = __doc__: __doc__,
        )

    __reduce_ex__ = __reduce__

    __providedBy__ = DecoratorSpecificationDescriptor()

