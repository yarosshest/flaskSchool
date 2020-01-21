import datetime
from datetime import datetime
import sqlalchemy
from sqlalchemy import create_engine, DateTime, func
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
import re
from sqlalchemy.dialects.sqlite import DATETIME

engine = create_engine('sqlite:///some.db', echo=False)
Base = declarative_base()


class Users(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    Login = Column(String)
    Password = Column(String)
    Opis = Column(String)

    def __init__(self, Login, Password, Opis):
        self.Login = Login
        self.Password = Password
        self.Opis = Opis


class Sessions(Base):
    __tablename__ = 'Sessions'
    id = Column(Integer, primary_key=True)
    start_time = Column(DateTime)
    finish_time = Column(DateTime)
    Users_id = Column(Integer, ForeignKey('Users.id'))
    Users = relationship(
        Users,
        backref=backref('Sessions',
                        uselist=True,
                        cascade='delete,all'))

    def __repr__(self):
        return "%s to %s" % (self.start_time, self.finish_time)


class DatabaseFuction(object):
    def __init__(self):
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def Insert(self, Log, Pass, Str):
        NewUser = Users(Log, Pass, Str)
        self.session.add(NewUser)
        self.session.commit()

    def Drop(self):
        self.session.query.delete()

    def LogOut(self, Log):
        for instance in self.session.query(Sessions.start_time, Sessions.finish_time, Sessions.id):
            if (None == instance.finish_time):
                Sesion = self.session.query(Sessions).filter_by(id=instance.id).first()
                Sesion.finish_time = datetime.now()
                self.session.add(Sesion)
                self.session.commit()

    def Login(self, Log, Pass):
        Exist = False
        data = datetime.now()
        for instance in self.session.query(Users.Login, Users.Password, Users.id):
            if ((instance.Login == Log) and (instance.Password == Pass)):
                Session = Sessions(start_time=datetime.now(), finish_time=None,
                                   Users=self.session.query(Users).filter_by(id=instance.id).first())
                self.session.add(Session)
                self.session.commit()
                Exist = True
        return Exist

    def Register(self, Log, Pass, Str):
        Exist = False
        for instance in self.session.query(Users.Login):
            if (instance.Login == Log):
                Exist = True

        if Exist:
            return False
        else:
            NewUser = Users(Log, Pass, Str)
            self.session.add(NewUser)
            self.session.commit()
            return True


def LogOutUser(login):
    DBase = DatabaseFuction()
    DBase.LogOut(login)
    return "User: " + login + " Logout"


def LoginUser(login, password):
    DBase = DatabaseFuction()
    result = DBase.Login(login, password)
    if result:
        return "Login success"
    else:
        return "Wrong login password"


def RegisterUser(login, password, Opis):
    DBase = DatabaseFuction()
    result = DBase.Register(login, password, Opis)
    if result:
        return "Register success"
    else:
        return "User already exists"


def FullDB(login, password, Opis):
    Base.metadata.create_all(engine)
    DBase = DatabaseFuction()
    DBase.Insert(login, password, Opis)

def createBd():
    Base.metadata.create_all(engine)


def DropTable():
    Base.metadata.create_all(engine)
    Users.__table__.drop(engine)
    Sessions.__table__.drop(engine)

