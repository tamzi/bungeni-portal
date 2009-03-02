Setup
-----

some setup for tests

   >>> from zope import component
   >>> from sqlalchemy import create_engine
   >>> from ore.alchemist.interfaces import IDatabaseEngine
   >>> from ore.alchemist import Session
   >>> from bungeni import models as model
   >>> import datetime

Setting up Database Connection and Utilities:

   >>> db = create_engine('postgres://localhost/bungeni-test', echo=False)
   >>> component.provideUtility( db, IDatabaseEngine, 'bungeni-db' )
   >>> model.metadata.bind = db   
   >>> model.metadata.create_all() 
   >>> session = Session()
   
Get some standard dates for testing   
   >>> today = datetime.date.today()
   >>> yesterday = today - datetime.timedelta(1)
   >>> tomorrow = today + datetime.timedelta(1)
   >>> dayat = today + datetime.timedelta(2)
   
   >>> 
   
Note that we only test the overlap of 'peers' here.
refer to test_dates.py to test  that contained objects are inside
their parents dates   
   
Parliaments
-----------   
   
   >>> parliament = model.Parliament( short_name=u"p_1", start_date=today, election_date=yesterday, end_date=tomorrow)  
   >>> session.save( parliament)
   >>> session.flush()
   
   >>> parliament.parliament_id 
   1L
   
   >>> from bungeni.ui.forms import validations
   >>> import bungeni.ui.queries.sqlvalidation as sql
   >>> validations.checkDateInInterval( None, yesterday, sql.checkParliamentInterval)
   
   >>> validations.checkDateInInterval( None, today, sql.checkParliamentInterval)
   'p_1'

   >>> validations.checkDateInInterval( None, tomorrow, sql.checkParliamentInterval)
   'p_1'

   >>> validations.checkDateInInterval( None, dayat, sql.checkParliamentInterval)   
   
   
Before you can add a new parliament all others must be closed
   
   >>> validations.checkDateInInterval( None, dayat, sql.checkForOpenParliamentInterval)      
   
Add a new (open ended) parliament
   >>> parliament2 = model.Parliament( short_name=u"p_2", start_date=tomorrow, election_date=today, end_date=None)  
   >>> session.save( parliament2)
   >>> session.flush()   
   
Note that the date yesterday is well ouside our p_2 so it does not matter.   
   >>> validations.checkDateInInterval( None, yesterday, sql.checkForOpenParliamentInterval)
   'p_2'
 
give the 2nd parliament an end date and save   
   >>> parliament2.end_date = dayat   
   >>> session.flush() 
   
No open parliaments  anymore 
   >>> validations.checkDateInInterval( None, today, sql.checkForOpenParliamentInterval)
   
Now check for overlapping dates but not for the current (edited) parliament   
   
   >>> validations.checkDateInInterval( parliament2.parliament_id , today, sql.checkMyParliamentInterval)   
   'p_1'
   
   >>> validations.checkDateInInterval( parliament2.parliament_id , dayat, sql.checkMyParliamentInterval)  
   
   >>> validations.checkDateInInterval( parliament.parliament_id , dayat, sql.checkMyParliamentInterval)   
   'p_2'
   
   >>> validations.checkDateInInterval( parliament.parliament_id , yesterday, sql.checkMyParliamentInterval) 
   
   >>> validations.checkDateInInterval( parliament.parliament_id , today, sql.checkMyParliamentInterval)    
   
Add a governmemt:

   >>> gov = model.Government(short_name=u"gov_1", start_date=today, end_date=tomorrow )
   >>> gov.parliament_id = parliament.parliament_id  
   >>> session.save( gov )
   >>> session.flush() 
 
   >>> validations.checkDateInInterval( parliament.parliament_id, yesterday, sql.checkGovernmentInterval)
   
   >>> validations.checkDateInInterval( parliament.parliament_id, today, sql.checkGovernmentInterval)
   'gov_1'

   >>> validations.checkDateInInterval( parliament.parliament_id, tomorrow, sql.checkGovernmentInterval)
   'gov_1'

   >>> validations.checkDateInInterval( parliament.parliament_id, dayat, sql.checkGovernmentInterval)       
      
Add a second government

   >>> gov2 = model.Government(short_name=u"gov_2", start_date=tomorrow, end_date=dayat )
   >>> gov2.parliament_id = parliament.parliament_id  
   >>> session.save( gov2 )
   >>> session.flush()       

   >>> validations.checkDateInInterval( gov2.government_id, yesterday, sql.checkMyGovernmentInterval)
   
   >>> validations.checkDateInInterval( gov.government_id, yesterday, sql.checkMyGovernmentInterval)
   
   >>> validations.checkDateInInterval( gov.government_id, today, sql.checkMyGovernmentInterval)

   >>> validations.checkDateInInterval( gov2.government_id, dayat, sql.checkMyGovernmentInterval)      

   >>> validations.checkDateInInterval( gov.government_id, dayat, sql.checkMyGovernmentInterval)
   'gov_2'

   >>> validations.checkDateInInterval( gov2.government_id, today, sql.checkMyGovernmentInterval)   
   'gov_1'


