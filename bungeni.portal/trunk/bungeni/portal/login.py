from urlparse import urlparse, urlunparse
from urllib import urlencode
try:
    from urlparse import parse_qs
except ImportError:
    from cgi import parse_qs

from paste.httpexceptions import HTTPFound
from paste.httpexceptions import HTTPUnauthorized
from paste.request import construct_url, resolve_relative_url, \
                          parse_dict_querystring, parse_formvars
from paste.response import replace_header, header_value

from zope.interface import implements

from repoze.who.plugins.form import FormPluginBase
from repoze.who.interfaces import IChallenger
from repoze.who.interfaces import IIdentifier

from cStringIO import StringIO

class FormAuthPlugin(FormPluginBase):
    """This plugin supports an application-based login procedure."""
    
    implements(IChallenger, IIdentifier)

    username = "login", "__ac_name"
    password = "password", "__ac_password"
    
    def __init__(self, login_form_url, login_handler_path,
                 logout_handler_path, rememberer_name,
                 post_logout_url=None, reason_param='reason'):
        self.login_form_url = login_form_url
        self.login_handler_path = login_handler_path
        self.logout_handler_path = logout_handler_path
        self.post_logout_url = post_logout_url
        self.rememberer_name = rememberer_name
        self.reason_param = reason_param
        
    def identify(self, environ):
        path_info = environ['PATH_INFO']
        query = parse_dict_querystring(environ)

        # we've been asked to perform a logout
        if path_info == self.logout_handler_path:
            form = parse_formvars(environ)
            form.update(query)
            environ['repoze.who.application'] = HTTPUnauthorized()
            return None

        # we've been asked to perform a login
        if path_info == self.login_handler_path:
            body = environ['wsgi.input'].read()
            stream = environ['wsgi.input'] = StringIO(body)
            form = parse_formvars(environ)
            form.update(query)
            stream.seek(0)

            # extract username and password
            for key in self.username:
                if key in form:
                    login = form[key]; break
            else:
                return None

            for key in self.password:
                if key in form:
                    password = form[key]; break
            else:
                return None

            return {
                'login': login,
                'password': password,
                }

    def challenge(self, environ, status, app_headers, forget_headers):
        """Override the parent's challenge to avoid challenging the
        user on logout, introduce a post-logout page and/or pass the
        login counter to the login form.
        """

        # if the current path matches the logout handler path, log out
        # the user without challenging.
        if environ['PATH_INFO'] == self.logout_handler_path:
            came_from = environ.get('came_from')
            script_path = environ.get('SCRIPT_PATH', '')
            
            if self.post_logout_url:
                # redirect to a predefined "post logout" URL.
                destination = self._get_full_path(
                    self.post_logout_url, environ)
                
                if came_from:
                    destination = self._insert_qs_variable(
                                  destination, 'came_from', came_from)
            else:
                # redirect to the referrer URL.
                destination = came_from or script_path or '/'

            return HTTPFound(destination, headers=forget_headers)

        return HTTPFound(headers=forget_headers)
    
    def _get_full_path(self, path, environ):
        """
        Return the full path to ``path`` by prepending the SCRIPT_PATH.
        
        If ``path`` is a URL, do nothing.
        
        """
        if path.startswith('/'):
            path = environ.get('SCRIPT_PATH', '') + path
        return path
    
    def _insert_qs_variable(self, url, var_name, var_value):
        """
        Insert the variable ``var_name`` with value ``var_value`` in the query
        string of ``url`` and return the new URL.
        
        """
        url_parts = list(urlparse(url))
        query_parts = parse_qs(url_parts[4])
        query_parts[var_name] = var_value
        url_parts[4] = urlencode(query_parts, doseq=True)
        return urlunparse(url_parts)


