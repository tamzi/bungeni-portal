import time

from zope import interface
from zope import component

from bungeni.core.interfaces import ISchedulingContext
from bungeni.core.globalsettings import getCurrentParliamentId
from bungeni.models.interfaces import IBungeniApplication
from bungeni.models.domain import GroupSitting
from bungeni.models.domain import Group

from ore.alchemist import Session

def format_date(date):
    return time.strftime("%Y-%m-%d %H:%M:%S", date.timetuple())
                  
class PrincipalGroupSchedulingContext(object):
    interface.implements(ISchedulingContext)

    group_id = None

    def __init__(self, context):
        self.__parent__ = context

    def get_group(self):
        session = Session()

        return session.query(Group).filter_by(
            group_id=self.group_id)[0]

    def get_sittings_container(self):
        group = self.get_group()
        return group.sittings

    def get_sittings(self, start_date=None, end_date=None):
        session = Session()

        if start_date is None and end_date is None:
            return session.query(GroupSitting).filter_by(
                group_id=self.group_id)
            
        assert start_date and end_date

        query = session.query(GroupSitting).filter(
            "group_id=:group_id and start_date>:start_date and end_date<:end_date")

        return query.params(
            group_id=self.group_id,
            start_date=format_date(start_date),
            end_date=format_date(end_date))
    
class PlenarySchedulingContext(PrincipalGroupSchedulingContext):
    component.adapts(IBungeniApplication)

    @property
    def group_id(self):
        """Return current parliament's group id."""

        return getCurrentParliamentId()
        
