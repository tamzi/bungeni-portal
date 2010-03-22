from zope.interface import implements
from Acquisition import aq_inner

from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView

from Products.groupworkspaces.interfaces import IMembershipView

from zope.app.component.hooks import getSite
import string


class MembershipView(BrowserView):
    """
    Browser view for membership listing.
    """
    implements(IMembershipView)
    def __init__(self,context, request):
        super(MembershipView, self).__init(context, request)
    
    def member_folders(self):
        portal_catalog = getToolByName(getSite(), 'portal_catalog')
        path = '/'.join(getSite().getPhysicalPath()) +'/membership'
        results = portal_catalog(path=dict(query=path, depth=1, sort_on='sortable_title'))
        return sorted([(dict(id=r.getId, url=r.getURL(), title=r.Title)) for r in results])


    def alphabetise(self):
        items = aq_inner(getSite().membership).getFolderContents({'sort_on':'sortable_title'})
        alphabets = {}
        for x in string.uppercase:
            alphabets[x] = []
            
        for item in items:
            char = item.Title[0].upper()
            if not alphabets.has_key(char):
                continue
            alphabets[char].append(item)
                
        return [{'letter': x, 'items': alphabets[x]} for x in  string.uppercase]
