# coding=utf-8

from os import path
from marshmallow import Schema, fields
from sqlalchemy import Column, String, ForeignKey, Enum, Boolean, Integer
#from sqlalchemy.sql.schema import ForeignKe
from .entity import Entity, Base
import enum


class Service(Entity, Base):
    __tablename__ = 'services'
    path = Column(String, nullable=True)
    separateur = Column(String, nullable=False)
    skiprows = Column(Integer, nullable=True)
    indexs = Column(String, nullable=True)
    indexName = Column(String, nullable=True)
    dateField = Column(String, nullable=True)
  
    def __init__(self, created_by, data_dict):
        Entity.__init__(self, created_by)
        self.path = data_dict['path']
        self.separateur = data_dict['separateur']
        self.skiprows = data_dict['skiprows']
        self.indexs = data_dict['indexs']
        self.indexName = data_dict['indexName']
        self.dateField = data_dict['dateField']

class ServiceSchema(Schema):
    id = fields.Number()
    path = fields.Str()
    separateur = fields.Str()
    skiprows = fields.Number()
    indexs = fields.Str()
    indexName = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    last_updated_by = fields.Str()
