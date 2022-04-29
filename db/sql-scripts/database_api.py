#!/usr/bin/python3
from sqlalchemy import create_engine

sDBPass = ""


def test_connection():
    try:
        with open('dbpass.txt', 'r') as f:
            sDBPass = f.readline()
        engine = create_engine('postgresql://student:%(sDBPass)s@localhost:5432/forestservicedb' % {"sDBPass" : sDBPass})
        conn = engine.connect()
        print("connected")
        conn.close()
    except:
        print("could not connect")

def get_valid_opts(str):
    with open('dbpass.txt', 'r') as f:
        sDBPass = f.readline()
    engine = create_engine('postgresql://student:%(sDBPass)s@localhost:5432/forestservicedb' % {"sDBPass" : sDBPass})
    with engine.connect() as con:
        if str == "forest":
            rs = con.execute('SELECT * FROM verification')
            for row in rs:
                print (row)


if __name__ == "__main__":
    test_connection()
    get_valid_opts("forest")