Sessions
-----------
A parliamentary Session

   >>> sess = model.ParliamentSession()
   >>> sess.parliament_id = parliament.parliament_id
   >>> sess.short_name = u"First Session"
   >>> sess.start_date = yesterday
   >>> sess.end_date = today
   >>> session.save(sess)
   >>> session.flush() 
 
   >>> sess.session_id
   1L
 
   >>> validations.checkDateInInterval( parliament.parliament_id, yesterday, sql.checkSessionInterval)
   'First Session'
      
   >>> validations.checkDateInInterval( parliament.parliament_id, today, sql.checkSessionInterval)
   'First Session'

   >>> validations.checkDateInInterval( parliament.parliament_id, tomorrow, sql.checkSessionInterval)


   >>> validations.checkDateInInterval( parliament.parliament_id, dayat, sql.checkSessionInterval) 
 
A second session
 
   >>> sess2 = model.ParliamentSession()
   >>> sess2.parliament_id = parliament.parliament_id
   >>> sess2.short_name = u"2nd Session"
   >>> sess2.start_date = tomorrow
   >>> sess2.end_date = dayat
   >>> session.save(sess2)
   >>> session.flush()  
 
   >>> validations.checkDateInInterval( sess.session_id, yesterday, sql.checkMySessionInterval) 

   >>> validations.checkDateInInterval( sess.session_id, today, sql.checkMySessionInterval) 
   
   >>> validations.checkDateInInterval( sess.session_id, dayat, sql.checkMySessionInterval)     
   '2nd Session'
   
   >>> validations.checkDateInInterval( sess.session_id, tomorrow, sql.checkMySessionInterval)     
   '2nd Session'   
   
   >>> validations.checkDateInInterval( sess2.session_id, yesterday, sql.checkMySessionInterval) 
   'First Session'
   
   >>> validations.checkDateInInterval( sess2.session_id, today, sql.checkMySessionInterval)  
   'First Session'
            
   >>> validations.checkDateInInterval( sess2.session_id, tomorrow, sql.checkMySessionInterval)              
   
   >>> validations.checkDateInInterval( sess2.session_id, dayat, sql.checkMySessionInterval)   
 
Sittings
---------
 
    >>> ssit = model.GroupSitting()
    >>> ssit.session_id = sess.session_id
    >>> ssit.start_date = today
    >>> ssit.end_date = tomorrow
    >>> session.save(ssit)
    >>> session.flush()    

Just check if we get something back because the return value depends on the times

    >>> validations.checkDateInInterval( sess.session_id, yesterday, sql.checkSittingSessionInterval) == None
    True
   
    >>> validations.checkDateInInterval( sess.session_id, today, sql.checkSittingSessionInterval) == None
    False

    >>> validations.checkDateInInterval( sess.session_id, tomorrow, sql.checkSittingSessionInterval) == None
    False

    >>> validations.checkDateInInterval( sess.session_id, dayat, sql.checkSittingSessionInterval) 
   
   
For Edit we need to be sure we do not check for the current data itself.
   
    >>> ssit2 = model.GroupSitting()
    >>> ssit2.session_id = sess.session_id
    >>> ssit2.start_date = yesterday
    >>> ssit2.end_date = today
    >>> session.save(ssit2)
    >>> session.flush()    
   
Just a quick check that the above validation for yesterday now fails   

    >>> validations.checkDateInInterval( sess.session_id, yesterday, sql.checkSittingSessionInterval) == None
    False

and the real check
            
    >>> validations.checkDateInInterval( ssit2.sitting_id, yesterday, sql.checkMySittingSessionInterval) == None
    True
   
    >>> validations.checkDateInInterval( ssit2.sitting_id, today, sql.checkMySittingSessionInterval) == None
    False

    >>> validations.checkDateInInterval( ssit2.sitting_id, tomorrow, sql.checkMySittingSessionInterval) == None
    False

    >>> validations.checkDateInInterval( ssit2.sitting_id, dayat, sql.checkMySittingSessionInterval)

Parliament members
Regions and provinces get their primary key with a db sequence:
 
 >>> region = model.Region()
 >>> region.region = u"Nairobi"
 >>> session.save(region)
 >>> session.flush() 

 >>> province = model.Province()
 >>> province.province= u"Central"
 >>> session.save(province)
 >>> session.flush()

 >>> constituency = model.Constituency()
 >>> constituency.name = u"Nairobi/Westlands"
 >>> constituency.region = 1
 >>> constituency.province = 1
 >>> constituency.start_date = today

 >>> session.save(constituency)
 >>> session.flush()

