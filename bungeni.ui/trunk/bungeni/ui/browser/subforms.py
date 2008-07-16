# utf-8
from zope.viewlet import viewlet, interfaces
from zope.app.pagetemplate import ViewPageTemplateFile
import bungeni.core.domain as domain
from ore.alchemist import Session


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
#            data['url']= '/parliament/obj-' + str(result.parliament_id) + urlpf
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
