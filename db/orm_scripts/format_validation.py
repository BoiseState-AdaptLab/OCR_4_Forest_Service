# THIS CODE IS NOT COMPLETE AND DOES NOT WORK. 

# Author: Sandra Busch
# Date: Fri 17 Dec 2021 08:11:52 AM MST
# Description:
# Contains an idea of a function to verify if the format 
# of a field in the report table is correct and matches the allowed input to the column. 
# Should return information about the type of input a column accepts.  
# It is not yet fully functioning. It returns the correct value, e.g. 
# if a column accepts only integers it returns INTEGER, but it also 
# returns all the names of the columns in the table as well. 
# I think this happens because I used the inspect function which might 
# always return all the names of the columns from the table it inspects...

from orm_scripts.map_all_tables import engine
from sqlalchemy.inspection import inspect


def format_validation(str):
    insp = inspect(engine)
    cols = insp.get_columns('report')
    for c in cols:
        if (c['name'] == str):
            return c['type']
    return None

# used to test if the function works as expected
result = format_validation('slope')
print(result)