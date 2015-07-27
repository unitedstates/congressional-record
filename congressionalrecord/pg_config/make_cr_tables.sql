DROP TABLE IF EXISTS cr_pages;
CREATE TABLE cr_pages (
       pageid varchar(35) PRIMARY KEY,
       title varchar(100),
       chamber varchar(21),
       extension boolean,
       cr_day varchar(2),
       cr_month varchar(15),
       cr_year varchar(4),
       num varchar(4),
       vol varchar(4),
       pages varchar(5),
       wkday varchar(10));

DROP TABLE IF EXISTS cr_bills;
CREATE TABLE cr_bills (
       relationid SERIAL PRIMARY KEY,
       congress smallint,
       context varchar(5),
       bill_type varchar(4),
       bill_no smallint,
       pageid varchar(25) REFERENCES cr_pages(pageid));

DROP TABLE IF EXISTS cr_speech;
CREATE TABLE cr_speech (
       speechid SERIAL PRIMARY KEY,
       speaker varchar(50),
       speaker_bioguide varchar(7) REFERENCES leg_bio(bioguideid),
       pageid varchar(25) REFERENCES cr_pages(pageid),
       text text,
       turn smallint NOT NULL);

CREATE INDEX speech_bio_ix ON cr_speech (speaker_bioguide);
       
