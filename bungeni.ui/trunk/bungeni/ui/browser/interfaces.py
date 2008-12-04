from zope.viewlet.interfaces import IViewletManager

class ISubFormViewletManager( IViewletManager ):
    """
    Manager for subform viewlets
    """    

class IResponeQuestionViewletManager( IViewletManager ):
    """
    Manager for question in reponseform
    """    
        
class IAtomFormViewletManager( IViewletManager ):
    """
    Manager for main content in atom view
    """    
    
class IAtomEntriesFormViewletManager( IViewletManager ):
    """
    Manager for related content in atom view
    """        
