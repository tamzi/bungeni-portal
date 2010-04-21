# Bungeni Parliamentary Information System - http://www.bungeni.org/
# Copyright (C) 2010 - Africa i-Parliaments - http://www.parliaments.info/
# Licensed under GNU GPL v2 - http://www.gnu.org/licenses/gpl-2.0.txt

"""Zope3 + Evoque Templating: http://evoque.gizmojo.org/

Evoque features & advantages (comapred to ZPT):
- No server restart needed each time a file-based template is modified.
- A template may invoke other templates (that may be within same collection or 
  within any other collection in the domain).
- Template inheritance, offering option to move page composition logic out of 
  the core application.
- Automatic XML/HTML escaping of all data values, guaranteeing XSS protection.
- May be used to generate output in any format, not only X/HTML e.g. JSON, CSS,
  JavaScript, INI, SQL, etc. 
- No "XML Situps" required.
- May be run in restricted mode (to allow untrusted authors to edit templates).
- Multiple templates may be defined in a single file, if so wished.
- A direct and immediately obvious syntax.
- Super fast, simple, extremely flexible, small.
- Lightweight:
  - to use Evoque with Zope you need this module + the evoque package (1000 LOC); 
  - for ZPT you'd need: zope.tal, zope.tales, zope.pagetemplate, 
    zope.app.pagetemplate, z3c.pt, z3c.template, z3c.ptcompat, chameleon.core, 
    chameleon.zpt, chameleon.html, ... ?!?

Current limitations:
- A "template" attribute may currently not be specified in a ZCML declaration 
  for an element -- for now, the "template" should be specified in the class.

Status:
This is still exploratory, to first verify that Evoque templates may be used
everywhere that ZPT are used.

Viewlets and ViewletManagers are confirmed to work, as proven by an 
implementation of a sample of each of these using an evoque template. 

The following still need to be 100% verified with real working examples:
- Using evoque templates with: BrowserViews, Forms/Widgets (formlib, do these 
  use ZPT templates?), any other Zope construct that uses a "template".
- i18n catalog extraction: this may simply mean adopting a supported alias for 
  the gettext() function -- the implementation below uses "i18n" as alias, 
  i.e. i18n(messageid) to get the translation for messageid, however the most 
  common is to use an "_" i.e. _(messageid).

$Id$
"""
log = __import__("logging").getLogger("bungeni.ui.z3evoque")
log.setLevel(10)

import os
import zope
from evoque.domain import Domain

#
# Configuration
#

# this is the core "high-level config" for evoque
# !+ should be externalized to the application's config.ini file
evoque_ini = {
    "evoque.default_dir":"templates",
    "evoque.default_template":None,
    "evoque.restricted":False,
    "evoque.errors":3,
    "evoque.cache_size":0,
    "evoque.auto_reload":2,
    "evoque.slurpy_directives":True,
    "evoque.quoting":"xml",
    "evoque.input_encoding":"utf-8"
}

# logger
evoque_logger_name = "evoque"
evoque_logger_level = 10 # debug

# The (absolute) path as root location against which to resolve all (relative) 
# domain/collection paths e.g. the abs path for the deployed application root. 
# Here we use the folder for the deployed bungeni.ui package:
abs_root = os.path.dirname(os.path.abspath(__file__))

# Other template collections: name, relative path to abs_root.
# Convention for collection names: dotted parent package name.
# !+ Add support for other collection parameters:
# cache_size, auto_reload, slurpy_directives, quoting, input_encoding, filters
# Currently each of these is defaulted to what is set on the domain.
additional_collections = {
    #"bungeni.ui":"templates", # already the "" default collection (default_dir)
    "bungeni.ui.viewlets":"viewlets/templates",
    #"bungeni.ui.forms":"forms/templates", 
    #"bungeni.ui.portlets":"portlets/templates",
    #"ploned.ui":"../../../ploned.ui/ploned/ui/templates",
    #"alchemist.ui":"../../../alchemist.ui/alchemist/ui/templates"
}

