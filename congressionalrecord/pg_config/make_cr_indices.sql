CREATE INDEX speech_bio_ix ON cr_speech (speaker_bioguide);
CREATE INDEX pageid_bills_ix ON cr_bills (pageid);
CREATE INDEX speech_txt_ix ON cr_speech USING gin(to_tsvector('english',text));