add some users:
    >>> mp_1 = model.ParliamentMember(u"mp_1", 
    ...        first_name=u"a", 
    ...        last_name=u'ab', 
    ...        email=u"mp1@example.com", 
    ...        date_of_birth=today,
    ...        gender='M')
    >>> mp_2 = model.ParliamentMember(u"mp_2", 
    ...        first_name=u"b", 
    ...        last_name=u"bc", 
    ...        date_of_birth=today,
    ...        email=u"mp2@example.com",
    ...        gender='M')
    >>> session.save(mp_1)
    >>> session.save(mp_2)
    >>> session.flush()
    
    >>> mp1 = model.MemberOfParliament()
    >>> mp1.group_id = parliament.group_id
    >>> mp1.user_id = mp_1.user_id
    >>> mp1.start_date = today
    >>> mp1.constituency_id = 1
    >>> mp1.elected_nominated = "E"
    >>> session.save(mp1)
    >>> session.flush()
    
    >>> mp2 = model.MemberOfParliament()
    >>> mp2.group_id = parliament.group_id
    >>> mp2.user_id = mp_2.user_id
    >>> mp2.start_date = today
    >>> mp2.constituency_id = 1
    >>> mp2.elected_nominated = "N"
    >>> session.save(mp2)
    >>> session.flush()

titles     
--------------

    >>> mrt1 = model.MemberTitle()
    >>> mrt1.user_type = 'memberofparliament'   
    >>> mrt1.user_role_name = u"President"
    >>> mrt1.user_unique = True
    >>> mrt1.sort_order = 10
    >>> session.save(mrt1)
    >>> session.flush()
    
    >>> mrt2 = model.MemberTitle()
    >>> mrt2.user_type = 'memberofparliament'   
    >>> mrt2.user_role_name = u"Member"
    >>> mrt2.user_unique = False
    >>> mrt2.sort_order = 20
    >>> session.save(mrt2)
    >>> session.flush()
    
    
    
    >>> mt1 = model.MemberRoleTitle()
    >>> mt1.membership_id = mp1.membership_id
    >>> mt1.title_name_id = mrt1.user_role_type_id
    >>> mt1.start_date = today
    >>> mt1.title_name_id = mrt1.user_role_type_id   
    >>> session.save(mt1)
    >>> session.flush()

A (group) member can only hold the same title once at a time
-------------------------------------------------------------

    >>> validations.checkBySQL(sql.checkMemberTitleDuplicates, { 'title_name_id' : mt1.title_name_id , 'membership_id' : mt1.membership_id , 'date' : today})
    'President'

    >>> mt1.end_date = tomorrow
    >>> session.flush()    
    >>> validations.checkBySQL(sql.checkMemberTitleDuplicates, { 'title_name_id' : mt1.title_name_id , 'membership_id' : mt1.membership_id , 'date' : dayat})
    
    >>> validations.checkBySQL(sql.checkMemberTitleDuplicates, { 'title_name_id' : mt1.title_name_id , 'membership_id' : mt1.membership_id , 'date' : today})    
    'President'
    
    >>> validations.checkBySQL(sql.checkMemberTitleDuplicates, { 'title_name_id' : mrt2.user_role_type_id , 'membership_id' : mt1.membership_id , 'date' : today})

exclude data with role_title_id when editing the record

    >>> validations.checkBySQL(sql.checkMyMemberTitleDuplicates, { 'title_name_id' : mt1.title_name_id , 'membership_id' : mt1.membership_id , 'date' : today, 'role_title_id' : mt1.role_title_id})    

    >>> validations.checkBySQL(sql.checkMyMemberTitleUnique, { 'title_name_id' : mt1.title_name_id , 'group_id' : parliament.group_id , 'date' : today, 'role_title_id' : mt1.role_title_id})    


Some titles must be unique inside a group
-----------------------------------------
    
    >>> mt2 = model.MemberRoleTitle()
    >>> mt2.membership_id = mp1.membership_id
    >>> mt2.title_name_id = mrt2.user_role_type_id
    >>> mt2.start_date = today
    >>> session.save(mt2)
    >>> session.flush()     
   
second check for same title at a time
    >>> validations.checkBySQL(sql.checkMemberTitleDuplicates, { 'title_name_id' : mt2.title_name_id , 'membership_id' : mt2.membership_id , 'date' : today})   
    'Member'

A president is allready there   
    >>> validations.checkBySQL(sql.checkMemberTitleUnique, { 'title_name_id' : mt1.title_name_id , 'group_id' : parliament.group_id , 'date' : today})    
    'President'

Members do not have to be unique    
    >>> validations.checkBySQL(sql.checkMemberTitleUnique, { 'title_name_id' : mt2.title_name_id , 'group_id' : parliament.group_id , 'date' : today})        

And the day after tomorrow there is no more president
    >>> validations.checkBySQL(sql.checkMemberTitleUnique, { 'title_name_id' : mt1.title_name_id , 'group_id' : parliament.group_id , 'date' : dayat})    

when editing exclude self
    >>> validations.checkBySQL(sql.checkMyMemberTitleDuplicates, { 'title_name_id' : mt2.title_name_id , 'membership_id' : mt2.membership_id , 'date' : today, 'role_title_id' : mt2.role_title_id})    
    
    >>> validations.checkBySQL(sql.checkMyMemberTitleUnique, { 'title_name_id' : mt1.title_name_id , 'group_id' : parliament.group_id , 'date' : today, 'role_title_id' : mt2.role_title_id})        
    'President'


Membership in a political group      
---------------------------   


      
      
clean up - commit open transactions
---------------------------------

   >>> session.flush()   
         
         
   
