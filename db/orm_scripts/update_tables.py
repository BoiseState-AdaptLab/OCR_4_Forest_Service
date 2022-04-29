from create_validation_tables import Session, engine, TemplateTable, ValidForest, ValidAllotment, ValidLivestock, ValidRangerDist

local_session = Session(bind=engine)

animal_to_update = local_session.query(ValidLivestock).filter(ValidLivestock.valid_strings=="horse").first()

animal_to_update.valid_strings = "mustang" # <-- the horse row in the table will be updated to mustang

local_session.commit()
