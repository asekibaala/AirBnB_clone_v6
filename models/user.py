#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import hashlib


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        """Hashes password to MD5 on set"""
        self._password = hashlib.md5(value.encode()).hexdigest()

    def __init__(self, *args, **kwargs):
        """Ensure password is hashed on creation"""
        pwd = kwargs.get('password')
        if pwd and not kwargs.get('_password'):
            kwargs['_password'] = hashlib.md5(pwd.encode()).hexdigest()
            kwargs.pop('password')
        super().__init__(*args, **kwargs)
