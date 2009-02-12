
from AccessControl import ClassSecurityInfo
from OFS.Cache import Cacheable

from Products.PlonePAS.plugins.group import PloneGroup
from Products.PlonePAS.interfaces import group as IPloneGroups
from Products.PageTemplates.PageTemplateFile import PageTemplateFile

from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PluggableAuthService.utils import classImplements
from Products.PluggableAuthService.interfaces.plugins import (IGroupsPlugin,
                                                              IGroupEnumerationPlugin)

#from zope import component
from datetime import datetime
import sqlalchemy as rdb
import schema

manage_addBungeniGroupManagerForm = PageTemplateFile('zmi/group-plugin-add.pt', globals())

def manage_addBungeniGroupManager(self, id, db_utility, title='', REQUEST=None):
    """Add a GroupManager to a Pluggable Auth Service.
    """
    rm = GroupManager(id, db_utility, title)
    self._setObject( id, rm)
    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect(
                                '%s/manage_workspace'
                                '?manage_tabs_message='
                                'BungeniGroupManager+added.'
                            % self.absolute_url())

class GroupManager( BasePlugin, Cacheable ):

    meta_type = "Bungeni Group Manager"

    security = ClassSecurityInfo()

    
    def __init__(self, id, title=None):
        self.id = self.id = id
        self.title = title

    #
    # IGroupsPlugin implementation
    #
    
    def getGroupsForPrincipal( self, principal, request=None ):
        """ principal -> ( group_1, ... group_N )

        o Return a sequence of group names to which the principal 
          (either a user or another group) belongs.

        o May assign groups based on values in the REQUEST object, if present
        """
        res = rdb.select( [ schema.groups.c.short_name ],
                          rdb.and_( schema.users.c.login == principal,
                                    schema.user_group_memberships.c.user_id == schema.users.c.user_id,
#                                    schema.groups.c.end_date >= datetime.now(),
                                    schema.groups.c.group_id == schema.user_group_memberships.c.group_id ) ).execute()
        return [ r[0] for r in res]
    #
    # IGroupsEnumeration implementation
    #        

    def enumerateGroups( self, id=None
                       , exact_match=False
                       , sort_by=None
                       , max_results=None
                       , **kw
                       ):
        """ see IGroupEnumeration """
        if id is None:
            clause = None
        elif isinstance( id, (list, tuple)) and exact_match:
            statements = []
            for i in id:
                statements.append( schema.groups.c.short_name == i )
            clause = rdb.or_( *statements )
        elif isinstance( id, (list, tuple)) and not exact_match:
            clause = rdb.or_(*(map( schema.groups.c.short_name.contains, id )))
        elif not exact_match:
            clause = schema.groups.c.short_name.contains( id )
        else:
            clause = schema.groups.c.short_name == id


        query = rdb.select( [ schema.groups.c.short_name ] )
        if clause:
            query = query.where( clause )
        if sort_by:
            assert sort_by in ('group_id', 'short_name')
            query = query.order_by( getattr( schema.groups.c, sort_by ) )

        if max_results is not None and isinstance( max_results, int ):
            query = query.limit( max_results )

        return [ dict( id=r[0], plugin=self.id ) for r in query.execute()]

    ####################
    # IGroupManagement 
    ####################
    
    def addGroup(self, id, **kw):
        """
        Create a group with the supplied id, roles, and groups.
        return True if the operation suceeded
        """
        insert = schema.groups.insert()
        insert.values( short_name = id,
                       full_name = kw.get('title',''),
                       description = kw.get('description', ''),
                       start_date = datetime.now(),
                       type = "group",
                       ).execute()
        return True
        
    def addPrincipalToGroup(self, principal_id, group_id):
        """
        Add a given principal to the group.
        return True on success
        """
        insert = schema.user_group_memberships.insert()
        group_id = self._gid( group_id )
        user_id  = self._uid( principal_id )
        if not group_id or not user_id:
            raise KeyError( "Invalid user %s or group %s"%( user_id, group_id ) )
        insert.values( group_id = group_id, user_id = user_id ).execute()
        return True

    def updateGroup(self, id, **kw):
        """
        Edit the given group. plugin specific
        return True on success
        """
        d = {}
        if 'title' in kw:
            d['full_name'] = kw['title']
        if 'description' in kw:
            d['description'] = kw['description']

        if not d:
            return True
        
        group_id = rdb.select( [schema.groups.c.group_id], schema.groups.c.short_name == id ).one()
        schema.groups.update( schema.c.group_id == group_id ).values( **d )
        return True

    def setRolesForGroup(self, group_id, roles=()):
        """
        set roles for group
        return True on success
        """
        # why the heck is this even in the group api ? silly enfold developers.. tricks are for kids
        raise NotImplemented


    #
    #   IDeleteCapability implementation
    #
    def allowDeletePrincipal(self, principal_id):
        """True iff this plugin can delete a certain group."""
        if self.getGroupById(principal_id):
            return True
        return False

    #
    #   IGroupCapability implementation
    #
    def allowGroupAdd(self, user_id, group_id):
        """True iff this plugin will allow adding a certain user to a certain group."""
        present = self.enumerateGroups(id=group_id)
        if present: return True   # if we have a group, we can add users to it
                                  # slightly naive, but should be okay.
        return False

    def allowGroupRemove(self, user_id, group_id):
        """True iff this plugin will allow removing a certain user from a certain group."""
        present = self._gid(group_id)
        if not present: return False   # if we don't have a group, we can't do anything
        
        groups = self.getGroupsForPrincipal(user_id)
        if group_id in groups: return True
        return False

    def removeGroup(self, group_id):
        """
        Remove the given group
        return True on success
        """
        # XXX also need to delete all memberships in the group, just set group as inactive
        gid = self._gid( group_id )
        schema.groups.delete().where( schema.groups.c.group_id == gid ).execute()

    def removePrincipalFromGroup(self, principal_id, group_id):
        """
        remove the given principal from the group
        return True on success
        """
        group_id = self._gid( group_id )
        user_id  = self._uid( principal_id )
        if not group_id or not user_id:
            return False
        ugm = schema.user_group_memberships
        schema.user_group_memberships.delete().where(
            rdb.and_( ugm.c.user_id == user_id, ugm.c.group_id == group_id )
            ).execute()
                
        return True
    
    ###########################
    # IGroupIntrospection
    ###########################
    def _gid( self, name ):
        res = rdb.select( [schema.groups.c.group_id ], schema.groups.c.short_name == name ).execute()
        gid_tuple = res.fetchone()
        if not gid_tuple:
            return None
        return gid_tuple[0]

    def _uid( self, login):
        cols = [ schema.users.c.user_id ]
        res = rdb.select( cols,
                          rdb.and_( schema.users.c.login == login,
                                    schema.users.c.active_p == 'A' )).execute()
                       
        uid_tuple = res.fetchone()
        if not uid_tuple:
            return None
        return uid_tuple[0]
    
    def getGroupById(self, group_id):
        """
        Returns the portal_groupdata-ish object for a group
        corresponding to this id.
        """
        gid = self._gid( group_id )
        if not gid:
            return None
        return PloneGroup( group_id ).__of__( self )

    #################################
    # these interface methods are suspect for scalability.
    #################################

    def getGroups( self ):
        """
        Returns an iteration of the available groups
        """
        
        res = rdb.select( [ schema.groups.c.short_name ],
                          #schema.groups.c.end_date > datetime.now()
                          ).execute()
        return [ PloneGroup(r[0]).__of__(self) for r in res]
        
    def getGroupIds( self ):
        """
        Returns a list of the available groups
        """
        res = rdb.select( [ schema.groups.c.short_name ],
                          #schema.groups.c.end_date > datetime.now()
                          ).execute()
        return [r[0] for r in res]

    def getGroupMembers(self, group_id):
        """
        return the members of the given group
        """
        ugm = schema.user_group_memberships
        res = rdb.select( [ schema.users.c.login ],
                          rdb.and_( schema.users.c.user_id == ugm.c.user_id,
                                    schema.groups.c.group_id == ugm.c.group_id,
                                    schema.groups.c.short_name == group_id ) ).execute()
        return [ r[0] for r in res]

            
classImplements( GroupManager,
                 IGroupsPlugin,
                 IGroupEnumerationPlugin,
                 IPloneGroups.IGroupIntrospection,
                 IPloneGroups.IGroupManagement )
