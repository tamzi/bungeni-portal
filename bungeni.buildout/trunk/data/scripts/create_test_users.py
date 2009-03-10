from zope import component
from sqlalchemy import create_engine
from ore.alchemist.interfaces import IDatabaseEngine
#from ore.alchemist import Session
from bungeni import models as model
from datetime import datetime

import zope.securitypolicy.interfaces

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import mapper

from alchemist.security.role import GlobalPrincipalRoleMap

from bungeni.models import domain, schema, orm
from bungeni.models import interfaces
from bungeni.models import metadata

from zope.configuration import xmlconfig
   
zcml_slug = """
<configure xmlns="http://namespaces.zope.org/zope"
           xmlns:db="http://namespaces.objectrealms.net/rdb">

  <include package="ore.alchemist" file="meta.zcml"/>
  <include package="alchemist.catalyst" file="meta.zcml"/>

  <!-- Setup Database Connection -->
  <db:engine
     name="bungeni-db"
     url="postgres://localhost/bungeni"
     />
     
  <db:bind
     engine="bungeni-db"
     metadata="bungeni.models.metadata" />

  <db:bind
     engine="bungeni-db"
     metadata="alchemist.security.metadata" />     

  <!-- Setup Core Model --> 
  <include package="bungeni.ui" file="catalyst.zcml"/>
 
</configure>
"""
    
xmlconfig.string( zcml_slug )
metadata.create_all( checkfirst=True )
   
#Setting up Database Connection and Utilities:

db = create_engine('postgres://localhost/bungeni', echo=False)

Session = sessionmaker(bind=db)
session = Session()

# create some users for testing


mp = domain.ParliamentMember()
mp.login = "member" 
mp.first_name=u"Test"
mp.last_name=u'Member' 
mp.birth_country="KE"
mp.email=u"mp1@example.com"
mp.date_of_birth=datetime.now()
mp.gender='M'
mp.user_id=4990

clerk = model.StaffMember(login = "clerk",
         first_name=u"Test", 
         last_name=u'Clerk', 
         birth_country="KE",
         email=u"clerk@example.com", 
         date_of_birth=datetime.now(),
         user_id=4991,
         gender='M')

speaker  = model.StaffMember(login = "speaker",
         first_name=u"Test", 
         last_name=u'Speaker', 
         birth_country="KE",
         email=u"clerk@example.com", 
         date_of_birth=datetime.now(),
         user_id=4992,
         gender='M') 

mp.setPassword(u"member")
clerk.setPassword(u"clerk")
speaker.setPassword(u"speaker")
 

         
session.save(mp)
session.save(clerk)
session.save(speaker)
session.flush()

global_prm = GlobalPrincipalRoleMap(None)
global_prm.assignRoleToPrincipal( u'bungeni.MP', mp.login)
global_prm.assignRoleToPrincipal( u'bungeni.Clerk', clerk.login)
global_prm.assignRoleToPrincipal( u'bungeni.Speaker', speaker.login)


session.commit()
session.close()
         
