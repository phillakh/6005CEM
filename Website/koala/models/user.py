import sqlalchemy
import hashlib

from .meta import Base
from .roles import UserModules
import koala.models as models

class User(Base):
    __tablename__ = "user"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)

    #Username
    name = sqlalchemy.Column(sqlalchemy.Text)

    #Email for login
    email = sqlalchemy.Column(sqlalchemy.Text)

    #Password
    password = sqlalchemy.Column(sqlalchemy.Text)

    #Role,  We can default to None for Students 
    role = sqlalchemy.Column(sqlalchemy.Integer)

    #Backlink to a profile
    profile = sqlalchemy.orm.relationship("UserProfile", uselist=False)

    #Backlink to modules
    modules = sqlalchemy.orm.relationship("Module", secondary="usermodules")

    def __init__(self, name, email, role=None):
        self.name = name
        self.email = email
        self.role = role
    


    def hashPassword(self, plaintext):
        #Salt the thing
        salted = "{0}{1}".format(plaintext, self.name)
        theHash = hashlib.sha256(salted.encode()).hexdigest()
        return theHash

    def setPassword(self, plaintext):
        """
        Update a user password
        """
        salted = self.hashPassword(plaintext)
        self.password = salted

    def checkPassword(self, plaintext):
        #Get the salted version
        salted = self.hashPassword(plaintext)
        #And do a compare
        if salted == self.password:
            return True
        else:
            return False
    
    def isAdmin(self, moduleId):
        if self.role == models.ADMIN:
            return True
        elif self.role == models.TEACHER:
            #TODO Fileter this
            return True
        else:
            return False
        

class UserProfile(Base):
    """
    Let a User have their own profile
    """

    __tablename__ = "userprofile"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key = True)

    userid = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id"))
    
    #And lots of informatoon that we may want to collect 

    #Link to Avatar
    avatar = sqlalchemy.Column(sqlalchemy.Text)

    #Do they have a plan
    plan = sqlalchemy.Column(sqlalchemy.Text)

    #Speficy a Gender DOB ect
    gender = sqlalchemy.Column(sqlalchemy.Text)
    dob = sqlalchemy.Column(sqlalchemy.DateTime)

    #Profileing Stuff, so we can optimise later
    location = sqlalchemy.Column(sqlalchemy.Text)
    browser = sqlalchemy.Column(sqlalchemy.Text)

    def __init__(self, userId):
        """
        Rely on Geters for the Rest
        """
        self.userid = userId
