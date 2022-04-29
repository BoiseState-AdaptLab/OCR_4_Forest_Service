# Author: Sandra Busch
# Date: Fri 17 Dec 2021 08:11:52 AM MST
# Description:
# This script contains functions that can be used
# to interact with the forestservicedb database and 
# insert / update / delete data.
#
from sqlalchemy import insert, update
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import Table, column
from config import DATABASE_URI
from sqlalchemy import create_engine, Integer, String
from sqlalchemy.orm import sessionmaker, relationship
import os

# the code block below establishes a conection to the database
# connection string needs to be changed based on the location of the database
# structure: "postgresql://[username]:[password]@[IP]/[database_name]"
# it is automatically mapping the psql database into sqlalchemy
# and a report database object is created for further use
Base = automap_base()
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()
Base.prepare(engine, reflect=True)
report = Base.classes.report

# this function creates a "report" by taking in
# the value of the field "writeup_no" and inserting
# it into the report table of the database
# a new report ID is created, inserted into its column
# returns report_id
def create_report(wr_no_value):
    new_report = report(writeup_no=wr_no_value)
    session.add(new_report)
    session.commit()

    return new_report.r_id


# the function can be used to insert information into
# any column of the report table in the datatbase
# given the respective report_id value, the column name,
# and the value of the field we wish to enter
# returns 0 
def update_report(report_id, column_name, value):
    session.query(report).filter(report.r_id == report_id).update({column_name: value})
    session.commit()
    
    return 0



# a simple test if the update_report() function works
# with the report_id = 5, column = photo_no and value = test_photo
test = update_report("5", "photo_no", "test_photo")

print(test)