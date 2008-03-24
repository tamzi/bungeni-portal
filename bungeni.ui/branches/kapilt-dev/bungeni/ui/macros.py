"""
$Id: $
"""

from zope.publisher.browser import BrowserView
from zope.app.basicskin.standardmacros import StandardMacros as BaseMacros
from zope.app.pagetemplate import ViewPageTemplateFile

class StandardMacros( BaseMacros ):

    macro_pages = ['ploned-layout', 'alchemist-form']

