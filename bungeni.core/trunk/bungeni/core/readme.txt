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

   >>> from sqlalchemy.orm import mapper
   >>> from bungeni.core import domain, schema

   
   
Setting up Database Connection and Utilities:

   >>> db = create_engine('postgres://localhost/bungeni-test', echo=False)
   >>> component.provideUtility( db, IDatabaseEngine, 'bungeni-db' )
   >>> model.metadata.bind = db   
   >>> model.metadata.create_all() 
   >>> session = Session()

region, country, province
--------------------------
get some values in those tables as they are needed later on

 >>> country = model.Country()
 >>> country.country_id = 'KE'
 >>> country.country_name = u"Kenya"
 >>> session.save(country)
 >>> session.flush()
 >>> country.country_id
 'KE'
 >>> country.country_name
 u'Kenya'

Regions and provinces get their primary key with a db sequence:
 
 >>> region = model.Region()
 >>> region.region = u"Nairobi"
 >>> session.save(region)
 >>> session.flush() 
 >>> region.region_id
 1L
 >>> province = model.Province()
 >>> province.province= u"Central"
 >>> session.save(province)
 >>> session.flush()
 >>> province.province_id
 1L

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
  ...        birth_country="KE",
  ...        email=u"mp1@example.com", 
  ...        date_of_birth=datetime.now(),
  ...        gender='M')
  >>> mp_2 = model.ParliamentMember(u"mp_2", 
  ...        first_name=u"b", 
  ...        last_name=u"bc", 
  ...        birth_country="KE",  
  ...        date_of_birth=datetime.now(),
  ...        email=u"mp2@example.com",
  ...        gender='M')
  >>> mp_3 = model.ParliamentMember(u"mp_3",
  ...        first_name=u"c", 
  ...        birth_country="KE",  
  ...        last_name=u"cd",
  ...        date_of_birth=datetime.now(),
  ...        email=u"mp3@example.com", 
  ...        gender='F')

Groups
------

Bungeni uses groups to model any collection of users. The relational inheritance
features of sqlalchemy to allow for subclassing group, with value storage in a 
different table. Bungeni uses this feature to model parliaments, committees, 
political parties, etc. Let's create some groups in the system to examine how
they work.

  >>> parliament = model.Parliament( short_name=u"p_1", start_date=datetime.now(), election_date=datetime.now())
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

Government
----------
  >>> gov = model.Government(short_name=u"gov_1", start_date=datetime.now())
  >>> gov.parliament_id = parliament.parliament_id
  >>> session.save(gov)
  >>> session.flush()  


Constituencies
-----------------
Constituencies have a fk on regions and provinces:

 >>> constituency = model.Constituency()
 >>> constituency.name = u"Nairobi/Westlands"
 >>> constituency.region = 1
 >>> constituency.province = 1
 >>> constituency.start_date = datetime.now()

 >>> session.save(constituency)
 >>> session.flush()
 
check the pk if it was saved and pk sequence is working

 >>> constituency.constituency_id
 1L
 

 

Role title names

  >>> mrt1 = model.MemberTitle()
  >>> mrt1.user_type = 'memberofparliament'   
  >>> mrt1.user_role_name = u"President"
  >>> mrt1.user_unique = True
  >>> mrt1.sort_order = 10
  >>> session.save(mrt1)
  >>> session.flush()
    
 
Members of parliament
----------------------
Members of parliament are defined by their membership in
the parliaments group and additional attributes.

  >>> mp4 = model.MemberOfParliament()
  >>> mp4.group_id = parliament.group_id
  >>> mp4.user_id = mp_1.user_id
  >>> mp4.start_date = datetime.now()
  >>> mp4.constituency_id = 1
  >>> mp4.elected_nominated = 'E'
  >>> session.save(mp4)
  >>> session.flush()   
  >>> mp4.membership_id
  7L            

Titles of Members
------------------
Members have a title in their groups

  >>> mt1 = model.MemberRoleTitle()
  >>> mt1.membership_id = mp4.membership_id
  >>> mt1.title_name_id = 1
  >>> mt1.start_date = datetime.now()
  >>> mt1.title_name_id = mrt1.user_role_type_id   
  >>> session.save(mt1)
      
  
Sittings
--------

any group can schedule a sitting, a sitting is treated as a physical
meeting of the group by the system. 

 >>> st = model.SittingType()
 >>> st.sitting_type = u"morning"
 >>> session.save(st)
 >>> session.flush()
 
 >>> st.sitting_type_id
 1L
 

 >>> sit = model.GroupSitting()
 >>> sit.group_id = committee_a.group_id
 >>> sit.start_date = datetime.now()
 >>> sit.end_date = datetime.now()
 >>> sit.sitting_type = st.sitting_type_id
 >>> session.save(sit)
 >>> session.flush() 

Sitting attendance
-------------------

the attendance of a member at a sitting.

 >>> at = model.AttendanceType()
 >>> at.attendance_type = u"present"
 >>> session.save(at)
 >>> session.flush()  
 
 >>> gsa = model.GroupSittingAttendance()
 >>> gsa.sitting_id = sit.sitting_id
 >>> gsa.member_id = mp_1.user_id
 >>> gsa.attendance_id = at.attendance_id
 >>> session.save(gsa)
 >>> session.flush() 
 
Sessions
-----------
A parliamentary Session

 >>> sess = model.ParliamentSession()
 >>> sess.parliament_id = parliament.parliament_id
 >>> sess.short_name = u"First Session"
 >>> sess.start_date = datetime.now()
 >>> sess.end_date = datetime.now()
 >>> session.save(sess)
 >>> session.flush() 
 
 >>> sess.session_id
 1L
 
Sitting in this session 
 
 >>> ssit = model.GroupSitting()
 >>> ssit.session_id = sess.session_id
 >>> ssit.start_date = datetime.now()
 >>> ssit.end_date = datetime.now()
 >>> ssit.sitting_type = st.sitting_type_id
 >>> session.save(ssit)
 >>> session.flush() 
 
Attendance

 >>> sgsa = model.GroupSittingAttendance()
 >>> sgsa.sitting_id = ssit.sitting_id
 >>> sgsa.member_id = mp_1.user_id
 >>> sgsa.attendance_id = at.attendance_id
 >>> session.save(sgsa)
 >>> session.flush() 

Motions
-------
  >>> motion = model.Motion()

Motions

Questions
---------

Note that the questions workflow is tested separated (see workflows/question.txt).

  >>> question = model.Question()
  
  >>> session.save(question)
  >>> session.flush()
  
  >>> question.question_id
  1L
  
Responses
---------
  >>> response = model.Response()
  >>> response.question_id = question.question_id
  >>> session.save(response)
  >>> session.flush()
 
  >>> response.question_id
  1L
  
  >>> response.response_id
  1L
  
Assignment  
++++++++++  

assigning a question to a ministry

Bill
----
  >>> bill = model.Bill()

Rota Preparation
----------------
 
Debates
--------------

 >>> debate = model.Debate()
 >>> debate.short_name=u'Debate'
 >>> debate.sitting_id = ssit.sitting_id
 >>> session.save(debate)
 >>> session.flush()

Clean up commit outstanding transactions
-----------------------------------------
 >>> session.flush() 
 

 




