from alchemist import ui
from zope.formlib.namedtemplate import NamedTemplate
from bungeni.ui.i18n import _

class AttributesEditViewlet(ui.core.DynamicFields, ui.viewlet.EditFormViewlet):
    mode = "edit"
    template = NamedTemplate('alchemist.subform')
    form_name = _(u"General")
