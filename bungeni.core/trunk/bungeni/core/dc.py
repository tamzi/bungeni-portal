from zope import interface
from zope import component
from zope.security.proxy import removeSecurityProxy
from zope.dublincore.interfaces import IDCDescriptiveProperties
from ore.alchemist import Session
from ore.alchemist.interfaces import IAlchemistContainer
from ore.alchemist.model import queryModelDescriptor

from bungeni.models import interfaces
from bungeni.models import domain
from bungeni.core.translation import is_translation
from bungeni.core.translation import get_language_by_name
from bungeni.core.i18n import _

class DublinCoreMetadataAdapter(object):
    """Generic dublin core metadata adapter which will retrieve
    metadata attributes lazily.

    Suitable for use as traversal path adapter (which can be used
    directly in templates using the ':' notation).
    """

    interfaces = IDCDescriptiveProperties,
    
    __slots__ = "context", "adapters"
    
    def __init__(self, context):
        self.context = context
        self.adapters = {}
        
    def __getattr__(self, attribute):
        for iface in self.interfaces:
            if attribute in iface.names():
                adapter = self.adapters.get(iface)
                if adapter is None:
                    adapter = self.adapters[iface] = iface(self.context)

                return getattr(adapter, attribute)

        raise AttributeError(attribute)

def get_descriptive_properties(context):
    return IDCDescriptiveProperties(context)

class DescriptiveProperties(object):
    interface.implements(IDCDescriptiveProperties)

    title = description = None
    
    def __init__(self, context):
        self.context = context
    
class QuestionDescriptiveProperties(DescriptiveProperties):
    component.adapts(interfaces.IQuestion)

    @property
    def title(self):
        if self.context.question_number is None:
            return self.context.short_name
            
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
        if self.context.identifier is None:
            return self.context.short_name
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
        if self.context.motion_number is None:
            return self.context.short_name
        return "#%d: %s" % (
            self.context.motion_number,
            self.context.short_name)

    @property
    def description(self):
        text = "Submitted by %s" % self.context.full_name

        if self.context.notice_date:
            text += ' (notice given on %s)' % self.context.notice_date

        return text + "."

class SittingDescriptiveProperties(DescriptiveProperties):
    component.adapts(interfaces.IGroupSitting)

    @property
    def title(self):
        return _(u"Sitting")

    @property
    def description(self):
        session = Session()
        group = session.query(domain.Group).selectone_by(
            group_id=self.context.group_id)
        return _(u"Sitting scheduled for '$group' ($start to $end).",
                 mapping={'group': group.short_name,
                          'start': self.context.start_date,
                          'end': self.context.end_date})

class ItemScheduleDescriptiveProperties(DescriptiveProperties):
    component.adapts(interfaces.IItemSchedule)

    @property
    def title(self):
        return _(u"Item scheduling")

    @property
    def description(self):
        session = Session()
        sitting = session.query(domain.GroupSitting).selectone_by(
            sitting_id=self.context.sitting_id)
        return _(u"Scheduled for sitting ($start to $end).",
                 mapping={'start': sitting.start_date,
                          'end': sitting.end_date})

class VersionDescriptiveProperties(DescriptiveProperties):
    component.adapts(interfaces.IVersion)

    @property
    def title(self):
        if is_translation(self.context):
            language = get_language_by_name(self.context.language)['name']
            return _(u"$language translation",
                     mapping={'language': language})

        return _(u"Version $version",
                 mapping={'version': self.context.version_id})
            
    @property
    def description(self):
        return _(u"Last modified $date.",
                 mapping={'date': self.context.change.date})
                 
class GroupDescriptiveProperties(DescriptiveProperties):
    component.adapts(interfaces.IBungeniGroup)          
    
    @property
    def title(self):
        return self.context.short_name

class ContainerDescriptiveProperties(DescriptiveProperties):
    component.adapts(IAlchemistContainer)

    @property
    def title(self):
        descriptor = queryModelDescriptor(self.context.domain_model)
        return descriptor.container_name
        
    @property
    def descrition(self):
        return u""        
    
class UserDescriptiveProperties(DescriptiveProperties):
    component.adapts(interfaces.IBungeniUser)
    
    @property
    def title(self):
        return "%s %s %s" % (self.context.titles,
                self.context.first_name,
                self.context.last_name)

class GroupMembershipDescriptiveProperties(DescriptiveProperties):
    component.adapts(interfaces.IBungeniGroupMembership)

    @property
    def title(self):
        context = removeSecurityProxy(self.context)
        if context.user:
            return "%s %s %s" % (context.user.titles,
                context.user.first_name,
                context.user.last_name)
        else:
            return u"New User"
            
class GroupSittingAttendanceDescriptiveProperties(DescriptiveProperties):
    component.adapts(interfaces.IGroupSittingAttendance)

    @property
    def title(self):
        context = removeSecurityProxy(self.context)
        if context.user:
            return "%s %s %s" % (context.user.titles,
                context.user.first_name,
                context.user.last_name)
        else:
            return u"New User"
            
class ParliamentSessionDescriptiveProperties(DescriptiveProperties):
    component.adapts(interfaces.IParliamentSession)  
    
    @property
    def title(self):
        return self.context.short_name   

class ScheduledItemDiscussionDescriptiveProperties(DescriptiveProperties):
    component.adapts(interfaces.IScheduledItemDiscussion)

    @property
    def title(self):
        time = self.context.sitting_time
        if time is not None:
            return _(u"Discussion ($time)",
                     mapping={'time': self.context.sitting_time})
        return _(u"Discussion")
        
