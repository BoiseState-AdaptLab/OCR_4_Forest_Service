from create_validation_tables import engine, ValidForest, ValidAllotment, ValidLivestock, ValidRangerDist

ValidForest.__table__.drop(engine)
ValidAllotment.__table__.drop(engine)
ValidLivestock.__table__.drop(engine)
ValidRangerDist.__table__.drop(engine)

