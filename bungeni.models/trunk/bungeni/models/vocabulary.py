"""
$Id: $
"""
import datetime
from zope import interface
from zope.schema.interfaces import IContextSourceBinder
from zope.schema import vocabulary
from zope.security.proxy import removeSecurityProxy
from zope.security import checkPermission

from ore.alchemist.vocabulary import DatabaseSource, ObjectSource, Session
from ore.alchemist.container import valueKey

#import ore.alchemist
from sqlalchemy.orm import mapper,  column_property 
import sqlalchemy as rdb
import sqlalchemy.sql.expression as sql
import schema, domain, utils, delegation

from i18n import _

#ModelTypeSource = ObjectSource( model.DataModelType, 'short_name', 'id')
#SecurityLevelSource = DatabaseSource( model.SecurityLevel, 'short_name', 'id' )



PoliticalParties  = ObjectSource( domain.PoliticalParty, 'full_name', "id")
ParliamentSessions = ObjectSource( domain.ParliamentSession, 'short_name', 'session_id')
QuestionType = vocabulary.SimpleVocabulary.fromItems( [(_(u"Ordinary"), "O"), (_(u"Private Notice"), "P")] )
ResponseType = vocabulary.SimpleVocabulary.fromItems( [(_("Oral"), "O"), (_(u"Written"), "W")] )
Gender = vocabulary.SimpleVocabulary.fromItems( [(_(u"Male"), "M"), (_(u"Female"), "F")] )
ElectedNominated = vocabulary.SimpleVocabulary.fromItems( [(_(u"elected"),'E'),(_(u"nominated") ,'N'), (_(u"ex officio"),'O')])
InActiveDead = vocabulary.SimpleVocabulary.fromItems([(_(u"active"),'A'),(_(u"inactive"), 'I'),(_(u"deceased"), 'D')])
ISResponse = vocabulary.SimpleVocabulary.fromItems([(_(u"initial"),'I'),(_(u"subsequent"), 'S'),])
OfficeType = vocabulary.SimpleVocabulary.fromItems( [(_(u"Speakers Office"), "S"), (_(u"Clerks Office"), "C")] )


Constituencies = ObjectSource( domain.Constituency, 'name', 'constituency_id')
Parliaments = ObjectSource(
    domain.Parliament, 'short_name', 'parliament_id',
    title_getter=lambda ob: "%s (%s-%s)" % (
        ob.full_name,
        ob.start_date and ob.start_date.strftime("%Y/%m/%d") or "?",
        ob.end_date and ob.end_date.strftime("%Y/%m/%d") or "?"))

ItemScheduleCategories = DatabaseSource(
    domain.ItemScheduleCategory, 'category_id', 'category_id', 'short_name')

SittingTypes = DatabaseSource(
    domain.SittingType, 'sitting_type', 'sitting_type_id',
    title_getter=lambda ob: "%s (%s-%s)" % (
        ob.sitting_type.capitalize(), ob.start_time, ob.end_time))

SittingTypeOnly = DatabaseSource(
    domain.SittingType, 
    title_field='sitting_type',
    token_field='sitting_type_id',
    value_field='sitting_type_id')


class SpecializedSource( object ):
    interface.implements( IContextSourceBinder )
    def __init__( self, token_field, title_field, value_field ):
        self.token_field = token_field
        self.value_field = value_field
        self.title_field = title_field

    def _get_parliament_id(self, context):
        trusted = removeSecurityProxy(context)
        parliament_id = getattr(trusted, 'parliament_id', None)
        if parliament_id is None:
            if trusted.__parent__ is None:
                return None
            else:    
                parliament_id = self._get_parliament_id(trusted.__parent__)            
        return parliament_id  
            
    def constructQuery( self, context ):
        raise NotImplementedError("Must be implemented by subclass.")
        
    def __call__( self, context=None ):
        query = self.constructQuery( context )
        results = query.all()
        
        terms = []
        title_field = self.title_field or self.token_field
        for ob in results:
            terms.append( 
                vocabulary.SimpleTerm( 
                    value = getattr( ob, self.value_field), 
                    token = getattr( ob, self.token_field),
                    title = getattr( ob, title_field) ,
                    ))
                    
        return vocabulary.SimpleVocabulary( terms )

