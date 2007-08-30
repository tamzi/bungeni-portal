from StringIO import StringIO
from os.path import basename
import os
import csv
import copy
import shelve
from DateTime.DateTime import DateTime
from Products.CMFCore.permissions import View
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.utils import shasattr
from Products.PlonePAS.utils import cleanId
from Products.BungeniDefaultContent.config import *
from Globals import package_home

from Products.Archetypes.debug import log

# TEAM_TYPES = ['Parliament', 'Committee', 'Ministry', 'Party', 'Reporters', 'Sitting']
TEAM_TYPES = ['Parliament', 'Committee', 'PoliticalGroup', 'Reporters', 'Office']
TEAMSPACE_TYPES = ['ParliamentWS', 'CommitteeWS']

new_actions = (
        {'id': 'glossary',
         'name': 'Glossary',
         'action': 'string:${portal_url}/help/glossary',
         'permission': View,
         'category': 'site_actions',},
        {'id': 'faq',
         'name': 'FAQ',
         'action': 'string:${portal_url}/help/faq',
         'permission': View,
         'category': 'site_actions',},
        {'id': 'help',
         'name': 'Help',
         'action': 'string:${portal_url}/help',
         'permission': View,
         'category': 'site_actions',},
        )

#
# Read CSV
#

# Describe the sources. 
# For records that correspond to objects in Plone:
# - how do their fields map to our Plone objects?
# - provide a template for missing information.
csv_sources = {
        'Committees_description': {
            'fields': {
                "committee_duration": 'duration',
                "committee_type": 'type',
                "committee_category": 'category',
                "committee_description": 'title',
                "committee_functions_of_committee": 'functions',
                "committee_max_no_of_members": 'maxMembers',
                "committee_proportional_representation": 'proportionalRepresentation',
                "committee_substitution_allowed": 'substitutionAllowed',
                "committee_presidency_internal": 'presidencyInternal',
                "committee_max_no_of_committee_deputy_chair": 'maxChairs',
                "committee_max_no_of_committee_secretary": 'maxSecretaries',
                "committee_min_no_in_attendance": 'minAttendance',
                # 'dissolutionDate',
                }, 
            'template': {
                'portal_type': 'Committee',
                },
            'id_field': 'committee_id'
            },  

        # Assign members to committees
        'Committees_membership': {'id_field': 'ID'}, 

        # Record periods for which each committee has existed?
        'Committees_reg': {'id_field': 'ID'}, 

        # Create hierarchy of region/province/constituency:
        'Constituencies_reg': {
            'fields': {
                'costituency_name': 'title',
                'costituency_voters': 'NumberOfVoters',
                'costituency_date_creation': 'CreatedDate',
                },
            'template': {
                'portal_type': 'Constituency',
                },
            'id_field': 'costituency_ID'}, 

        # Relations between MP and ministry:
        'Government_ministers': {'id_field': 'ID'}, 

        # Relations between ministry and govt.
        'Government_ministries': {'id_field': 'ID'}, 

        # ATVocabularyManager or PloneOntology for portfolio vocab .. relations aren't working yet.
        'Government_ministries_descrip': {
                'fields': {
                    'government_ministry_full_name': 'title',
                    'government_ministry_acronym': 'shortTitle',
                    'government_ministry_portfolio': 'portfolio',
                    },
                'template': {
                    'portal_type': 'Ministry', 
                    'children': None,
                    },
                'id_field': 'ministry_id'}, 

        # Linking MP to parliament, constituency .. 
        'MP_reg': {'id_field': 'ID'}, 

        # When an MP was speaker/leader/secretary of a group ..
        'MP_role': {'id_field': 'ID'}, 

        # The kinds of roles an MP may have. These correspond to relationships
        # btw group & MP. The relationship fields need mutators that update
        # group membership (active/inactive, as well as member roles). 
        'MP_role_Des': {'id_field': 'MP_role_ID'}, 

        'Parliamentary_sessions': {
                'fields': {
                    'session_type': 'type',
                    'session_date_start': 'startDate',
                    'session_date_end': 'endDate',
                    'session_notes': 'notes',
                    },
                'template': {
                    'portal_type': 'Session',
                    'children': None,
                    },
                'id_field': 'session_id'}, 

        'Parliamentary_session_type_des': {'id_field': 'session_type'}, 

        'Parliament_num_duration': {
                'fields': {
                    "parliament_number": 'number',
                    "parliament_date_of_election":'dateElected',
                    "parliament_date_inaugrated": 'dateInaugurated',
                    "parliament_date_dissolved": 'dateDissolved',
                    },
                'template': {
                    'portal_type': 'ParliamentWS',
                    'description': "Parliament of ...",
                    'children': [
                        {'title': 'Committees',
                            'portal_type': 'CommitteeFolder',
                            'children': None},
                        ]
                    },
                'id_field': 'parliament_id'},  

        'Persons_ID_register': {
                'fields': {
                    #                              'salutation',
                    "person_first_name":         'firstname',
                    "person_middle_name":        'middlename',
                    "person_last_name":          'surname',
                    #                              'maidenname',
                    #                              'fullname',
                    "person_place_birth":        'placeOfBirth',
                    "person_date_birth":         'dateOfBirth',
                    "person_date_death":         'dateOfDeath',
                    "person_gender":             'gender',
                    "person_national_id_number": 'nationalIdNumber',
                    },
                'template': {
                    'portal_type': 'MemberOfParliament', 
                    'email': 'jean.jordaan@gmail.com',
                    'password': 'asdfasdf',
                    'confirm_password': 'asdfasdf'
                    },
                'id_field': 'person_id'}, 

        'Political_group_des': {
                'fields': {
                    "pol_group_name": 'title',
                    # 'shortTitle',
                    # 'registrationDate',
                    # 'cessationDate',
                    },
                'template': {
                    'portal_type': 'PoliticalGroup',
                    'children': None, # Members ..
                    },
                'id_field': 'pol_group_ID'},  

        # Set membership of persons to parties
        'Political_group_memb': {'id_field': 'ID'}, 
        'Seating_attendance': {
                'id_field': 'ID',
                'split_by_field': 'seating_id'}, 
        'Seating_att_id_des': {'id_field': 'attendance_id'}, 
        'Seating_schedule': {
                'fields': {
                    'seating_begin_date': 'startDate',
                    'seating_end_date': 'endDate',
                    'seating_type': 'type',
                    },
                'template': {
                    'portal_type': 'Sitting',
                    'children': [
                        {'title': 'Debate record folder', 
                            'portal_type': 'DebateRecordFolder', },
                        ]
                    },
                # reference_fields specifies the type for which IDs
                # should be resolved
                'reference_fields': (
                    ('attendees', 'MemberOfParliament'),
                    ),
                'id_field': 'seating_id'}, 
        'Seating_type_des': {'id_field': 'seating_type'}, 

        'Staff_office_des': {
                'fields': {
                    'staff_office_des': 'title',
                    },
                'template': {
                    'portal_type': 'Office',
                    'children': None, # Members ..
                    },
                'id_field': 'staff_office_ID'}, 

        # Set membership of staff to offices
        'Staff_reg': {'id_field': 'ID'}, 

        # Set membership type of staff to offices
        'Staff_role_des': {'id_field': 'staff_role_ID'}, 

        }

