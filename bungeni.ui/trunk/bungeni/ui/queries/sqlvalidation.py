# encoding: utf-8


checkSessionInterval = """
                         SELECT "short_name"  
                         FROM "public"."sessions" 
                         WHERE ( ( "parliament_id" = %(parent_key)s ) 
                                AND ( '%(date)s' 
                                    BETWEEN "start_date" AND "end_date") )
                        """
checkSittingSessionInterval = """
                        SELECT "start_date" || ' - ' || "end_date" AS interval
                        FROM "public"."group_sittings" 
                        WHERE ( ( "session_id" = %(parent_key)s )
                                 
                                AND ( '%(date)s' 
                                    BETWEEN "start_date" AND "end_date") )
                        """
checkSittingGroupInterval = """
                        SELECT "start_date" || ' - ' || "end_date" AS interval
                        FROM "public"."group_sittings" 
                        WHERE (  ( "group_id" = %(parent_key)s )
                                AND ( '%(date)s' 
                                    BETWEEN "start_date" AND "end_date") )
                        """                      
                        
checkGovernmentInterval = """
                            SELECT "groups"."short_name" 
                            FROM "public"."government", "public"."groups" 
                            WHERE ( ( "government"."government_id" = "groups"."group_id" )
                                AND ( '%(date)s' 
                                    BETWEEN "start_date" AND "end_date") )
                        """
    
checkParliamentInterval = """
                            SELECT "groups"."short_name" 
                            FROM "public"."parliaments", "public"."groups" 
                            WHERE ( ( "parliaments"."parliament_id" = "groups"."group_id" )
                                AND ( '%(date)s' 
                                    BETWEEN "start_date" AND "end_date") )
                        """
checkForOpenParliamentInterval = """
                            SELECT "groups"."short_name" 
                            FROM "public"."parliaments", "public"."groups" 
                            WHERE ( ( "parliaments"."parliament_id" = "groups"."group_id" )
                                    AND "end_date" IS NULL )
                        """

checkForOpenSessionInterval = """
                           SELECT "full_name" FROM "public"."sessions" AS "sessions" 
                           WHERE "end_date" IS NULL 
                           AND "parliament_id" = %(parliament_id)s
                        """



checkForOpenPartymembership = """
                            SELECT "groups"."short_name" 
                            FROM "public"."user_group_memberships", "public"."groups", "public"."political_parties" 
                            WHERE ( "user_group_memberships"."group_id" = "groups"."group_id" 
                                   AND "political_parties"."party_id" = "groups"."group_id" ) 
                              AND ( ( "user_group_memberships"."user_id" = %(user_id)s
                                    AND "user_group_memberships"."end_date" IS NULL ) )
                            
                        """
                       
checkPartymembershipInterval = """
                            SELECT "groups"."short_name" 
                            FROM "public"."user_group_memberships", "public"."groups", "public"."political_parties" 
                            WHERE ( "user_group_memberships"."group_id" = "groups"."group_id" 
                                   AND "political_parties"."party_id" = "groups"."group_id" ) 
                              AND ( ( "user_group_memberships"."user_id" = %(user_id)s )
                                    AND ( '%(date)s' 
                                         BETWEEN "user_group_memberships"."start_date" AND "user_group_memberships"."end_date" ) )
                        """

# check that a member has the title only once
checkMemberTitleDuplicates = """
                        SELECT "user_role_types"."user_role_name", "role_titles"."start_date", "role_titles"."end_date" 
                        FROM "public"."role_titles", "public"."user_role_types" 
                        WHERE ( "role_titles"."title_name_id" = "user_role_types"."user_role_type_id" ) 
                        AND ( ( "role_titles"."title_name_id" = %(title_name_id)s AND "role_titles"."membership_id" = %(membership_id)s ) )
                        AND (('%(date)s' BETWEEN "role_titles"."start_date" AND "role_titles"."end_date")
                             OR (('%(date)s' >= "role_titles"."start_date" AND "role_titles"."end_date" IS NULL)))
                        """
# some member title must be unique at a given time
# in a given group ministery, parliament, ...
# only one minister, speaker, ...
checkMemberTitleUnique = """
                        SELECT "user_role_types"."user_role_name", "role_titles"."start_date", "role_titles"."end_date" 
                        FROM "public"."role_titles", "public"."user_role_types", "public"."user_group_memberships" 
                        WHERE ( "role_titles"."title_name_id" = "user_role_types"."user_role_type_id" 
                            AND "role_titles"."membership_id" = "user_group_memberships"."membership_id" ) 
                        AND ( ( "role_titles"."title_name_id" = %(title_name_id)s 
                                AND "user_group_memberships"."group_id" = %(group_id)s
                                AND "user_role_types"."user_unique" = True ) )
                        AND  ( ('%(date)s' BETWEEN "role_titles"."start_date" AND "role_titles"."end_date")
                             OR (('%(date)s' >= "role_titles"."start_date" AND "role_titles"."end_date" IS NULL)) ) 
                        """
                        

##################
# Edit forms specific validation

checkMySittingSessionInterval = """
                            SELECT "group_sittings_1"."start_date"  || ' - ' ||  "group_sittings_1"."end_date" AS interval
                            FROM "public"."group_sittings" ,  "public"."group_sittings" AS  "group_sittings_1"
                            WHERE ((("group_sittings_1"."session_id" = "group_sittings"."session_id" ) 
                                        AND ( "group_sittings"."sitting_id" = %(parent_key)s ) )
                                    AND ( "group_sittings_1"."sitting_id" !=  %(parent_key)s )
                                    AND ( '%(date)s' 
                                        BETWEEN  "group_sittings_1"."start_date" AND  "group_sittings_1"."end_date"))
                           """
