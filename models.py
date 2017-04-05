# -*- encoding: utf-8 -*-
# begin

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, BigInteger,String, ForeignKey, Unicode, Binary, LargeBinary, Time, DateTime, Date, Text, Boolean, Float
from sqlalchemy.orm import relationship, backref, deferred
from sqlalchemy.orm import sessionmaker
from flask_login import UserMixin,_compat
import datetime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
class Posts (Base):
    __tablename__ = "posts"
    post_id = Column('post_id', Integer, primary_key = True)
    title = Column('title', Unicode)
    content = Column('content', Text)
    created = Column('created', Time , default=datetime.datetime.now)
    updated = Column('updated', Time , onupdate=datetime.datetime.now)
    user_id = Column('user_id', Integer, ForeignKey('users.user_id'))
    cat_id = Column('cat_id', Integer, ForeignKey('categories.cat_id'))

    categories = relationship('Categories', foreign_keys=cat_id)
    users = relationship('Users', foreign_keys=user_id)

class Users (Base , UserMixin):
    def get_id(self):
        try:
            return _compat.text_type(self.user_id)
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')

    __tablename__ = "users"
    user_id = Column('user_id', Integer, primary_key = True)
    user_name = Column('user_name', Unicode)
    hash_pwd = Column('hash_pwd', Unicode)
    full_name = Column('full_name', Unicode)
    active = Column('active', Integer)

class Categories (Base):
    __tablename__ = "categories"
    cat_id = Column('cat_id', Integer, primary_key = True)
    cat_name = Column('cat_name', Unicode)

class Comments (Base):
    __tablename__ = "comments"
    comment_id = Column('comment_id', Integer, primary_key = True)
    user_id = Column('user_id', Integer, ForeignKey('users.user_id'))
    post_id = Column('post_id', Integer, ForeignKey('posts.post_id'))
    content = deferred(Column('content', Text))
    created = Column('created', Time , default=datetime.datetime.now)

    posts = relationship('Posts', foreign_keys=post_id)
    users = relationship('Users', foreign_keys=user_id)

# end
