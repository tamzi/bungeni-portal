from plone import maintemplate
from bungeni import portal

import os

bungeni = maintemplate.Layout(
    os.path.join(
        portal.__path__[0], 'static', 'html', 'bungeni.html'))
