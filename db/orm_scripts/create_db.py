from create_validation_tables import engine, Base, ValidForest, ValidAllotment, ValidLivestock, ValidRangerDist

Base.metadata.create_all(engine)