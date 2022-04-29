# This code uses sqlalchemy to create tables that contain
# information about certain fields in the forest report
# e.g. the "valid_forests" table contains "Sawtooth"
# because this is the only forest of concern

from sqlalchemy import create_engine, Column, Integer, String
from config import DATABASE_URI
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


# the code block below establishes a connection to the database
# DATABASE_URI needs to be updated according to user credentials
Base = declarative_base()
engine = create_engine(DATABASE_URI, echo=True)
Session = sessionmaker()

# define verification tables
class TemplateTable(object):
    id   = Column(Integer, primary_key=True)
    valid_strings = Column(String, unique=True)

class ValidForest(TemplateTable, Base):
    __tablename__ = "valid_forest"

class ValidAllotment(TemplateTable, Base):
    __tablename__ = "valid_allotment"

class ValidLivestock(TemplateTable, Base):
    __tablename__ = "valid_livestock"

class ValidRangerDist(TemplateTable, Base):
    __tablename__ = "valid_ranger_dist"