def add_plone_role_names():
    # Map FZ's roles to Plone roles
    plone_role_map = {
            '1': 'Speaker',
            '2': 'DeputySpeaker',
            '3': 'Leader',
            '4': 'DeputyLeader',
            '5': 'Spokesperson',
            '6': 'Secretary',
            '7': 'MemberOfParliament', # Our addition
            '8': 'MemberOfGroup', # Our addition
            }
    fz_mp_roles_to_plone_roles_map = shelve.open('MP_role_Des',
            writeback=True)
    for rid, rolename in plone_role_map.items():
        if fz_mp_roles_to_plone_roles_map.has_key(rid):
            fz_mp_roles_to_plone_roles_map[
                    rid]['role'] = plone_role_map[rid]
        else:
            fz_mp_roles_to_plone_roles_map[
                    rid] = {'role': plone_role_map[rid]}
    fz_mp_roles_to_plone_roles_map.close()

    plone_role_map = {
            '1': 'ParliamentClerk',
            '2': 'DeputyParliamentClerk',
            '3': 'CommitteeClerk',
            '4': 'ChiefEditor',
            '5': 'DeputyChiefEditor',
            '6': 'Editor',
            '7': 'Reporter',
            }
    fz_staff_roles_to_plone_roles_map = shelve.open('Staff_role_des',
            writeback=True)
    for rid, rolename in plone_role_map.items():
        fz_staff_roles_to_plone_roles_map[
                rid]['role'] = plone_role_map[rid]
    fz_staff_roles_to_plone_roles_map.close()

committee_plone_role_map = {
        'Chairperson': 'Chairperson',
        'Committee Clerk': 'CommitteeClerk',
        'Deputy Chairperson': 'DeputyChairperson',
        'Deputy Committee Clerk': 'DeputyCommitteeClerk',
        'Member': 'CommitteeMember',
        'Secretary': 'Secretary',
        }

def shelve_csv_data():
    """ Using the csv_sources data structure, create shelves to stage
    the information for import.
    """
    #
    # Build structures for data import
    #

    def translate_dicts(field_map, source_dict, target_dict):
        for csv_field in source_dict.keys():
            at_field = field_map.get(csv_field, csv_field)
            target_dict[at_field] = source_dict[csv_field]
        return target_dict

    def read_shelf(shelf, id_field, field_map, dict_template, source_dicts):
        """ Read a list of source dictionaries into a shelf
        """
        for source_dict in source_dicts:
            target_dict = {'id_field': id_field}
            target_dict.update(dict_template)
            if (target_dict.has_key('children') and
                    target_dict.get('children', None) == None):
                target_dict['children'] = []
            shelf[source_dict[id_field]] = translate_dicts(
                    field_map, source_dict, target_dict)

    # Read all the data into dictionaries.
    # data = {}
    for csv_name in csv_sources:
        field_map = csv_sources[csv_name].get('fields', {})
        dict_template = csv_sources[csv_name].get('template', {})
        id_field = csv_sources[csv_name]['id_field']
        split_by_field = csv_sources[csv_name].get('split_by_field', None)
        if (os.path.exists('%s.dat'%csv_name) or 
                os.path.exists('%s_1.dat'%csv_name)):
            # "_1" in case of splitting ..
            log('%s.* exists, skipping .. (delete to re-create).'%csv_name)
            continue
        log('opening %s'%csv_name) #DBG
        csv_path = os.path.join( package_home( product_globals ), 'demo-parliament', csv_name+'.csv' )
        
        csv_lines = [line for line in csv.DictReader(open(csv_path ) ) ]
        if split_by_field:
            splits = {}
            for d in csv_lines:
                splits[d[split_by_field]] = None
            splits = splits.keys()
            csv_sources[csv_name]['splits'] = splits
            csv_lines_map = {}
            for split in splits:
                csv_lines_map[split] = []
            for d in csv_lines:
                csv_lines_map[d[split_by_field]].append(d)
            for split in splits:
                shelf = shelve.open('%s_%s'%(csv_name, split), writeback=True)
                read_shelf(shelf, id_field, field_map, dict_template,
                        csv_lines_map[split])
                log('closing after first read'); shelf.close(); log('done')
            del csv_lines_map
        else:
            shelf = shelve.open(csv_name, writeback=True)
            read_shelf(shelf, id_field, field_map, dict_template, csv_lines)
            log('closing after first read: %s'%csv_name); shelf.close(); log('done')

def sort_children(sort_key, children):
    """
    """
    if not children:
        return children
    # decorate/sort/undecorate
    if type(children[0].get(sort_key, '')) == type(''):
        def get(sort_key, c):
            return c.get(sort_key, 'aaaaaaaaaaaa')
    else:
        def get(sort_key, c):
            return int(c.get(sort_key, 0))
    decorated = [(get(sort_key, c), c) for c in children]
    decorated.sort()
    return [t[1] for t in decorated]

