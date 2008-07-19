#!/usr/bin/env python

from bungeniauditlog import BungeniAuditLogParser
from bungeniauditlog import BungeniAuditLogConfig
from bungeniauditlog import BungeniAuditLogDump

fp=open("audit.txt")
m=BungeniAuditLogParser(fp)
m.process_messages()
#m.print_list_messages()
d=BungeniAuditLogConfig()
d.build_mappings()
out=BungeniAuditLogDump(d.get_portal_type_mappings(), d.get_attribute_mappings(), m.get_list_messages() )
out.dump_data()
