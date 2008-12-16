from zope import component

from zope.app.pagetemplate import ViewPageTemplateFile
from zope.traversing.browser.absoluteurl import absoluteURL

from ore.xapian.interfaces import IIndexSearch
from ore.xapian.interfaces import IResolver

from bungeni.ui.i18n import MessageFactory as _

from bungeni.core.workflows.question import states

class Manager(object):
    """Workspace viewlet manager."""

class QuestionsListingViewletbase(object):
    """Renders a listing of questions."""
    
    render = ViewPageTemplateFile("templates/questions.pt")

    title = description = state = None

    count = 5
    
    def update(self):
        """Run query."""

        if self.state is None:
            return NotImplementedError("Subclass must provide ``state``.")

        searcher = component.getUtility(IIndexSearch)()
        query = searcher.query_field('status', self.state)

        # resolve items
        resolver = component.getUtility(IResolver)
        results = searcher.search(query, 0, self.count)
        questions = [result.object() for result in results]

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
        
class Draft(QuestionsListingViewletbase):
    state = states.draft
    title = _(u"Drafts")
    description = _(u"Questions in draft state.")
