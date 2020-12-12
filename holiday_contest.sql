-- -------------------------------------------------------------
-- TablePlus 3.12.0(354)
--
-- https://tableplus.com/
--
-- Database: db
-- Generation Time: 2020-12-11 21:33:08.4110
-- -------------------------------------------------------------


-- This script only contains the table creation statements and does not fully represent the table in the database. It's still missing: indices, triggers. Do not use it as a backup.

-- Sequence and defined type
CREATE SEQUENCE IF NOT EXISTS holiday_contest_id_seq1;

-- Table Definition
CREATE TABLE "public"."holiday_contest" (
    "id" int4 NOT NULL DEFAULT nextval('holiday_contest_id_seq1'::regclass),
    "uid" numeric,
    "score" numeric DEFAULT 0,
    PRIMARY KEY ("id")
);

