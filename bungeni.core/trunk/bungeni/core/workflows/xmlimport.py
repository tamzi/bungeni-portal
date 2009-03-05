"""
Support for xml defined workflows, and security manipulations by state.
"""

import amara

from zope.dottedname.resolve import resolve
from zope.i18nmessageid import Message

from bungeni.core.workflows.states import GRANT
from bungeni.core.workflows.states import DENY
from bungeni.core.workflows.states import State
from bungeni.core.workflows.states import StateTransition
from bungeni.core.workflows.states import StateWorkflow

from ore.workflow import interfaces

trigger_value_map = {
    'manual':interfaces.MANUAL,
    'automatic':interfaces.AUTOMATIC,
    'system':interfaces.SYSTEM
    }

def load( uri ):
    #print uri
    doc = parse( uri )
    
    return _load( doc.workflow )

def parse( uri ):
    doc = amara.parse( uri )
    return doc

def _load( workflow ):
    transitions = []
    states = []
    domain = getattr( workflow, 'domain', None )

    for s in getattr( workflow, 'state', ()):
        permissions = []
        for g in getattr( s, 'grant', () ):
            permissions.append(
                ( GRANT, g.permission, g.role )
                )
        for d in getattr( s, 'deny', () ):
            permissions.append(
                (DENY, d.permission, d.role )
                )
        state_id  = s.id #=  resolve( s.id , 'bungeni.core.workflows' )       
        states.append( State( state_id, Message(s.title, domain), permissions ) )
    
    for t in workflow.transition:
        try:
            source = t.source and t.source or None
            if source:
                tsource = source #resolve( source , 'bungeni.core.workflows' )  
            else:
                tsource = None       
            tdestination = t.destination #resolve( t.destination , 'bungeni.core.workflows' )         
            args = ( t.id, Message( t.title, domain), tsource, tdestination )
            kw = {}
        except AttributeError:
            raise SyntaxError( t.toxml() )

        # optionals
        for i in ('trigger', 'order', 'permission'):
            val = getattr( t,i,None )
            if not val:
                continue
            kw[i] = val

        if 'trigger' in kw:
            k = kw['trigger']
            v = trigger_value_map[ k ]
            kw['trigger'] = v

        # optional python resolvables
        for i in('condition', 'action', 'event'):
            val = getattr( t,i,None)
            if not val:
                continue
            val = resolve( val , 'bungeni.core.workflows' ) # raises importerror/nameerror
            kw[i] = val
        transitions.append( StateTransition( *args, **kw ) )

    return StateWorkflow( transitions, states )


