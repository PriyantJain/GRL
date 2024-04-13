-- -- CREATE DATABASE GRL_backend_testing;

-- CREATE TABLE STATS (
--     Id int unique auto_increment,
--     Score varchar(255),
--     DT_1 varchar(255),
--     DT_2 varchar(255),
--     DT_3 varchar(255),
--     DT_1_completed bool,
--     DT_2_completed bool,
--     DT_3_completed bool,
--     Last_Open varchar(255),
--     Last_Day_Score varchar(255),
--     PRIMARY KEY (Id)
-- );

-- create table TO_DO_TASKS (
--     Sr_No int unique auto_increment,
--     Task_Name varchar(511),
--     Completion_Date varchar(31),
--     Task_Points varchar(255),
--     Filter varchar(127)
-- )

-- CREATE TABLE RECURRING_TASKS (
--     Sr_No int unique auto_increment,
--     Task_Name varchar(511),
--     Last_Completion_Date varchar(31),
--     Task_Points varchar(255)
-- );

-- CREATE TABLE USER_LOGS (
-- 	Sr_No int NOT NULL unique auto_increment,
-- 	Log varchar(511)
-- );

-- CREATE TABLE TO_DO_LIST (
-- 	Sr_No int unique auto_increment,
--     Task_Name varchar(511),
--     Track int DEFAULT 0,
--     Parent int
-- );

-- CREATE TABLE TO_DO_COMPLETED (
-- 	Sr_No int unique auto_increment,
--     Task_Name varchar(511),
--     Track int DEFAULT 0,
--     Parent int,
--     Task_Points varchar(255),
--     Completion_Date varchar(31)
-- );

-- update to_do_list 
-- SET to_do_list.Parent = to_do_list.Sr_No
-- WHERE to_do_list.Sr_No > -1;

-- INSERT INTO to_do_completed (Sr_No, Task_Name, Task_Points, Completion_Date)
-- SELECT Sr_No, Task_Name, Task_Points, Completion_Date FROM to_do_tasks
-- WHERE Completion_Date <> '-1';

-- DELIMITER $$
-- CREATE TRIGGER parent_default BEFORE INSERT ON TO_DO_LIST
-- FOR EACH ROW

-- BEGIN
-- 	IF NEW.parent = -1 THEN SET NEW.parent = (SELECT AUTO_INCREMENT FROM information_schema.tables WHERE table_name = 'to_do_list');
-- 	END IF;
-- END;

-- $$
-- DELIMITER ;

-- DROP TRIGGER parent_default;

WITH TEMPTB AS (SELECT MAX(Sr_No) FROM TO_DO_LIST)
UPDATE TO_DO_Linsert INTO to_do_list (Task_Name) values ('Del');IST
SET Parent = (SELECT * FROM TEMPTB)
WHERE Sr_No = (SELECT * FROM TEMPTB);




-- CREATE TABLE TO_DO_LIST (
-- 	Sr_No int unique auto_increment,
--     Task_Name varchar(511),
--     Track int DEFAULT 0,
--     Parent int
-- );

-- CREATE TABLE TO_DO_COMPLETED (
-- 	Sr_No int unique auto_increment,
--     Task_Name varchar(511),
--     Track int DEFAULT 0,
--     Parent int,
--     Task_Points varchar(255),
--     Completion_Date varchar(31)
-- );

-- CREATE TABLE RECURRING_TASKS (
--     Sr_No int unique auto_increment,
--     Task_Name varchar(511),
--     Last_Completion_Date varchar(31),
--     Task_Points varchar(255)
-- );

-- CREATE TABLE VOUCHERS (
--     Sr_No int unique auto_increment,
--     V_name varchar(511),
--     Quantity int DEFAULT 0,
--     Price int
-- );


-- ALTER TABLE RECURRING_TASKS
-- ADD Track int DEFAULT 0, 
-- ADD Parent int;

-- UPDATE RECURRING_TASKS 
-- SET RECURRING_TASKS.Parent = RECURRING_TASKS.Sr_No
-- WHERE RECURRING_TASKS.Sr_No > -1;

SHOW TRIGGERS