"""
$Id: $
"""
from zope.schema import vocabulary
from ore.alchemist.vocabulary import DatabaseSource, ObjectSource
from bungeni import core
import sqlalchemy as rdb
import schema
from sqlalchemy.orm import mapper, relation, column_property

#ModelTypeSource = ObjectSource( model.DataModelType, 'short_name', 'id')
#SecurityLevelSource = DatabaseSource( model.SecurityLevel, 'short_name', 'id' )

#Constituency = ObjectSource( )
ParliamentMembers = ObjectSource( core.ParliamentMember, 'name', 'member_id' )
PoliticalParties  = ObjectSource( core.PoliticalParty, 'full_name', "id")
ParliamentSessions = ObjectSource( core.ParliamentSession, 'short_name', 'session_id')
QuestionType = vocabulary.SimpleVocabulary.fromItems( [("(O)rdinary", "O"), ("(P)rivate Notice", "P")] )
Constituencies = ObjectSource( core.Constituency, 'name', 'constituency_id')
Parliaments = ObjectSource( core.Parliament, 'identifier', 'parliament_id')


    

                      
        
        
        
