from bungeni.core.workflows import utils

class actions:
    @staticmethod
    def create(info, context):
        utils.setBillSubmissionDate( info, context )
        utils.setParliamentId(info, context)

    @staticmethod
    def submit(info, context):
        utils.setBillPublicationDate( info, context )
        utils.setSubmissionDate(info, context)
        #bill = removeSecurityProxy(context)
        #rpm = zope.securitypolicy.interfaces.IRolePermissionMap( bill )
        #rpm.grantPermissionToRole( 'bungeni.bill.view', u'bungeni.Everybody' )
        #rpm.denyPermissionToRole( 'bungeni.motion.edit', u'bungeni.Owner' )
        #rpm.denyPermissionToRole( 'bungeni.motion.delete', u'bungeni.Owner' )

    @staticmethod
    def withdraw(info, context):
        pass

    @staticmethod
    def schedule_first(info, context):
        pass

    @staticmethod
    def postpone_first(info, context):
        pass

