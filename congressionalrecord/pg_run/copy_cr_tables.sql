COPY cr_pages FROM '/home/ncj/projects/congress2/congressionalrecord2/dbfiles/pages.csv' WITH CSV DELIMITER '|' ENCODING 'UTF8';
COPY cr_bills FROM '/home/ncj/projects/congress2/congressionalrecord2/dbfiles/bills.csv' WITH CSV DELIMITER '|' ENCODING 'UTF8';
COPY cr_speech FROM '/home/ncj/projects/congress2/congressionalrecord2/dbfiles/speeches.csv' WITH CSV DELIMITER '|' ENCODING 'UTF8';
