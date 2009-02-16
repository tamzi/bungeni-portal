import os

try:
    from plone.maintemplate import Layout
except ImportError:
    from chameleon.html.template import DynamicHTMLFile as Layout
    
from bungeni import portal

bungeni = Layout(
    os.path.join(
        portal.__path__[0], 'static', 'html', 'bungeni.html'))