class MemberOfParliament( object ):
    """ Member of Parliament = user join group membership"""
    
member_of_parliament = rdb.join( schema.user_group_memberships, 
                    schema.users,
                    schema.user_group_memberships.c.user_id == 
                    schema.users.c.user_id)    

mapper(MemberOfParliament, member_of_parliament)
        

class MemberOfParliamentImmutableSource(SpecializedSource):
    """if a user is allready assigned to the context 
    the user will not be editable """
    def __init__(self, value_field):
        self.value_field = value_field
                          
    def constructQuery(self, context):
        session= Session()
        trusted=removeSecurityProxy(context)
        user_id = getattr(trusted, self.value_field, None)
        if user_id:
            query = session.query( domain.User 
                    ).filter(domain.User.user_id == 
                        user_id).order_by(domain.User.last_name,
                            domain.User.first_name,
                            domain.User.middle_name)                                                                                                                 
            return query
        else:
            parliament_id = self._get_parliament_id(trusted)
            if parliament_id:
                query = session.query(MemberOfParliament).filter(
                    sql.and_(MemberOfParliament.group_id ==
                            parliament_id,
                            MemberOfParliament.active_p ==
                            True)).order_by(MemberOfParliament.last_name,
                            MemberOfParliament.first_name,
                            MemberOfParliament.middle_name) 
            else:
                query = session.query(MemberOfParliament).order_by(
                            MemberOfParliament.last_name,
                            MemberOfParliament.first_name,
                            MemberOfParliament.middle_name)                
        return query                                                                                                           

    def __call__( self, context=None ):
        query = self.constructQuery( context )
        results = query.all()        
        terms = []
        for ob in results:
            terms.append( 
                vocabulary.SimpleTerm( 
                    value = getattr( ob, 'user_id'), 
                    token = getattr( ob, 'user_id'),
                    title = "%s %s" % (getattr( ob, 'first_name') ,
                            getattr( ob, 'last_name'))
                    ))
        user_id = getattr(context, self.value_field, None) 
        if user_id:
            if len(query.filter(schema.users.c.user_id == user_id).all()) == 0:
                # The user is not a member of this parliament. 
                # This should not happen in real life
                # but if we do not add it her the view form will 
                # throw an exception 
                session = Session()            
                ob = session.query(domain.User).get(user_id)
                terms.append( 
                vocabulary.SimpleTerm( 
                    value = getattr( ob, 'user_id'), 
                    token = getattr( ob, 'user_id'),
                    title = "(%s %s)" % (getattr( ob, 'first_name') ,
                            getattr( ob, 'last_name'))
                    ))
        return vocabulary.SimpleVocabulary( terms )

class MemberOfParliamentSource(MemberOfParliamentImmutableSource):
    """ you may change the user in this context """
    def constructQuery(self, context):
        session= Session()
        trusted=removeSecurityProxy(context)
        user_id = getattr(trusted, self.value_field, None)
        parliament_id = self._get_parliament_id(trusted)        
        if user_id:
            if parliament_id:
                query = session.query( MemberOfParliament
                        ).filter(
                        sql.or_(
                        sql.and_(MemberOfParliament.user_id == user_id,
                                MemberOfParliament.group_id ==
                                parliament_id),
                        sql.and_(MemberOfParliament.group_id ==
                                parliament_id,
                                MemberOfParliament.active_p ==
                                True)                     
                        )).order_by(
                            MemberOfParliament.last_name,
                            MemberOfParliament.first_name,
                            MemberOfParliament.middle_name).distinct()                                                                                                                       
                return query
            else:
                query = session.query(MemberOfParliament).order_by(
                            MemberOfParliament.last_name,
                            MemberOfParliament.first_name,
                            MemberOfParliament.middle_name)                 
        else:
            if parliament_id:
                query = session.query(MemberOfParliament).filter(                    
                    sql.and_(MemberOfParliament.group_id ==
                            parliament_id,
                            MemberOfParliament.active_p ==
                            True)).order_by(
                                MemberOfParliament.last_name,
                                MemberOfParliament.first_name,
                                MemberOfParliament.middle_name)
            else:
                query = session.query(MemberOfParliament).order_by(
                            MemberOfParliament.last_name,
                            MemberOfParliament.first_name,
                            MemberOfParliament.middle_name)                
        return query   

