# encoding: utf-8

##########################
# add form specific validations

# sessions of a parliament cannot overlap
# this is called for start and end date of the session to be added
checkSessionInterval = """
     SELECT "short_name"  
     FROM "public"."sessions" 
     WHERE ( ( "parliament_id" =  :parent_key  ) 
            AND ( :date  
                BETWEEN "start_date" AND "end_date") )
                        """
# sittings of a seesion cannot overlap
# this is called for start and end date of a sitting
                        
checkSittingSessionInterval = """
    SELECT "start_date" || ' - ' || "end_date" AS interval
    FROM "public"."group_sittings" 
    WHERE ( ( "group_id" =  :parent_key  )
             
            AND ( :date  
                BETWEEN "start_date" AND "end_date") )
                        """
# sittings of a group cannot overlap                        
# this is called for start and end date of a sitting
checkSittingGroupInterval = """
    SELECT "start_date" || ' - ' || "end_date" AS interval
    FROM "public"."group_sittings" 
    WHERE (  ( "group_id" =  :parent_key  )
            AND ( :date  
                BETWEEN "start_date" AND "end_date") )
                        """                      
# governments cannot overlap
# called for start and end date of a government to be added
                        
checkGovernmentInterval = """
    SELECT "groups"."short_name" 
    FROM "public"."government", "public"."groups" 
    WHERE ( ( "government"."government_id" = "groups"."group_id" )
        AND ( :date  
            BETWEEN "start_date" AND "end_date") )
                        """
# parliaments cannot overlap
# called for start and end date of the parliament to be added 
    
checkParliamentInterval = """
    SELECT "groups"."short_name" 
    FROM "public"."parliaments", "public"."groups" 
    WHERE ( ( "parliaments"."parliament_id" = "groups"."group_id" )
        AND ( :date  
            BETWEEN "start_date" AND "end_date") )
            """
# A new parliament can only be added when all other 
# parliaments have an end date                        
checkForOpenParliamentInterval = """
    SELECT "groups"."short_name" 
    FROM "public"."parliaments", "public"."groups" 
    WHERE ( ( "parliaments"."parliament_id" = "groups"."group_id" )
            AND "end_date" IS NULL )
                        """

# A new session can only be added when all other sessions 
# of this parliament have an end date

checkForOpenSessionInterval = """
   SELECT "full_name" FROM "public"."sessions" AS "sessions" 
   WHERE "end_date" IS NULL 
   AND "parliament_id" =  :parliament_id 
                        """

# A new partymembership can only be added when all other
# partymemberships for this user have an end date
checkForOpenPartymembership = """
    SELECT "groups"."short_name" 
    FROM "public"."user_group_memberships", 
        "public"."groups", 
        "public"."political_parties" 
    WHERE ( "user_group_memberships"."group_id" = "groups"."group_id" 
           AND "political_parties"."party_id" = "groups"."group_id" ) 
      AND ( ( "user_group_memberships"."user_id" =  :user_id 
            AND "user_group_memberships"."end_date" IS NULL ) )
                            
                        """
# partymemberships cannot overlap
# called for start and end date of the parymembership to be added
                       
checkPartymembershipInterval = """
    SELECT "groups"."short_name" 
    FROM "public"."user_group_memberships", 
        "public"."groups", 
        "public"."political_parties" 
    WHERE ( "user_group_memberships"."group_id" = "groups"."group_id" 
           AND "political_parties"."party_id" = "groups"."group_id" ) 
      AND ( ( "user_group_memberships"."user_id" =  :user_id  )
            AND ( :date  
                 BETWEEN "user_group_memberships"."start_date" 
                 AND "user_group_memberships"."end_date" ) )
                        """

# check that a member has the title only once

