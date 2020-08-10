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

    def __init__(self, Login, Password):
        self.Login = Login
        self.Password = Password


class Notes(Base):
    __tablename__ = 'Notes'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    body = Column(String)
    Users_id = Column(Integer, ForeignKey('Users.id'))
    Users = relationship(
        Users,
        backref=backref('Notes',
                        uselist=True,
                        cascade='delete,all'))


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
        self.Session = sessionmaker(bind=engine)

    def Insert(self, Log, Pass):
        NewUser = Users(Log, Pass)
        session = self.Session()
        session.add(NewUser)
        session.commit()
        session.close()

    def Drop(self):
        session = self.Session()
        session.query.delete()
        session.close()

    def LogOut(self, Log):
        session = self.Session()
        for instance in session.query(Sessions.start_time, Sessions.finish_time, Sessions.id):
            if (None == instance.finish_time):
                SesionUser = session.query(Sessions).filter_by(id=instance.id).first()
                SesionUser.finish_time = datetime.now()
                session.add(SesionUser)
                session.commit()
        session.close()

    def Login(self, Log, Pass):
        Exist = False
        data = datetime.now()
        session = self.Session()
        for instance in session.query(Users.Login, Users.Password, Users.id):
            if ((instance.Login == Log) and (instance.Password == Pass)):
                SesionUser = Sessions(start_time=datetime.now(), finish_time=None,
                                      Users=session.query(Users).filter_by(id=instance.id).first())
                session.add(SesionUser)
                session.commit()
                Exist = True
        session.close()
        return Exist

    def addNote(self, login, title, body):
        session = self.Session()
        userId = session.query(Users).filter_by(Login=login).first()
        Note = Notes(title=title, body=body, Users=userId)
        session.add(Note)
        session.commit()
        session.close()

    def getNotes(self, login):
        session = self.Session()
        userId = session.query(Users).filter_by(Login=login).first()
        noteList = session.query(Notes).filter_by(Users=userId)
        session.close()
        return noteList

    def getNote(self, id):
        session = self.Session()
        note = session.query(Notes).filter_by(id=id).first()
        session.close()
        return note

    def delNote(self, id):
        session = self.Session()
        session.delete(session.query(Notes).filter_by(id=id).first())
        session.commit()
        session.close()

    def Register(self, Log, Pass):
        session = self.Session()
        Exist = False
        for instance in session.query(Users.Login):
            if (instance.Login == Log):
                Exist = True

        if Exist:
            session.close()
            return False
        else:
            NewUser = Users(Log, Pass)
            session.add(NewUser)
            session.commit()
            session.close()
            return True
        session.close()


def addNote(DBase, login, title, body):
    DBase.addNote(login, title, body)


def getNotes(DBase, login):
    return DBase.getNotes(login)


def getNote(DBase, id):
    return DBase.getNote(id)


def delNote(DBase, id):
    DBase.delNote(id)


def LogOutUser(DBase, login):
    DBase.LogOut(login)
    return True


def LoginUser(DBase, login, password):
    result = DBase.Login(login, password)
    if result:
        return "Login success"
    else:
        return "Wrong login password"


def RegisterUser(DBase, login, password):
    result = DBase.Register(login, password)
    if result:
        return "Register success"
    else:
        return "User already exists"


def FullDB(DBase, login, password):
    DBase.Insert(login, password)


def createBd():
    Base.metadata.create_all(engine)
    DBase = DatabaseFuction()
    return DBase


def DropTable():
    Users.__table__.drop(engine)
    Sessions.__table__.drop(engine)
