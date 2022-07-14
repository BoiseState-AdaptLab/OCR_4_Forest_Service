-- site_an_08_00.jpg

-- for testing
-- USE ForestServiceReferenceDB;


INSERT INTO report (r_id, writeup_no, photo_no,
        forest, ranger_district, allotment, examiner, date,
        transect_no, type_designation, type_des_trend, livestock, slope, aspect,
        location, elevation_min, elevation_max)
VALUES (5, 'S-6', '1-205',
        'Sawtooth', 'Fairfield', 'Bremner', 'G. Simonds', '07-16',
        '1 of 3', 'S-4', Null, 'Cattle', 20, 'W',
        'See Aerial Photo', Null, Null);
