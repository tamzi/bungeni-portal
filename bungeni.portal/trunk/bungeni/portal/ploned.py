from chameleon.core.template import Macro
from z3c.pt.pagetemplate import ViewPageTemplateFile

import layout

class PlonedLayout(object):
    template = ViewPageTemplateFile("ploned.pt")
    
    def __init__(self, context, request):
        def render(**kwargs):
            return layout.bungeni.render_macro(
                "", global_scope=False, parameters=kwargs)

        self.macros = {
            'page': Macro(render)}

    def __getitem__(self, key):
        return self.template.macros.bind(macros=self.macros)[key]
