from zope.publisher.browser import BrowserView
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.formlib import form
from zope.formlib import namedtemplate
from zope import schema
from zope import interface
from bungeni.ui.i18n import _
from bungeni.ui.forms.common import set_widget_errors
from ore.alchemist import Session
from bungeni.transcripts import domain
from bungeni.transcripts import orm
from alchemist.catalyst import ui
from zope.traversing.browser import absoluteURL
from zope.component import getMultiAdapter
from bungeni import models

class MainView(BrowserView):
    def __call__(self):
        self.group = self.get_group()
        self.group_id = self.context.group_id
        self.sitting_id = self.context.sitting_id
        self.sitting_media_path = self.get_media_path()
        self.transcripts = self.get_transcripts()
        return super(MainView, self).__call__()
        
    def get_group(self):
        try:              
            group = self.context.get_group()
        except:
            session = Session()
            group = session.query(models.domain.Group).get(self.context.group_id)
        return group
    
    def get_media_path(self):
        session = Session()
        sitting = session.query(domain.Sitting).filter(domain.Sitting.sitting_id == self.context.sitting_id).first()
        if sitting is not None:
            media_path = sitting.media_path
        else:
            media_path = None
        return media_path
    
    def get_transcripts(self):
        session = Session()
        transcripts = session.query(domain.Transcript).filter(domain.Transcript.sitting_id == self.context.sitting_id).order_by(domain.Transcript.start_time)
        new_t = []
        for t in transcripts:
            t.version_link = absoluteURL(t, self.context)  + '/version'
            new_t.append(t);
        import pdb; pdb.set_trace();
        return transcripts
        
class Add(ui.AddForm):
    class IReportingForm(interface.Interface):
        start_time = schema.TextLine(
            title=_(u"Start Time"),
            required=True)
        end_time = schema.TextLine(
            title=_(u"EndTime"),
            required=True)
        text = schema.Text(title=u'Speech Text',
                   required=False,
                   )
        person = schema.TextLine(title=u'Person',
                   required=False,
                   )
        
    template = namedtemplate.NamedTemplate('alchemist.form')
    form_fields = form.Fields(IReportingForm)
    
    def setUpWidgets(self, ignore_request=False):
        class context:
            start_time = None
            end_time = None
            text = None
            person = None
            
        self.adapters = {
            self.IReportingForm: context
            }
        self.widgets = form.setUpEditWidgets(
            self.form_fields, self.prefix, self.context, self.request,
            adapters=self.adapters, ignore_request=ignore_request)
    
    def update(self):
        self.status = self.request.get('portal_status_message', '')
        super(Add, self).update()
        set_widget_errors(self.widgets, self.errors)

    def validate(self, action, data):    
        errors = super(Add, self).validate(action, data)
        return errors
        
    @form.action(_(u"Save"))  
    def handle_preview(self, action, data):
        session = Session()
        transcript = domain.Transcript()
        transcript.start_time =  data['start_time']                    
        transcript.end_time =  data['end_time']                      
        transcript.text = data['text']
        transcript.person = data['person'] 
        transcript.sitting_id = self.context.sitting_id
        session.add(transcript)
        session.commit()
        '''
        ob = self.createAndAdd(data)
        
        name = self.context.domain_model.__name__

        if not self._next_url:
            self._next_url = absoluteURL(
                ob, self.request) + \
                '?portal_status_message=%s added' % name'''
       
                
