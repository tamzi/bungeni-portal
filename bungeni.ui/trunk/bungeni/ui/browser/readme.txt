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
   
   
      
         
         
   
