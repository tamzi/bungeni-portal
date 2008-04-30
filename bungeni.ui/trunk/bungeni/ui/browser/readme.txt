Setup
-----

some setup for tests

   >>> from zope import component
   >>> from sqlalchemy import create_engine
   >>> from ore.alchemist.interfaces import IDatabaseEngine
   >>> from ore.alchemist import Session
   >>> from bungeni import core as model
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
   
   >>> parliament = model.Parliament( short_name=u"p_1", start_date=today, election_date=yesterday, end_date=tomorrow)  
   >>> session.save( parliament)
   >>> session.flush()
   
   >>> parliament.parliament_id 
   1L
   
   >>> from bungeni.ui.browser import validations
   >>> validations.checkDateInInterval( None, yesterday, validations.sql_checkParliamentInterval)
   
   >>> validations.checkDateInInterval( None, today, validations.sql_checkParliamentInterval)
   'p_1'

   >>> validations.checkDateInInterval( None, tomorrow, validations.sql_checkParliamentInterval)
   'p_1'

   >>> validations.checkDateInInterval( None, dayat, validations.sql_checkParliamentInterval)   
   
   
Before you can add a new parliament all others must be closed
   
   >>> validations.checkDateInInterval( None, dayat, validations.sql_checkForOpenParliamentInterval)      
   
Add a new (open ended) parliament
   >>> parliament = model.Parliament( short_name=u"p_2", start_date=tomorrow, election_date=today, end_date=None)  
   >>> session.save( parliament)
   >>> session.flush()   
   
Note that the date yesterday is well ouside our p_2 so it does not matter.   
   >>> validations.checkDateInInterval( None, yesterday, validations.sql_checkForOpenParliamentInterval)
   'p_2'
   
Add a governmemt:

   >>> gov = model.Government(short_name=u"gov_1", start_date=today, end_date=tomorrow )
   >>> gov.parliament_id = parliament.parliament_id  
   >>> session.save( gov )
   >>> session.flush() 
 
   >>> validations.checkDateInInterval( parliament.parliament_id, yesterday, validations.sql_checkGovernmentInterval)
   
   >>> validations.checkDateInInterval( parliament.parliament_id, today, validations.sql_checkGovernmentInterval)
   'gov_1'

   >>> validations.checkDateInInterval( parliament.parliament_id, tomorrow, validations.sql_checkGovernmentInterval)
   'gov_1'

   >>> validations.checkDateInInterval( parliament.parliament_id, dayat, validations.sql_checkGovernmentInterval)       
      

Sessions
-----------
A parliamentary Session

   >>> sess = model.ParliamentSession()
   >>> sess.parliament_id = parliament.parliament_id
   >>> sess.short_name = u"First Session"
   >>> sess.start_date = today
   >>> sess.end_date = tomorrow
   >>> session.save(sess)
   >>> session.flush() 
 
   >>> sess.session_id
   1L
 
   >>> validations.checkDateInInterval( parliament.parliament_id, yesterday, validations.sql_checkSessionInterval)
   
   >>> validations.checkDateInInterval( parliament.parliament_id, today, validations.sql_checkSessionInterval)
   'First Session'

   >>> validations.checkDateInInterval( parliament.parliament_id, tomorrow, validations.sql_checkSessionInterval)
   'First Session'

   >>> validations.checkDateInInterval( parliament.parliament_id, dayat, validations.sql_checkSessionInterval) 
 
 
Sittings
---------
 
    >>> ssit = model.GroupSitting()
    >>> ssit.session_id = sess.session_id
    >>> ssit.start_date = today
    >>> ssit.end_date = tomorrow
    >>> session.save(ssit)
    >>> session.flush()    

Just check if we get something back because the return value depends on the times

   >>> validations.checkDateInInterval( sess.session_id, yesterday, validations.sql_checkSittingInterval) == None
   True
   
   >>> validations.checkDateInInterval( sess.session_id, today, validations.sql_checkSittingInterval) == None
   False

   >>> validations.checkDateInInterval( sess.session_id, tomorrow, validations.sql_checkSittingInterval) == None
   False

   >>> validations.checkDateInInterval( sess.session_id, dayat, validations.sql_checkSittingInterval) 

      
clean up commit open transactions
   >>> session.flush()   
         
         
   
