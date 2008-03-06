"""
$Id: $
"""

from zope.schema import vocabulary
from ore.alchemist.vocabulary import DatabaseSource, ObjectSource
from sqlalchemy.orm import mapper, relation, column_property

import sqlalchemy as rdb
import schema, domain


#ModelTypeSource = ObjectSource( model.DataModelType, 'short_name', 'id')
#SecurityLevelSource = DatabaseSource( model.SecurityLevel, 'short_name', 'id' )

#Constituency = ObjectSource( )
ParliamentMembers = ObjectSource( domain.ParliamentMember, 'name', 'member_id' )
PoliticalParties  = ObjectSource( domain.PoliticalParty, 'full_name', "id")
ParliamentSessions = ObjectSource( domain.ParliamentSession, 'short_name', 'session_id')
QuestionType = vocabulary.SimpleVocabulary.fromItems( [("(O)rdinary", "O"), ("(P)rivate Notice", "P")] )
Constituencies = ObjectSource( domain.Constituency, 'name', 'constituency_id')
Parliaments = ObjectSource( domain.Parliament, 'identifier', 'parliament_id')


SittingTypes = DatabaseSource( domain.SittingType, 'sitting_type', 'sitting_type_id' )    

                      
        
        
        
