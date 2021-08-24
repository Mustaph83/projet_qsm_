# coding=utf-8

from ..entities.script import Script
from datetime import date
from sqlalchemy.sql.expression import null, true
from marshmallow import Schema, fields
from sqlalchemy import Column, String, ForeignKey, Enum,Boolean, schema
#from sqlalchemy.sql.schema import ForeignKey
from .entity import Entity, Base

import enum


class ConfigOtarie1(Entity, Base):
    __tablename__= 'config'
    scriptName = Column(String, ForeignKey('scripts.name'), nullable=False)
    date = Column(String, nullable=True)
    format = Column(String, nullable= true)
    separateur = Column(String, nullable=False)
    dateField = Column(String, nullable=True)
    elasticServer = Column(String, nullable=False)
    indexName = Column(String, nullable=False)
    mappingFile = Column(String, nullable=False)

    def __init__(self, creat_by, data_dict):
        Entity.__init__(self, creat_by)
        self.scriptName = data_dict['scriptName']
        self.date = data_dict['date']
        self.format = data_dict['format']
        self.separateur = data_dict['separateur']
        self.dateField = data_dict['dateField']
        self.elasticServer = data_dict['elasticServer']
        self.indexName = data_dict['indexName']
        self.mappingFile = data_dict['mappingFile']

class ConfigFileOtarie1Schema(Schema):
    id = fields.Number()
    scriptName = fields.Str()
    date = fields.Str()
    format = fields.Str()
    separateur = fields.Str()
    dateField = fields.Str()
    elasticServer = fields.Str()
    indexName = fields.Str()
    mappingFile = fields.Str()

        