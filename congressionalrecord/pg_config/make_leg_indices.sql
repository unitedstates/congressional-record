ALTER TABLE leg_bio ADD COLUMN dob_date date; 
UPDATE leg_bio SET dob_date = to_date(dob,'YYYY-MM-DD');
ALTER TABLE leg_terms ADD COLUMN start_date date;
UPDATE leg_terms SET start_date = to_date(start,'YYYY-MM-DD');
ALTER TABLE leg_terms ADD COLUMN end_date date;
UPDATE leg_terms SET end_date = to_date("end", 'YYYY-MM-DD');

CREATE INDEX terms_bioguide_ix ON leg_terms (bioguideid);
CREATE INDEX terms_start_ix ON leg_terms(start_date);
CREATE INDEX fec_bioguide_ix ON leg_fec (bioguideid);
CREATE INDEX bio_name_ix ON leg_bio (official_full);
