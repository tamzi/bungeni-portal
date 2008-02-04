
import re
from zope import interface, schema

class ILoginForm( interface.Interface ):
    login = schema.TextLine( title=u"Username")
    password = schema.Password( title=u"Password")    

def check_password( signup ):
    if not signup.password_repeat == signup.password:
        raise schema.ValidationError(u"Passwords do not match")

def check_email( email ):
    if EMAIL_RE.match( email ) is None:
        return False
    return True
                 
EMAIL_RE = "([0-9a-zA-Z_&.+-]+!)*[0-9a-zA-Z_&.+-]+@(([0-9a-zA-Z]([0-9a-zA-Z-]*[0-9a-z-A-Z])?\.)+[a-zA-Z]{2,6}|([0-9]{1,3}\.){3}[0-9]{1,3})$"
EMAIL_RE = re.compile( EMAIL_RE )            

class ISignupForm(interface.Interface):

    interface.invariant( check_password )    
    
    login = schema.TextLine(title=u"Username", min_length=5)
    first_name = schema.TextLine(title=u"First Name", min_length=3)
    last_name = schema.TextLine(title=u"Last Name", min_length=3)
    email = schema.TextLine(title=u"Email Address", constraint=check_email )
    password = schema.Password(title=u"Password", min_length=5)
    password_repeat = schema.Password(title=u"Repeat password")