##  # Short names
##  members_map = shelve.open('Persons_ID_register')
##  parties_map = shelve.open('Political_group_des', writeback=True)
##  offices_map = shelve.open('Staff_office_des', writeback=True)
##  parliaments_map = shelve.open('Parliament_num_duration', writeback=True)
##  constituencies_map = shelve.open('Constituencies_reg', writeback=True)
##  parliament_committee_map = shelve.open('Committees_reg', writeback=True)

# Accumulate content for adding later
# TODO shelve.open('content', writeback=True) = {}
# TODO shelve.open('teams', writeback=True) = []

def set_staff_members():
    """ Update Persons_ID_register so that we can add Staff objects for
    staff instead of MemberOfParliament objects.
    """
    # TODO
    fz_office_membership = shelve.open('Staff_reg')
    members_map = shelve.open('Persons_ID_register', writeback=True)
    for mid, membership_info in fz_office_membership.items():
        members_map[membership_info['person_id']]['portal_type'] = 'Staff'
    fz_office_membership.close()
    members_map.close()
    log('closing after set_staff_members'); members_map.close(); log('done')

def set_titles_for_parliaments():
    #
    # Set titles for parliaments
    #
    parliaments_map = shelve.open('Parliament_num_duration', writeback=True)
    for id, parliament_info in parliaments_map.items():
        parliament_info['title'] = 'Parliament %s' % parliament_info['number']
    log('closing after parliament titles'); parliaments_map.close(); log('done')

member_roles_per_polgroup = {
        # {parliament_id: 
        #   {party_id: 
        #       {person_id: 
        #           {role: (from_date, to_date)}}}
        }
def get_member_roles_per_party():
    """ Populate a temporary global structure
    member_roles_per_party with role info per party.
    """
    global member_roles_per_polgroup 
    fz_member_roles = shelve.open('MP_role')
    fz_member_role_names = shelve.open('MP_role_Des')
    for rid, role_info in fz_member_roles.items():
        parliament = member_roles_per_polgroup.get(
                role_info['parliament_id'], {})
        political_group = parliament.get(
                role_info['MP_pol_group'], {})
        person_info = political_group.get(
                role_info['person_id'], {})
        role_name = fz_mp_roles_to_plone_roles_map[
                role_info['MP_role_ID']]
        role_info = person_info.get(
                role_info)


def set_parliament_membership():
    """ Create a 'parties_per_parliament' shelf to create a set of
    members per party for each parliament.
    """
    fz_party_membership = shelve.open('Political_group_memb')
    members_map = shelve.open('Persons_ID_register')
    parties_map = shelve.open('Political_group_des')
    parties_per_parliament = shelve.open('parties_per_parliament', writeback=True)
    for mid, membership_info in fz_party_membership.items():
        person = members_map[membership_info['person_id']]
        party = parties_map[membership_info['pol_group_ID']]
        parliament_party = parties_per_parliament.get(
                '%s_%s'%(membership_info['pol_group_ID'],
                    membership_info['parliament_id']),
                copy.deepcopy(party))
        parliament_party['title'] = "%s (of parliament %s)" % (
                party['title'], membership_info['parliament_id'])
        entry = {'firstname': person['firstname'],
                'surname': person['surname'],
                'sort_by': person['surname'] + person['firstname'],
                'effectiveDate':  membership_info['pol_group_join'],
                'expirationDate': membership_info['pol_group_leave'],
                'portal_type': 'Team Membership',
                }
        if entry not in parliament_party['children']:
            parliament_party['children'].append(entry)
            parties_per_parliament[
                    '%s_%s'%(membership_info['pol_group_ID'],
                        membership_info['parliament_id'])
                    ] = parliament_party
    for pid, party in parties_per_parliament.items():
        party['children'] = sort_children('sort_by', party['children'])
    log('closing after party membership'); parties_per_parliament.close(); log('done')
    parties_map.close()
    fz_party_membership.close()
    members_map.close()

member_roles_per_office = {
        # office_id: {person_id: {role: (from_date, to_date)}}
        }
def get_member_roles_per_office():
    """ Populate a temporary global structure
    member_roles_per_office with role info per office.
    """
    # TODO
    pass

def set_office_membership():
    """ Extend the Staff_office_des shelf with membership info.
    """
    fz_office_membership = shelve.open('Staff_reg')
    members_map = shelve.open('Persons_ID_register')
    offices_map = shelve.open('Staff_office_des', writeback=True)
    for mid, membership_info in fz_office_membership.items():
        person_dict = members_map[membership_info['person_id']]
        office = offices_map[membership_info['staff_office_ID']]
        entry = {'firstname': person_dict['firstname'],
                'surname': person_dict['surname'],
                'sort_by': person_dict['surname'] + person_dict['firstname'],
                'effectiveDate':  membership_info['staff_date_join'],
                'expirationDate': membership_info['staff_date_leave'],
                'reason': membership_info['staff_leave_reason'],
                'portal_type': 'Team Membership',
                }
        if entry not in office['children']:
            office['children'].append(entry)
    for oid, office in offices_map.items():
        office['children'] = sort_children('sort_by', office['children'])
    log('closing after office membership'); offices_map.close(); log('done')
    fz_office_membership.close()
    members_map.close()

member_roles_per_parliament = {
        # parliament_id: {person_id: {role: (from_date, to_date)}}
        }
def get_member_roles_per_parliament():
    """ Populate a temporary global structure
    member_roles_per_parliament with role info per parliament.
    """
    # TODO
    pass

members_per_parliament = {
        # parliament_id: [member_dict, ..]
        }
def get_members_per_parliament():
    """ Populate a temporary global structure members_per_parliament
    with membership info for each parliament.
    """
    fz_parliament_membership = shelve.open('MP_reg')
    members_map = shelve.open('Persons_ID_register')
    global members_per_parliament
    for mid, membership_info in fz_parliament_membership.items():
        members = members_per_parliament.get(membership_info['parliament_id'], [])
        members_per_parliament[membership_info['parliament_id']] = members
        person_dict = members_map[membership_info['person_id']]
        entry = {'firstname': person_dict['firstname'],
                'surname': person_dict['surname'],
                'sort_by': person_dict['surname'] + person_dict['firstname'],
                'effectiveDate':  membership_info['MP_date_join'],
                'expirationDate': membership_info['MP_date_leave'],
                'reason': membership_info['MP_leave_reason'],
                'portal_type': 'Team Membership',
                }
        if entry not in members:
            members.append(entry)
    for pid, members in members_per_parliament.items():
        members_per_parliament[pid] = sort_children('sort_by', members)
    fz_parliament_membership.close()
    members_map.close()

