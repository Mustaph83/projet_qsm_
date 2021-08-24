# coding=utf-8

from sqlalchemy.ext.declarative import declared_attr
from marshmallow import Schema, fields
from sqlalchemy import Column, String, ForeignKey, Enum, Boolean
#from sqlalchemy.sql.schema import ForeignKe
from .entity import Entity, Base
from .source import Source, SourceSchema
import enum

class Otarie(Entity, Base, Source):
    __tablename__ = 'otarie'
    @declared_attr
    def hostName(cls):
        return Column(String, ForeignKey('hotes.name'))

    @declared_attr
    def scriptAssociate(cls):
        return Column(String, ForeignKey('scripts.name'))

    date = Column(String, nullable=True)
    format = Column(String, nullable= True)
    separateur = Column(String, nullable=False)
    dateField = Column(String, nullable=True)

    #status = Column(Boolean, nullable=False)
    def __init__(self, creat_by, data_dict):
        Entity.__init__(self, creat_by)
        Source.__init__(self, data_dict)
        self.date = data_dict['date']
        self.format = data_dict['format']
        self.separateur = data_dict['separateur']
        self.dateField = data_dict['dateField']
    
            
class OtarieSchema(SourceSchema):
    date = fields.Str()
    format = fields.Str()
    separateur = fields.Str()
    dateField = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    last_updated_by = fields.Str()
    
