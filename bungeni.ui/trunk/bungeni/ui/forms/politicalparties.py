# encoding: utf-8

# Political parties

sql_getcount_mp_parties = """
SELECT "parliaments"."parliament_id", 
        "political_parties"."party_id",  
        COUNT( "user_group_memberships"."user_id" ) AS no_members, 
        MIN( "groups_1"."short_name" )
FROM "public"."parliaments", 
    "public"."groups", 
    "public"."user_group_memberships", 
    "public"."user_group_memberships" AS "user_group_memberships_1", 
    "public"."groups" AS  "groups_1",
    "public"."political_parties" 
    WHERE (( "parliaments"."parliament_id" = "groups"."group_id" 
            AND "user_group_memberships"."group_id" = "groups"."group_id" 
            AND "user_group_memberships_1"."group_id" = "groups_1"."group_id" 
            AND "user_group_memberships_1"."user_id" = "user_group_memberships"."user_id" 
            AND "political_parties"."party_id" = "groups_1"."group_id" 
            )
        AND (
            (('2000-1-1' BETWEEN "user_group_memberships"."start_date" AND "user_group_memberships"."end_date")
             OR ('2000-1-1' > "user_group_memberships"."start_date" AND "user_group_memberships"."end_date" IS NULL)
             )
            AND
            (('2000-1-1' BETWEEN "user_group_memberships_1"."start_date" AND "user_group_memberships_1"."end_date")
             OR ('2000-1-1' > "user_group_memberships_1"."start_date" AND "user_group_memberships_1"."end_date" IS NULL)
             )             
        ))
GROUP BY "parliaments"."parliament_id", "party_id"         
UNION
SELECT "parliaments"."parliament_id", 0 AS "party_id",       
       COUNT( "user_group_memberships"."user_id" ) AS no_members,
       'N/A' as party
FROM "public"."parliaments", 
    "public"."groups", 
    "public"."user_group_memberships", 
    "public"."users" 
    WHERE (( "parliaments"."parliament_id" = "groups"."group_id" 
        AND "user_group_memberships"."group_id" = "groups"."group_id" 
        AND "user_group_memberships"."user_id" = "users"."user_id" )
     AND(
        ('2000-1-1' BETWEEN "user_group_memberships"."start_date" AND "user_group_memberships"."end_date")
         OR ('2000-1-1' > "user_group_memberships"."start_date" AND "user_group_memberships"."end_date" IS NULL)
        )
    AND "users"."user_id" NOT IN
        (SELECT "user_group_memberships_1"."user_id" 
        FROM "public"."political_parties", 
            "public"."groups" AS party_group, 
            "public"."user_group_memberships" AS "user_group_memberships_1"
        WHERE (( "political_parties"."party_id" = "party_group"."group_id" 
                AND "user_group_memberships_1"."group_id" = "party_group"."group_id" )    
            AND (('2000-1-1' BETWEEN "user_group_memberships_1"."start_date" AND "user_group_memberships_1"."end_date")
             OR ('2000-1-1' > "user_group_memberships_1"."start_date" AND "user_group_memberships_1"."end_date" IS NULL)
             ))
        )
    )        
        
GROUP BY "parliaments"."parliament_id", "party_id" 
ORDER BY no_members DESC
"""

 
sql_get_mp_parties = """
SELECT "parliaments"."parliament_id", "political_parties"."party_id", "user_group_memberships"."user_id", 
       MIN( "groups_1"."short_name" ) AS party,
       MIN("users"."last_name" || ', ' || "users"."first_name") as fullname 
FROM  "public"."parliaments", 
    "public"."groups", 
    "public"."user_group_memberships", 
    "public"."user_group_memberships" AS "user_group_memberships_1", 
    "public"."groups" AS  "groups_1",
    "public"."political_parties", 
    "public"."users" 
        WHERE (( "parliaments"."parliament_id" = "groups"."group_id" 
            AND "user_group_memberships"."group_id" = "groups"."group_id" 
            AND "user_group_memberships_1"."group_id" = "groups_1"."group_id" 
            AND "user_group_memberships_1"."user_id" = "user_group_memberships"."user_id" 
            AND "political_parties"."party_id" = "groups_1"."group_id" 
            AND "user_group_memberships"."user_id" = "users"."user_id"
            )
        AND (
            (('2000-1-1' BETWEEN "user_group_memberships"."start_date" AND "user_group_memberships"."end_date")
             OR ('2000-1-1' > "user_group_memberships"."start_date" AND "user_group_memberships"."end_date" IS NULL)
             )
            AND
            (('2000-1-1' BETWEEN "user_group_memberships_1"."start_date" AND "user_group_memberships_1"."end_date")
             OR ('2000-1-1' > "user_group_memberships_1"."start_date" AND "user_group_memberships_1"."end_date" IS NULL)
             )             
        ))
          
GROUP BY "parliaments"."parliament_id", "political_parties"."party_id", "user_group_memberships"."user_id" 
UNION
SELECT "parliaments"."parliament_id", 0 AS "party_id", "user_group_memberships"."user_id", 
       'N/A' AS party,
       ("users"."last_name" || ', ' || "users"."first_name") as fullname 

FROM "public"."parliaments", 
    "public"."groups", 
    "public"."user_group_memberships", 
    "public"."users" 
    WHERE (( "parliaments"."parliament_id" = "groups"."group_id" 
        AND "user_group_memberships"."group_id" = "groups"."group_id" 
        AND "user_group_memberships"."user_id" = "users"."user_id" )
     AND(
        ('2000-1-1' BETWEEN "user_group_memberships"."start_date" AND "user_group_memberships"."end_date")
         OR ('2000-1-1' > "user_group_memberships"."start_date" AND "user_group_memberships"."end_date" IS NULL)
        )
    AND "users"."user_id" NOT IN
        (SELECT "user_group_memberships_1"."user_id" 
        FROM "public"."political_parties", 
            "public"."groups" AS party_group, 
            "public"."user_group_memberships" AS "user_group_memberships_1"
        WHERE (( "political_parties"."party_id" = "party_group"."group_id" 
                AND "user_group_memberships_1"."group_id" = "party_group"."group_id" )    
            AND (('2000-1-1' BETWEEN "user_group_memberships_1"."start_date" AND "user_group_memberships_1"."end_date")
             OR ('2000-1-1' > "user_group_memberships_1"."start_date" AND "user_group_memberships_1"."end_date" IS NULL)
             ))
        )
    )

GROUP BY "parliaments"."parliament_id", "party_id", "user_group_memberships"."user_id" , fullname
ORDER BY "party_id", fullname
"""