checkMySittingGroupInterval = """
                            SELECT "group_sittings_1"."start_date"  || ' - ' ||  "group_sittings_1"."end_date" AS interval
                            FROM "public"."group_sittings" ,  "public"."group_sittings" AS  "group_sittings_1"
                            WHERE ((( "group_sittings_1"."group_id" = "group_sittings"."group_id" )
                                        AND ( "group_sittings"."sitting_id" = %(parent_key)s ) )
                                    AND ( "group_sittings_1"."sitting_id" !=  %(parent_key)s )
                                    AND ( '%(date)s' 
                                        BETWEEN  "group_sittings_1"."start_date" AND  "group_sittings_1"."end_date"))
                           """
                           

checkMySessionInterval = """
                         SELECT "sessions_1"."short_name"  
                         FROM "public"."sessions", "public"."sessions"  AS "sessions_1"
                         WHERE ( ( "sessions_1"."parliament_id" = "sessions"."parliament_id" )
                                AND ( "sessions"."session_id" = %(parent_key)s )
                                AND ( "sessions_1"."session_id" != %(parent_key)s )
                                AND ( '%(date)s' 
                                    BETWEEN "sessions_1"."start_date" AND "sessions_1"."end_date") )
                        """

                        
checkMyGovernmentInterval = """
                            SELECT "groups"."short_name" 
                            FROM "public"."government", "public"."groups" 
                            WHERE ( ( "government"."government_id" = "groups"."group_id" )
                                AND ( "government"."government_id" != %(parent_key)s )
                                AND ( '%(date)s' 
                                    BETWEEN "start_date" AND "end_date") )
                        """
    
checkMyParliamentInterval = """
                            SELECT "groups"."short_name" 
                            FROM "public"."parliaments", "public"."groups" 
                            WHERE ( ( "parliaments"."parliament_id" = "groups"."group_id" )
                                AND ( "parliaments"."parliament_id" != %(parent_key)s )
                                AND ( '%(date)s' 
                                    BETWEEN "start_date" AND "end_date") )
                        """
                        
checkForMyOpenParliamentInterval = """
                            SELECT "groups"."short_name" 
                            FROM "public"."parliaments", "public"."groups" 
                            WHERE ( ( "parliaments"."parliament_id" = "groups"."group_id" )
                                    AND ( "parliaments"."parliament_id" != %(parent_key)s )
                                    AND "end_date" IS NULL )
                        """

#XXX
checkForMyOpenPartymembership = """
                            SELECT "groups"."short_name" 
                            FROM "public"."user_group_memberships", "public"."groups", "public"."political_parties" 
                            WHERE ( "user_group_memberships"."group_id" = "groups"."group_id" 
                                   AND "political_parties"."party_id" = "groups"."group_id" ) 
                              AND ( ( "user_group_memberships"."user_id" = %(user_id)s
                                    AND "user_group_memberships"."end_date" IS NULL ) )
                              AND ( "user_group_memberships"."membership_id" != %(parent_key)s )                            
                        """
#XXX                        
checkMyPartymembershipInterval = """
                            SELECT "groups"."short_name" 
                            FROM "public"."user_group_memberships", "public"."groups", "public"."political_parties" 
                            WHERE ( "user_group_memberships"."group_id" = "groups"."group_id" 
                                   AND "political_parties"."party_id" = "groups"."group_id" ) 
                              AND ( ( "user_group_memberships"."user_id" = %(user_id)s )
                                    AND ( '%(date)s' 
                                         BETWEEN "user_group_memberships"."start_date" AND "user_group_memberships"."end_date" ) )
                              AND ( "user_group_memberships"."membership_id" != %(parent_key)s )                                                                     
                        """

# check that a member has the title only once
checkMyMemberTitleDuplicates = """
                        SELECT "user_role_types"."user_role_name", "role_titles"."start_date", "role_titles"."end_date" 
                        FROM "public"."role_titles", "public"."user_role_types" 
                        WHERE ( "role_titles"."title_name_id" = "user_role_types"."user_role_type_id" ) 
                        AND ( ( "role_titles"."title_name_id" = %(title_name_id)s AND "role_titles"."membership_id" = %(membership_id)s ) )
                        AND (('%(date)s' BETWEEN "role_titles"."start_date" AND "role_titles"."end_date")
                             OR (('%(date)s' >= "role_titles"."start_date" AND "role_titles"."end_date" IS NULL)))
                        AND ( "role_titles"."role_title_id" != %(role_title_id)s )
                        """
# some member title must be unique at a given time
# in a given group ministery, parliament, ...
# only one minister, speaker, ...
checkMyMemberTitleUnique = """
                        SELECT "user_role_types"."user_role_name", "role_titles"."start_date", "role_titles"."end_date" 
                        FROM "public"."role_titles", "public"."user_role_types", "public"."user_group_memberships" 
                        WHERE ( "role_titles"."title_name_id" = "user_role_types"."user_role_type_id" 
                            AND "role_titles"."membership_id" = "user_group_memberships"."membership_id" ) 
                        AND ( ( "role_titles"."title_name_id" = %(title_name_id)s 
                                AND "user_group_memberships"."group_id" = %(group_id)s
                                AND "user_role_types"."user_unique" = True ) )
                        AND  ( ('%(date)s' BETWEEN "role_titles"."start_date" AND "role_titles"."end_date")
                             OR (('%(date)s' >= "role_titles"."start_date" AND "role_titles"."end_date" IS NULL)) ) 
                        AND ( "role_titles"."role_title_id" != %(role_title_id)s )                             
                        """



                        