# (tmp hack) localedirs for i18n domains
i18n_domain_localedirs = {
    "bungeni.ui": os.path.join(os.path.dirname(os.path.abspath(
        __import__("bungeni.ui").__file__)), "ui/locales")
}

#
# Setup of the Evoque Domain
#

# Global evoque domain singleton utility
# Summary of usage:
#   from bungeni.ui.z3evoque import domain
#   print domain.get_template( ... ).evoque( ... )
# See: http://evoque.gizmojo.org/usage/api/
#
domain = None

def set_domain(evoque_domain):
    """Set the evoque domain onto global domain attribute. 
    Also (even if not really necessary) register it as a ZC utility.
    """
    # tag with IEvoqueDomain
    zope.interface.alsoProvides(evoque_domain, IEvoqueDomain)
    # register as utility
    zope.component.getGlobalSiteManager(
            ).registerUtility(evoque_domain, IEvoqueDomain)
    # set utility onto z3evoque.domain
    global domain
    domain = zope.component.getUtility(IEvoqueDomain)

class IEvoqueDomain(zope.interface.Interface):
    """Marker for an Evoque Domain instance."""

def setup_evoque():
    import logging
    evoque_domain = Domain(
        # root folder for the default template collection, must be abspath;
        os.path.join(abs_root, evoque_ini.get("evoque.default_dir", "")),
        
        # whether evaluation namespace is restricted or not 
        restricted = evoque_ini.get("evoque.restricted", False),    
        
        # how should any evaluation errors be rendered
        # int 0 to 4, for: [silent, zero, name, render, raise]
        errors = int(evoque_ini.get("evoque.errors", 3)),
        
        # evoque logger; additional setings should be specified via the app's 
        # config ini file, just as for any other logger in the application
        log = logging.getLogger(evoque_logger_name),
        
        # [collections] int, max loaded templates in a collection
        cache_size = int(evoque_ini.get("evoque.cache_size", 0)), 
        
        # [collections] int, min seconds to wait between checks for
        # whether a template needs reloading
        auto_reload = int(evoque_ini.get("evoque.auto_reload", 60)), 
        
        # [collections] bool, consume all whitespace trailing a directive
        slurpy_directives = evoque_ini.get("evoque.slurpy_directives", True),
        
        # [collections/templates] str or class, to specify the *escaped* 
        # string class that should be used i.e. if any str input is not of 
        # this type, then cast it to this type). 
        # Builtin str key values are: "xml" -> qpy.xml, "str" -> unicode
        quoting = evoque_ini.get("evoque.quoting", "xml"),
        
        # [collections/templates] str, preferred encoding to be tried 
        # first when decoding template source. Evoque decodes template
        # strings heuristically, i.e. guesses the input encoding.
        input_encoding = evoque_ini.get("evoque.input_encoding", "utf-8"),
        
        # [collections/templates] list of filter functions, each having 
        # the following signature: filter_func(s:basestring) -> basestring
        # The functions will be called, in a left-to-right order, after 
        # template is rendered. NOTE: not settable from the conf ini.
        filters=[]
    )
    # set log level (!+ should not be here)
    evoque_domain.log.setLevel(evoque_logger_level)
    
    # additional collections
    for name, path in additional_collections.items():
        evoque_domain.set_collection(name, 
            os.path.normpath(os.path.join(abs_root, path)))
    
    # default template (optional) i.e. 
    # what to receive when calling domain.get_template() with no params
    if evoque_ini.get("evoque.default_template"):
        evoque_domain.get_collection().get_template("", 
                src=evoque_ini.get("evoque.default_template"))
    
    # set the evoque_domain singleton utility
    set_domain(evoque_domain)
    
    # log setup finished
    domain.log.debug(evoque_domain.__dict__)


#
# View Templates
#


