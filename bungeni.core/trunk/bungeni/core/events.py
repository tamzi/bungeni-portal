#
# note that other events are handled in workflows
# audit and files!

from zope.security.proxy import removeSecurityProxy
from ore.alchemist import Session
from bungeni.core import audit


def consignatory_added(ob, event): 
    session = Session()
    ob = removeSecurityProxy(ob)
    if ob.user:
        title=  "%s %s %s" % (ob.user.titles,
                ob.user.first_name,
                ob.user.last_name)
    else:                
        title = ""        
    event.cls =  ob.__class__.__name__
    event.description = u" %s: %s added" % (
            ob.__class__.__name__ , 
            title)
    if ob.item:                        
        audit.objectContained( ob.item, event)

    
def consignatory_modified(ob, event):
    session = Session()
    ob = removeSecurityProxy(ob)
    if ob.user:
        title=  "%s %s %s" % (ob.user.titles,
                ob.user.first_name,
                ob.user.last_name)
    else:                
        title = ""        
    event.cls =  ob.__class__.__name__
    event.description = u" %s: %s modified" % (
            ob.__class__.__name__ , 
            title)
    if ob.item:                        
        audit.objectContained( ob.item, event)
