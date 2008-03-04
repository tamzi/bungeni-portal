/* import bungeni demo data */
/* call with bin/psql bungeni < ~/devel/bungenidata/importpg.sql */
/* replace /home/undesa/devel/bungenidata/ with the absolute(!) path where your importdata is located */


copy public.countries from '/home/undesa/devel/bungenidata/countries.csv' csv ;
/* workaround for now because vocabulary source does not accept unicode */
/* XXX */

delete from countries where country_id not in ('AO', 'KE', 'UG', 'ZA');

copy public.provinces from '/home/undesa/devel/bungenidata/provinces.csv' csv ;

copy public.regions from '/home/undesa/devel/bungenidata/regions.csv' csv ;

copy public.constituencies (constituency_id, name, province, region, start_date) from '/home/undesa/devel/bungenidata/constituencies.csv' csv ;

copy public.constituency_details (constituency_id, voters, "date", population) from
'/home/undesa/devel/bungenidata/constituency_details.csv' csv ;

copy public.users ( user_id, first_name, middle_name, last_name, date_of_birth, date_of_death, 
email, birth_country, gender, national_id, active_p, type) 
from  '/home/undesa/devel/bungenidata/users.csv' with delimiter ';' csv ;

update public.users set active_p = 'D' where date_of_death is not null;

update public.users set titles = 'Mrs.' where gender = 'F';
update public.users set titles = 'Mr.' where gender = 'M';


copy public.groups ( group_id, short_name, full_name, start_date, end_date, type) 
from '/home/undesa/devel/bungenidata/parliament_group.csv' with delimiter ';' csv ;

copy public.parliaments (parliament_id, election_date) from '/home/undesa/devel/bungenidata/parliaments.csv'
with delimiter ';' csv;

copy public.groups ( group_id, short_name, full_name, start_date, end_date, type) 
from '/home/undesa/devel/bungenidata/government_group.csv'
csv ;

copy public.government from  '/home/undesa/devel/bungenidata/governments.csv'
csv ;


copy public.groups ( group_id, short_name, full_name, description, start_date, end_date, type) 
from '/home/undesa/devel/bungenidata/ministry_group.csv'
csv ;

copy public.ministries ( government_id, ministry_id ) 
from '/home/undesa/devel/bungenidata/ministries.csv'
csv ; 




copy public.user_group_memberships (membership_id, user_id, group_id, start_date, end_date, notes)
from '/home/undesa/devel/bungenidata/parliament_group_members.csv'
csv;

copy public.parliament_members (membership_id, constituency_id,  elected_nominated , leave_reason)
    from '/home/undesa/devel/bungenidata/parliament_members.csv'
csv ;

update public.parliament_members set elected_nominated ='N' where constituency_id = 0; 

copy public.sessions (session_id, parliament_id, short_name, start_date, end_date, notes)
from '/home/undesa/devel/bungenidata/sessions.csv'
csv ;

/* political parties */
copy public.groups( group_id, short_name, start_date, type )
from '/home/undesa/devel/bungenidata/parties.csv'
csv ;

copy public.political_parties (party_id)
from '/home/undesa/devel/bungenidata/party_groups.csv'
csv ;

/* comittees */
copy public.committee_types
from '/home/undesa/devel/bungenidata/committee_types.csv'
csv;

copy public.groups ( group_id, start_date, end_date, short_name, full_name, description, type)
from '/home/undesa/devel/bungenidata/committee_groups.csv'
csv ;

copy public.committees ( committee_id, parliament_id, committee_type_id, no_members, min_no_members,
quorum, proportional_representation)
from '/home/undesa/devel/bungenidata/committees.csv'
csv;

 SELECT setval('user_group_memberships_membership_id_seq', 2000);

copy public.user_group_memberships ( group_id, user_id, title, start_date, end_date)
from '/home/undesa/devel/bungenidata/committees_membership.csv'
csv;


copy public.user_group_memberships ( group_id, user_id, start_date, end_date, notes)
from '/home/undesa/devel/bungenidata/ministers.csv'
csv;

copy public.sitting_type (sitting_type_id, sitting_type)
from '/home/undesa/devel/bungenidata/sitting_type.csv'
csv;

copy public.group_sittings (sitting_id, group_id, session_id, sitting_type, start_date, end_date)
from '/home/undesa/devel/bungenidata/sittings.csv'
csv;

copy public.attendance_type( attendance_id, attendance_type)
from '/home/undesa/devel/bungenidata/attendance_type.csv'
csv;

copy public.user_group_memberships ( user_id, group_id, start_date, end_date)
from '/home/undesa/devel/bungenidata/partymembers.csv'
csv;


/* set the active flags to something sane */

update user_group_memberships set active_p =  false where end_date is not null;

update user_group_memberships set active_p =  true  where end_date is  null;

update users set active_p = 'I' where user_id not in (select user_id from user_group_memberships where active_p = True);

update users set active_p = 'D' where date_of_death is not null;

copy public.sitting_attendance( sitting_id, member_id, attendance_id)
from '/home/undesa/devel/bungenidata/sitting_attendance.csv'
csv;


/*get all sequences */
select  sequence_name from information_schema.sequences
where sequence_schema='public';

/*set the sequences to a new value*/
 
 SELECT setval('groups_group_id_seq', 1000);
 SELECT setval('sessions_session_id_seq', 1000);
 SELECT setval('item_sequence', 1000);
 SELECT setval('group_sittings_sitting_id_seq', 5000);
 SELECT setval('items_schedule_schedule_id_seq', 1000);
 SELECT setval('question_changes_change_id_seq', 1000);
 SELECT setval('bill_versions_version_id_seq', 1000);
 SELECT setval('question_versions_version_id_seq', 1000);
 SELECT setval('responses_response_id_seq', 1000);
 SELECT setval('bill_changes_change_id_seq', 1000);
 SELECT setval('object_subscriptions_subscriptions_id_seq', 1000);
 SELECT setval('group_assignments_assignment_id_seq', 1000);
 SELECT setval('item_votes_vote_id_seq', 1000);
 SELECT setval('provinces_province_id_seq', 1000);
 SELECT setval('users_user_id_seq', 1000);
 SELECT setval('takes_take_id_seq', 1000);
 SELECT setval('take_media_media_id_seq', 1000);
 SELECT setval('rotas_rota_id_seq', 1000);
 SELECT setval('transcripts_transcript_id_seq', 1000);
 SELECT setval('regions_region_id_seq', 1000);
 SELECT setval('motion_amendments_amendment_id_seq', 1000);
 SELECT setval('motion_changes_change_id_seq', 1000);
 SELECT setval('committee_types_committee_type_id_seq', 1000);
 SELECT setval('constituencies_constituency_id_seq', 1000);
 SELECT setval('motion_versions_version_id_seq', 1000);
 SELECT setval('constituency_details_constituency_detail_id_seq', 1000);






