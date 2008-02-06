"""
Auditing of Changes for Domain Objects
"""
from datetime import datetime

from zope import component, interface, schema
from zope.security.proxy import removeSecurityProxy
from zope.security.management import checkPermission, getInteraction
from zope.publisher.interfaces import IRequest

from zope import lifecycleevent

from ore.alchemist import Session
from ore.alchemist.interfaces import IRelationChange
from sqlalchemy import orm

import interfaces
import sqlalchemy as rdb

import schema

def objectAdded( ob, event):
    auditor = globals()['%sAuditor'%(ob.__class__.__name__)]
    auditor.objectAdded( removeSecurityProxy(ob), event )
    
def objectModified( ob, event ):
    auditor = globals()['%sAuditor'%(ob.__class__.__name__)]
    auditor.objectModified( removeSecurityProxy(ob), event )    
    
def objectDeleted( ob, event ):
    auditor = globals()['%sAuditor'%(ob.__class__.__name__)]
    auditor.objectDeleted( removeSecurityProxy(ob), event )        

class AuditorFactory( object ):

    def __init__( self, change_table ):
        self.change_table = change_table

    def objectAdded( self, object, event ):
        self._objectChanged(u'added', object )
    
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
        self._objectChanged(u'modified', object, description )
        
    def objectDeleted( self, object, event ):
        self._objectChanged(u'deleted', object )

    def _objectChanged( self, change_kind, object, description=u'' ):
        oid, otype = self._getKey( object )
        user_name = self._getCurrentUserName()

        self.change_table.insert(
            values = dict( action = change_kind,
                           date = datetime.now(),
                           user_name = user_name,
                           description = description,
                           content_type = otype,
                           content_id = oid )
            ).execute()
        
    def _getKey( self, ob ):
        mapper = orm.object_mapper( ob )
        primary_key = mapper.primary_key_from_instance( ob )[0]
        return primary_key, unicode( ob.__class__.__name__ )

    def _getCurrentUserName( self ):
        interaction = getInteraction()
        for participation in interaction.participations:
            if IRequest.providedBy(participation):
                return participation.principal.title
        raise RuntimeError(_("No IRequest in interaction"))    
        
BillAuditor = AuditorFactory( schema.bill_changes )        
MotionAuditor = AuditorFactory( schema.motion_changes )
QuestionAuditor = AuditorFactory( schema.question_changes )