"""
Classes to manage roles and premissions

Loads of assicative arrays
"""

import sqlalchemy

from .meta import Base

#class CourseMembers(Base):
#    """Associatve arr


""" Association Table object that allows us to allocate user modules """
class UserModules(Base):
    __tablename__ = 'usermodules'
    userId = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('user.id'), primary_key=True)
    moduleId = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('module.id'), primary_key=True)
    role = sqlalchemy.Column(sqlalchemy.Integer)  #Optional Role
    