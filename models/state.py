#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import String, Column
from sqlalchemy.orm import relationship
from os import getenv
from models import engine


class State(BaseModel, Base):
    """ State class """
    if getenv("HBNB_TYPE_STORAGE") == 'db':
        __tablename__ = "states"
        name = Column(String(128), nullable=False)
        citites = relationship("City", cascade="all, delete", backref="states")

    else:
        name = ""

        @property
        def cities(self):
            """ getter for cities for the state """
            from models import storage

            cities = []
            for v in storage.all("City").values():
                if v.state_id == self.id:
                    cities.append(v)
            return cities

    def __init__(self, *args, **kwargs):
        """ initializes state """
        super().__init__(*args, **kwargs)
