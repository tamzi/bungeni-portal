from plone.app.layout.viewlets import common

class GlobalSectionsViewlet(common.GlobalSectionsViewlet):
    #index = ViewPageTemplateFile('sections.pt')

    def update(self):
        super(GlobalSectionsViewlet, self).update()
        pass
