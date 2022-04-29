-- for testing 
-- USE ForestServiceDB; 


INSERT INTO report (r_id, writeup_no, photo_no, examiner, transect_no, slope, aspect,
elevation_min, elevation_max, forest, ranger_district, allotment, location, livestock, 
type_designation, type_des_trend, date, total_grass, total_forb, total_browse, desirable, 
intermediate, least_desirable, composition, production, forage_condition, ground_cover, erosion, 
soil_condition, browse_condition, trend, notes)
VALUES (112, 'S-10', 'EGT-6-106', 'Sutton', '1-1', 10, 'NW',
NULL, NULL, 'Sawtooth', 'Fairfield', 'Boardman Cr', 'Bench at the head of the canyon', 'goats, sheep',
'S3', '61/64', '1966-08-18', 43, 94, 10, 38,
47, 15, 27, 34, 61, 18, 46, 
64, 'fair', 'right', 'none');


INSERT INTO biomass_summary(b_id, r_id, species, trans1, trans2, trans3, total, dry_weight, prod_dry_weight, composition, desirability_D, desirability_I, desirability_L)
VALUES(13, 112, 'Melz', 14, NULL, NULL, 14, 70, NULL, NULL, NULL, 1, NULL);

INSERT INTO biomass_summary(b_id, r_id, species, trans1, trans2, trans3, total, dry_weight, prod_dry_weight, composition, desirability_D, desirability_I, desirability_L)
VALUES(14, 112, 'Sihy', 3, NULL, NULL, 3, 15, NULL, NULL, NULL, 1, NULL);

INSERT INTO biomass_summary(b_id, r_id, species, trans1, trans2, trans3, total, dry_weight, prod_dry_weight, composition, desirability_D, desirability_I, desirability_L)
VALUES(15, 112, 'Stoc', 26, NULL, NULL, 26, 156, NULL, NULL, 1, NULL, NULL);

INSERT INTO biomass_summary(b_id, r_id, species, trans1, trans2, trans3, total, dry_weight, prod_dry_weight, composition, desirability_D, desirability_I, desirability_L)
VALUES(16, 112, 'Lupz', 68, NULL, NULL, 68, 184, NULL, NULL, NULL, NULL, NULL);

INSERT INTO biomass_summary(b_id, r_id, species, trans1, trans2, trans3, total, dry_weight, prod_dry_weight, composition, desirability_D, desirability_I, desirability_L)
VALUES(17, 112, 'Astz', 8, NULL, NULL, 8, 24, NULL, NULL, NULL, 1, NULL);

INSERT INTO biomass_summary(b_id, r_id, species, trans1, trans2, trans3, total, dry_weight, prod_dry_weight, composition, desirability_D, desirability_I, desirability_L)
VALUES(18, 112, 'Penz', 10, NULL, NULL, 10, 30, NULL, NULL, 1, NULL, NULL);

INSERT INTO biomass_summary(b_id, r_id, species, trans1, trans2, trans3, total, dry_weight, prod_dry_weight, composition, desirability_D, desirability_I, desirability_L)
VALUES(19, 112, 'Linw', 112, NULL, NULL, 112, 6, NULL, NULL, NULL, 1, NULL);

INSERT INTO biomass_summary(b_id, r_id, species, trans1, trans2, trans3, total, dry_weight, prod_dry_weight, composition, desirability_D, desirability_I, desirability_L)
VALUES(20, 112, 'Eriz', 6, NULL, NULL, 6, 18, NULL, NULL, NULL, 1, NULL);

INSERT INTO biomass_summary(b_id, r_id, species, trans1, trans2, trans3, total, dry_weight, prod_dry_weight, composition, desirability_D, desirability_I, desirability_L)
VALUES(21, 112, 'Hafr', 10, NULL, NULL, 10, 50, NULL, NULL, NULL, 1, NULL);


INSERT INTO cover_summary(c_id, r_id, type, total, average)
VALUES(11, 112, 'Overstory (Trees)', NULL, NULL);

INSERT INTO cover_summary(c_id, r_id, type, total, average)
VALUES(12, 112, 'Overstory (Shrub)', NULL, NULL);

INSERT INTO cover_summary(c_id, r_id, type, total, average)
VALUES(13, 112, 'Crown Cover (Herb)', 7, NULL);

INSERT INTO cover_summary(c_id, r_id, type, total, average)
VALUES(14, 112, 'Bare Ground', 35, NULL);

INSERT INTO cover_summary(c_id, r_id, type, total, average)
VALUES(15, 112, 'Rock/Pav (Nat)', 1, NULL);

INSERT INTO cover_summary(c_id, r_id, type, total, average)
VALUES(16, 112, 'Rock/Pav (Unnat)', 10, NULL);

