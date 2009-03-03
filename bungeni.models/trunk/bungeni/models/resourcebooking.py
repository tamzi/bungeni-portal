#!/usr/bin/env python
# encoding: utf-8
import datetime

import sqlalchemy.sql.expression as sql
from sqlalchemy.orm import mapper
import sqlalchemy as rdb

from ore.alchemist import Session

from bungeni.models import domain, schema

from i18n import _ 


bookedresources = rdb.join(schema.resources, schema.resourcebookings, 
                            schema.resources.c.resource_id == schema.resourcebookings.c.resource_id).join(
                            schema.sittings, 
                            schema.resourcebookings.c.sitting_id == schema.sittings.c.sitting_id)

class BookedResources( object ):
    """
    resources booked for a sitting
    """
    
mapper( BookedResources, bookedresources) 


def get_available_resources( start, end ):
    """
    get all resources that are not booked for a sitting
    in the given time period
    select * from resources where resource_id not in (
        select resource_id from resourceboookings, sittings
        where resourcebookings.sitting_id = sittings.sitting_id
        and (?start between sitting.start_date and sitting.end_date
            or ?end between sitting.start_date and sitting.end_date)   
    """
    assert( type(start) == datetime.datetime )
    assert( type(end) == datetime.datetime )  
    session = Session()
    start_end={'start': start, 'end':end}
    sql_booked_resources =  """
    SELECT resources.resource_id AS resources_resource_id
    FROM resources JOIN resourcebookings ON resources.resource_id = resourcebookings.resource_id 
                   JOIN group_sittings ON resourcebookings.sitting_id = group_sittings.sitting_id 
    WHERE group_sittings.start_date BETWEEN '%(start)s' AND '%(end)s' 
          OR group_sittings.end_date BETWEEN '%(start)s' AND '%(end)s'     
    """ % start_end 
    
    sql_resources = """
    SELECT resources_1.resource_id AS resources_1_resource_id
    FROM resources AS resources_1
    WHERE resources_1.resource_id NOT IN ( %s ) 
    """ % sql_booked_resources
    connection = session.connection( domain.Resource )                                              
    query = connection.execute(sql_resources)
    #query = session.query( domain.Resource ).filter(sql.not_(domain.Resource.resource_id.in_([1,2]) ) )       
    return query.fetchall()                   

def get_unavailable_resources( start, end ):
    """
    get all resources that are  booked 
    in the given time period
    """
    assert( type(start) == datetime.datetime )
    assert( type(end) == datetime.datetime )  
    session = Session()
    b_filter = sql.or_( 
                    sql.between(schema.sittings.c.start_date, start, end), 
                    sql.between(schema.sittings.c.end_date, start, end)
                    )
                    
    query = session.query(BookedResources).filter(b_filter)       
    return query.all()                        
    
def check_bookings( start, end, resource ):
    """
    return all sittings a resource is booked for
    in the period
    """    
    assert( type(resource) == domain.Resource )
    assert( type(start) == datetime.datetime )
    assert( type(end) == datetime.datetime )    
    session = Session()
    b_filter = sql.and_(
                    schema.resources.c.resource_id == resource.resource_id,
                    sql.or_( 
                        sql.between(schema.sittings.c.start_date, start, end), 
                        sql.between(schema.sittings.c.end_date, start, end)
                        )
                    )
    query = session.query(BookedResources).filter(b_filter)    
    return query.all()

                    
def check_availability( start, end, resource):
    """
    check if the resource is available 
    in the given period
    """
    assert( type(resource) == domain.Resource )
    assert( type(start) == datetime.datetime )
    assert( type(end) == datetime.datetime ) 
    return check_bookings( start, end, resource ) == []    

def book_resource( sitting, resource ):
    """
    book a resource for a sitting,
    check if the resource is available first
    """
    assert( type(sitting) == domain.GroupSitting)
    assert( type(resource) == domain.Resource )
    session = Session()
    # check if resource is allready boooked for this sitting
    cq = session.query( domain.ResourceBooking).filter( sql.and_(domain.ResourceBooking.resource_id == resource.resource_id,
                                                                    domain.ResourceBooking.sitting_id == sitting.sitting_id) )
    results = cq.all()
    if results:
        print "allready booked"
        return
        #nothing to do here it is already booked            
    
    if check_availability( sitting.start_date, sitting.end_date, resource):
        booking = domain.ResourceBooking()
        booking.resource_id = resource.resource_id
        booking.sitting_id = sitting.sitting_id 
        session.save(booking)
        session.flush()
        
    else:
        print "not available"
                        

def unbook_resource( sitting, resource ):
    """
    remove a resource from a sitting
    """
    assert( type(sitting) == domain.GroupSitting)
    assert( type(resource) == domain.Resource )
    session = Session()
    cq = session.query( domain.ResourceBooking).filter( sql.and_( domain.ResourceBooking.resource_id == resource.resource_id,
                                                                    domain.ResourceBooking.sitting_id == sitting.sitting_id ))
    results = cq.all()
    for result in results:
        session.delete(result)
        session.flush()

                    
    


