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
from zope.publisher.browser import BrowserView

from ore.alchemist.interfaces import IAlchemistContainer, IAlchemistContent
from ore.alchemist.model import queryModelDescriptor
from ore.wsgiapp.interfaces import IApplication
from alchemist.traversal.managed import ManagedContainerDescriptor

from bungeni.ui.utils import getDisplayDate
from bungeni.core.translation import get_all_languages
from bungeni.core.translation import get_available_translations
from bungeni.core.app import BungeniApp
from bungeni.core import location

from bungeni.ui.utils import absoluteURL

import datetime


class LanguageViewlet(object):
    """Language selection viewlet."""

    render = ViewPageTemplateFile("templates/language.pt")
    showFlags = False
    available = True
    
    def update(self):
        translations = get_available_translations(self.context)
        languages = get_all_languages()
        selected = self.request.locale.getLocaleID()
        url = absoluteURL(getSite(), self.request)

        # self.available = len(translations) > 0
        
        self.languages = [{
            'code': language,
            'flag': url+languages[language].get('flag',''),
            'name': languages[language]['name'],
            'selected': language == selected,
            'url': "%s/change-language?lang=%s" % (url, language),
            } for language in languages]
            
class ChangeLanguage(BrowserView):  

    def __call__(self):
        """set the I18N_LANGUAGES cookie and redirect back to referrer"""
        response = self.request.response
        lang = self.request.get('lang', None)
        if lang:
            response.setCookie('I18N_LANGUAGES', lang, path='/')
        else:
            response.expireCookie('I18N_LANGUAGES', path='/')                        
        url =  self.request.get('HTTP_REFERER','..')
        return response.redirect(url)

              