def set_teams_for_parliaments():
    """ Data to create team objects for each parliament.
    """
    fz_mp_roles_to_plone_roles_map = shelve.open('MP_role_Des')
    parliaments_map = shelve.open('Parliament_num_duration')
    teams = shelve.open('teams', writeback=True)
    teams['teams'] = []
    for pid, parliament_info in parliaments_map.items():
        parliament_info['title'] = 'Parliament %s' % parliament_info['number']
        copied = copy.deepcopy(parliament_info)
        copied['portal_type'] = 'Parliament'
        copied['allowed_team_roles'] = [
                r['role'] for r in fz_mp_roles_to_plone_roles_map.values()
                ]
        copied['default_team_roles'] = ('MemberOfParliament', )
        copied['children'] = members_per_parliament[
                parliament_info['parliament_id']]
        if copied not in teams['teams']:
            teams['teams'].append(copied)
    log('closing after handling parliaments membership'); teams.close(); log('done')
    parliaments_map.close()

members_per_committee = {}
def set_committee_membership():
    """ Populate a temporary global structure members_per_committee with
    membership info for each committee, during each parliament.
    """
    # 
    # Gather info about committee membership
    #
    fz_committee_membership = shelve.open('Committees_membership')
    members_map = shelve.open('Persons_ID_register')
    global members_per_committee
    for cmid, cm_info in fz_committee_membership.items():
        committee_id = cm_info['committee_id']
        parliament_id = cm_info['parliament_id']
        members = members_per_committee.get('%s_%s'%(
            parliament_id, committee_id), [])
        person_dict = members_map[cm_info['person_id']]
        entry = {'firstname': person_dict['firstname'],
                'surname': person_dict['surname'],
                'sort_by': person_dict['surname'] + person_dict['firstname'],
                'effectiveDate':  cm_info['committee_date_begin'],
                'expirationDate': cm_info['committee_date_end'],
                'role': cm_info['committee_role'],
                'portal_type': 'Team Membership',
                }
        if entry not in members:
            members.append(entry)
            members_per_committee['%s_%s'%(
                parliament_id, committee_id)] = members
    for cid, members in members_per_committee.items():
        members_per_committee[cid] = sort_children('sort_by', members)
    log('closing after committee membership'); fz_committee_membership.close(); log('done')
    members_map.close()
    #DBG data members_per_committee['18'] = members_per_committee['17'] 

def set_committee_teams_and_workspaces():
    #
    # Add committees and committee workspaces to parliaments
    #
    fz_committees = shelve.open('Committees_description')
    parliament_committee_map = shelve.open('Committees_reg')
    parliaments_map = shelve.open('Parliament_num_duration',
            writeback=True)
    global members_per_committee
    teams = shelve.open('teams', writeback=True)
    for cid, committee_info in parliament_committee_map.items():
        committee_id = committee_info['committee_id']
        parliament_id = committee_info['parliament_id']
        committee = fz_committees[committee_id]
        parliament = parliaments_map[parliament_id]
        copied = copy.deepcopy(committee)
        copied['title'] = '%s (parliament %s)'%(
                committee['title'], parliament['number'])
        copied['allowed_team_roles'] = committee_plone_role_map.values()
        copied['default_team_roles'] = ('CommitteeMember',)
        # (1) Add members to committee
        copied['children'] = members_per_committee[
                '%s_%s'%(parliament_id, committee_id)]
        # (2) Add a team object
        if copied not in teams['teams']:
            teams['teams'].append(copied)
        # (3) Add a workspace to the appropriate parliament
        copied = copy.deepcopy(committee)
        copied['title'] = '%s (parliament %s)'%(
                committee['title'], parliament['number'])
        copied['portal_type'] = 'CommitteeWS'
        if parliament['children'][0]['children'] == None:
            parliament['children'][0]['children'] = []
        committee_workspaces = parliament['children'][0]['children']
        if copied not in committee_workspaces:
            committee_workspaces.append(copied)
    log('closing after committee teams & workspaces'); teams.close(); log('done')
    fz_committees.close()
    parliament_committee_map.close()
    parliaments_map.close()

ministers_map = {}
def set_ministers_per_ministry():
    """ Populate a temporary global structure ministers_map with
    ministries per parliament.
    """
    #
    # Ministers per ministry
    #
    fz_ministers_info = shelve.open('Government_ministers')
    global ministers_map
    for id, minister_info in fz_ministers_info.items():
        parliament = ministers_map.setdefault(
                minister_info['parliament_id'], {})
        ministry = parliament.setdefault(
                minister_info['ministry_id'], [])
        if minister_info['ID'] not in ministry:
            ministry.append(minister_info['ID'])
    fz_ministers_info.close()

