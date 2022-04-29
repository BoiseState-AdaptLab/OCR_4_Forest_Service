#
# Author: Sandra Busch
# Date: Fri 17 Dec 2021 08:11:52 AM MST
# Description:
# This code uses sqlalchemy to map all tables of 
# the forestservice database into sqlalchemy after the 
# ForestServiceDatabaseINIT.sql script and the 
# create_validation_tables script have been run.
# this is necessary in order to work with the 
# database through python / sqlalchemy
#
from orm_scripts.create_validation_tables import engine, session, valid_allotment
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import Table, column
from sqlalchemy.inspection import inspect

# reflects all tables of database using automap
# so that the sql database can be interacted with 
# using python sqlalchemy
# it will map the database that is connected to the
# engine, here use the imported engine from the
# create_validation_tables script
# if you wish to map a different database, you can use
# the following code instead of importing the engine
# connection_string = "postgresql://[username]:[password]@[IP]/[database_name]"
# engine = create_engine(connection_string)
Base = automap_base()
Base.prepare(engine, reflect=True)

# mapped classes can be refered to like below
# to create an object for each table if used in
# a function for example
report = Base.classes.report
biomass = Base.classes.biomass

# this method automaps tables one by one
# and not the whole database
# class report(Base):
#     __table__ = Table("report", Base.metadata, autoload=True, autoload_with=engine)


# can be used to test if automap / reflection of the tables worked
columns = [column.name for column in inspect(valid_allotment).c]
print (columns)
