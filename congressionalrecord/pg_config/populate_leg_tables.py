import csv
import os

import psycopg2 as pg
import yaml

AUXDATA_DIR = "/home/ncj/devel/congress/congress_leg_info"
YAML_DIR = "/home/ncj/devel/congress/congress-legislators"

"""
Given hardcoded output locations in auxdata, append rows to csv
"""


def load_yaml(afile):
    with open(afile, "r") as inf:
        the_yaml = yaml.safe_load(inf)
    return the_yaml


def parse_legislators(afile, append=False, idstart=0):
    if append:
        mode = "a"
    else:
        mode = "w"
    leg_bio = open(os.path.join(AUXDATA_DIR, "leg_bio.csv"), mode)
    bio_fields = [
        "bioguideid",
        "dob",
        "gender",
        "religion",
        "cspan",
        "govtrack",
        "house_history",
        "icpsr",
        "lis",
        "maplight",
        "opensecrets",
        "thomas",
        "votesmart",
        "washington_post",
        "wikipedia",
        "name_first",
        "name_last",
        "official_full",
        "name_middle",
        "name_suffix",
        "name_nickname",
    ]
    leg_terms = open(os.path.join(AUXDATA_DIR, "leg_terms.csv"), mode)
    term_fields = [
        "idn",
        "bioguideid",
        "address",
        "contact_form",
        "district",
        "start",
        "end",
        "office",
        "party",
        "phone",
        "state",
        "ttype",
        "url",
    ]
    leg_fec = open(os.path.join(AUXDATA_DIR, "leg_fec.csv"), mode)
    fec_fields = ["fec_id", "bioguideid"]
    leg_yaml = load_yaml(afile)

    bio_writer = csv.DictWriter(leg_bio, fieldnames=bio_fields, delimiter="|")
    term_writer = csv.DictWriter(leg_terms, fieldnames=term_fields, delimiter="|")
    fec_writer = csv.DictWriter(leg_fec, fieldnames=fec_fields, delimiter="|")
    idn = idstart
    for leg in leg_yaml:
        bio_row = {}
        for inkey, outkey in [
            ("bioguide", "bioguideid"),
            ("cspan", "cspan"),
            ("govtrack", "govtrack"),
            ("house_history", "house_history"),
            ("icpsr", "icpsr"),
            ("lis", "lis"),
            ("maplight", "maplight"),
            ("opensecrets", "opensecrets"),
            ("thomas", "thomas"),
            ("votesmart", "votesmart"),
            ("washington_post", "washington_post"),
            ("wikipedia", "wikipedia"),
        ]:
            if inkey in list(leg["id"].keys()):
                bio_row[outkey] = leg["id"][inkey]

        for inkey, outkey in [
            ("birthday", "dob"),
            ("gender", "gender"),
            ("religion", "religion"),
        ]:
            if inkey in list(leg["bio"].keys()):
                bio_row[outkey] = leg["bio"][inkey]

        for inkey, outkey in [
            ("first", "name_first"),
            ("last", "name_last"),
            ("official_full", "official_full"),
            ("middle", "name_middle"),
            ("suffix", "name_suffix"),
            ("nickname", "name_nickname"),
        ]:
            if inkey in list(leg["name"].keys()):
                bio_row[outkey] = leg["name"][inkey]
            else:
                bio_row[outkey] = ""

        bio_writer.writerow(bio_row)
        for term in leg["terms"]:
            term_row = {}
            term_row["idn"] = idn
            idn += 1
            term_row["bioguideid"] = leg["id"]["bioguide"]
            for inkey, outkey in [
                ("address", "address"),
                ("contact_form", "contact_form"),
                ("district", "district"),
                ("start", "start"),
                ("end", "end"),
                ("office", "office"),
                ("party", "party"),
                ("phone", "phone"),
                ("state", "state"),
                ("type", "ttype"),
                ("url", "url"),
            ]:
                if inkey in list(term.keys()):
                    term_row[outkey] = term[inkey]
            term_writer.writerow(term_row)

        if "fec" not in list(leg["id"].keys()):
            pass
        else:
            for fec in leg["id"]["fec"]:
                fec_row = {}
                fec_row["bioguideid"] = leg["id"]["bioguide"]
                fec_row["fec_id"] = fec
                fec_writer.writerow(fec_row)

    for afile in [leg_bio, leg_terms, leg_fec]:
        afile.close()


if __name__ == "__main__":
    import os

    parse_legislators(os.path.join(YAML_DIR, "legislators-current.yaml"))
    tid = 0
    with open(os.path.join(AUXDATA_DIR, "leg_terms.csv"), "r") as inf:
        for l in inf:
            tid += 1

    past = parse_legislators(
        os.path.join(YAML_DIR, "legislators-historical.yaml"), append=True, idstart=tid
    )

    conn = pg.connect("dbname = congress")
    cur = conn.cursor()
    for table, fpath in [
        ("leg_bio", os.path.join(AUXDATA_DIR, "leg_bio.csv")),
        ("leg_terms", os.path.join(AUXDATA_DIR, "leg_terms.csv")),
        ("leg_fec", os.path.join(AUXDATA_DIR, "leg_fec.csv")),
    ]:
        with open(fpath, "r") as infile:
            cur.copy_from(table, infile, sep="|")
    conn.close()
