"""
$Id: $
"""

from ore.alchemist.vocabulary import DatabaseSource, ObjectSource
from bungeni import core
 
#ModelTypeSource = ObjectSource( model.DataModelType, 'short_name', 'id')
#SecurityLevelSource = DatabaseSource( model.SecurityLevel, 'short_name', 'id' )

#Constituency = ObjectSource( )
ParliamentMembers = ObjectSource( core.ParliamentMember, 'name', 'member_id' )
PoliticalParties  = ObjectSource( core.PoliticalParty, 'full_name', "id")
ParliamentSessions = ObjectSource( core.ParliamentSession, 'short_name', 'session_id')


                             
                      
        
        
        
