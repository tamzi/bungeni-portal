
from zope.viewlet import viewlet
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.security.proxy import removeSecurityProxy
from zope import interface

from alchemist.traversal.managed import ManagedContainerDescriptor
from ore.alchemist.interfaces import IAlchemistContainer, IAlchemistContent

class ConstraintNavigation( viewlet.ViewletBase ):
    """
    for alchemist content not containers
    """
    
    template = ViewPageTemplateFile('contained-constraint-navigation.pt')
    
    def render( self ):
        return self.template()
        
    def constraints( self ):

        assert IAlchemistContent.providedBy( self.context)

        context_class = self.context.__class__
        context_class = removeSecurityProxy( context_class )    
        
        for k, v in context_class.__dict__.items():
            if isinstance( v, ManagedContainerDescriptor ):
                i = { 'name' : v.domain_container._class.__name__,
                      'url'  : k }
                yield i
