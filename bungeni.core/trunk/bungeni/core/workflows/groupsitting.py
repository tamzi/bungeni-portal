from bungeni.core.workflows import dbutils
from zope.security.proxy import removeSecurityProxy

class actions:

    @staticmethod
    def draftminutes(info, context):
        dbutils.set_real_order(removeSecurityProxy(context))