checkMemberTitleDuplicates = """
    SELECT "user_role_types"."user_role_name", 
        "role_titles"."start_date", 
        "role_titles"."end_date" 
    FROM "public"."role_titles", 
        "public"."user_role_types" 
    WHERE ( "role_titles"."title_name_id" = 
            "user_role_types"."user_role_type_id" ) 
    AND ( ( "role_titles"."title_name_id" =  :title_name_id  
        AND "role_titles"."membership_id" =  :membership_id  ) )
    AND ((:date  BETWEEN "role_titles"."start_date" 
        AND "role_titles"."end_date")
         OR ((:date  >= "role_titles"."start_date" 
            AND "role_titles"."end_date" IS NULL)))
                        """

# some member title must be unique at a given time
# in a given group ministery, parliament, ...
# only one minister, speaker, ...
checkMemberTitleUnique = """
    SELECT "user_role_types"."user_role_name", 
        "role_titles"."start_date", 
        "role_titles"."end_date" 
    FROM "public"."role_titles", 
        "public"."user_role_types", 
        "public"."user_group_memberships" 
    WHERE ( "role_titles"."title_name_id" = "user_role_types"."user_role_type_id" 
        AND "role_titles"."membership_id" = "user_group_memberships"."membership_id" ) 
    AND ( ( "role_titles"."title_name_id" =  :title_name_id  
            AND "user_group_memberships"."group_id" =  :group_id 
            AND "user_role_types"."user_unique" = True ) )
    AND  ( (:date  BETWEEN "role_titles"."start_date" 
                AND "role_titles"."end_date")
         OR ((:date  >= "role_titles"."start_date" 
                AND "role_titles"."end_date" IS NULL)) ) 
    """
    

##################
# Edit forms specific validation


# sessions of a parliament cannot overlap
# this is called for start and end date of the session to be added
# excludes the session itself
checkMySessionInterval = """
     SELECT "sessions_1"."short_name"  
     FROM "public"."sessions", 
        "public"."sessions"  AS "sessions_1"
     WHERE ( ( "sessions_1"."parliament_id" = "sessions"."parliament_id" )
            AND ( "sessions"."session_id" =  :parent_key  )
            AND ( "sessions_1"."session_id" !=  :parent_key  )
            AND ( :date  
                BETWEEN "sessions_1"."start_date" 
                AND "sessions_1"."end_date") )
                        """


# sittings of a seesion cannot overlap
# this is called for start and end date of a sitting
# and excludes the sitting itself

checkMySittingSessionInterval = """
    SELECT "group_sittings_1"."start_date"  || ' - ' ||  
        "group_sittings_1"."end_date" AS interval
    FROM "public"."group_sittings" ,  
        "public"."group_sittings" AS  "group_sittings_1"
    WHERE (( ( "group_sittings"."sitting_id" =  :parent_key  ) )
            AND ( "group_sittings_1"."sitting_id" !=   :parent_key  )
            AND ( :date  
                BETWEEN  "group_sittings_1"."start_date" 
                AND  "group_sittings_1"."end_date"))
                           """
                           
# sittings of a group cannot overlap                        
# this is called for start and end date of a sitting
# excludes the sitting itself
                           
checkMySittingGroupInterval = """
    SELECT "group_sittings_1"."start_date"  || ' - ' ||  
        "group_sittings_1"."end_date" AS interval
    FROM "public"."group_sittings" ,  
        "public"."group_sittings" AS  "group_sittings_1"
    WHERE ((( "group_sittings_1"."group_id" = "group_sittings"."group_id" )
                AND ( "group_sittings"."sitting_id" =  :parent_key  ) )
            AND ( "group_sittings_1"."sitting_id" !=   :parent_key  )
            AND ( :date  
                BETWEEN  "group_sittings_1"."start_date" 
                AND  "group_sittings_1"."end_date"))
           """
                           
# governments cannot overlap
# called for start and end date of a government edited
# excludes the government itself
                        
checkMyGovernmentInterval = """
    SELECT "groups"."short_name" 
    FROM "public"."government", 
        "public"."groups" 
    WHERE ( ( "government"."government_id" = "groups"."group_id" )
        AND ( "government"."government_id" !=  :parent_key  )
        AND ( :date  
            BETWEEN "start_date" 
            AND "end_date") )
        """
    
# parliaments cannot overlap
# called for start and end date of the parliament edited
# excludes the parliament itself
    
