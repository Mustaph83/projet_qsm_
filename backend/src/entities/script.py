# coding=utf-8

from marshmallow import Schema, fields
from sqlalchemy import Column, String, ForeignKey, Enum,Boolean
#from sqlalchemy.sql.schema import ForeignKey
from .entity import Entity, Base

import enum

class Script(Entity, Base):
    __tablename__ = 'scripts'
    name = Column(String, unique=True, nullable=False)
    domaine = Column(String, nullable=False)
    fileType = Column(String, nullable=False)
    location = Column(String, unique=True ,nullable=False)
    collectScript = Column(String, nullable=False)
    parsingScript = Column(String, nullable=False)
    configFiles = Column(String, nullable=False)
    description = Column(String, nullable=True)

    def __init__(self, created_by, json_obj):
        Entity.__init__(self ,created_by)
        self.name = json_obj['name']
        self.domaine = json_obj['domaine']
        self.fileType = json_obj['fileType']
        self.location = json_obj['location']
        self.collectScript = json_obj['collectScript']
        self.parsingScript = json_obj['parsingScript']
        self.configFiles = json_obj['configFiles']
        self.description = json_obj['description']


class ScriptSchema(Schema):
    id = fields.Number()
    name = fields.Str()
    domaine = fields.Str()
    fileType = fields.Str()
    location = fields.Str()
    collectScript = fields.Str()
    parsingScript = fields.Str()
    configFiles = fields.Str()
    description = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    last_updated_by = fields.Str()