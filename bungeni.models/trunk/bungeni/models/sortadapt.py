from sqlalchemy import sql
from bungeni.models import domain
from bungeni.models import schema

def sort_on_partymember():
#sort on ['last_name', 'first_name', 'middle_name']
    pass

def sort_replace_partymember(sort_key):
#sort replace {'user_id': ['last_name', 'first_name']}
    pass

def sort_on_parliamentsession():
#sort on ['start_date']
    pass

def sort_on_motion():
#sort on ['motion_number', 'submission_date']
    pass

def sort_replace_motion(sort_key):
#sort replace {'owner_id': ['last_name', 'first_name']}
    pass

def sort_replace_parliamentaryitem(sort_key):
#sort replace {'owner_id': ['last_name', 'first_name']}
    pass

def sort_on_question():
#sort on ['question_number', 'submission_date']
    pass

def sort_replace_question(sort_key):
#sort replace {'owner_id': ['last_name', 'first_name']}
    pass

def sort_on_committeestaff():
#sort on ['last_name', 'first_name', 'middle_name']
    pass

def sort_replace_committeestaff(sort_key):
#sort replace {'user_id': ['last_name', 'first_name']}
    pass

def sort_on_committeemember():
#sort on ['last_name', 'first_name', 'middle_name']
    pass

def sort_replace_committeemember(sort_key):
#sort replace {'user_id': ['last_name', 'first_name']}
    pass

def sort_on_government():
#sort on ['start_date']
    pass

def sort_on_bill():
#sort on ['submission_date']
    pass

def sort_replace_bill(sort_key):
#sort replace {'owner_id': ['last_name', 'first_name']}
    pass

def sort_on_groupmembership():
#sort on ['last_name', 'first_name', 'middle_name']
    pass

def sort_replace_groupmembership(sort_key):
#sort replace {'user_id': ['last_name', 'first_name']}
    pass

def sort_replace_constituency(sort_key):
#sort replace {'province_id': ['province'], 'region_id': ['region']}
    pass

def sort_replace_committee(sort_key):
#sort replace {'committee_type_id': ['committee_type']}
    pass

def sort_on_memberofparliament():
#sort on ['last_name', 'first_name', 'middle_name']
    return [ domain.User.last_name.desc(), 
            domain.User.first_name.desc(), 
            domain.User.middle_name.desc() ]
        

def sort_replace_memberofparliament(sort_key):
#sort replace {'constituency_id': ['name'], 'user_id': ['last_name', 'first_name']}
    pass

def sort_replace_agendaitem(sort_key):
#sort replace {'owner_id': ['last_name', 'first_name']}
    pass

def sort_replace_eventitem(sort_key):
#sort replace {'owner_id': ['last_name', 'first_name']}
    pass

def sort_on_user():
#sort on ['last_name', 'first_name', 'middle_name']
    pass

def sort_replace_user(sort_key):
#sort replace {'user_id': ['last_name', 'first_name']}
    pass

def sort_on_officemember():
#sort on ['last_name', 'first_name', 'middle_name']
    pass

def sort_replace_officemember(sort_key):
#sort replace {'user_id': ['last_name', 'first_name']}
    pass

def sort_replace_heading(sort_key):
#sort replace {'owner_id': ['last_name', 'first_name']}
    pass

def sort_on_parliament():
#sort on ['start_date']
    pass

def sort_replace_tableddocument(sort_key):
#sort replace {'owner_id': ['last_name', 'first_name']}
    pass

def sort_on_minister():
#sort on ['last_name', 'first_name', 'middle_name']
    pass

def sort_replace_minister(sort_key):
#sort replace {'user_id': ['last_name', 'first_name']}
    pass

def sort_on_groupsittingattendance():
#sort on ['last_name', 'first_name', 'middle_name']
    pass

def sort_replace_groupsittingattendance(sort_key):
#sort replace {'user_id': ['last_name', 'first_name']}
    pass

