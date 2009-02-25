import datetime
import base64

from z3c.pt.pagetemplate import ViewPageTemplateFile
from zope.traversing.browser import absoluteURL 
from zope.security.proxy import removeSecurityProxy
from zope.publisher.browser import BrowserView

from ore.alchemist.model import queryModelDescriptor
from ore.alchemist.container import stringKey

from bungeni.ui.forms.fields import BungeniAttributeDisplay
from bungeni.ui.i18n import _

class AtomFeedView(BrowserView):
    """Base atom feed view.

    To-Do: This view is broken; it should be enabled for content for
    which it makes sense to issue a content listing, e.g. containers.
    """
    
    template = ViewPageTemplateFile('templates/atom-feed.pt')
    content = ViewPageTemplateFile('templates/atom-content.pt')
    
    form_name = None  
    form_title = None
    
    def get_form_name(self):
        if self.form_name is not None:
            return self.form_name

        parent = self.context.__parent__
        if parent is not None:
            descriptor = queryModelDescriptor(
                parent.domain_model)
        if descriptor:
            name = getattr(descriptor, 'display_name', None)
        if name is None:
            assert parent is not None
            name = parent.domain_model.__name__
        return name

    def get_form_title(self):
        if self.form_title is not None:
            return self.form_title
        return self.get_form_name()
    
    def __call__(self):
        """We firts call the ``update`` method of the viewlet mixin,
        then prepare template variables."""

        viewlet = BungeniAttributeDisplay(
            self.context, self.request, self, None)
        
        viewlet.update()

        name = self.get_form_name()
        title = self.get_form_title()

        updated = datetime.datetime.now().isoformat()          

        uid = "urn:uuid:" + base64.urlsafe_b64encode(
            self.context.__class__.__name__ + ':' + stringKey(
                removeSecurityProxy(self.context)))

        url = absoluteURL(self.context, self.request)
        feed_url = url.rstrip('/') + '/atom.xml'

        content = type(self).content.bind(viewlet)
        
        return self.template(
            title=title,
            updated=updated,
            uid=uid,
            name=name,
            url=url,
            feed_url=feed_url,
            content=content)

class AtomPersonFeedView(AtomFeedView):
    form_name = _(u"Bio info")

class AtomPartyFeedView(AtomFeedView):
    form_name = _(u"Party")

class AtomCommitteeFeedView(AtomFeedView):
    form_name = _(u"Commitee")