def set_ministries():
    """ Create an object for each ministry and portfolio
    """
    members_map = shelve.open('Persons_ID_register')
    parliaments_map = shelve.open('Parliament_num_duration')
    fz_ministry_info = shelve.open('Government_ministries')
    fz_ministers_info = shelve.open('Government_ministers')
    fz_ministries_description = shelve.open('Government_ministries_descrip', writeback=True)
    global ministers_map
    # teams = shelve.open('teams', writeback=True)
    for id, ministry_info in fz_ministry_info.items():
        copied = {}
        ministry_id = ministry_info['ministry_id']
        parliament_id = ministry_info['parliament_id']
        parliament = parliaments_map[parliament_id]
        minister_id = ministers_map[parliament_id][ministry_id][:1][0]
        ministry = fz_ministries_description[ministry_id]
        ministry['sort_by'] = ministry['title']
        portfolio = {
                'title': ministry['portfolio'],
                'portal_type': 'Portfolio',
                'Minister': [minister_id], # TODO convert to UID
                'reference_fields': [('Minister', 'MemberOfParliament'), ]
                }
        if not portfolio in ministry['children']:
            ministry['children'].append(portfolio)
        # TODO Set minister as reference on portfolio

        # copied = copy.deepcopy(ministry)
        # copied['title'] = '%s (parliament %s)'%(
        #         ministry['title'], parliament['number'])

        #
        # Ministers won't be added as team members any more.
        #
        # for minister_id in ministers_map[parliament_id][ministry_id]:
        #     minister_info = fz_ministers_info[minister_id]
        #     person_dict = members_map[minister_info['person_id']]
        #     entry = {'firstname': person_dict['firstname'],
        #             'surname': person_dict['surname'],
        #             'sort_by': person_dict['surname'] + person_dict['firstname'],
        #             'effectiveDate': minister_info['person_date_join'],
        #             'expirationDate': minister_info['person_date_leave'],
        #             'reason': minister_info['persons_leave_reason'],
        #             }
        #     if entry not in copied['children']:
        #         copied['children'].append(entry)
        #
        # copied['children'] = sort_children('sort_by', copied['children'])
        # copied['allowed_team_roles'] = (
        #         'Minister', 
        #         'DeputyMinister',
        #         # TODO more roles within the ministry? Staff?
        #         )
        # copied['default_team_roles'] = ('Minister',)

        #
        # Ministries aren't teams anymore.
        #
        # if copied not in teams['teams']:
        #     teams['teams'].append(copied)
        # copied = copy.deepcopy(ministry)
        # copied['title'] = '%s (parliament %s)'%(
        #         ministry['title'], parliament['number'])
        # copied['portal_type'] = 'MinistryWS'
        # if parliament['children'][1]['children'] == None:
        #     parliament['children'][1]['children'] = []
        # ministry_workspaces = parliament['children'][1]['children']
        # if copied not in ministry_workspaces:
        #     ministry_workspaces.append(copied)
    log('closing after ministries'); fz_ministries_description.close(); log('done')
    log('closing after ministries'); parliaments_map.close(); log('done')
    # log('closing after ministries'); teams.close(); log('done')
    fz_ministry_info.close()
    del ministers_map

def set_sittings_for_sessions():
    """ Extend the Seating_schedule shelf with attendance info (TODO)
    and the Parliamentary_sessions shelf with sittings.
    """
    #
    # Add sittings to sessions
    # 
    fz_sittings = shelve.open('Seating_schedule', writeback=True)
    fz_sessions = shelve.open('Parliamentary_sessions', writeback=True)
    for sid, sitting in fz_sittings.items():
        session = fz_sessions[sitting['session_id']]
        if not session.has_key('title'):
            session['title'] = 'Session %s of parliament %s' % (
                    session['session_id'],
                    session['parliament_id'],
                    )
        if session['children'] == None:
            session['children'] = []
        #
        # Handle sitting attendance
        #
        # I think this way of doing it still puts all the attendance info
        # into to Parliamentary_sessions shelf, which will be too unwieldy.
        # Work towards one where attendance info is only read when that
        # sitting is created.
        #
        # TODO translate to UIDs
        #
        # attendees = []
        # fz_attendees = shelve.open('Seating_attendance_%s'%seating_id)
        # for id, record in fz_attendees.items():
        #     attendees.append(record['person_id'])
        # fz_attendees.close()
        # sitting['attendees'] = attendees
        sitting['title'] = 'Sitting %s of session %s' % (
                    sitting['seating_id'],
                    sitting['session_id'],
                    )
        sitting['attendees'] = [] # TODO
        if sitting not in session['children']:
            session['children'].append(sitting)
    for sid, session in fz_sessions.items():
        fz_sessions[sid]['children'] = sort_children('seating_id',
                session['children'])
    log('closing after adding sittings to sessions'); fz_sessions.close(); log('done')
    fz_sittings.close()

def set_sessions_for_parliaments():
    """ Extend the Parliament_num_duration shelf with session info.
    """
    # 
    # Add session info to parliaments
    #
    fz_session_types = shelve.open('Parliamentary_session_type_des')
    fz_sessions = shelve.open('Parliamentary_sessions')
    parliaments_map = shelve.open('Parliament_num_duration', writeback=True)
    for session_id, session in fz_sessions.items():
        # Translate session id into session name
        session['type'] = fz_session_types[session['type']]
        parliament = parliaments_map[session['parliament_id']]
        if session not in parliament['children']:
            parliament['children'].append(session)
    log('closing after parliament sessions'); parliaments_map.close(); log('done')
    fz_sessions.close()
    fz_session_types.close()

def set_consituencies():
    """ Create a shelf with a hierarchy of region/province/constituency.
    """
    # 
    # Info to create constituencies
    #
    constituencies_shelf = shelve.open('constituencies', writeback=True)
    constituencies_shelf['constituencies'] = []
    regions = []
    provinces = {}
    constituencies = {}
    # {'Region': [
    #   {'children': [{'Province': [
    #       {'children': ['Constituency']}
    #       ]}]}
    #   ]}
    constituencies_map = shelve.open('Constituencies_reg')
    # TODO: add MP info to constituencies. This can be tricky: one
    # constituency has different MPs over time. Should this just be a
    # reference to the latest one? Or should constituency also be a
    # team? If it's a team, should previous MPs just be inactive
    # memberships? And MPs who return, should they be memberships with
    # active/inactive history?
    # fz_parliament_membership = shelve.open('MP_reg')
    for constituency_id, constituency in constituencies_map.items():
        region_name = constituency['costituency_region']
        if region_name not in regions:
            regions.append(region_name)
            provinces[region_name] = []
            region = {'portal_type': 'Region', 'title': region_name,
                    'children': []}
            constituencies_shelf['constituencies'].append(region)
        else:
            region = [r for r in constituencies_shelf['constituencies'] 
                    if r['title'] == region_name][0]
        province_name = constituency['costituency_province']
        if province_name not in provinces[region_name]:
            provinces[region_name].append(province_name)
            constituencies[province_name] = []
            province = {'portal_type': 'Province', 
                    'title': province_name, 'children': []}
            region['children'].append(province)
        constituency_name = constituency['title']
        if constituency_name not in constituencies[province_name]:
            constituencies[province_name].append(constituency_name)
            province['children'].append(constituency)
    log('closing after constituencies'); constituencies_shelf.close(); log('done')
    constituencies_map.close()

