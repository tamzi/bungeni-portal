"""

some things we add on

 - custom events

 - state security manipulations
"""

import amara
import logging

import bungeni.core

from zope.dottedname.resolve import resolve
from ore.workflow.workflow import Workflow, Transition
from ore.workflow import interfaces
from zope.i18nmessageid import Message

trigger_value_map = {
    'manual':interfaces.MANUAL,
    'automatic':interfaces.AUTOMATIC,
    'system':interfaces.SYSTEM
    }

def load( uri ):
    print uri
    doc = parse( uri )
    
    return _load( doc.workflow )

def parse( uri ):
    doc = amara.parse( uri )
    return doc

def _load( workflow ):
    transitions = []

    domain = getattr( workflow, 'domain', None )
    
    for t in workflow.transition:
        try:
            args = ( t.id, Message( t.title, domain), t.source, t.destination )
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
        for i in('condition', 'action'):
            val = getattr( t,i,None)
            if not val:
                continue
            val = resolve( val, 'bungeni.core.workflows' ) # raises importerror/nameerror
            kw[i] = val
            
        transitions.append( Transition( *args, **kw ) )

    return Workflow( transitions )
        
if __name__ == '__main__':
    import sys
    workflow = load( sys.argv[1] )


    try:
        for t in workflow._id_transitions.values():
            print  t.transition_id, "|", t.source, "->", t.destination, t.permission, t.condition
    except:
       import pdb, traceback, sys
       traceback.print_exc()
       pdb.post_mortem(   sys.exc_info()[-1] ) 

