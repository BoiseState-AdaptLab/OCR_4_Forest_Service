from sqlalchemy.orm import sessionmaker, relationship
from create_validation_tables import Session, engine, Base, ValidForest, ValidAllotment, ValidLivestock, ValidRangerDist


local_session = Session(bind=engine)


# input for the tables defined
# lists of valid strings for each table/column
allotments = [
    {
        "valid_allotment":"bremner"
    },
    {
        "valid_allotment":"blueridge"
    },
    {
        "valid_allotment":"lime creek"
    },
    {
        "valid_allotment":"fisher-federal"
    },
    {
        "valid_allotment":"greenhorn"
    }

]

livestock = [
    {
        "valid_livestock":"cattle"
    },
    {
        "valid_livestock":"sheep"
    },
    {
        "valid_livestock":"horse"
    }
]

ranger_dist = [
    {
        "valid_ranger_dist":"fairfield"
    },
    {
        "valid_ranger_dist":"D5"
    },
    {
        "valid_ranger_dist":"hailey"
    },
    {
        "valid_ranger_dist":"ketchum"
    }
]

# the code below inserts the defined values into the created tables

new_forest = ValidForest(valid_strings="sawtooth")
local_session.add(new_forest)
local_session.commit()

for a in allotments:
    new_allotment=ValidAllotment(valid_strings=a["valid_allotment"])
    local_session.add(new_allotment)
    local_session.commit()
for l in livestock:
    new_livestock=ValidLivestock(valid_strings=l["valid_livestock"])
    local_session.add(new_livestock)
    local_session.commit()
for r in ranger_dist:
    new_ranger_dist=ValidRangerDist(valid_strings=r["valid_ranger_dist"])
    local_session.add(new_ranger_dist)
    local_session.commit()

