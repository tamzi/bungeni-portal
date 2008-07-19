#!/usr/bin/env python

import sys
import rfc822
import re
from cStringIO import StringIO
from pysqlite2 import dbapi2 as sqldb
import bungeniauditconstants

bungeniauditconstants.BOUNDARY_EXPRESSION = "-+\s+[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]\s[0-9][0-9]:[0-9][0-9]:[0-9][0-9],[0-9]+\s+-+\s+INFO+\s-+"
bungeniauditconstants.DATA_DB = "db/auditlog_db.db"
bungeniauditconstants.CONFIG_DB = "db/auditlogconfig.db"

"""
BungeniAuditLogParser class.

"""
class BungeniAuditLogParser:
    def __init__(self, fp):
        self.list_messages = [] #list of all message objects
        self.current_message_object = None #runtime object to current message
        self.file_pointer = fp #file pointer to audit file
        self.boundary_expression = bungeniauditconstants.BOUNDARY_EXPRESSION
    
    def process_messages(self):
        self.build_messages(self.file_pointer)
    
    def get_list_messages(self):
        return self.list_messages
    """
    build_messages
    Function that takes a recursive stream pointer to the audit log file.
    The way the python rfc822 works, it does not read continuous boundaries, but reads
    the header boundary, until the content-type attribute - the rest of the file is available
    as as stream pointer.
    build_message reads the stream pointer after the content-type attribute and parses the next
    message header from it.
    """
    def build_messages(self, message_fp):
        msg_object = rfc822.Message(message_fp)
        #now we have a current message object with all the attributes mapped
        #as keys in a dictionary, but without the content body.
        #
        #
        #read content body by recursing messages through Message object
        #msg_object now contains all the keys except content...
        #parse content and add content key
        message_body = msg_object.fp.read()
        reg_expr = re.compile(self.boundary_expression)
        regex_obj = reg_expr.search(message_body)
        if (regex_obj): #matching expression found
            #starting point of match
            startExpression = regex_obj.start()
            #ending point of match
            endExpression = regex_obj.end()
            #message content is the boundary upto start of next message
            message_content = message_body[:startExpression]
            #update message dictionary with message content
            msg_object['message_content'] = message_content.strip()
            #append to main list of messages in class
            self.append_to_list_messages(msg_object)
            #now process next message
            #get new message begin offset...
            new_message = str(message_body[startExpression:])
            #convert message string to iostream
            new_message_fp = StringIO(new_message)
            #make recursive call ....
            self.build_messages(new_message_fp)
            
    def append_to_list_messages(self, msgObject):        
        self.list_messages.append(msgObject)
   
    def print_list_messages(self):
        i=1
        for elem in self.list_messages:
            print "printing message number " + str(i) 
            print elem
            print "**********************"
            i=i+1
    


"""
BungeniAuditLogConfig class.
Connects to the configuration database and builds a map of system parameters.
portal_type_mappings -- maps a plone content type to a corresponding database table
portal_attribute_mappings -- maps a plone attribute (found within a plone content type) to a table column
"""
class BungeniAuditLogConfig:
    def __init__(self):
        self.con_config = sqldb.connect(bungeniauditconstants.CONFIG_DB)
        self.portal_type_mappings=dict()
        self.portal_attribute_mappings=dict()
    
    def build_type_mappings(self):
        cursor_mapping = self.con_config.cursor()
        cursor_mapping.execute("select * from portal_type_mapping")
        for (id, plone_type, registry_type) in cursor_mapping:
            self.portal_type_mappings[plone_type]=registry_type
    
    def build_attribute_mappings(self):
        cursor_mapping = self.con_config.cursor()
        for elem in self.portal_type_mappings.keys():
            attrib_mappings = dict()
            cursor_mapping.execute("select p.* from portal_attribute_mapping p, \
                               portal_type_mapping t where p.portal_mapping_id = t.portal_mapping_id \
                               and t.portal_type='"+str(elem)+"'")
            for (id, portal_mapping, portal_attribute, registry_attrib) in cursor_mapping:
                attrib_mappings[portal_attribute]=registry_attrib
            self.portal_attribute_mappings[elem]=attrib_mappings

    def build_mappings(self):
        print "building config mappings..."
        self.build_type_mappings()
        self.build_attribute_mappings()
        
                
    def get_attribute_mappings(self):
        return self.portal_attribute_mappings
    
    def get_portal_type_mappings(self):
        return self.portal_type_mappings
        
    def test(self):
        tbl_cursor = self.con_config.cursor()
        tbl_cursor.execute("select * from portal_attribute_mapping")
       

class BungeniAuditLogDump:
    def __init__(self, type_mappings, attribute_mappings, list_rfc822_messages):
        print "initializing audit dump"
        self.con_data = sqldb.connect(bungeniauditconstants.DATA_DB)
        self.portal_type_mappings = type_mappings
        self.portal_attribute_mappings = attribute_mappings
        self.list_messages = list_rfc822_messages
    
    def dump_data(self):
        for msg in self.list_messages:
            #iterate through all the rfc822 messages
            #portal_type key contains plone content type
            plone_type = msg['portal_type']
            #get the corresponding data table type from the audit config type_mappings dictionary
            if (self.portal_type_mappings.has_key(plone_type)):
                print "dumping " + str(plone_type) + " with id = " + msg["id"]
                data_table = "plone_"+ self.portal_type_mappings[plone_type]
                sql_insert_query = "insert into "+ data_table + " ("          
                
                #messages are coereced into data_table
                #build the sql query, by getting the plone-> data table attribute mappings
                #for every plone attribute there is a corresponding table column mapping
                table_attributes = self.portal_attribute_mappings[plone_type]
                
                #filter plone attribs in message which have corresponding table attributes
                valid_plone_attributes = [col for col in msg.keys() if table_attributes.has_key(col)]
                sql_column_list = ",".join(valid_plone_attributes)
                sql_insert_query = sql_insert_query + sql_column_list + ") values ("
                sql_value_prefix = ",".join(['?' for q in range(len(valid_plone_attributes))])
                
                valid_message_values = []
                for plone_attrib in valid_plone_attributes:
                    valid_message_values.append(msg[plone_attrib])
                sql_value_list = tuple(valid_message_values)
                
                sql_insert_query=sql_insert_query + sql_value_prefix + ") "
                insert_cursor = self.con_data.cursor()
                insert_cursor.execute(sql_insert_query, sql_value_list)
                self.con_data.commit()           
            else:
                print "ignoring unmapped type: " + str(plone_type)
                
            
