# encoding: utf-8

from zope import component
from zope.app.component.hooks import getSite
from zope.location.interfaces import ILocation
from zope.dublincore.interfaces import IDCDescriptiveProperties
from zope.security import proxy
from zope.viewlet import viewlet
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.app.publisher.interfaces.browser import IBrowserMenu
from zope.app.component.hooks import getSite
from ore.alchemist.interfaces import IAlchemistContainer, IAlchemistContent
from ore.alchemist.model import queryModelDescriptor
from ore.wsgiapp.interfaces import IApplication
from alchemist.traversal.managed import ManagedContainerDescriptor

from bungeni.ui.utils import getDisplayDate
from bungeni.core.translation import get_all_languages
from bungeni.core.translation import get_available_translations
from bungeni.core.app import BungeniApp
from bungeni.core import location

import datetime
from zope.traversing.browser import absoluteURL 

class LanguageViewlet(object):
    """Language selection viewlet."""

    render = ViewPageTemplateFile("templates/language.pt")
    showFlags = True
    available = True
    
    def update(self):
        translations = get_available_translations(self.context)
        languages = get_all_languages()
        selected = "en"
        url = absoluteURL(getSite(), self.request)

        # self.available = len(translations) > 0
        
        self.languages = [{
            'code': language,
            'flag': url+languages[language]['flag'],
            'name': languages[language]['name'],
            'selected': language == selected,
            'url': "%s/change-language?name=%s" % (url, language),
            } for language in translations]