class _ViewTemplateBase(object):
    """Evoque template used as method of a view defined as a Python class.
    """
    name = None
    src = None
    collection = None
    
    i18n_domain = None
    
    _descriptor_view = None
    _descriptor_type = None
    
    def __init__(self, *args, **kw):
        raise NotImplemented("ViewTemplateBase.__init__ may not be called "
            "directly. Must be overrided by subslasses.")
    
    def __get__(self, view, type_):
        """Non-data descriptor to grab a reference to the caller view.
        For the case of viewlets configured in ZCML, this is an instance of:
            zope.viewlet.metaconfigure.<<SpecificViewletClass>>
        """
        self._descriptor_view = view
        self._descriptor_type = type_
        return self
    
    @property
    def template(self):
        """The evoque template instance."""
        return domain.get_template(
                            self.name, self.src, collection=self.collection)
    
    # !+ support other evoque() params: raw=None, quoting=None
    def __call__(self, *args, **kwds):
        """Wrapper on template.evoque()."""
        namespace = self._get_context()
        return self.template.evoque(namespace, **kwds)
    
    def _get_context(self):
        view = self._descriptor_view
        namespace = {}
        namespace["view"] = view
        namespace["request"] = view.request
        namespace["context"] = view.context
        namespace['views'] = ViewMapper(view.context, view.request)
        namespace["i18n"] = self._get_gettext(
                self.i18n_domain, view.request.locale.getLocaleID())
        return namespace
    
    def _get_gettext(self, i18n_domain, language):
        """Get a _() i18n gettext function bound to domain and language.
        !+ There must be a better way to do this, but this does not work:
            zope.i18nmessageid.MessageFactory(self.i18n_domain)
        """
        import gettext
        t = gettext.translation(
            i18n_domain,
            localedir=i18n_domain_localedirs[i18n_domain],
            languages=[language])
        return t.gettext

class ViewTemplateString(_ViewTemplateBase):
    """Evoque string-based template used as method of a view 
    defined as a Python class.
    """
    def __init__(self, name, src, collection=None, i18n_domain=None):
        """
        name: str
        src: str, template source string
        collection: either(None, str, Collection)
            None implies default collection, else 
            str/Collection refer to an existing collection
        """
        if name is not None: self.name = name
        if src is not None: self.src = src
        if collection is not None: self.collection = collection
        if i18n_domain is not None: self.i18n_domain = i18n_domain
        # templates from string must be explicitly set onto their collection
        domain.set_template(self.name, src=self.src, 
                                collection=self.collection, from_string=True)
        log.debug("ViewTemplateString name=%s collection=%s : %s" % (
                                                    name, collection, self))

class ViewTemplateFile(_ViewTemplateBase):
    """Evoque file-based template used as method of a view 
    defined as a Python class.
    """
    def __init__(self, name, src=None, collection=None, i18n_domain=None):
        """
        name: str, if no src this is collection-root-relative locator
        src: either(None, str), collection-root-relative locator
        collection: either(None, str, Collection)
            None implies default collection, else 
            str/Collection refer to an existing collection
        """
        if name is not None: self.name = name
        if src is not None: self.src = src
        if collection is not None: self.collection = collection
        if i18n_domain is not None: self.i18n_domain = i18n_domain
        log.debug("ViewTemplateFile name=%s collection=%s : %s" % (
                                                    name, collection, self))

# View Helpers

class ViewMapper(object):
    """from: zope.app.pagetemplate.viewpagetemplatefile.ViewMapper"""
    def __init__(self, ob, request):
        self.ob = ob
        self.request = request
    def __getitem__(self, name):
        return zope.component.getMultiAdapter((self.ob, self.request), name=name)


''' Idea here is to separate all page-concerns from templates:
class Page(object):
    """Wrapper on a ViewTemplate instance, adding page-related features
    
    usage: Page(ViewTemplateFile( ... ), "text/x-json")
    """
    def __init__(self, view_template, content_type):
        self.view_template = view_template
        self.content_type = content_type

    def __call__(self, instance, *args, **kw):
        response = instance.view_template.request.response
        if not response.getHeader("Content-Type"):
            response.setHeader("Content-Type", self.content_type)
        return instance.view_template(*args, **kw)
'''