def massage_data():
    """ Massage the structures we created to fit the desired Plone
    content hierarchy.
    """
    # Massage a bit to get things into the expected format
    members_map = shelve.open('Persons_ID_register')
    members = shelve.open('members', writeback=True)
    members['members'] = members_map.values()
    members.close()
    members_map.close()
    fz_mp_roles_to_plone_roles_map = shelve.open('MP_role_Des')
    fz_staff_roles_to_plone_roles_map = shelve.open('Staff_role_des')
    fz_ministries_description = shelve.open('Government_ministries_descrip')
    parties_per_parliament = shelve.open('parties_per_parliament')
    offices_map = shelve.open('Staff_office_des')
    teams = shelve.open('teams', writeback=True)
    for team in parties_per_parliament.values():
        team['allowed_team_roles'] = [
                r['role'] for r in fz_mp_roles_to_plone_roles_map.values()
                ]
        team['default_team_roles'] = ('MemberOfGroup', )
        teams['teams'].extend([team])
    for team in offices_map.values():
        team['allowed_team_roles'] = [
                r['role'] for r in fz_staff_roles_to_plone_roles_map.values()
                ]
        team['allowed_team_roles'].extend(committee_plone_role_map.values())
        team['default_team_roles'] = ('CommitteeClerk', )
        teams['teams'].extend([team])
    teams.close()
    offices_map.close()
    parties_per_parliament.close()

    content = shelve.open('content', writeback=True)
    content['content'] = {}
    parliaments_map = shelve.open('Parliament_num_duration')
    constituencies = shelve.open('constituencies')
    content['content'].update({
            'parliaments': [
                {'title': 'Parliaments',
                    'portal_type': 'Folder',
                    'children': parliaments_map.values()
                    },
                ],
            'constituencies': [
                {'title': 'Constituencies',
                    'portal_type': 'Regions', 
                    'children': constituencies['constituencies'],
                    },
                ], 
            'ministries': [
                {'title': 'Ministries',
                    'portal_type': 'MinistryFolder',
                    'children': sort_children('sort_by',
                        fz_ministries_description.values())
                    }
                ],
            })
    content.close()
    # from ipdb import set_trace; set_trace()


# End reading of CSV data

def get_id(d):
    """ Look for an id in a dictionary
    """
    id = d.get('id', d.get('title'))
    if id:
        return id
    if d.has_key('firstname'):
        return ' '.join([n for n in [d['firstname'], d['surname']] if n])

def do_transition(root, structure, transition, reason=''):
    """ Perform the initial workflow transition(s)
    """
    normalizeString = getToolByName(root, 'plone_utils').normalizeString
    reason = reason and reason or 'Installer: %s'%transition
    folderish_ids = []
    for d in structure:
        # Transition individual objects
        id = normalizeString(get_id(d))
        if d.get('children'):
            folderish_ids.append(id)
        else:
            obj = root.get(id, None)
            if obj:
                obj.content_status_modify(transition, reason, None, None,)
    paths = ['/'.join(root[i].getPhysicalPath()) for i in folderish_ids]
    if paths:
        # Transition folderish objects
        root.folder_publish(workflow_action=transition, paths=paths,
                comment=reason, include_children=True)

created_obj_counter = 0

def add_default_content(root, structure, initial_transitions=['publish']):
    """ Create default content
    """
    # TODO: We need a way to relate ids in the input CSV with UIDs of the
    # corresponding Plone objects, to enable easy creation of references.
    # (portal_type, id): UID, ...
    id_uid_map = shelve.open('id_uid_map', writeback=True)

    out = StringIO()
    plone = getToolByName(root, 'portal_url').getPortalObject()
    normalizeString = getToolByName(plone, 'plone_utils').normalizeString
    membership_tool = getToolByName(root, 'portal_membership')

    def add_object(parent, d, edit=False):
        obj_id = normalizeString(get_id(d))

        #
        # Pull out the snippets that edit objects, so that we can use
        # them for updating existing objects as well.
        #
        def set_membership_roles(obj, d):
            roles = d.get('roles', [])
            if roles:
                obj.editTeamRoles(roles)
        def set_membership_activation(obj, d):
            expirationDate = d.get('expirationDate', None)
            if expirationDate:
                if DateTime(expirationDate) < DateTime():
                    do_transition(obj, [d], 'deactivate', d.get('reason'))
            else:
                do_transition(obj, [d], 'activate', d.get('reason'))
        def set_layout(obj, d):
            layout = d.get('layout', None)
            if layout:
                obj.setLayout(layout)
        def set_team_roles(obj, d):
            if obj.portal_type in TEAM_TYPES:
                roles = list(obj.getAllowedTeamRoles())
                roles.extend(d.get('allowed_team_roles', []))
                obj.setAllowedTeamRoles(roles)
                roles = list(obj.getDefaultRoles())
                roles.extend(d.get('default_team_roles', []))
                obj.setDefaultRoles(roles)
        def set_team_members(obj, d):
            if obj.portal_type in TEAMSPACE_TYPES:
                team_ids = [normalizeString(d['title'])]
                team_ids.extend(d.get('team_ids', []))
                obj.editTeams(team_ids)
        def do_process_form(obj, d):
            if not 'Criteri' in d['portal_type']:
                # Criterions shouldn't get cataloged, and processForm
                # does this.
                obj.processForm(data=1, values=d)

        #
        # Short-circuit if the object exists: allow incremental updates.
        #
        # Not very sophisticated now .. 
        # - if the code is changed, we want to re-add everything anyway,
        # - if the data is modified, we can pass edit=True to update the
        #   object, but object initialisation code won't run. 
        # - if data is deleted, we won't know about it.
        #
        if shasattr(parent, obj_id):
            log('add_object> %s already has %s'% (parent.getId(), obj_id) ) #DBG 
            obj = parent[obj_id]
            if edit:
                log('add_object> editing ...')
                if 'Criteri' in d['portal_type']:
                    obj.edit(**d)
                elif d['portal_type'] == 'Team Membership':
                    edit_membership_roles(obj, d)
                    set_membership_activation(parent, d)
                else:
                    set_layout(obj, d)
                    set_team_roles(obj, d)
                    set_team_members(obj, d)
                do_process_form(obj, d)
            return obj

        if 'Criteri' in d['portal_type']:
            obj = parent.addCriterion(d['field'], d['portal_type'])
            obj.edit(**d)
        elif d['portal_type'] == 'Team Membership':
            obj = parent.addMember(obj_id, 'Team Membership')
            set_membership_roles(obj, d)
            set_membership_activation(parent, d)
        else:
            parent.invokeFactory(d['portal_type'], obj_id,)
            obj = parent[obj_id]
            set_layout(obj, d)
            set_team_roles(obj, d)
            set_team_members(obj, d)
            if d.has_key('create_home_folder'):
                membership_tool.createMemberArea(obj_id)
        do_process_form(obj, d)
        if d.has_key('id_field'):
            log('add_object> %s %s (%s) is %s'% (obj.portal_type, d[d['id_field']], obj.getId(), obj.UID()))
            id_uid_map['%s_%s'%(obj.portal_type, d[d['id_field']])] = obj.UID()
            id_uid_map['%s_%s'%(obj.portal_type, d[d['id_field']])] = obj.UID()

        # Commit a subtransaction every 1000 objects, to conserve memory
        global created_obj_counter
        created_obj_counter = created_obj_counter + 1
        log('add_object> counting .. %s (added %s in %s)'% (created_obj_counter, obj_id, parent.getId()) )
        if created_obj_counter % 10 == 0:
            import transaction
            # transaction.savepoint(optimistic=True)
            transaction.commit()
            log('add_object> committed at %s'% created_obj_counter )
        return obj

    def add_structure(root, structure):
        """ Recursively add content as specified in sequences of dicts.
        """
        for d in structure:
            if d.has_key('reference_fields'):
                for field, portal_type in d['reference_fields']:
                    d[field] = [id_uid_map['%s_%s'%(portal_type, id)] for id in d[field]]
            obj = add_object(root, d)
            if d.get('children', None):
                add_structure(obj, d['children'])

    add_structure(root, structure)

    if initial_transitions:
        for t in initial_transitions:
            do_transition(root, structure, t)

    print >>out, 'Created testing content'

    return out.getvalue()


