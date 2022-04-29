# !/bin/bash

# start the PostGres database server
./../tools/postgresql-install/bin/pg_ctl -D ../forest_data start
echo "-- Started server"

# run sql file to create all tables
./../tools/postgresql-install/bin/psql -U flociaglia -d postgres -f db/sql-scripts/ForestServiceDatabaseINIT.sql
echo "-- Report table and others created"

# run SQLAlchemy scripts to create and populate validation tables
python3 db/orm_scripts/create_validation_tables.py 
echo "-- Created validation tables"

python3 db/orm_scripts/create_db.py
echo "-- Created SQLAlchemy engine"

python3 db/orm_scripts/populate_tables.py
echo "-- Populated validation tables"