INSERT INTO cover_summary(c_id, r_id, type, total, average)
VALUES(17, 112, 'Veg/Litter', 54, NULL);

INSERT INTO cover_summary(c_id, r_id, type, total, average)
VALUES(18, 112, 'Soil Disturbance', NULL, NULL);

INSERT INTO cover_summary(c_id, r_id, type, total, average)
VALUES(19, 112, 'Droppings', NULL, NULL);

INSERT INTO cover_summary(c_id, r_id, type, total, average)
VALUES(20, 112, 'Pellet Groups', NULL, NULL);


INSERT INTO transect(t_id, r_id, transect_no, location, elevation, slope, type_designation, aspect)
VALUES (4, 112, 1, 'Bench at the head of the canyon', NULL, 10, 'S3', 'NW');


INSERT INTO plot(p_id, t_id, plot_number)
VALUES (31, 4, 1);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(292, 31, 'Grass', 'Melz', 6);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(293, 31, 'Grass', 'Sihy', NULL);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(294, 31, 'Grass', 'Stoc', NULL);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(295, 31, 'Forb', 'Lupz', 8);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(296, 31, 'Forb', 'Astz', 2);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(297, 31, 'Forb', 'Penz', NULL);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(298, 31, 'Forb', 'Linw', NULL);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(299, 31, 'Forb', 'Eriz', NULL);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(300, 31, 'Browse', 'Hafr', NULL);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(301, 31, 'Overstory (Trees)', NULL);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(302, 31, 'Overstory (Shrub)', NULL);
 
INSERT INTO cover(c_id, p_id, type, value)
VALUES(303, 31, 'Crown Cover (Herb)', 10);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(304, 31, 'Bare Ground', 10);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(305, 31, 'Rock/Pav (Nat)', NULL);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(306, 31, 'Rock/Pav (Unnat)', 10);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(307, 31, 'Veg/Litter', 80);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(308, 31, 'Soil Disturbance', NULL);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(309, 31, 'Droppings', NULL);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(310, 31, 'Pellet Groups', NULL);


INSERT INTO plot(p_id, t_id, plot_number)
VALUES (32, 4, 2);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(301, 32, 'Grass', 'Melz', 1);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(302, 32, 'Grass', 'Sihy', 1);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(303, 32, 'Grass', 'Stoc', NULL);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(304, 32, 'Forb', 'Lupz', 4);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(305, 32, 'Forb', 'Astz', NULL);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(306, 32, 'Forb', 'Penz', 7);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(307, 32, 'Forb', 'Linw', NULL);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(308, 32, 'Forb', 'Eriz', NULL);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(309, 32, 'Browse', 'Hafr', NULL);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(311, 32, 'Overstory (Trees)', NULL);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(312, 32, 'Overstory (Shrub)', NULL);
 
INSERT INTO cover(c_id, p_id, type, value)
VALUES(313, 32, 'Crown Cover (Herb)', 20);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(314, 32, 'Bare Ground', 10);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(315, 32, 'Rock/Pav (Nat)', NULL);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(316, 32, 'Rock/Pav (Unnat)', 10);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(317, 32, 'Veg/Litter', 80);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(318, 32, 'Soil Disturbance', NULL);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(319, 32, 'Droppings', NULL);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(320, 32, 'Pellet Groups', NULL);


INSERT INTO plot(p_id, t_id, plot_number)
VALUES (33, 4, 3);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(310, 33, 'Grass', 'Melz', NULL);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(311, 33, 'Grass', 'Sihy', NULL);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(312, 33, 'Grass', 'Stoc', 6);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(313, 33, 'Forb', 'Lupz', NULL);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(314, 33, 'Forb', 'Astz', NULL);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(315, 33, 'Forb', 'Penz', 1);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(316, 33, 'Forb', 'Linw', NULL);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(317, 33, 'Forb', 'Eriz', NULL);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(318, 33, 'Browse', 'Hafr', NULL);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(321, 33, 'Overstory (Trees)', NULL);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(322, 33, 'Overstory (Shrub)', NULL);
 
INSERT INTO cover(c_id, p_id, type, value)
VALUES(323, 33, 'Crown Cover (Herb)', NULL);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(324, 33, 'Bare Ground', 10);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(325, 33, 'Rock/Pav (Nat)', NULL);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(326, 33, 'Rock/Pav (Unnat)', 20);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(327, 33, 'Veg/Litter', 70);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(328, 33, 'Soil Disturbance', NULL);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(329, 33, 'Droppings', NULL);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(330, 33, 'Pellet Groups', NULL);


