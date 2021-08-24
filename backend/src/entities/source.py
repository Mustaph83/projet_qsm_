# coding=utf-8

from marshmallow import Schema, fields
from sqlalchemy import Column, String, ForeignKey, Enum, Boolean
#from sqlalchemy.sql.schema import ForeignKe
from .entity import Entity, Base
import enum

class Source():
    name = Column(String, unique=True ,nullable=False)
    path = Column(String, nullable=False)
    accessMode = Column(String, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String ,nullable=False)
    ipAddress = Column(String, nullable=False)
    hostName = Column(String, ForeignKey('hotes.name'), nullable=False)
    scriptAssociate = Column(String , ForeignKey('scripts.name'),nullable=False)
    fileType = Column(String, nullable=False)
    pattern = Column(String,nullable=True)
    indexName = Column(String, nullable=False)
    mappingFile = Column(String, nullable=True)
    domaine = Column(String, nullable=True)
    description = Column(String, nullable=True)
    
    #status = Column(Boolean, nullable=False)
    def __init__(self, data_dict):
        self.name = data_dict['name']
        self.path = data_dict['path']
        self.accessMode = data_dict['accessMode']
        self.username = data_dict['username']
        self.password = data_dict['password']
        self.ipAddress = data_dict['ipAddress']
        self.hostName = data_dict['hostName']
        self.scriptAssociate = data_dict['scriptAssociate']
        self.fileType = data_dict['fileType']
        self.pattern = data_dict['pattern']
        self.indexName = data_dict['indexName']
        self.mappingFile = ''
        self.domaine = data_dict['domaine']
        self.description = data_dict['description']
        self.status = False


        
class SourceSchema(Schema):
    id = fields.Number()
    name = fields.Str()
    path = fields.Str()
    accessMode = fields.Str()
    username = fields.Str()
    password = fields.Str()
    ipAddress = fields.Str()
    hostName = fields.Str()
    scriptAssociate = fields.Str()
    fileType = fields.Str()
    pattern = fields.Str()
    indexName = fields.Str()
    mappingFile = fields.Str()
    domaine = fields.Str()
    description = fields.Str()
    
    
