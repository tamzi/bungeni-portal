from zope.component import getUtility


from repoze.bfg.wsgi import wsgiapp
from repoze.bfg.chameleon_zpt import render_template_to_response
from repoze.bfg.view import static
from repoze.bfg.traversal import model_path
from repoze.bfg.interfaces import ISettings
from paste.urlparser import StaticURLParser

def static_view(context, request):
    settings = getUtility(ISettings)
    path = settings.path
    request.path_info = context.path[len(path):]
    static = StaticURLParser(path, cache_max_age=3600)
    return request.get_response(static)

def directory_view(context, request):
    """directory view

    Show a list of packages or files in a directory.    
    """
    return render_template_to_response(
        'templates/page.pt', project='pkgindex',
        items=[(name, model_path(item)) for (name, item) in context.items()])

