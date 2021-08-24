# coding:utf-8

from marshmallow import Schema, fields
from sqlalchemy import Column, String, ForeignKey, Enum,Boolean
#from sqlalchemy.sql.schema import ForeignKey
from .entity import Entity, Base

import enum


class Host(Entity, Base):
    __tablename__ = 'hotes'
    name = Column(String, unique=True,nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    ipAddress = Column(String, nullable=False)
    deploymentPath = Column(String, nullable=False)
    nodeElastic = Column(String, nullable=False)
    nodeDeploy = Column(String, nullable=False)
    description = Column(String, nullable=True)

    
    def __init__(self, creat_by, json_ob):
        Entity.__init__(self, creat_by)
        self.name = json_ob['name']
        self.username = json_ob['username'] 
        self.password = json_ob['password'] 
        self.ipAddress = json_ob['ipAddress']
        self.deploymentPath = json_ob['deploymentPath']
        self.nodeElastic = json_ob['nodeElastic']
        self.nodeDeploy = json_ob['nodeDeploy']
        self.description = json_ob['description']
    
    
class HostSchema(Schema):
    id = fields.Number()
    name = fields.Str()
    username = fields.Str()
    password = fields.Str()
    ipAddress = fields.Str()
    deploymentPath = fields.Str()
    nodeElastic = fields.Str()
    nodeDeploy = fields.Str()
    description = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    last_updated_by = fields.Str()
    