INSERT INTO plot(p_id, t_id, plot_number)
VALUES (34, 4, 4);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(319, 34, 'Grass', 'Melz', 5);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(320, 34, 'Grass', 'Sihy', NULL);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(321, 34, 'Grass', 'Stoc', NULL);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(322, 34, 'Forb', 'Lupz', 1);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(323, 34, 'Forb', 'Astz', NULL);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(324, 34, 'Forb', 'Penz', NULL);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(325, 34, 'Forb', 'Linw', 2);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(326, 34, 'Forb', 'Eriz', NULL);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(327, 34, 'Browse', 'Hafr', NULL);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(331, 34, 'Overstory (Trees)', NULL);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(332, 34, 'Overstory (Shrub)', NULL);
 
INSERT INTO cover(c_id, p_id, type, value)
VALUES(333, 34, 'Crown Cover (Herb)', NULL);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(334, 34, 'Bare Ground', 40);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(335, 34, 'Rock/Pav (Nat)', NULL);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(336, 34, 'Rock/Pav (Unnat)', 10);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(337, 34, 'Veg/Litter', 50);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(338, 34, 'Soil Disturbance', NULL);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(339, 34, 'Droppings', NULL);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(340, 34, 'Pellet Groups', NULL);


INSERT INTO plot(p_id, t_id, plot_number)
VALUES (35, 4, 5);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(328, 35, 'Grass', 'Melz', NULL);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(329, 35, 'Grass', 'Sihy', NULL);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(330, 35, 'Grass', 'Stoc', 2);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(331, 35, 'Forb', 'Lupz', 55);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(332, 35, 'Forb', 'Astz', NULL);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(333, 35, 'Forb', 'Penz', NULL);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(334, 35, 'Forb', 'Linw', NULL);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(335, 35, 'Forb', 'Eriz', 4);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(336, 35, 'Browse', 'Hafr', NULL);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(341, 35, 'Overstory (Trees)', NULL);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(342, 35, 'Overstory (Shrub)', NULL);
 
INSERT INTO cover(c_id, p_id, type, value)
VALUES(343, 35, 'Crown Cover (Herb)', 40);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(344, 35, 'Bare Ground', 20);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(345, 35, 'Rock/Pav (Nat)', NULL);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(346, 35, 'Rock/Pav (Unnat)', NULL);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(347, 35, 'Veg/Litter', 80);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(348, 35, 'Soil Disturbance', NULL);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(349, 35, 'Droppings', NULL);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(350, 35, 'Pellet Groups', NULL);


INSERT INTO plot(p_id, t_id, plot_number)
VALUES (36, 4, 6);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(337, 36, 'Grass', 'Melz', NULL);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(338, 36, 'Grass', 'Sihy', 2);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(339, 36, 'Grass', 'Stoc', 4);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(340, 36, 'Forb', 'Lupz', NULL);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(341, 36, 'Forb', 'Astz', 4);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(342, 36, 'Forb', 'Penz', NULL);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(343, 36, 'Forb', 'Linw', NULL);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(344, 36, 'Forb', 'Eriz', NULL);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(345, 36, 'Browse', 'Hafr', NULL);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(351, 36, 'Overstory (Trees)', NULL);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(352, 36, 'Overstory (Shrub)', NULL);
 
INSERT INTO cover(c_id, p_id, type, value)
VALUES(353, 36, 'Crown Cover (Herb)', NULL);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(354, 36, 'Bare Ground', 50);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(355, 36, 'Rock/Pav (Nat)', NULL);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(356, 36, 'Rock/Pav (Unnat)', 10);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(357, 36, 'Veg/Litter', 40);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(358, 36, 'Soil Disturbance', NULL);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(359, 36, 'Droppings', NULL);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(360, 36, 'Pellet Groups', NULL);


INSERT INTO plot(p_id, t_id, plot_number)
VALUES (37, 4, 7);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(346, 37, 'Grass', 'Melz', 2);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(347, 37, 'Grass', 'Sihy', NULL);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(348, 37, 'Grass', 'Stoc', 2);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(349, 37, 'Forb', 'Lupz', NULL);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(350, 37, 'Forb', 'Astz', 1);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(351, 37, 'Forb', 'Penz', NULL);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(352, 37, 'Forb', 'Linw', NULL);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(353, 37, 'Forb', 'Eriz', NULL);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(354, 37, 'Browse', 'Hafr', NULL);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(361, 37, 'Overstory (Trees)', NULL);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(362, 37, 'Overstory (Shrub)', NULL);
 
INSERT INTO cover(c_id, p_id, type, value)
VALUES(363, 37, 'Crown Cover (Herb)', NULL);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(364, 37, 'Bare Ground', 60);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(365, 37, 'Rock/Pav (Nat)', NULL);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(366, 37, 'Rock/Pav (Unnat)', 30);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(367, 37, 'Veg/Litter', 10);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(368, 37, 'Soil Disturbance', NULL);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(369, 37, 'Droppings', NULL);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(370, 37, 'Pellet Groups', NULL);


