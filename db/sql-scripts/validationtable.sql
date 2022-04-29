
\c forestservicedb;
--create schema forestservice;
set search_path to forestservice;

DROP TABLE IF EXISTS forestservice.validation;

CREATE TABLE forestservice.validation (
  r_id int NOT NULL,
  column_name varchar(255),
  validated boolean,
  confidence float,
  field_image varchar(255)
);


ALTER TABLE forestservice.validation
ADD CONSTRAINT FK_parent_report_t
FOREIGN KEY (r_id) 
REFERENCES report(r_id); 

