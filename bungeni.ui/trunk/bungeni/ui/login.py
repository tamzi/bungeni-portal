import re
from zope import interface, schema, component
from zope.formlib import form
from alchemist.ui.core import BaseForm
from ore.alchemist import Session
from zope.app.authentication.interfaces import IAuthenticatorPlugin
from zope.app.security.interfaces import IUnauthenticatedPrincipal
from bungeni.core.i18n import _
from bungeni.core import User

class ILoginForm( interface.Interface ):
    login = schema.TextLine( title=_(u"Username"))
    password = schema.Password( title=_(u"Password"))    

class NotAnEmailAddress(schema.ValidationError):
    """This is not a valid email address"""

def check_password( signup ):
    if not signup.password_repeat == signup.password:
        raise schema.ValidationError(_(u"Passwords do not match"))

def check_email( email ):
    if EMAIL_RE.match( email ) is None:
        raise NotAnEmailAddress(email)
        return False
    return True
                 
EMAIL_RE = "([0-9a-zA-Z_&.+-]+!)*[0-9a-zA-Z_&.+-]+@(([0-9a-zA-Z]([0-9a-zA-Z-]*[0-9a-z-A-Z])?\.)+[a-zA-Z]{2,6}|([0-9]{1,3}\.){3}[0-9]{1,3})$"
EMAIL_RE = re.compile( EMAIL_RE )            

class ISignupForm(interface.Interface):

    interface.invariant( check_password )    
    
    login = schema.TextLine(title=_(u"Username"), min_length=5)
    first_name = schema.TextLine(title=_(u"First Name"), min_length=3)
    last_name = schema.TextLine(title=_(u"Last Name"), min_length=3)
    email = schema.TextLine(title=_(u"Email Address"), constraint=check_email )
    password = schema.Password(title=_(u"Password"), min_length=5)
    password_repeat = schema.Password(title=_(u"Repeat password"))


class Login( BaseForm ):

    form_fields = form.Fields( ILoginForm )
    prefix = ""
    form_name = _(u"Login")
    
    def update( self ):
        self.status = self.request.get('status_message', '')
        super( Login, self).update()
        
    @form.action( _(u"Login") )
    def handle_login( self, action, data ):
        if IUnauthenticatedPrincipal.providedBy(self.request.principal):
            self.status=_(u"Invalid Account Credentials")
        else:
            camefrom = self.request.get('camefrom', '.')
            self.status = _("You are now logged in")
            self.request.response.redirect( camefrom )

class SignUp( BaseForm ):
    
    form_name = "signup"
    form_fields = form.Fields( ISignupForm )
    
    @form.action( _(u"Sign Up") )
    def handle_signup( self, action, data ):
        principals = component.getUtility( IAuthenticatorPlugin, 'rdb-auth')

        # check if the user already exists
        info = principals.principalInfo( data['login'])
        if info is not None:
            self.status = _("Username already taken")

        # add principal to principal folder        
        # todo - should separate out a non event sending form lib set_data()
        u = User( data['login'] )
        u.first_name = data['first_name']
        u.last_name = data['last_name']
        u.email = data['email']
        u.setPassword( data['password'] )
        s = Session()
        s.save(u)
        
        # todo - add registration event notification
        # see zope.authentication.interfaces.IPrincipalCreatedEvent
        msg = _(u"Registration+Successful")
        self.request.response.redirect(u'/@@login?status_message=%s'%(msg) )

