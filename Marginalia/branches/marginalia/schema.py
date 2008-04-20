import sqlalchemy as rdb
from datetime import datetime
from sqlalchemy.orm import mapper, relation, column_property
from zope.interface import implements
from marginalia.interfaces import IAnnotation

metadata = rdb.MetaData()

annotations_table = rdb.Table(
    "annotations",
   metadata,
    rdb.Column('id', rdb.Integer, primary_key=True),  
    rdb.Column("url", rdb.Unicode(80)),
    rdb.Column("start_block", rdb.Unicode(80)),
    rdb.Column("start_xpath", rdb.Unicode(80)),
    rdb.Column("start_word", rdb.Unicode(80)),
    rdb.Column("start_char", rdb.Unicode(80)),
    rdb.Column("end_block", rdb.Unicode(80)),
    rdb.Column("end_xpath", rdb.Unicode(80)),
    rdb.Column("end_word", rdb.Unicode(80)),
    rdb.Column("end_char", rdb.Unicode(80)),
    rdb.Column("note", rdb.Unicode(80)), 
    rdb.Column("access", rdb.Unicode(80)),
    rdb.Column("action", rdb.Unicode(80)),
    rdb.Column("edit_type", rdb.Unicode(80)),
    rdb.Column("quote", rdb.Unicode(80)),
    rdb.Column("quote_title", rdb.Unicode(80)),
    rdb.Column("quote_author", rdb.Unicode(80)),
    rdb.Column("link_title", rdb.Unicode(80)),
    rdb.Column("indexed_url", rdb.Unicode(80)),
    rdb.Column("link", rdb.Unicode(80)),
   )
   
class AnnotationMaster(object):
    """Annotation Master Class."""

    def __repr__(self):
        return '<Annotation %s>'%(self.id)


mapper(AnnotationMaster, annotations_table)
    
