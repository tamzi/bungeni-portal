# encoding: utf-8

sql_addMinister = """
    SELECT DISTINCT "users"."titles" || ' ' || 
        "users"."first_name" || ' ' || 
        "users"."middle_name" || ' ' || 
        "users"."last_name" AS fullname, 
        "users"."user_id", 
        "users"."last_name" 
    FROM "public"."ministries", 
        "public"."government", 
        "public"."parliaments", 
        "public"."user_group_memberships", 
        "public"."users" 
    WHERE ( "ministries"."government_id" = "government"."government_id" 
    AND "government"."parliament_id" = "parliaments"."parliament_id" 
    AND "user_group_memberships"."group_id" = "parliaments"."parliament_id" 
    AND "user_group_memberships"."user_id" = "users"."user_id" ) 
    AND ( "user_group_memberships"."active_p" = True 
        AND "ministries"."ministry_id" = :primary_key )
    AND ( "users"."user_id" NOT IN 
        ( SELECT "user_id" 
            FROM "public"."user_group_memberships" 
            WHERE ( "group_id"  = :primary_key 
                    AND "active_p" = True) 
            )                                           
        ) 
    UNION
    SELECT DISTINCT "users"."titles" || ' ' || 
            "users"."first_name" || ' ' || 
            "users"."middle_name" || ' ' || 
            "users"."last_name" 
        AS fullname, 
        "users"."user_id", 
        "users"."last_name" 
    FROM "public"."ministries", 
        "public"."government", 
        "public"."groups", 
        "public"."extension_groups", 
        "public"."user_group_memberships", 
        "public"."users" 
    WHERE ( "ministries"."government_id" = "government"."government_id" 
    AND "ministries"."ministry_id" = "groups"."group_id" 
    AND "extension_groups"."group_type" = "groups"."type" 
    AND "extension_groups"."extension_type_id" = "user_group_memberships"."group_id" 
    AND "user_group_memberships"."user_id" = "users"."user_id" 
    AND "extension_groups"."parliament_id" = "government"."parliament_id" ) 
    AND ( "user_group_memberships"."active_p" = True 
        AND "ministries"."ministry_id" = :primary_key )
    AND ( "users"."user_id" NOT IN ( 
        SELECT "user_id" 
        FROM "public"."user_group_memberships" 
        WHERE ( "group_id"  = :primary_key 
                AND "active_p" = True) 
        )                                           
    )                                     
    ORDER BY "last_name"
                """

#XXX currently filters by "type" = 'memberofparliament' 
#-> has to be replaced with all electable usertypes

sql_addExtensionMember = """
    SELECT DISTINCT "users"."titles" || ' ' || 
            "users"."first_name" || ' ' || 
            "users"."middle_name" || ' ' || 
            "users"."last_name" AS fullname, 
            "users"."user_id", 
            "users"."last_name" 
    FROM "public"."users" 
    WHERE ( ( "active_p" = 'A' 
                AND "type" = 'memberofparliament' )
    AND ( "users"."user_id" NOT IN ( 
            SELECT "user_id" 
            FROM "public"."user_group_memberships" 
            WHERE ( "group_id"  = :primary_key 
                    AND "active_p" = True) 
            )                                           
        )
    AND ( "users"."user_id" NOT IN (
        SELECT "user_group_memberships"."user_id" 
        FROM "public"."user_group_memberships", "public"."extension_groups" 
        WHERE ( "user_group_memberships"."group_id" = "extension_groups"."parliament_id" ) 
        AND ( "extension_groups"."extension_type_id" = :primary_key  
                AND "active_p" = True) 
        )
        )         
        )                    
    ORDER BY "last_name"
    """


