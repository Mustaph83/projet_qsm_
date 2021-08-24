# coding=utf-8
from marshmallow import Schema, fields
from sqlalchemy import Column, String, ForeignKey, Enum, Boolean
#from sqlalchemy.sql.schema import ForeignKe
from .entity import Entity, Base
import enum

class User(Entity, Base):
    __tablename__ = 'users'
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    profil = Column(String, nullable=False)
    email = Column(String, nullable=True)
    
    def __init__(self, created_by, user_data):
        super().__init__(created_by)
        self.username = user_data['username']
        self.password = user_data['password']
        self.profil = user_data ['profil']
        self.email = user_data['email']

class UserSchema(Schema):
    id = fields.Number()
    username = fields.Str()
    password = fields.Str()
    profil = fields.Str()
    email = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    last_updated_by = fields.Str()


