from zope import interface
from zope import component
from zope.security.proxy import removeSecurityProxy
from zope.dublincore.interfaces import IDCDescriptiveProperties
from ore.alchemist import Session
from ore.alchemist.interfaces import IAlchemistContainer
from ore.alchemist.model import queryModelDescriptor

#from marginalia.interfaces import IMarginaliaAnnotation

from bungeni.models import interfaces
from bungeni.models import domain
from bungeni.models import vocabulary
from bungeni.core.translation import is_translation
from bungeni.core.translation import get_language_by_name
from bungeni.core.i18n import _

from zope.securitypolicy.interfaces import IPrincipalRoleMap


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
        #prm = IPrincipalRoleMap(self.context)
        context = removeSecurityProxy(self.context)
        if context.question_number is None:
            return context.short_name
            
        return "#%d: %s" % (
            context.question_number,
            context.short_name)

    @property
    def description(self):
        text = "Submitted by %s" % self.context.owner.first_name + ' ' + \
               self.context.owner.last_name

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
        text = "Submitted by %s" % self.context.owner.first_name + ' ' + \
               self.context.owner.last_name

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
        text = "Submitted by %s" %  self.context.owner.first_name + ' ' + \
               self.context.owner.last_name

        if self.context.notice_date:
            text += ' (notice given on %s)' % self.context.notice_date

        return text + "."

class SittingDescriptiveProperties(DescriptiveProperties):
    component.adapts(interfaces.IGroupSitting)

    @property
    def title(self):
        return _(u"Sitting: $group ($start to $end)",
                 mapping={'group': self.context.group.short_name,
                          'start': self.context.start_date.strftime('%Y-%m-%d %H:%M'),
                          'end': self.context.end_date.strftime('%H:%M')})

    @property
    def description(self):
        session = Session()
        return _(u"Sitting scheduled for '$group' ($start to $end).",
                 mapping={'group': self.context.group.short_name,
                          'start': self.context.start_date.strftime('%Y-%m-%d %H:%M'),
                          'end': self.context.end_date.strftime('%H:%M')})

class ItemScheduleDescriptiveProperties(DescriptiveProperties):
    component.adapts(interfaces.IItemSchedule)

    @property
    def title(self):
        return _(u"Item scheduling")

    @property
    def description(self):
        session = Session() 
        trusted = removeSecurityProxy(self.context)
        session.add(trusted)
        sitting = self.context.sitting                             
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
        session = Session()
        trusted = removeSecurityProxy(self.context)
        session.add(trusted)
        return "%s - %s" %(
            #self.context.type.capitalize(),
            self.context.short_name,
            self.context.full_name)           

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

    @property
    def description(self):            
        return u""

            
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
    @property
    def description(self):            
        session = Session()
        trusted = removeSecurityProxy(self.context)
        session.add(trusted)
        return self.context.attendance_type.attendance_type



class ConsignatoryDescriptiveProperties(DescriptiveProperties):
    component.adapts(interfaces.IConsignatory)

    @property
    def title(self):
        context = removeSecurityProxy(self.context)
        if context.user:
            return "%s %s %s" % (context.user.titles,
                context.user.first_name,
                context.user.last_name)
        else:
            return u"New User"
    @property
    def description(self):            
       return u""

            
class ParliamentSessionDescriptiveProperties(DescriptiveProperties):
    component.adapts(interfaces.IParliamentSession)  
    
    @property
    def title(self):
        return self.context.short_name   

    @property
    def description(self):            
        return self.context.full_name   
                
class ConstituencyDescriptiveProperties(DescriptiveProperties):
    component.adapts(interfaces.IConstituency)  
    
    @property
    def title(self):
        return self.context.name         
        
    @property
    def description(self):            
        session = Session()
        trusted = removeSecurityProxy(self.context)
        session.add(trusted)
        return u"%s - %s -%s" %( self.context.name,
            self.context.province.province,
            self.context.region.region)
                                

