"""
$Id$
"""

from zope.publisher.browser import BrowserView
from zope.app.basicskin.standardmacros import StandardMacros as BaseMacros
from zope.app.pagetemplate import ViewPageTemplateFile

class PlonedLayout( BrowserView ):

    template = ViewPageTemplateFile('templates/ploned-template.pt')

    def __getitem__(self, key):
        return self.template.macros[key]

class StandardMacros( BaseMacros ):

    macro_pages = ['ploned-layout', 'alchemist-form']

