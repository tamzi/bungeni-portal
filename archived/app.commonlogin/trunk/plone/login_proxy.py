# Example code:

# Import a standard function, and get the HTML request and response objects.
from Products.PythonScripts.standard import html_quote
import base64
import urllib

def loginProxy(self):
	#request = container.REQUEST
	#RESPONSE =  request.RESPONSE
	# userpass=  "speaker:speaker"
	FORWARD_URL = 'http://portal.bungenisrv.local/@@login_proxy'
	if (self.REQUEST.cookies.has_key('guserpass')):
		userpass = self.REQUEST.cookies['guserpass']
		userpass = urllib.unquote(userpass)
		listuserpass = str(userpass).split(':')
		hexencodeduser= listuserpass[0].encode('hex')
		hexencodedpass= listuserpass[1].encode('hex')
		b64encodedlog = base64.b64encode(hexencodeduser + ":" + hexencodedpass)
		self.REQUEST.RESPONSE.setCookie('__ac',b64encodedlog, path='/')
		self.REQUEST.RESPONSE.setCookie('plone.loggedin','true', expires='Wed, 31 Dec 2008 23:45:00', path='/', domain='.bungenisrv.local')
		return self.REQUEST.RESPONSE.redirect(FORWARD_URL)
	else:
		return str(self.REQUEST)
	#return str(self.REQUEST)

	