class ScheduledItemDiscussionDescriptiveProperties(DescriptiveProperties):
    component.adapts(interfaces.IScheduledItemDiscussion)

    @property
    def title(self):
        time = self.context.sitting_time
        if time is not None:
            return _(u"Discussion ($time)",
                     mapping={'time': self.context.sitting_time})
        return _(u"Discussion")

    @property
    def description(self):            
        return u""

class SittingTypeDescriptiveProperties(DescriptiveProperties):
    component.adapts(interfaces.ISittingType)

    @property
    def title(self):
        term = vocabulary.SittingTypes(self.context).getTermByToken(
            self.context.sitting_type)

        return _(term.title.split('(')[0].strip())
    @property
    def description(self):            
        return u""
        
class ChangeDescriptiveProperties(DescriptiveProperties):
    component.adapts(interfaces.IChange)  
    
    @property
    def title(self):
        return self.context.action   
    @property
    def description(self):            
        return u""  

class UserAddressDescriptiveProperties(DescriptiveProperties):
    component.adapts(interfaces.IUserAddress)  
    
    @property
    def title(self):
        return u"Address"   

    @property
    def description(self):            
        return u""
        
#class MarginaliaDescriptiveProperties(DescriptiveProperties):
#    component.adapts(IMarginaliaAnnotation)  
#    
#    @property
#    def title(self):
#        return u"Marginalia"   
        
class AgendaItemDescriptiveProperties(DescriptiveProperties):
    component.adapts(interfaces.IAgendaItem)

    @property
    def title(self):
        context = removeSecurityProxy(self.context)
        session = Session()
        session.add(context)  
        return u"%s - %s" % (context.short_name, context.group.short_name)

            
class TabledDocumentDescriptiveProperties(DescriptiveProperties):
    component.adapts(interfaces.ITabledDocument)
    
    @property
    def title(self):    
        return self.context.short_name
    @property
    def description(self):            
        return u""

class ConstituencyDetailsDescriptiveProperties(DescriptiveProperties):
    component.adapts(interfaces.IConstituencyDetail)
    
    @property
    def title(self):  
        return '%s - %i' % (self.context.constituency.name,
            self.context.date.year)

    @property
    def description(self):            
        return u""

class GroupItemAssignmentDescriptiveProperties(DescriptiveProperties):
    component.adapts(interfaces.IGroupItemAssignment)
    
    @property
    def title(self):  
        return '%s - %s ' % (self.context.item.short_name, self.context.group.short_name)

    @property
    def description(self):            
        return u""

class MemberRoleTitleDescriptiveProperties(DescriptiveProperties):                        
    component.adapts(interfaces.IMemberRoleTitle)
    
    @property
    def title(self): 
        context = removeSecurityProxy(self.context)
        return context.title_name.user_role_name                                   

    @property
    def description(self):            
        return u""


class ReportDescriptiveProperties(DescriptiveProperties):                        
    component.adapts(interfaces.IReport)
    
    @property
    def title(self): 
        context = removeSecurityProxy(self.context)
        session = Session()
        session.add(context)        
        return u'%s: %s - %s' %(context.group.short_name, 
            context.start_date, context.end_date)                                  

    @property
    def description(self):        
        context = removeSecurityProxy(self.context)
        session = Session()
        session.add(context)           
        return u"Created on %s by %s" %( context.created_date.strftime('%Y-%m-%d'),
            context.user_id)

class ItemScheduleCategoryDescriptiveProperties(DescriptiveProperties):                        
    component.adapts(interfaces.IItemScheduleCategory)         
    
    @property
    def title(self):    
        return self.context.short_name
           
    @property
    def description(self):            
        return u""
    
class UserDelegationDescriptiveProperties(DescriptiveProperties):                        
    component.adapts(interfaces.IUserDelegation)         
    
    @property
    def title(self):    
        context = removeSecurityProxy(self.context)
        session = Session()
        session.add(context)      
        if getattr(context, 'delegation', None):
            return u'%s %s' % (context.delegation.first_name,
                context.delegation.last_name)
        else:
            return u""                
           
    @property
    def description(self):            
        return u""    
