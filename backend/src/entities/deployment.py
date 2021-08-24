# coding=utf-8

#from marshmallow import Schema, fields
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.sql.sqltypes import Boolean, DateTime

from .entity import Entity, Base

class Deployment(Entity, Base):
    __tablename__ = 'deployment'
    pathEnv = Column(String, nullable=False)
    hostName = Column(String, ForeignKey('host.id'),nullable=False)
    hostActif = Column(Boolean, nullable=False)
    dateDeploy = Column(DateTime, nullable=False)


    def __init__(self, creat_by,pathEnv, hostName, hostActif, dateDeploy):
        Entity.__init__(self, creat_by)
        self.pathEnv = pathEnv
        self.hostName = hostName
        self.hostActif = hostActif
        self.dateDeploy = dateDeploy
    
        