from zope import interface
from zope import component
from zope.security.proxy import removeSecurityProxy
from zope.dublincore.interfaces import IDCDescriptiveProperties
from ore.alchemist import Session

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
        return "Group sitting #%d" % self.context.sitting_id

    @property
    def description(self):
        session = Session()
        group = session.query(domain.Group).selectone_by(
            group_id=self.context.group_id)
        return "Sitting scheduled for group '%s' from %s to %s." % (
            group.short_name, self.context.start_date, self.context.end_date)

class ItemScheduleDescriptiveProperties(DescriptiveProperties):
    component.adapts(interfaces.IItemSchedule)

    @property
    def title(self):
        return "Scheduled item #%d" % self.context.schedule_id

    @property
    def description(self):
        session = Session()
        sitting = session.query(domain.GroupSitting).selectone_by(
            sitting_id=self.context.sitting_id)
        return "scheduled for sitting (%s to %s)." % (
            sitting.start_date, sitting.end_date)

class VersionDescriptiveProperties(DescriptiveProperties):
    component.adapts(interfaces.IVersion)

    @property
    def title(self):
        if is_translation(self.context):
            language = get_language_by_name(self.context.language)
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
        #import pdb; pdb.set_trace()
        if context.user:
            return "%s %s %s" % (context.user.titles,
                context.user.first_name,
                context.user.last_name)
        else:
            return u"New User"
                    

               
