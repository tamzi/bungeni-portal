from zope.app.pagetemplate import ViewPageTemplateFile
from zope.publisher.browser import BrowserView
from zope.viewlet import viewlet
import zope.interface
from zope.security import proxy
import bungeni.core.schema as schema
import bungeni.core.domain as domain
from bungeni.ui.browser import container
import base64
import urllib

class LoginProxy(BrowserView):
	def __call__(self):
		#CONTEXT = self.context
		#REQUEST = self.request
		#RESPONSE = self.request.response
		FORWARD_URL = 'http://www.bungenisrv.local/bungeni.html'
		if (self.request.has_key('guserpass')):
			userpass = self.request.get('guserpass')
			userpass = urllib.unquote(userpass)
			encoded_userpass = base64.b64encode(userpass)
			self.request.response.setCookie('wc.cookiecredentials',encoded_userpass, path='/')
			self.request.response.setCookie('portal.loggedin', 'true', expires='Wed, 31 Dec 2008 23:45:00', path='/', domain='.bungenisrv.local')
			return self.request.response.redirect(FORWARD_URL)