class MemberOfParliamentDelegationSource(MemberOfParliamentSource):
    """ A logged in User will only be able to choose
    himself if he is a member of parliament or those 
    Persons who gave him rights to act on his behalf"""
    def constructQuery(self, context):
        mp_query = super(MemberOfParliamentDelegationSource, 
                self).constructQuery(context)
        #XXX clerks cannot yet choose MPs freely                
        user_id = utils.get_db_user_id()
        if user_id:            
            user_ids=[user_id,]
            for result in delegation.get_user_delegations(user_id):
                user_ids.append(result.user_id)
            query = mp_query.filter(
                domain.MemberOfParliament.user_id.in_(user_ids))                        
            if len(query.all()) > 0:                
                return query
        return mp_query
                       

class MinistrySource(SpecializedSource):
    """ Ministries in the current parliament """

    def __init__(self, value_field):
        self.value_field = value_field    
    
    def constructQuery( self, context):
        session= Session()
        trusted=removeSecurityProxy(context)
        ministry_id = getattr(trusted, self.value_field, None)
        parliament_id = self._get_parliament_id(trusted)
        today = datetime.date.today()   
        if parliament_id:
            governments = session.query(domain.Government).filter(
                sql.and_(
                    domain.Government.parent_group_id == parliament_id,
                    sql.or_( 
                        sql.and_(
                            domain.Government.start_date <= today,
                            domain.Government.end_date == None
                            ),
                        sql.between(today, 
                                domain.Government.start_date,
                                domain.Government.end_date)                        
                        )
                    ))  
            government = governments.all()
            if len(government) == 1:
                gov_id = government[0].group_id
                if ministry_id:
                    query = session.query(domain.Ministry).filter(
                        sql.or_(
                            domain.Ministry.group_id == ministry_id,
                            sql.and_(
                                domain.Ministry.parent_group_id == gov_id,
                                sql.or_( 
                                    sql.and_(
                                        domain.Ministry.start_date <= today,
                                        domain.Ministry.end_date == None
                                        ),
                                    sql.between(today, 
                                            domain.Ministry.start_date,
                                            domain.Ministry.end_date)                        
                                    )
                                ))  
                    )
                else:
                    query = session.query(domain.Ministry).filter(
                            sql.and_(
                                domain.Ministry.parent_group_id== gov_id,
                                sql.or_( 
                                    sql.and_(
                                        domain.Ministry.start_date <= today,
                                        domain.Ministry.end_date == None
                                        ),
                                    sql.between(today, 
                                            domain.Ministry.start_date,
                                            domain.Ministry.end_date)                        
                                    )
                                ))                                                       
            else:
                if ministry_id:
                    query = session.query(domain.Ministry).filter(
                            domain.Ministry.group_id == ministry_id)                          
                else:                    
                    query = session.query(domain.Ministry)            
        else:
            query = session.query(domain.Ministry)
        return query     
               
    def __call__( self, context=None ):
        query = self.constructQuery( context )
        results = query.all()        
        terms = []
        for ob in results:
            terms.append( 
                vocabulary.SimpleTerm( 
                    value = getattr( ob, 'group_id'), 
                    token = getattr( ob, 'group_id'),
                    title = "%s - %s" % (getattr( ob, 'short_name') ,
                            getattr( ob, 'full_name'))
                    ))

        return vocabulary.SimpleVocabulary( terms )                

class MemberTitleSource(SpecializedSource):
    """ get titles (i.e. roles/functions) in the current context """
    
    def __init__(self, value_field):
        self.value_field = value_field 
    
    def _get_user_type(self, context):
        user_type = getattr(context, 'membership_type', None)
        if not user_type:            
            user_type = self._get_user_type(context.__parent__)                        
        return user_type
    
    def constructQuery( self, context):
        session= Session()
        trusted=removeSecurityProxy(context)
        user_type = self._get_user_type(trusted)  
        titles = session.query(domain.MemberTitle).filter(
            domain.MemberTitle.user_type == user_type).order_by(
                domain.MemberTitle.sort_order)
        return titles

    def __call__( self, context=None ):
        query = self.constructQuery( context )
        results = query.all()        
        terms = []
        for ob in results:
            terms.append( 
                vocabulary.SimpleTerm( 
                    value = getattr( ob, 'user_role_type_id'), 
                    token = getattr( ob, 'user_role_type_id'),
                    title = getattr( ob, 'user_role_name'),
                    ))
        return vocabulary.SimpleVocabulary( terms )  

                    
