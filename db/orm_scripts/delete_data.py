from create_validation_tables import Session, engine, TemplateTable, ValidForest, ValidAllotment, ValidLivestock, ValidRangerDist

local_session = Session(bind=engine)

animal_to_delete = local_session.query(ValidLivestock).filter(ValidLivestock.valid_strings=="sheep").first()
local_session.delete(animal_to_delete)
local_session.commit()
