#

# Static navigation for bungeni demo

from zope.viewlet import viewlet
from zope.app.pagetemplate import ViewPageTemplateFile

class StaticViewletBungeniNavigation( viewlet.ViewletBase ):
    """
    just a static portlet to make the plone and zope parts play together
    for demo purposes
    """

    render = ViewPageTemplateFile( 'templates/static-bungeni-public-navtree.pt' )        