class UserSource(SpecializedSource):
    """ All active users """
    def constructQuery( self, context):
        session= Session()
        
        users = session.query(domain.User).order_by(
                domain.User.last_name, domain.User.first_name)
        return users    
    

class UserNotMPSource(SpecializedSource):
    """ All users that are NOT a MP """
        
    def constructQuery( self, context):
        session= Session()    
        trusted=removeSecurityProxy(context)
        parliament_id = self._get_parliament_id(trusted)
        #connection = session.connection(domain.Parliament)
        mp_user_ids = sql.select([schema.user_group_memberships.c.user_id], 
            schema.user_group_memberships.c.group_id == parliament_id)
        query = session.query(domain.User).filter( sql.and_(
            sql.not_(domain.User.user_id.in_( mp_user_ids)),
            domain.User.active_p == 'A')).order_by(
                domain.User.last_name, domain.User.first_name)
        return query                       

    def __call__( self, context=None ):
        query = self.constructQuery( context )
        results = query.all()        
        terms = []
        for ob in results:
            terms.append( 
                vocabulary.SimpleTerm( 
                    value = getattr( ob, 'user_id'), 
                    token = getattr( ob, 'user_id'),
                    title = "%s %s" % (getattr( ob, 'first_name') ,
                            getattr( ob, 'last_name'))
                    ))
        user_id = getattr(context, self.value_field, None) 
        if user_id:
            if len(query.filter(domain.GroupMembership.user_id == user_id).all()) == 0:
                # The user is not a member of this group. 
                # This should not happen in real life
                # but if we do not add it her the view form will 
                # throw an exception 
                session = Session()            
                ob = session.query(domain.User).get(user_id)
                terms.append( 
                vocabulary.SimpleTerm( 
                    value = getattr( ob, 'user_id'), 
                    token = getattr( ob, 'user_id'),
                    title = "(%s %s)" % (getattr( ob, 'first_name') ,
                            getattr( ob, 'last_name'))
                    ))
        return vocabulary.SimpleVocabulary( terms )



class UserNotStaffSource(SpecializedSource):
    """ all users that are NOT staff """
    def constructQuery( self, context):
        session= Session()
        
        
class SubstitutionSource(SpecializedSource):
    """ active user of the same group """
    def _get_group_id(self, context):
        trusted = removeSecurityProxy(context)        
        group_id = getattr(trusted,'group_id', None)
        if not group_id:
             group_id = getattr(trusted.__parent__,'group_id', None)
        return group_id

    def _get_user_id(self, context):
        trusted = removeSecurityProxy(context)        
        user_id = getattr(trusted,'user_id', None)
        if not user_id:
             user_id = getattr(trusted.__parent__,'user_id', None)
        return user_id

                     
    def constructQuery( self, context):
        session= Session()
        query = session.query(domain.GroupMembership).order_by(
            'last_name', 'first_name').filter(
            domain.GroupMembership.active_p == True)
        user_id = self._get_user_id(context)     
        if user_id:
             query = query.filter(
                domain.GroupMembership.user_id != user_id)
        group_id = self._get_group_id(context)
        if group_id:
            query = query.filter(
                domain.GroupMembership.group_id == group_id)
        return query                
                    
        
        
    def __call__( self, context=None ):
        query = self.constructQuery( context )
        results = query.all()        
        tdict = {}
        for ob in results:
            tdict[getattr( ob.user, 'user_id')] = "%s %s" % (
                    getattr( ob.user, 'first_name') ,
                    getattr( ob.user, 'last_name'))
        user_id = getattr(context, 'replaced_id', None) 
        if user_id:
            if len(query.filter(domain.GroupMembership.replaced_id == user_id).all()) == 0:
                session = Session()            
                ob = session.query(domain.User).get(user_id)
                tdict[getattr( ob, 'user_id')] = "%s %s" % (
                            getattr( ob, 'first_name') ,
                            getattr( ob, 'last_name'))
        terms = []
        for t in tdict.keys():
            terms.append( 
                vocabulary.SimpleTerm( 
                    value = t, 
                    token = t,
                    title = tdict[t]
                    ))        
        return vocabulary.SimpleVocabulary( terms )

