"""
Auditing of Changes for Domain Objects
"""
from datetime import datetime

from zope import interface
from zope.security.proxy import removeSecurityProxy
from zope.security.management import getInteraction
from zope.publisher.interfaces import IRequest

from zope import lifecycleevent

from ore.alchemist.interfaces import IRelationChange
from sqlalchemy import orm

import interfaces

import schema


from i18n import _ 

def getAuditor( ob ):
    auditor = globals()['%sAuditor'%(ob.__class__.__name__)]
    return auditor
    
def objectAdded( ob, event):
    auditor = getAuditor( ob )
    auditor.objectAdded( removeSecurityProxy(ob), event )
    
def objectModified( ob, event ):
    auditor = getAuditor( ob )  
    auditor.objectModified( removeSecurityProxy(ob), event )    
    
def objectDeleted( ob, event ):
    auditor = getAuditor( ob )    
    auditor.objectDeleted( removeSecurityProxy(ob), event )        

def objectNewVersion( ob, event ):
    auditor = getAuditor( ob )
    if not getattr( event, 'change_id', None):
        change_id = auditor.objectNewVersion( removeSecurityProxy(ob), event )
    else:
        change_id = event.change_id
    event.version.change_id = change_id
        
def objectRevertedVersion( ob, event ):
    # slightly obnoxious hand off between event handlers (objectnewV, objectrevertedV),
    # stuffing onto the event for value passing
    auditor = getAuditor( ob )
    change_id = auditor.objectRevertedVersion( removeSecurityProxy(ob), event )   
    event.change_id = change_id
    
class AuditorFactory( object ):

    def __init__( self, change_table ):
        self.change_table = change_table

    def objectAdded( self, object, event ):
        return self._objectChanged(u'added', object )
    
    def objectModified( self, object, event ):
        attrset =[]
        for attr in event.descriptions:
            if lifecycleevent.IAttributes.providedBy( attr ):
                attrset.extend(
                    [ attr.interface[a].title for a in attr.attributes]
                    )
            elif IRelationChange.providedBy(attr):
                attrset.append( attr.description )

        description = u", ".join( attrset )
        return self._objectChanged(u'modified', object, description )
        
    def objectDeleted( self, object, event ):
        return self._objectChanged(u'deleted', object )

    def objectNewVersion( self, object, event ):
        return self._objectChanged(u"new-version", object, description=event.message )

    def objectRevertedVersion( self, object, event ):
        return self._objectChanged(u'reverted-version', object, description=event.message )
        
    def _objectChanged( self, change_kind, object, description=u'' ):
        oid, otype = self._getKey( object )
        user_id = self._getCurrentUserId()

        statement = self.change_table.insert(
            values = dict( action = change_kind,
                           date = datetime.now(),
                           user_id = user_id,
                           description = description,
                           content_type = otype,
                           content_id = oid )
            )
        value = statement.execute()
        return value.last_inserted_ids()[0]
        
    def _getKey( self, ob ):
        mapper = orm.object_mapper( ob )
        primary_key = mapper.primary_key_from_instance( ob )[0]
        return primary_key, unicode( ob.__class__.__name__ )

    def _getCurrentUserId( self ):
        interaction = getInteraction()
        for participation in interaction.participations:
            if IRequest.providedBy(participation):
                return participation.principal.id
        raise RuntimeError(_("No IRequest in interaction"))    
        
BillAuditor = AuditorFactory( schema.bill_changes )        
MotionAuditor = AuditorFactory( schema.motion_changes )
QuestionAuditor = AuditorFactory( schema.question_changes )