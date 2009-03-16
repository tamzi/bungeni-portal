"""
$Id: $
"""

import os
from os import path

from zope import interface

from zope.app.component import site
from zope.app.container.sample import SampleContainer

from ore.wsgiapp.app import Application
from ore.svn import repos
from ore.library.library import Library

from bungeni.models import domain
from bungeni.models import interfaces
from bungeni.core import location

_container_name_mapping = location.model_to_container_name_mapping

class BungeniApp( Application ):

    interface.implements( interfaces.IBungeniApplication )

class BungeniAdmin( SampleContainer ):

    interface.implements( interfaces.IBungeniAdmin  )
    
def setUpSubscriber( object, event ):
    initializer = interfaces.IBungeniSetup( object )
    initializer.setUp()

class AppSetup( object ):

    interface.implements( interfaces.IBungeniSetup )

    def __init__( self, context ):
        self.context = context
        
    def setUp( self ):
        
        import index
        # ensure indexing facilities are setup ( lazy )
        index.setupFieldDefinitions(index.indexer)        

        # ensure version file are setup
        import files
        files.setup()
        
        sm = site.LocalSiteManager( self.context )
        self.context.setSiteManager( sm )

        # domain objects
        #governments = domain.GovernmentContainer()
        #self.context['governments'] = governments
        
        parliaments = domain.ParliamentContainer()
        self.context[_container_name_mapping[domain.Parliament]] = parliaments
        
        #committees = domain.CommitteeContainer()
        #self.context['committees'] = committees
        
        bills = domain.BillContainer()
        self.context[_container_name_mapping[domain.Bill]] = bills
        
        motions = domain.MotionContainer()
        self.context[_container_name_mapping[domain.Motion]] = motions

        questions = domain.QuestionContainer()
        self.context[_container_name_mapping[domain.Question]] = questions
        
        #tableddocuments = domain.TabledDocumentContainer()        
        #self.context['tableddocuments'] = tableddocuments
        
        #documentsources = domain.DocumentSourceContainer() 
        #self.context['documentsources'] = documentsources    
        
        agendaitems = domain.AgendaItemContainer()
        self.context[_container_name_mapping[domain.AgendaItem]] = agendaitems

        users = domain.UserContainer()
        self.context[_container_name_mapping[domain.User]] = users

        mps = domain.ParliamentMemberContainer()
        self.context[_container_name_mapping[domain.ParliamentMember]] = mps
        
        staff_members = domain.StaffMemberContainer()
        self.context[_container_name_mapping[domain.StaffMember]] = staff_members
        
        #groups = domain.GroupContainer()       
        #self.context['groups'] = groups
        
        constituency = domain.ConstituencyContainer()
        self.context[_container_name_mapping[domain.Constituency]] = constituency
        
        provinces = domain.ProvinceContainer()
        self.context[_container_name_mapping[domain.Province]] = provinces
        
        regions = domain.RegionContainer()
        self.context[_container_name_mapping[domain.Region]] = regions

        #ministries = domain.MinistryContainer()
        #self.context['ministries'] = ministries
        
        #parties = domain.PoliticalPartyContainer()
        #self.context['politicalparties'] = parties

        sessions = domain.ParliamentSessionContainer()
        self.context[_container_name_mapping[domain.ParliamentSession]] = sessions
        
        countries = domain.CountryContainer()
        self.context[_container_name_mapping[domain.Country]] = countries


        self.context['repository'] = Library( repository_storage )

        ##########
        # Admin User Interface
        self.context['admin'] = admin = BungeniAdmin()
        
        #admin['users'] = admin_user = domain.UserContainer()
        #interface.directlyProvides( admin_user, interfaces.IAdminUserContainer )
        #admin['groups'] = domain.GroupContainer()
        
        ##########
        
        #titles = domain.MemberTitleContainer()
        #self.context('titles') = titles
        
        # todo separate out to url module
        #url.setupResolver( self.context )
        # 
        # provide a url resolver for object urls
        
        ######### does this cause the multiadapter error? ########
        
        #url_resolver = url.AbsoluteURLFactory( self.context )
        #sm.registerAdapter( factory=url_resolver, 
        #                    required=(IAlchemistContent, IHTTPRequest), 
        #                    provided=IAbsoluteURL, name="absolute_url")
                           
        #sm.registerAdapter( factory=url_resolver, 
        #                    required=(IAlchemistContent, IHTTPRequest),
        #                    provided=IAbsoluteURL )

# we store files in buildout/parts/repository
# 
def setupStorageDirectory( ):
    # we start in buildout/src/bungeni.core/bungeni/core
    # we end in buildout/parts/repository    
    store_dir = __file__
    x = 0
    while x < 5:
        x += 1
        store_dir = path.split( store_dir )[0]

    store_dir = path.join( store_dir, 'parts', 'repository')
    if path.exists( store_dir ):
        assert path.isdir( store_dir )
    else:
        try:
            repos.create( store_dir )
        except:
            import pdb, sys, traceback
            traceback.print_exc()
            pdb.post_mortem(sys.exc_info()[-1])
            raise
    return store_dir


repository_storage = setupStorageDirectory()
