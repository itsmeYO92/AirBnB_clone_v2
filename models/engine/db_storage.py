#!/usr/bin/python3
"""
    DBStorage module: module for storing in the database
"""
from os import getenv
from sqlalchemy import create_engine, MetaData
from models.base_model import Base
from sqlalchemy.orm import sessionmaker, scoped_session
from models.city import City
from models.state import State
from models.user import User
from models.place import Place


class DBStorage:
    """ Storage engine for the database """

    __engine = None
    __session = None

    classes = {
        "City": City,
        "State": State,
        "User" : User,
        "Place": Place
    }

    def __init__(self):
        """ init the db engine with sql alchemy """
        __user = getenv("HBNB_MYSQL_USER")
        __pwd = getenv("HBNB_MYSQL_PWD")
        __host = getenv("HBNB_MYSQL_HOST")
        __database = getenv("HBNB_MYSQL_DB")
        __mysqlurl = "mysql+mysqldb://{}:{}@{}/{}".format(__user, __pwd, __host, __database)

        self.__engine = create_engine(__mysqlurl, pool_pre_ping=True)
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ queery the database and return objects of aclass cls """
        if not self.__session:
            self.reload()

        objects = {}
        if type(cls) == str:
            if cls in self.classes:
                cls = self.classes[cls]
            else:
                cls = None

        for v in self.classes.values():
            if v == cls or not cls:
                results = self.__session.query(v)
                for obj in results:
                    objects[obj.__class__.__name__ + '.' + obj.id] = obj
        return objects

    def new(self, obj):
        """ adds an object to the database """
        if not self.__session:
            self.reload()

        self.__session.add(obj)
        
    def save(self):
        """ commits all the changes to db"""
        self.__session.commit()

    def delete(self, obj=None):
        """ delete an object from the database """
        if not self.__session:
            self.reload()
            
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """ creates the tables in the database and the current database session """
        Base.metadata.create_all(self.__engine)

        pre_session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(pre_session)
