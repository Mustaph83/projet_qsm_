# coding=utf-8

from sqlalchemy.ext.declarative import declared_attr
from marshmallow import Schema, fields
from sqlalchemy import Column, String, ForeignKey, Enum, Boolean
#from sqlalchemy.sql.schema import ForeignKe
from .entity import Entity, Base
from .source import Source, SourceSchema
import enum

class U2020Others(Entity, Base, Source):
    __tablename__ = 'u2020others'
    @declared_attr
    def hostName(cls):
        return Column(String, ForeignKey('hotes.name'))

    @declared_attr
    def scriptAssociate(cls):
        return Column(String, ForeignKey('scripts.name'))

    date = Column(String, nullable=True)
    format = Column(String, nullable= True)
    patternToCopy = Column(String, nullable=False)
    patternToNotCopy = Column(String, nullable=True)

    #status = Column(Boolean, nullable=False)
    def __init__(self, creat_by, data_dict):
        Entity.__init__(self, creat_by)
        Source.__init__(self, data_dict)
        self.date = data_dict['date']
        self.format = data_dict['format']
        self.patternToCopy = data_dict['patternToCopy']
        self.patternToNotCopy = data_dict['patternToNotCopy']
    
            
class U2020OthersSchema(SourceSchema):
    date = fields.Str()
    format = fields.Str()
    patternToCopy = fields.Str()
    patternToNotCopy = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    last_updated_by = fields.Str()
    
