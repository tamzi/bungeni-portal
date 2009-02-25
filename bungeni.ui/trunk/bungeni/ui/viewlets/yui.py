from zope.viewlet import viewlet
from zc.resourcelibrary import need
from z3c.pt.texttemplate import ViewTextTemplateFile

class YUITabView( viewlet.ViewletBase ):
    """Get the JS into the form."""

    render = ViewTextTemplateFile("scripts/tabview.js")
    for_display = True

    def update(self):
        need("yui-tab")
