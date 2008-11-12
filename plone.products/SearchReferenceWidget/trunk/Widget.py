from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from Products.Archetypes.Registry import registerWidget
from Acquisition import aq_base, aq_parent
from Products.Archetypes.Widget import ReferenceWidget
from Products.CMFCore.utils import getToolByName


class SearchReferenceWidget(ReferenceWidget):
    """ SearchReferenceWidget. Live search on reference titles """

    _properties = ReferenceWidget._properties.copy()
    _properties.update({
        'macro' : "searchreference_widget",
        'addable' : 0, # create createObject link for every addable type
        'destination' : None, # may be:
                              # - ".", context object;
                              # - None, any place where
                              #   Field.allowed_types can be added;
                              # - string path;
                              # - name of method on instance
                              #   (it can be a combination list);
                              # - a list, combining all item above;
                              # - a dict, where
                              #   {portal_type:<combination of the items above>}
                              # destination is relative to portal root

        'base_search' : None,      # dictionary suitable for passing to catalog search. Unused if None.
        })
    
    security = ClassSecurityInfo()

    def getDestination(self, instance):
        if not self.destination:
            purl = getToolByName(instance, 'portal_url')
            return purl.getRelativeUrl(aq_parent(instance))
        else:
            value = getattr(aq_base(instance), self.destination,
                            self.destination)
            if callable(value):
                value = value()

            return value


InitializeClass(SearchReferenceWidget)

registerWidget(SearchReferenceWidget,
               title='SearchReferenceWidget',
               description="Renders a reference widget + input fields",
               used_for=('Products.Archetypes.Field.ReferenceField',
                         'Products.BiReference.BiReferenceField.BiReferenceField',)
)
