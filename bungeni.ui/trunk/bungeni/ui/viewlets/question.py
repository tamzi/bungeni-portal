from zope import component

from zope.app.pagetemplate import ViewPageTemplateFile
from zope.traversing.browser.absoluteurl import absoluteURL

from ore.xapian.interfaces import IIndexSearch

import xapian

from bungeni.ui.i18n import MessageFactory as _

from bungeni.core.workflows.question import states

marker = object()

class QuestionsListingViewletBase(object):
    """Renders a listing of questions."""
    
    render = ViewPageTemplateFile("templates/questions.pt")

    name = title = description = None
    count = 5
        
    def update(self):
        """Run query."""

        questions = [result.object() for result in self.query()]

        
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

    def query(self):
        return NotImplementedError("Subclass must implement this method.")

class QuestionsInParticularStateViewlet(QuestionsListingViewletBase):
    state = marker

    def query(self):
        if self.state is marker:
            return NotImplementedError("Subclass must provide ``state``.")
    
        searcher = component.getUtility(IIndexSearch)()
        query = searcher.query_field('status', self.state)
        brains = searcher.search(query, 0, self.count)

        return brains
        
class Draft(QuestionsInParticularStateViewlet):
    name = state = states.draft
    title = _(u"Drafts")
    description = _(u"Questions in draft state.")

class Submitted(QuestionsInParticularStateViewlet):
    name = state = states.submitted
    title = _(u"Submitted")
    description = _(u"Questions submitted to Clerk's office.")

class Archive(QuestionsListingViewletBase):
    title = _(u"Archive")
    description = _(u"Past submitted questions.")
    name = 'archive'
    
    def query(self):
        searcher = component.getUtility(IIndexSearch)()

        draft = searcher.query_field('status', states.draft)
        all = searcher.query_all()
        
        query = searcher.query_filter(all, draft, exclude=True)        
        brains = searcher.search(query, 0, self.count)

        return brains