sql_AddCommitteeMember = """
    SELECT DISTINCT "users"."titles" || ' ' || 
        "users"."first_name" || ' ' || 
        "users"."middle_name" || ' ' || 
        "users"."last_name" AS fullname, 
        "users"."user_id", 
        "users"."last_name" 
    FROM "public"."user_group_memberships", 
        "public"."users", 
        "public"."extension_groups", 
        "public"."groups", 
        "public"."committees", 
        "public"."parliaments" 
    WHERE ( "user_group_memberships"."user_id" = "users"."user_id" 
            AND "extension_groups"."extension_type_id" = "user_group_memberships"."group_id" 
            AND "extension_groups"."group_type" = "groups"."type" 
            AND "committees"."committee_id" = "groups"."group_id" 
            AND "committees"."parliament_id" = "parliaments"."parliament_id" 
            AND "extension_groups"."parliament_id" = "parliaments"."parliament_id" ) 
            AND ( "committees"."committee_id" = :primary_key  
                AND "user_group_memberships"."active_p" = True )
            AND ( "users"."user_id" NOT IN ( 
                SELECT "user_id" 
                FROM "public"."user_group_memberships" 
                WHERE ( "group_id"  = :primary_key 
                        AND "active_p" = True) 
                )                                           
                ) 
    UNION
    SELECT DISTINCT "users"."titles" || ' ' || "
        users"."first_name" || ' ' || 
        "users"."middle_name" || ' ' || 
        "users"."last_name" AS fullname,  
        "users"."user_id", 
        "users"."last_name" 
    FROM "public"."committees", "public"."parliaments", "public"."groups", 
        "public"."user_group_memberships", "public"."users" 
    WHERE ( "committees"."parliament_id" = "parliaments"."parliament_id" 
    AND "parliaments"."parliament_id" = "groups"."group_id" 
    AND "user_group_memberships"."group_id" = "groups"."group_id" 
    AND "user_group_memberships"."user_id" = "users"."user_id" ) 
    AND ( "user_group_memberships"."active_p" = True 
        AND "committees"."committee_id" = :primary_key )
    AND ( "users"."user_id" NOT IN ( 
        SELECT "user_id" 
        FROM "public"."user_group_memberships" 
        WHERE ( "group_id"  = :primary_key 
                AND "active_p" = True) 
                            )                                           
        )
    ORDER BY "last_name"
    """

sql_AddCommitteeStaff = """                        
    SELECT DISTINCT "users"."titles" || ' ' || 
        "users"."first_name" || ' ' || 
        "users"."middle_name" || ' ' || 
        "users"."last_name" AS fullname, 
        "users"."user_id", 
        "users"."last_name" 
    FROM "public"."users" 
    WHERE ( ( "active_p" = 'A' AND "type" = 'staff' )
            AND ( "users"."user_id" NOT IN ( 
                SELECT "user_id" 
                FROM "public"."user_group_memberships" 
                WHERE ( "group_id"  = :primary_key 
                        AND "active_p" = True) 
                )                                           
                )                                   
           )                    
    ORDER BY "last_name"                       
                        """
                        
sql_AddMemberOfParliament = """
    SELECT "titles" ||' ' || 
        "first_name" || ' ' || 
        "middle_name" || ' ' || 
        "last_name" AS fullname, 
        "user_id" 
    FROM "public"."users" 
    WHERE ( ( "active_p" = 'A' ) 
        AND ( "users"."user_id" NOT IN ( 
            SELECT "user_id" 
            FROM "public"."user_group_memberships" 
            WHERE ( "group_id"  = :primary_key 
                    AND "active_p" = True) 
            )                                           
            )
        )
    ORDER BY "users"."last_name"  
    """
                            
sql_add_members ='''
    SELECT "users"."titles" || ' ' || 
        "users"."first_name" || ' ' || 
        "users"."middle_name" || ' ' || 
        "users"."last_name" AS user_name, 
        "users"."user_id", 
        "group_sittings"."sitting_id" 
    FROM "public"."group_sittings",  
        "public"."user_group_memberships", 
        "public"."users" 
    WHERE ("user_group_memberships"."group_id" = "group_sittings"."group_id" 
    AND "user_group_memberships"."user_id" = "users"."user_id" )
    AND ( "user_group_memberships"."active_p" = True )
    AND ("group_sittings"."sitting_id" = :primary_key)
    AND ( "users"."user_id" NOT IN (
        SELECT member_id 
        FROM sitting_attendance 
        WHERE sitting_id = :primary_key )                                           
        )
    ORDER BY "users"."last_name"                    
    '''
                    
sql_addMemberTitle = '''
    SELECT "user_role_types"."sort_order" || ' - ' || 
        "user_role_types"."user_role_name" AS "ordered_title", 
        "user_role_types"."user_role_type_id"
    FROM "public"."user_role_types", 
        "public"."user_group_memberships" 
    WHERE ( "user_role_types"."user_type" = "user_group_memberships"."membership_type" ) 
        AND ( ( "user_group_memberships"."membership_id" = :primary_key ) ) 
    ORDER BY "user_role_types"."sort_order" ASC
                       '''

sql_select_question_ministry_add = """
    SELECT "groups"."short_name", 
        "groups"."full_name", 
        "groups"."group_id"  
    FROM "public"."ministries" AS "ministries", 
        "public"."groups" AS "groups" 
    WHERE "ministries"."ministry_id" = "groups"."group_id"
    AND ( (current_date BETWEEN "groups"."start_date" 
            AND  "groups"."end_date")
         OR ( ("groups"."start_date" < current_date) 
            AND ("groups"."end_date" IS NULL))
         )
    ORDER BY short_name
        """

#################
# return only current member
# Members should not be editable (exchanged) once they were added

