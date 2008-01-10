-------------
Bungeni Model
-------------

Setup
-----

some setup for tests

   >>> from zope import component
   >>> from sqlalchemy import create_engine
   >>> from ore.alchemist.interfaces import IDatabaseEngine
   >>> from ore.alchemist import Session
   >>> from bungeni import core as model

Setting up Database Connection and Utilities:

   >>> db = create_engine('postgres://localhost/bungeni', echo=False)
   >>> component.provideUtility( db, IDatabaseEngine, 'bungeni-db' )
   >>> model.metadata.bind = db   
   >>> session = Session()

Users
-----

First we can create some users.

  >>> user = model.User()
  >>>

Members of Parliament
---------------------

  >>> mp_1 = model.ParliamentMember()
  >>> mp_2 = model.ParliamentMember()
  >>> mp_3 = model.ParliamentMember()


Groups
------

  >>> parliament = model.Parliament()
  >>> political_party_a = model.PoliticalParty()
  >>> political_party_b = model.PoliticalParty()
  >>> comittee_a = model.Committee()

  >>> membership = model.GroupMembership( mp_1, political_party_a )

  >>> session.save( mp_1 )

  
Sittings
--------

any group can schedule a sitting, a sitting is treated as a physical
meeting of the group by the system. 


Questions
---------

  >>> question = model.Question()



 