def install(self):
    """ Do stuff that GS will do for us soon ..
    """
    #
    # Prepare shelves from the CSV input
    # We need to call all these in order. Only the first is idempotent.
    # If you call the others repeatedly, they will collect redundant
    # data. However, this should be ignored by add_default_content during import
    #
    shelve_csv_data()
    add_plone_role_names()
    set_staff_members()
    set_titles_for_parliaments()
    set_parliament_membership()
    set_office_membership()
    get_members_per_parliament()
    set_teams_for_parliaments()
    set_committee_membership()
    set_committee_teams_and_workspaces()
    set_ministers_per_ministry()
    set_ministries()
    set_sittings_for_sessions()
    set_sessions_for_parliaments()
    set_consituencies()
    massage_data()

    out = StringIO()
    plone = getToolByName(self, 'portal_url').getPortalObject()
    normalizeString = getToolByName(plone, 'plone_utils').normalizeString

    #
    # Filter the navigation
    #
    ntp = getToolByName(self, 'portal_properties').navtree_properties

    # Repeat from Products/TeamSpace/Extensions/Install.py .. it gets
    # squashed by remember/profiles/default/propertiestool.xml
    prop_name = 'metaTypesNotToList'
    blacklist = ntp.getProperty(prop_name)
    if blacklist is not None:
        blacklist = list(blacklist)
        # TODO Add BungeniTeamsTool?
        if not 'TeamsTool' in blacklist:
            blacklist.append('TeamsTool')
        ntp.manage_changeProperties(**{prop_name:tuple(blacklist)})

    # Add some of the new content to the site actions
    actions_tool = getToolByName(self, 'portal_actions')
    for action in new_actions:
        actions_tool.addAction(
                action.get('id'),
                action.get('name'),
                action.get('action'),
                action.get('condition'),
                action.get('permission'),
                action.get('category'),
                visible=1,
                )

    #
    # Add default members
    #
    properties_tool = getToolByName(self, 'portal_properties')
    # Don't send mail while adding
    properties_tool.site_properties.manage_changeProperties(validate_email=0)
    memberdata_tool = getToolByName(self, 'portal_memberdata')
    result = add_default_content(
            memberdata_tool,
            shelve.open('members')['members'],
            #DBG initial_transitions=[])
            initial_transitions=['trigger',])
    # OK, start sending mail again
    properties_tool.site_properties.manage_changeProperties(validate_email=1)
    print >>out, result

    #
    # Add default teams
    #
    teams_tool = getToolByName(self, 'portal_bungeniteamstool')
    result = add_default_content(
            teams_tool,
            shelve.open('teams')['teams'],
            initial_transitions=[])
    print >>out, result

    #
    # Add default content
    #
    for content in shelve.open('content')['content'].values():
        result = add_default_content(self, content, initial_transitions=[])
        print >>out, result

    # Publish existing content
    # We don't want this content to be deleted upon uninstallation
    do_transition(self, EXISTING_SITE_CONTENT, transition='publish')
    print >>out, 'Published existing content'

    # DBG Cause an exception just before we're done. I want to be able
    # to rerun this install, without going via uninstall. 
    asfd

    # Filter the global tabs
    # TODO

    # TODO # Hide from navigation
    # TODO for obj in [self.Members, self.workspace, self.help, ]:
    # TODO     obj.setExcludeFromNav(True)
    # TODO     obj.reindexObject()