sql_edit_members = '''
    SELECT "users"."titles" || ' ' || 
        "users"."first_name" || ' ' || 
        "users"."middle_name" || ' ' || 
        "users"."last_name" AS user_name, 
    "users"."user_id" 
    FROM  "public"."users" 
    WHERE  "users"."user_id" = :member_id                                                                  
                    '''            


sql_editSubstitution = """
    SELECT "users"."titles" || ' ' || 
        "users"."first_name" || ' ' || 
        "users"."middle_name" || ' ' || 
        "users"."last_name" AS user_name,        
        "users"."user_id" , 
        "users"."last_name"
    FROM "public"."user_group_memberships", 
        "public"."users" 
    WHERE ( "user_group_memberships"."user_id" = "users"."user_id" ) 
        AND ( ( "user_group_memberships"."group_id" = :group_id 
            AND "user_group_memberships"."user_id" != :user_id 
            AND "user_group_memberships"."active_p" = True ) ) 
    UNION
    SELECT "users"."titles" || ' ' || 
        "users"."first_name" || ' ' || 
        "users"."middle_name" || ' ' || 
        "users"."last_name" AS user_name,        
        "users"."user_id" , 
        "users"."last_name"
    FROM  "public"."user_group_memberships", 
        "public"."users"
    WHERE (( "user_group_memberships"."replaced_id" = "users"."user_id" ) 
        AND "user_group_memberships"."user_id" = :user_id )                             
    ORDER BY "last_name" ASC
        """
                        
sql_EditMemberTitle = '''
    SELECT "user_role_types"."sort_order" || ' - ' || 
        "user_role_types"."user_role_name" AS "ordered_title", 
        "user_role_types"."user_role_type_id"
    FROM "public"."user_role_types", 
        "public"."user_group_memberships" 
    WHERE ( "user_role_types"."user_type" = "user_group_memberships"."membership_type" ) 
        AND ( ( "user_group_memberships"."membership_id" = :primary_key ) ) 
    ORDER BY "user_role_types"."sort_order" ASC
       '''
                          
sql_select_question_ministry_edit = """
    SELECT "groups"."short_name", 
        "groups"."full_name", 
        "groups"."group_id"
    FROM "public"."ministries" AS "ministries", 
        "public"."groups" AS "groups", 
        "public"."government" AS "government" 
    WHERE "ministries"."ministry_id" = "groups"."group_id" 
        AND "ministries"."government_id" = "government"."government_id" 
        AND "government"."parliament_id" = :parliament_id
        AND ( (current_date BETWEEN "groups"."start_date" 
            AND  "groups"."end_date")
             OR ( ("groups"."start_date" < current_date) 
                AND ("groups"."end_date" IS NULL))
             )
    ORDER BY short_name
    """


# timeline for a bill
# select all relevant events:
# sittings for which this bill was scheduled,
# manually created events,
# workflow changes, 
# manually created versions.


sql_bill_timeline = """
     SELECT 'schedule' AS "atype",  
            "items_schedule"."item_id" AS "item_id", 
            "items_schedule"."item_status" AS "title", 
            "group_sittings"."start_date" AS "adate" 
        FROM "public"."items_schedule" AS "items_schedule", 
            "public"."group_sittings" AS "group_sittings" 
        WHERE "items_schedule"."sitting_id" = "group_sittings"."sitting_id" 
        AND "items_schedule"."active" = True
        AND "items_schedule"."item_id" = :item_id
     UNION
        SELECT "parliamentary_items"."type" AS "atype", 
            "parliamentary_items"."parliamentary_item_id" AS "item_id", 
            "parliamentary_items"."short_name" AS "title", 
            "event_items"."event_date" AS "adate"
        FROM "public"."event_items" AS "event_items", 
            "public"."parliamentary_items" AS "parliamentary_items" 
        WHERE "event_items"."event_item_id" = "parliamentary_items"."parliamentary_item_id"
        AND "event_items"."event_item_id" = :item_id
     UNION
        SELECT "action" as "atype", "content_id" AS "item_id", 
        "description" AS "title", 
        "date" AS "adate" 
        FROM "public"."bill_changes" AS "bill_changes" 
        WHERE "action" = 'workflow'
        AND "content_id" = :item_id
     UNION
        SELECT 'version' AS "atype", 
            "bill_changes"."change_id" AS "item_id", 
            "bill_changes"."description" AS "title", 
            "bill_changes"."date" AS "adate" 
        FROM "public"."bill_versions" AS "bill_versions", 
            "public"."bill_changes" AS "bill_changes" 
        WHERE "bill_versions"."change_id" = "bill_changes"."change_id" 
        AND "bill_versions"."manual" = True           
        AND "bill_changes"."content_id" = :item_id   
     ORDER BY adate DESC
     """
