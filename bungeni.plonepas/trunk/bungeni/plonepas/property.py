

class PropertyProvider( object ):


    def getPropertiesForUser(self, user, request=None):
        """Get property values for a user or group.

        Returns a dictionary of values or a PropertySheet.
        """
        pass

    #
    # IMutablePropertiesPlugin implementation
    #
    def setPropertiesForUser(self, user, propertysheet):
        pass
    
