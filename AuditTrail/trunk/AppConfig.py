import os
from Globals import INSTANCE_HOME 

LOG_PATH = os.path.join(INSTANCE_HOME, 'log', 'audit.log')

# # We depend on marshall because we want to register one consistent
# # marshaller to use for the auditing.
# DEPENDENCIES = [
#     'Marshall',
#     ]

