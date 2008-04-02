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
   >>> from datetime import datetime

Setting up Database Connection and Utilities:

   >>> db = create_engine('postgres://localhost/bungeni', echo=False)
   >>> component.provideUtility( db, IDatabaseEngine, 'bungeni-db' )
   >>> model.metadata.bind = db   
   >>> session = Session()

Users
-----

First we can create some users.

  >>> user = model.User("jsmith")
  >>>

Members of Parliament
---------------------

  >>> mp_1 = model.ParliamentMember(u"mp_1", 
  ...        first_name=u"a", 
  ...        last_name=u'ab', 
  ...        email=u"mp1@example.com", 
  ...        date_of_birth=datetime.now(),
  ...        birth_country="SA",
  ...        gender='M')
  >>> mp_2 = model.ParliamentMember(u"mp_2", 
  ...        first_name=u"b", 
  ...        last_name=u"bc", 
  ...        date_of_birth=datetime.now(),
  ...        email=u"mp2@example.com",
  ...        gender='M')
  >>> mp_3 = model.ParliamentMember(u"mp_3",
  ...        first_name=u"c", 
  ...        last_name=u"cd",
  ...        date_of_birth=datetime.now(),
  ...        email=u"mp3@example.com", 
  ...        gender='M')

Groups
------

Bungeni uses groups to model any collection of users. The relational inheritance
features of sqlalchemy to allow for subclassing group, with value storage in a 
different table. Bungeni uses this feature to model parliaments, committees, 
political parties, etc. Let's create some groups in the system to examine how
they work.

  >>> parliament = model.Parliament( short_name=u"p_1", start_date=datetime.now())
  >>> political_party_a = model.PoliticalParty(short_name=u"pp_1", start_date=datetime.now())
  >>> political_party_b = model.PoliticalParty(short_name=u"pp_2", start_date=datetime.now())
  >>> committee_a = model.Committee(short_name=u"commitee_1", start_date=datetime.now())

A user is associated to a group via a membership, where we can store additional properties, such
as a user's role/title in a group.

Let's create some memberships and see what we can do with them.

  >>> for mp in [ mp_1, mp_2, mp_3 ]:
  ...    membership = model.GroupMembership()
  ...    membership.user = mp
  ...    membership.group = parliament
  ...    session.save( membership )
  ...    membership = model.GroupMembership()
  ...    membership.user = mp
  ...    membership.group = political_party_a
  ...    session.save( membership )
  
  >>> session.save( mp_1 )
  >>> session.save( committee_a )
  >>> session.save( membership )

Check that we can access the membership through the containment object

  >>> session.flush()
  >>> len( list( parliament.users.values() ) )
  3
  
Sittings
--------

any group can schedule a sitting, a sitting is treated as a physical
meeting of the group by the system. 


Motions
-------

Motions

Questions
---------

Note that the questions workflow is tested separated (see workflows/question.txt).

  >>> question = model.Question()

Assignment  
++++++++++  

assigning a question to a ministry

Bill
----
  >>> bill = model.Bill()

Rota Preparation
----------------
 