checkMyParliamentInterval = """
    SELECT "groups"."short_name" 
    FROM "public"."parliaments", "public"."groups" 
    WHERE ( ( "parliaments"."parliament_id" = "groups"."group_id" )
        AND ( "parliaments"."parliament_id" !=  :parent_key  )
        AND ( :date  
            BETWEEN "start_date" AND "end_date") )
    """

# A parliament can only be edited when all _other_ 
# parliaments have an end date                    
          
checkForMyOpenParliamentInterval = """
    SELECT "groups"."short_name" 
    FROM "public"."parliaments", "public"."groups" 
    WHERE ( ( "parliaments"."parliament_id" = "groups"."group_id" )
            AND ( "parliaments"."parliament_id" !=  :parent_key  )
            AND "end_date" IS NULL )
    """

#XXX
# A  partymembership can only be edited when all _other_
# partymemberships for this user have an end date

checkForMyOpenPartymembership = """
    SELECT "groups"."short_name" 
    FROM "public"."user_group_memberships", 
        "public"."groups", 
        "public"."political_parties" 
    WHERE ( "user_group_memberships"."group_id" = "groups"."group_id" 
           AND "political_parties"."party_id" = "groups"."group_id" ) 
      AND ( ( "user_group_memberships"."user_id" =  :user_id 
            AND "user_group_memberships"."end_date" IS NULL ) )
      AND ( "user_group_memberships"."membership_id" !=  :parent_key  )                            
    """
#XXX       
# partymemberships cannot overlap
                 
checkMyPartymembershipInterval = """
    SELECT "groups"."short_name" 
    FROM "public"."user_group_memberships", 
        "public"."groups", 
        "public"."political_parties" 
    WHERE ( "user_group_memberships"."group_id" = "groups"."group_id" 
           AND "political_parties"."party_id" = "groups"."group_id" ) 
      AND ( ( "user_group_memberships"."user_id" =  :user_id  )
            AND ( :date  
                 BETWEEN "user_group_memberships"."start_date" 
                 AND "user_group_memberships"."end_date" ) )
      AND ( "user_group_memberships"."membership_id" !=  :parent_key  )                                                                     
    """

# check that a member has the title only once
checkMyMemberTitleDuplicates = """
    SELECT "user_role_types"."user_role_name", 
        "role_titles"."start_date", 
        "role_titles"."end_date" 
    FROM "public"."role_titles", 
        "public"."user_role_types" 
    WHERE ( "role_titles"."title_name_id" = "user_role_types"."user_role_type_id" ) 
    AND ( ( "role_titles"."title_name_id" =  :title_name_id  
        AND "role_titles"."membership_id" =  :membership_id  ) )
    AND ((:date  BETWEEN "role_titles"."start_date" 
                AND "role_titles"."end_date")
         OR ((:date  >= "role_titles"."start_date" 
            AND "role_titles"."end_date" IS NULL)))
    AND ( "role_titles"."role_title_id" !=  :role_title_id  )
    """
# some member title must be unique at a given time
# in a given group ministery, parliament, ...
# only one minister, speaker, ...
checkMyMemberTitleUnique = """
    SELECT "user_role_types"."user_role_name", 
        "role_titles"."start_date", 
        "role_titles"."end_date" 
    FROM "public"."role_titles", 
        "public"."user_role_types", 
        "public"."user_group_memberships" 
    WHERE ( "role_titles"."title_name_id" = "user_role_types"."user_role_type_id" 
        AND "role_titles"."membership_id" = "user_group_memberships"."membership_id" ) 
    AND ( ( "role_titles"."title_name_id" =  :title_name_id  
            AND "user_group_memberships"."group_id" =  :group_id 
            AND "user_role_types"."user_unique" = True ) )
    AND  ( (:date  BETWEEN "role_titles"."start_date" 
                    AND "role_titles"."end_date")
         OR ((:date  >= "role_titles"."start_date" 
                AND "role_titles"."end_date" IS NULL)) ) 
    AND ( "role_titles"."role_title_id" !=  :role_title_id  )                             
    """

