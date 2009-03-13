from zope import interface
from zope import component
from zope.dublincore.interfaces import IDCDescriptiveProperties

from bungeni.models import interfaces

class DescriptiveProperties(object):
    interface.implements(IDCDescriptiveProperties)

    title = description = None
    
    def __init__(self, context):
        self.context = context
    
class QuestionDescriptiveProperties(DescriptiveProperties):
    component.adapts(interfaces.IQuestion)

    @property
    def title(self):
        return "#%d: %s" % (
            self.context.question_number,
            self.context.short_name)

    @property
    def description(self):
        text = "Submitted by %s" % self.context.full_name

        if self.context.approval_date:
            text += ' (approved on %s)' % self.context.approval_date

        return text + "."

class BillDescriptiveProperties(DescriptiveProperties):
    component.adapts(interfaces.IBill)

    @property
    def title(self):
        return "#%d: %s" % (
            self.context.identifier,
            self.context.short_name)

    @property
    def description(self):
        text = "Submitted by %s" % self.context.full_name

        if self.context.publication_date:
            text += ' (published on %s)' % self.context.publication_date

        return text + "."

class MotionDescriptiveProperties(DescriptiveProperties):
    component.adapts(interfaces.IMotion)

    @property
    def title(self):
        return "#%d: %s" % (
            self.context.motion_number,
            self.context.short_name)

    @property
    def description(self):
        text = "Submitted by %s" % self.context.full_name

        if self.context.notice_date:
            text += ' (notice given on %s)' % self.context.notice_date

        return text + "."