# This one installs from AppConfig.py
#
# def install(self):
#     """ Do stuff that GS will do for us soon ..
#     """
#     out = StringIO()
#     plone = getToolByName(self, 'portal_url').getPortalObject()
#     normalizeString = getToolByName(plone, 'plone_utils').normalizeString
# 
#     #
#     # Filter the navigation
#     #
#     ntp = getToolByName(self, 'portal_properties').navtree_properties
# 
#     # Repeat from Products/TeamSpace/Extensions/Install.py .. it gets
#     # squashed by remember/profiles/default/propertiestool.xml
#     prop_name = 'metaTypesNotToList'
#     blacklist = ntp.getProperty(prop_name)
#     if blacklist is not None:
#         blacklist = list(blacklist)
#         # TODO Add BungeniTeamsTool?
#         if not 'TeamsTool' in blacklist:
#             blacklist.append('TeamsTool')
#         ntp.manage_changeProperties(**{prop_name:tuple(blacklist)})
# 
#     # Add some of the new content to the site actions
#     actions_tool = getToolByName(self, 'portal_actions')
#     for action in new_actions:
#         actions_tool.addAction(
#                 action.get('id'),
#                 action.get('name'),
#                 action.get('action'),
#                 action.get('condition'),
#                 action.get('permission'),
#                 action.get('category'),
#                 visible=1,
#                 )
# 
#     #
#     # Add default members
#     #
#     properties_tool = getToolByName(self, 'portal_properties')
#     # Don't send mail while adding
#     properties_tool.site_properties.manage_changeProperties(validate_email=0)
#     memberdata_tool = getToolByName(self, 'portal_memberdata')
#     result = add_default_content(memberdata_tool, DEFAULT_MEMBERS,
#             initial_transitions=['trigger',])
#     # OK, start sending mail again
#     properties_tool.site_properties.manage_changeProperties(validate_email=1)
#     print >>out, result
# 
#     #
#     # Add content for some members
#     #
#     membership_tool = getToolByName(self, 'portal_membership')
#     members = membership_tool.getMembersFolder()
#     for mp in DEFAULT_MEMBER_DOCS.keys():
#         mf = members[cleanId(normalizeString(mp))]
#         result = add_default_content(mf, DEFAULT_MEMBER_DOCS[mp],
#                 initial_transitions=['submit_to_clerk'])
#         print >>out, result
# 
#     #
#     # Add default groups
#     #
#     portal_groups = getToolByName(self, 'portal_groups')
#     portal_groupdata = getToolByName(self, 'portal_groupdata')
#     for group_dict in DEFAULT_GROUPS:
#         group_id = group_dict['title']
#         group = portal_groups.getGroupById(group_id)
#         if not group:
#             portal_groups.addGroup(group_id)
#             group = portal_groups.getGroupById(group_id)
# 
#         processed={}
#         for id, property in portal_groupdata.propertyItems():
#             processed[id]=group_dict.get(id, None)
#         group.setGroupProperties(processed)
# 
#         for member_title in group_dict['members']:
#             member_id = normalizeString(member_title)
#             group.addMember(member_id)
#         roles = group_dict.get('roles', None)
#         if roles:
#             portal_groups.editGroup(group_id,
#                     roles=[r for r in group_dict['roles']])
# 
#     # Rename the teams tool: ?
#     # TODO teams_tool = getToolByName(self, 'portal_teams')
# 
#     # Add default committees
#     # teams_tool = getToolByName(self, 'portal_teams')
#     teams_tool = getToolByName(self, 'portal_bungeniteamstool')
#     result = add_default_content(teams_tool, DEFAULT_TEAMS, initial_transitions=[])
#     print >>out, result
# 
#     # Add default content
#     result = add_default_content(self, DEFAULT_SITE_CONTENT)
#     print >>out, result
#     result = add_default_content(self, DEFAULT_WORKSPACES, initial_transitions=[])
#     print >>out, result
# 
#     # Publish existing content
#     # We don't want this content to be deleted upon uninstallation
#     do_transition(self, EXISTING_SITE_CONTENT, transition='publish')
#     print >>out, 'Published existing content'
# 
#     # Filter the global tabs
#     # TODO
# 
#     # Hide from navigation
#     for obj in [self.Members, self.workspace, self.help, ]:
#         obj.setExcludeFromNav(True)
#         obj.reindexObject()


def uninstall(self):
    out = StringIO()

    plone = getToolByName(self, 'portal_url').getPortalObject()
    normalizeString = getToolByName(self, 'plone_utils').normalizeString

    # Delete the content we added
    ids = [normalizeString(get_id(d)) for d in DEFAULT_SITE_CONTENT+DEFAULT_WORKSPACES]
    ids = [i for i in ids if plone.get(i, None)]
    plone.manage_delObjects(ids) 
    print >>out, 'Deleted our testing content'

    # Delete the members we added
    membership_tool = getToolByName(self, 'portal_membership')
    membership_tool.deleteMembers([
            normalizeString(get_id(d)) for d in DEFAULT_MEMBERS])
    print >>out, 'Deleted our testing members'

    # Delete the groups we added
    portal_groups = getToolByName(self, 'portal_groups')
    group_ids = [normalizeString(group['title']) for group in DEFAULT_GROUPS]
    group_ids = [i for i in group_ids if portal_groups.getGroupById(i)]
    portal_groups.removeGroups(group_ids)

    # Delete the teams we added
    # teams_tool = getToolByName(self, 'portal_teams')
    teams_tool = getToolByName(self, 'portal_bungeniteamstool')
    ids = [normalizeString(get_id(d)) for d in DEFAULT_TEAMS]
    ids = [i for i in ids if teams_tool.get(i, None)]
    teams_tool.manage_delObjects(ids) 
    print >>out, 'Deleted our testing teams'

    # Automatic?
    # # Remove the new actions
    # REMOVE_ACTIONS=[a['id'] for a in new_actions]
    # idxs = []
    # idx = 0
    # actions_tool = getToolByName(self, 'portal_actions')
    # for action in actions_tool.listActions():
    #     if action.getId() in REMOVE_ACTIONS:
    #         idxs.append(idx)
    #         print >>out, 'Will remove action %s'%action.getId()
    #     idx += 1
    # actions_tool.deleteActions(idxs)
    # print >>out, 'Removed our actions'

    return out.getvalue()