class PartyMembership(object):
    pass




party_membership = sql.join(schema.political_parties, schema.groups,
                schema.political_parties.c.party_id == schema.groups.c.group_id).join(
                   schema.user_group_memberships,
                  schema.groups.c.group_id == schema.user_group_memberships.c.group_id)

mapper(PartyMembership,party_membership)

class BillSource(SpecializedSource):  
    
    def constructQuery( self, context):
        session= Session()
        trusted=removeSecurityProxy(context)
        parliament_id = self._get_parliament_id(context)
        query = session.query(domain.Bill).filter(
            sql.and_(
            sql.not_(domain.Bill.status.in_(
                ['draft','withdrawn','approved','rejected'])),
            domain.Bill.parliament_id == parliament_id))
        return query                
                
class CommitteeSource(SpecializedSource):  

    def constructQuery( self, context):
        session= Session()
        trusted=removeSecurityProxy(context)
        parliament_id = self._get_parliament_id(context)
        query = session.query(domain.Committee).filter(
            sql.and_(
            domain.Committee.status == 'active',
            domain.Committee.parent_group_id == parliament_id))
        return query                



class MotionPartySource(SpecializedSource):    

    def constructQuery( self, context):
        session= Session()
        trusted=removeSecurityProxy(context)
        user_id = getattr(trusted, 'owner_id', None)
        if user_id is None:
            user_id = utils.get_db_user_id()
        parliament_id = self._get_parliament_id(context)
        
        if user_id: 
            query = session.query(PartyMembership
                ).filter(
                    sql.and_(PartyMembership.active_p ==True,
                        PartyMembership.user_id == user_id,
                        PartyMembership.parent_group_id == parliament_id)
                        )
        else:
            query = session.query(PartyMembership).filter(                    
                        PartyMembership.parent_group_id == parliament_id)
        return query                        
        

class QuerySource( object ):
    """ call a query with an additonal filter and ordering
    note that the domain_model *must* not have a where and order_by clause 
    (otherwise the parameters passed to this query will be ignored),
    the order_by and filter_field fields *must* be public attributes"""
    interface.implements( IContextSourceBinder )
    
    def getValueKey(self, context):
        """iterate through the parents until you get a valueKey """
        if context.__parent__ is None:
            return None
        else:            
            try:
                value_key = valueKey( context.__parent__.__name__ )[0]
            except:
                value_key = self.getValueKey( context.__parent__)
        return value_key         
        
        
    def __init__( self, 
                    domain_model, 
                    token_field, 
                    title_field, 
                    value_field, 
                    filter_field, 
                    filter_value=None, 
                    order_by_field=None,  ):
        self.domain_model = domain_model
        self.token_field = token_field
        self.value_field = value_field
        self.title_field = title_field
        self.filter_field = filter_field
        self.order_by_field = order_by_field
        self.filter_value = filter_value
        
    def constructQuery( self, context ):
        session = Session()
        trusted=removeSecurityProxy(context)
        #pdb.set_trace() 
        if self.filter_value:       
            query = session.query( self.domain_model ).filter(
                self.domain_model.c[self.filter_field] == 
                trusted.__dict__[self.filter_value] )
        else:
            #pfk = valueKey( context.__parent__.__parent__.__name__ )[0]
            pfk = self.getValueKey(context)
            query = session.query( self.domain_model )
            #pdb.set_trace()
            query = query.filter(self.domain_model.c[self.filter_field] == pfk )
            
        query = query.distinct()
        if self.order_by_field:
            query = query.order_by(self.domain_model.c[self.order_by_field])
            
            
        return query
        
    def __call__( self, context=None ):
        query = self.constructQuery( context )
        results = query.all()
        
        terms = []
        title_field = self.title_field or self.token_field
        for ob in results:
            terms.append( 
                vocabulary.SimpleTerm( 
                    value = getattr( ob, self.value_field), 
                    token = getattr( ob, self.token_field),
                    title = getattr( ob, title_field) ,
                    ))
                    
        return vocabulary.SimpleVocabulary( terms )



    



                      
        
        
        
