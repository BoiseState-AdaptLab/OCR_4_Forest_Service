--returns all of the summaries that we have--
SELECT report.*, biomass_summary.*, cover_summary.*
FROM report
INNER JOIN biomass_summary
ON (report.r_id = biomass_summary.r_id)
INNER JOIN cover_summary
ON (report.r_id = cover_summary.r_id);

--returns the summary page based on specific parameter--
SELECT 
report.*, biomass_summary.*, cover_summary.*
from report INNER JOIN biomass_summary
ON (report.r_id = biomass_summary.r_id)
INNER JOIN cover_summary
ON (report.r_id = cover_summary.r_id)
WHERE report.writeup_no = 'A-13';


SELECT 
report.*, biomass_summary.*, cover_summary.*
from report INNER JOIN biomass_summary
ON (report.r_id = biomass_summary.r_id)
INNER JOIN cover_summary
ON (report.r_id = cover_summary.r_id)
WHERE report.photo_no = 'NBV-6-701';

SELECT 
report.*, biomass_summary.*, cover_summary.*
from report INNER JOIN biomass_summary
ON (report.r_id = biomass_summary.r_id)
INNER JOIN cover_summary
ON (report.r_id = cover_summary.r_id)
WHERE report.examiner = 'H Hess'
AND report.date > '1971-07-06'
AND report.date < '1973-07-06';

--returns transect pages based on specific parameters w/out cover section--
SELECT
report.date,
transect.transect_no, transect.location,
plot.plot_number,
biomass.type, biomass.species, biomass.green_weight
FROM report
INNER JOIN transect
ON (report.r_id = transect.r_id)
INNER JOIN plot
ON (transect.t_id = plot.t_id)
INNER JOIN biomass
ON (plot.p_id = biomass.p_id)
WHERE biomass.species = 'AGSPI';

SELECT
report.date,
transect.transect_no, transect.location,
plot.plot_number,
biomass.type, biomass.species, biomass.green_weight
FROM report
INNER JOIN transect
ON (report.r_id = transect.r_id)
INNER JOIN plot
ON (transect.t_id = plot.t_id)
INNER JOIN biomass
ON (plot.p_id = biomass.p_id)
WHERE biomass.species = 'AGSPI'
AND report.date > '1971-07-06'
AND report.date < '1973-07-06';

--transect page w/cover section. Need to rerun with real data.--
--these tables only hold date from report table. We can return just a report table seperately--
SELECT
report.date,
transect.transect_no, transect.location,
plot.plot_number,
biomass.type, biomass.species, biomass.green_weight,
cover.type, cover.value
FROM report
INNER JOIN transect
ON (report.r_id = transect.r_id)
INNER JOIN plot
ON (transect.t_id = plot.t_id)
INNER JOIN biomass
ON (plot.p_id = biomass.p_id)
INNER JOIN cover
ON (plot.p_id = cover.p_id)
WHERE biomass.species = 'AGSPI';

SELECT
report.date,
transect.transect_no, transect.location,
plot.plot_number,
biomass.type, biomass.species, biomass.green_weight,
cover.type, cover.value
FROM report
INNER JOIN transect
ON (report.r_id = transect.r_id)
INNER JOIN plot
ON (transect.t_id = plot.t_id)
INNER JOIN biomass
ON (plot.p_id = biomass.p_id)
INNER JOIN cover
ON (plot.p_id = cover.p_id)
WHERE biomass.species='AGSPI'
AND report.date > '1971-07-06'
AND report.date < '1973-07-06'; 

--Only want to look at transect one--
--Did we want to do this?--
select
report.r_id,
transect.*, 
plot.plot_number,
cover.type, cover.value,
biomass.type, biomass.species, biomass.green_weight
FROM report
INNER JOIN transect
ON (report.r_id = transect.r_id)
INNER JOIN plot
ON (transect.t_id = plot.t_id)
INNER JOIN biomass
ON (plot.p_id = biomass.p_id)
INNER JOIN cover
ON (plot.p_id = cover.p_id)
WHERE transect.transect_no = 1
AND cover.type='Forbs';


