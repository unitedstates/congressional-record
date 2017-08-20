DROP TABLE IF EXISTS cr_pages CASCADE;
CREATE TABLE cr_pages (
       pageid varchar(35) PRIMARY KEY,
       title text,
       chamber varchar(21),
       extension boolean,
       cr_day varchar(2),
       cr_month varchar(15),
       cr_year varchar(4),
       num varchar(4),
       vol varchar(4),
       pages varchar(15),
       wkday varchar(10));

DROP TABLE IF EXISTS cr_bills;
CREATE TABLE cr_bills (
       congress smallint,
       context varchar(50),
       bill_type varchar(7),
       bill_no smallint,
       pageid varchar(35) REFERENCES cr_pages(pageid));

DROP TABLE IF EXISTS cr_speech;
CREATE TABLE cr_speech (
       speechid varchar(50) PRIMARY KEY,
       speaker varchar(100),
       speaker_bioguide varchar(7) REFERENCES leg_bio(bioguideid),
       pageid varchar(35) REFERENCES cr_pages(pageid),
       text text,
       turn smallint NOT NULL);
       
