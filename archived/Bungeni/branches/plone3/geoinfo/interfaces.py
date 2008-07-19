# -*- coding: utf-8 -*-

from zope.interface import Interface

##code-section HEAD
##/code-section HEAD

class IRegion(Interface):
    """Marker interface for .Region.Region
    """

class IConstituency(Interface):
    """Marker interface for .Constituency.Constituency
    """

class IRegions(Interface):
    """Marker interface for .Regions.Regions
    """

class IProvince(Interface):
    """Marker interface for .Province.Province
    """

##code-section FOOT
##/code-section FOOT