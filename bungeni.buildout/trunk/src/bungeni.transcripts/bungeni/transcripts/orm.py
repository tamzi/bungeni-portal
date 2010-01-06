import sqlalchemy as rdb
from sqlalchemy.orm import mapper, relation, column_property, deferred, backref

import schema
import domain

mapper( domain.Transcript, schema.transcript_table, )
mapper( domain.Sitting, schema.sitting_table, )
