-- test7.jpeg

-- for testing
-- USE ForestServiceReferenceDB;


INSERT INTO report (r_id, writeup_no, photo_no,
        forest, ranger_district, allotment, examiner, date,
        transect_no, type_designation, type_des_trend, livestock, slope, aspect,
        location, elevation_min, elevation_max)
VALUES (20, 'P-13', 'ESH-3-239',
        'Sawtooth', 'D-5', 'Blue Ridge', 'Patton', '1968-07-05',
        '1 of 3', 'S15', Null, 'Sheep', 35, 'S',
        'RIDGE ABOVE SLICK EAR CREEK', 7200, 7200);
