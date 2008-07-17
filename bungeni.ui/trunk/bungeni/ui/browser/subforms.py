# utf-8
from zope.viewlet import viewlet, interfaces
from zope.app.pagetemplate import ViewPageTemplateFile
import bungeni.core.domain as domain
from bungeni.core.interfaces import IMemberOfParliament
from ore.alchemist import Session
from ore.alchemist.model import queryModelDescriptor
from bungeni.core.i18n import _
from forms import BungeniAttributeDisplay


from alchemist.ui.viewlet import EditFormViewlet, AttributesViewViewlet, DisplayFormViewlet
#from alchemist.ui.core import DynamicFields

from zope.formlib import form

class MPTitleViewlet( viewlet.ViewletBase ):

    def __init__( self,  context, request, view, manager ):        
        self.context = context
        self.request = request
        self.__parent__= view
        self.manager = manager
        self.query = None


    def getData(self):
        """
        return data as dict
        """
        data_list=[]
        #urlpf=getDateFilter(self.request)        
        results = self.query.all()
        for result in results:            
            data ={}
            data['url']= 'titles/obj-' + str(result.role_title_id) #+ urlpf
            data['short_name'] = result.short_name
            data['start_date'] = str(result.start_date)
            data['end_date'] = str(result.end_date)
#            data['mpurl']= '/parliament/obj-' + str(result.parliament_id) + '/parliamentmembers' + urlpf
#            data['current'] = 'odd'
            data_list.append(data)
        return data_list
        
    
    def update(self):
        """
        refresh the query
        """       
        session = Session()
        membership_id = self.context.membership_id
        self.query = session.query(domain.MemberRoleTitle).filter(domain.MemberRoleTitle.c.membership_id == membership_id)   

    render = ViewPageTemplateFile ('templates/mp_title_viewlet.pt')                
    
class PersonInfo( BungeniAttributeDisplay):
    """
    Bio Info / personal data about the MP
    """
    mode = "view"
    template = ViewPageTemplateFile('templates/display_subform.pt')        
    form_name = _(u"Personal Info")   
    
    def __init__( self,  context, request, view, manager ):        
        self.context = context
        self.request = request
        self.__parent__= view
        self.manager = manager
        self.query = None
        md = queryModelDescriptor(domain.ParliamentMember)          
        self.form_fields=md.fields #.select('user_id', 'start_date', 'end_date')
        
    def update(self):
        """
        refresh the query
        """       
        session = Session()
        user_id = self.context.user_id
        self.query = session.query(domain.ParliamentMember).filter(domain.ParliamentMember.c.user_id == user_id) 
        self.context = self.query.all()[0]
        self.context.__parent__=None
        super( PersonInfo, self).update()



    
            
    
