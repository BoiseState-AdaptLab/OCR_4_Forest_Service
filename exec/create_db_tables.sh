# !/bin/bash

# start the server
./tools/postgresql-install/bin/pg_ctl -D forest_data start
echo "-- Started server"

# run sql file to create all main tables
./tools/postgresql-install/bin/psql -U flociaglia -d postgres -f ForestryServiceDatabase/db/sql-scripts/ForestServiceDatabaseINIT.sql
echo "-- Report table and others created"

# run SQLAlchemy scripts to create and populate validation tables
python3 ForestryServiceDatabase/db/orm_scripts/create_validation_tables.py 
echo "-- Created validation tables"

python3 ForestryServiceDatabase/db/orm_scripts/create_db.py
echo "-- Created SQLAlchemy engine"

python3 ForestryServiceDatabase/db/orm_scripts/populate_tables.py
echo "-- Populated validation tables"

# connect and query the database
./tools/postgresql-install/bin/psql -U flociaglia forestservicedb < insert_report.txt
echo "-- Inserted values in report table"

# connect and query the database
./tools/postgresql-install/bin/psql -U flociaglia forestservicedb < validation_tables.txt
echo "-- Connected to the forestservicedb"

# query the report table
./tools/postgresql-install/bin/psql -U flociaglia forestservicedb < select_report.txt

python3 ForestryServiceDatabase/db/orm_scripts/create_report.py 

# isert entire report data
./tools/postgresql-install/bin/psql -U flociaglia forestservicedb < insert_report.txt
echo "-- Inserted values in report table"

# query the report table
./tools/postgresql-install/bin/psql -U flociaglia forestservicedb < select_report.txt

# stop the server
./tools/postgresql-install/bin/pg_ctl -D forest_data stop