"""
$Id: $
"""

from zope.publisher.browser import BrowserView
from zope.app.basicskin.standardmacros import StandardMacros as BaseMacros
from zope.app.pagetemplate import ViewPageTemplateFile

class BungeniLayout( BrowserView ):

    template = ViewPageTemplateFile('templates/bungeni-template.pt')

    def __getitem__(self, key):
        return self.template.macros[key]

class StandardMacros( BaseMacros ):

    macro_pages = ['bungeni-layout', 'alchemist-form']