INSERT INTO plot(p_id, t_id, plot_number)
VALUES (38, 4, 8);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(355, 38, 'Grass', 'Melz', NULL);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(356, 38, 'Grass', 'Sihy', NULL);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(357, 38, 'Grass', 'Stoc', 1);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(358, 38, 'Forb', 'Lupz', NULL);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(359, 38, 'Forb', 'Astz', 1);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(360, 38, 'Forb', 'Penz', 2);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(361, 38, 'Forb', 'Linw', NULL);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(362, 38, 'Forb', 'Eriz', 2);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(363, 38, 'Browse', 'Hafr', NULL);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(371, 38, 'Overstory (Trees)', NULL);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(372, 38, 'Overstory (Shrub)', NULL);
 
INSERT INTO cover(c_id, p_id, type, value)
VALUES(373, 38, 'Crown Cover (Herb)', NULL);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(374, 38, 'Bare Ground', 70);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(375, 38, 'Rock/Pav (Nat)', NULL);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(376, 38, 'Rock/Pav (Unnat)', 10);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(377, 38, 'Veg/Litter', 20);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(378, 38, 'Soil Disturbance', NULL);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(379, 38, 'Droppings', NULL);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(380, 38, 'Pellet Groups', NULL);


INSERT INTO plot(p_id, t_id, plot_number)
VALUES (39, 4, 9);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(364, 39, 'Grass', 'Melz', NULL);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(365, 39, 'Grass', 'Sihy', NULL);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(366, 39, 'Grass', 'Stoc', 8);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(367, 39, 'Forb', 'Lupz', NULL);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(368, 39, 'Forb', 'Astz', NULL);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(369, 39, 'Forb', 'Penz', NULL);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(370, 39, 'Forb', 'Linw', NULL);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(371, 39, 'Forb', 'Eriz', NULL);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(372, 39, 'Browse', 'Hafr', NULL);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(381, 39, 'Overstory (Trees)', NULL);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(382, 39, 'Overstory (Shrub)', NULL);
 
INSERT INTO cover(c_id, p_id, type, value)
VALUES(383, 39, 'Crown Cover (Herb)', NULL);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(384, 39, 'Bare Ground', 70);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(385, 39, 'Rock/Pav (Nat)', 10);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(386, 39, 'Rock/Pav (Unnat)', NULL);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(387, 39, 'Veg/Litter', 20);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(388, 39, 'Soil Disturbance', NULL);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(389, 39, 'Droppings', NULL);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(390, 39, 'Pellet Groups', 16);


INSERT INTO plot(p_id, t_id, plot_number)
VALUES (40, 4, 10);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(373, 40, 'Grass', 'Melz', 3);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(374, 40, 'Grass', 'Sihy', NULL);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(375, 40, 'Grass', 'Stoc', NULL);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(376, 40, 'Forb', 'Lupz', NULL);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(377, 40, 'Forb', 'Astz', NULL);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(378, 40, 'Forb', 'Penz', NULL);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(379, 40, 'Forb', 'Linw', NULL);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(380, 40, 'Forb', 'Eriz', NULL);

INSERT INTO biomass(b_id, p_id, type, species, green_weight)
VALUES(381, 40, 'Browse', 'Hafr', 10);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(391, 40, 'Overstory (Trees)', NULL);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(392, 40, 'Overstory (Shrub)', NULL);
 
INSERT INTO cover(c_id, p_id, type, value)
VALUES(393, 40, 'Crown Cover (Herb)', NULL);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(394, 40, 'Bare Ground', 10);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(395, 40, 'Rock/Pav (Nat)', NULL);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(396, 40, 'Rock/Pav (Unnat)', NULL);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(397, 40, 'Veg/Litter', 80);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(398, 40, 'Soil Disturbance', NULL);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(399, 40, 'Droppings', NULL);

INSERT INTO cover(c_id, p_id, type, value)
VALUES(400, 40, 'Pellet Groups', NULL);


INSERT INTO soil_summary(s_id, r_id, surface_texture, surf_text_thick, surf_text_ph,
subsoil_texture, sub_text_thick, sub_text_ph, substratum_mat, eff_root_depth,
general_remarks, avg_surface_loss, loss_over_area, gullies_length, gullies_depth,
erosion_remarks, detachability, rock_coverage, adj_detachability, permeability,
erod_index, erod_index_class, slope, eros_haz_class, compaction,
displacement, cover_dispersion, potential_product, suit_reasons)
VALUES(2, 112, 'Sandy to gravel', 12, 5.7,
       'Gravel', 12, 5.5, 'Granitic soil', '12-14',
       'none', NULL, NULL, NULL, NULL,
       'no soil erosion', 7, 50, 3.5, 4,
       14, 'II', 15, 'II', 'light',
       'none', 'Variable', 600, 'Effective soil depth exceeds 10", gravel cover between 40-60%, slope 0-15%');