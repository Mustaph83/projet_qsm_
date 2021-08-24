from sqlalchemy.ext.declarative import declared_attr
from marshmallow import Schema, fields
from sqlalchemy import Column, String, ForeignKey, Enum, Boolean
#from sqlalchemy.sql.schema import ForeignKe
from .entity import Entity, Base
from .source import Source, SourceSchema
import enum

class SourceIn(Entity, Base, Source):
    __tablename__ = 'sourcein'
    
    @declared_attr
    def hostName(cls):
        return Column(String, ForeignKey('hotes.name'))

    @declared_attr
    def scriptAssociate(cls):
        return Column(String, ForeignKey('scripts.name'))
    pattern_dir = Column(String, nullable=True)
    date = Column(String, nullable=True)
    format = Column(String, nullable=True)
    other_pattern = Column(String, nullable=True)
    other_dir = Column(String, nullable=True)
 
    def __init__(self, created_by, data_dict):
        Entity.__init__(self, created_by)
        Source.__init__(self, data_dict)
        self.pattern_dir = data_dict['patternDir']
        self.date = data_dict['date']
        self.format = data_dict['format']
        self.other_pattern = data_dict['otherPattern']
        self.other_dir = data_dict['otherDir']
 
    

    

    
class SourceInSchema(SourceSchema):
    pattern_dir = fields.Str()
    date = fields.Str()
    format = fields.Str()
    other_pattern = fields.Str()
    other_dir = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    last_updated_by = fields.Str()