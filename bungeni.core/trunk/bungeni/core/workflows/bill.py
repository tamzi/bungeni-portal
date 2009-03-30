from bungeni.core.workflows import utils
from bungeni.core.workflows import dbutils

class conditions:
    @staticmethod
    def is_scheduled(info, context):
        return dbutils.isItemScheduled(context.bill_id)

class actions:
    @staticmethod
    def create(info, context):
        utils.setBillSubmissionDate( info, context )
        utils.setParliamentId(info, context)

    @staticmethod
    def submit(info, context):
        utils.setBillPublicationDate( info, context )
        utils.setSubmissionDate(info, context)


    @staticmethod
    def withdraw(info, context):
        pass

    @staticmethod
    def schedule_first(info, context):
        pass

    @staticmethod
    def postpone_first(info, context):
        pass

