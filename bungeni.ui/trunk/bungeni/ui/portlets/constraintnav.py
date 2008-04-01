
from zope.viewlet import viewlet
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.security.proxy import removeSecurityProxy

from alchemist.traversal.managed import ManagedContainerDescriptor
from ore.alchemist.model import queryModelDescriptor
from ore.alchemist.interfaces import  IAlchemistContent

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
        
        items =[]
        for k, v in context_class.__dict__.items():
            if isinstance( v, ManagedContainerDescriptor ):
                domain_model = v.domain_container._class 
                descriptor = queryModelDescriptor( domain_model )
                if descriptor:
                    name = getattr( descriptor, 'display_name', None)
                if not name:
                    name = domain_model.__name__
                    
                i = { 'name' : name,
                      'url'  : k }
                items.append( i )
        return items
