from zope import component

from zope.app.pagetemplate import ViewPageTemplateFile
from zope.traversing.browser.absoluteurl import absoluteURL

from ore.xapian.interfaces import IIndexSearch
from ore.xapian.interfaces import IResolver

from bungeni.ui.i18n import MessageFactory as _

from bungeni.core.workflows.question import states

marker = object()

class QuestionsListingViewletBase(object):
    """Renders a listing of questions."""
    
    render = ViewPageTemplateFile("questions.pt")

    title = description = None
    state = marker

    count = 5
    
    def update(self):
        """Run query."""

        if self.state is marker:
            return NotImplementedError("Subclass must provide ``state``.")

        searcher = component.getUtility(IIndexSearch)()
        query = searcher.query_field('status', self.state)

        # resolve items
        resolver = component.getUtility(IResolver)
        brains = searcher.search(query, 0, self.count)
        questions = [brain.object() for brain in brains]

        results = []

        for question in questions:
            try:
                url = absoluteURL(question, self.request)
            except TypeError: # TODO: Not necessary after we have the proper adapter
                              # set up.
                url = '#'
                
            item = dict(title=question.subject,
                        url=url)

            results.append(item)

        self.results = results
        
class Draft(QuestionsListingViewletBase):
    state = states.draft
    title = _(u"Drafts")
    description = _(u"Questions in draft state.")

class Submitted(QuestionsListingViewletBase):
    state = states.submitted
    title = _(u"Submitted")
    description = _(u"Questions submitted to Clerk's office.")
