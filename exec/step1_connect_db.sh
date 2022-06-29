# !/bin/bash

# Call this file if there's issues between step 0 and step 2
./../tools/bin/pg_ctl -D ../forest_data start

# if $? -eq 0
# check if the output is 0 and deliver message 
