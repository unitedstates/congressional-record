import json
import logging
import os
import random
import re
import unittest

from congressionalrecord.govinfo import cr_parser as cr

logging.basicConfig(filename="tests.log", level=logging.DEBUG)

"""
These tests make sure that basic parser functions
run as expected, generating files full of JSON output
such that nothing that looks like
a speech exists outside of a "speech" JSON item.
"""


class testCRDir(unittest.TestCase):
    def setUp(self):
        pass

    def test_crdir(self):
        """
        CRDir pointed at correct path
        """
        input_string = "tests/test_files/CREC-2005-07-20"
        crdir = cr.ParseCRDir(input_string)
        self.assertEqual(crdir.cr_dir, input_string)


class testCRFile(unittest.TestCase):
    def setUp(self):
        input_string = "tests/test_files/CREC-2005-07-20"
        self.crdir = cr.ParseCRDir(input_string)
        input_dir = os.path.join(input_string, "html")
        input_file = random.choice(os.listdir(input_dir))  # nosec
        self.input_path = os.path.join(input_dir, input_file)

    def test_top_level_keys(self):
        """
        CRFile has all the right fixins' in the crdoc
        """
        crfile = cr.ParseCRFile(self.input_path, self.crdir)
        for x in ["doc_title", "header", "content", "id"]:
            self.assertIn(x, crfile.crdoc.keys(), msg="{0} not in crdoc!".format(x))

    def test_content_length(self):
        crfile = cr.ParseCRFile(self.input_path, self.crdir)
        self.assertGreater(len(crfile.crdoc["content"]), 0, msg="No items in content!")


class testLineBreak(unittest.TestCase):
    def setUp(self):
        self.sp = re.compile(
            r"^(\s{1,2}|<bullet>)(?P<name>((((Mr)|(Ms)|(Mrs)|(Miss))\. (([-A-Z\'])(\s)?)+( of [A-Z][a-z]+)?)|((The ((VICE|ACTING|Acting) )?(PRESIDENT|SPEAKER|CHAIR(MAN)?)( pro tempore)?)|(The PRESIDING OFFICER)|(The CLERK)|(The CHIEF JUSTICE)|(The VICE PRESIDENT)|(Mr\. Counsel [A-Z]+))( \([A-Za-z.\- ]+\))?))\."
        )

    def test_fixedLineBreak(self):
        rootdir = "tests/test_files/CREC-2005-07-20/json"
        for apath in os.listdir(rootdir):
            thepath = os.path.join(rootdir, apath)
            with open(thepath, "r") as thefile:
                thejson = json.load(thefile)
            for item in thejson["content"]:
                if item["kind"] != "speech":
                    for line in item["text"].split("\n"):
                        self.assertFalse(self.sp.match(line), "Check {0}".format(apath))



class _DocumentTest(unittest.TestCase):
    """Parses one committed document & read its items."""

    ROOT = "tests/test_files"

    def items(self, day, granule):
        crdir = cr.ParseCRDir(os.path.join(self.ROOT, day))
        path = os.path.join(self.ROOT, day, "html", granule + ".htm")
        return cr.ParseCRFile(path, crdir).crdoc["content"]

    def speakers(self, day, granule):
        return [i["speaker"] for i in self.items(day, granule) if i["kind"] == "speech"]

    def item_headed_by(self, day, granule, header):
        for item in self.items(day, granule):
            if item["text"].split("\n")[0].strip().startswith(header):
                return item
        return None

    def assert_heads_a_speech(self, day, granule, header, speaker, bioguide=None):
        """header starts its own speech, published under speaker."""
        item = self.item_headed_by(day, granule, header)
        if item is None:
            self.fail(
                "{0!r} starts no item in {1}, it was swallowed into {2}".format(
                    header, granule, self._swallowed_by(day, granule, header)
                )
            )
        self.assertEqual(
            item["kind"], "speech", msg="{0!r} is not a speech".format(header)
        )
        self.assertEqual(item["speaker"], speaker)
        if bioguide is not None:
            self.assertEqual(item["speaker_bioguide"], bioguide, msg="wrong member id")
        return item

    def assert_not_a_speech(self, day, granule, line):
        """line starts a line of the document, and does not begin a speech.
        """
        starts_a_line = any(
            text_line.strip().startswith(line)
            for item in self.items(day, granule)
            for text_line in item["text"].split("\n")
        )
        if not starts_a_line:
            self.fail(
                "{0!r} starts no line in {1} -- nothing was checked".format(
                    line, granule
                )
            )
        item = self.item_headed_by(day, granule, line)
        if item is not None and item["kind"] == "speech":
            self.fail(
                "{0!r} was published as a speech by {1!r}".format(
                    line, item["speaker"]
                )
            )

    def _swallowed_by(self, day, granule, header):
        for item in self.items(day, granule):
            if header in item["text"]:
                return "a {0} published under {1!r} ({2} words)".format(
                    item["kind"], item["speaker"], len(item["text"].split())
                )
        return "nothing. The text is not in this document"


class testNameBody(_DocumentTest):
    """What a member's surname may look like.
    """

    REMOVE_DAY = "CREC-2016-03-23"
    REMOVE_GRANULE = "CREC-2016-03-23-pt1-PgH1555-5"
    INITIAL_DAY = "CREC-2007-07-12"
    INITIAL_GRANULE = "CREC-2007-07-12-pt1-PgH7674-2"
    PREFIX_DAY = "CREC-1997-02-05"
    PREFIX_GRANULE = "CREC-1997-02-05-pt1-PgS1018-2"
    PROSE_DAY = "CREC-2007-01-09"
    PROSE_GRANULE = "CREC-2007-01-09-pt1-PgE49-2"

    def test_pledge_annotation_is_not_a_speech(self):
        self.assert_not_a_speech(
            self.REMOVE_DAY,
            self.REMOVE_GRANULE,
            "Mr. JODY B. HICE of Georgia led the Pledge of Allegiance",
        )

    def test_initial_in_prose_is_not_a_header(self):
        self.assert_not_a_speech(
            self.PROSE_DAY, self.PROSE_GRANULE, "Mr. Q. Byrum Hurst had two passions"
        )

    def test_middle_initial_speaker_keeps_their_whole_name(self):
        self.assert_heads_a_speech(
            self.INITIAL_DAY,
            self.INITIAL_GRANULE,
            "Ms. LINDA T. SAENCHEZ of California.",
            "Ms. LINDA T. SAENCHEZ of California",
        )

    def test_lowercase_prefix_surname_is_a_speaker(self):
        self.assert_heads_a_speech(
            self.PREFIX_DAY, self.PREFIX_GRANULE, "Mr. McCAIN.", "Mr. McCAIN"
        )


class testMultiwordState(_DocumentTest):

    DAY = "CREC-2007-01-09"
    GRANULE = "CREC-2007-01-09-pt1-PgH132"
    HEADER = "Mr. KING of New York."

    def test_two_word_state_is_part_of_the_speaker(self):
        self.assert_heads_a_speech(
            self.DAY, self.GRANULE, self.HEADER, "Mr. KING of New York"
        )


class testHonorificSpellings(_DocumentTest):
    """Tests the new honorifics"""

    MISS_DAY = "CREC-2020-03-27"
    MISS_GRANULE = "CREC-2020-03-27-pt1-PgH1732"
    MISS_HEADER = "Miss GONZALES-COLON of Puerto Rico."
    CAPS_DAY = "CREC-2020-12-03"
    CAPS_GRANULE = "CREC-2020-12-03-pt1-PgH6061"
    CAPS_HEADER = "MR. WOODALL."

    def test_bare_miss_is_an_honorific(self):
        self.assert_heads_a_speech(
            self.MISS_DAY,
            self.MISS_GRANULE,
            self.MISS_HEADER,
            "Miss GONZALES-COLON of Puerto Rico",
        )

    def test_all_caps_honorific_is_an_honorific(self):
        self.assert_heads_a_speech(
            self.CAPS_DAY, self.CAPS_GRANULE, self.CAPS_HEADER, "MR. WOODALL"
        )


class testHonorificSpacing(_DocumentTest):
    DAY = "CREC-2024-11-12"
    GRANULE = "CREC-2024-11-12-pt1-PgE1124-4"
    HEADER = "Mr.  LaMALFA."

    def test_double_spaced_honorific_starts_a_speech(self):
        """Two spaces after Mr. still begins a speech."""
        self.assert_heads_a_speech(
            self.DAY, self.GRANULE, self.HEADER, "Mr. LaMALFA", "L000578"
        )


class testManagerCounsel(_DocumentTest):

    DAY = "CREC-2020-01-21"
    MANAGER_GRANULE = "CREC-2020-01-21-pt1-PgS377"
    WOMAN_GRANULE = "CREC-2020-01-21-pt1-PgS406"

    def test_manager_is_a_title(self):
        self.assert_heads_a_speech(
            self.DAY, self.MANAGER_GRANULE, "Mr. Manager SCHIFF.", "Mr. Manager SCHIFF"
        )

    def test_woman_manager_with_a_state_is_a_speaker(self):
        self.assert_heads_a_speech(
            self.DAY,
            self.WOMAN_GRANULE,
            "Ms. Manager GARCIA of Texas.",
            "Ms. Manager GARCIA of Texas",
        )


class testOfficerTitles(_DocumentTest):
    """New Officer Titles
    """

    ACTING_DAY = "CREC-2022-05-04"
    ACTING_GRANULE = "CREC-2022-05-04-pt1-PgS2296-2"
    CHAPLAIN_DAY = "CREC-2025-09-11"
    CHAPLAIN_GRANULE = "CREC-2025-09-11-pt1-PgH4241-2"
    TEMPORE_DAY = "CREC-1996-04-24"
    TEMPORE_GRANULE = "CREC-1996-04-24-pt1-PgH3792"
    MIXED_DAY = "CREC-2005-07-20"
    MIXED_GRANULE = "CREC-2005-07-20-pt1-PgH6117-3"
    CAPS_DAY = "CREC-2005-07-20"
    CAPS_GRANULE = "CREC-2005-07-20-pt1-PgS8582-2"

    def test_modifier_attaches_to_any_officer_title(self):
        self.assert_heads_a_speech(
            self.ACTING_DAY,
            self.ACTING_GRANULE,
            "The ACTING PRESIDING OFFICER.",
            "The ACTING PRESIDING OFFICER",
        )

    def test_chaplain_is_an_officer_title(self):
        self.assert_heads_a_speech(
            self.CHAPLAIN_DAY, self.CHAPLAIN_GRANULE, "The CHAPLAIN.", "The CHAPLAIN"
        )

    def test_all_caps_pro_tempore_is_recognized(self):
        self.assert_heads_a_speech(
            self.TEMPORE_DAY,
            self.TEMPORE_GRANULE,
            "The SPEAKER PRO TEMPORE.",
            "The SPEAKER PRO TEMPORE",
        )

    def test_title_case_officer_title_is_recognized(self):
        self.assert_heads_a_speech(
            self.MIXED_DAY,
            self.MIXED_GRANULE,
            "The Acting Chairman.",
            "The Acting Chairman",
        )

    def test_all_caps_article_is_recognized(self):
        self.assert_heads_a_speech(
            self.CAPS_DAY,
            self.CAPS_GRANULE,
            "THE PRESIDING OFFICER.",
            "THE PRESIDING OFFICER",
        )


class testCollapseSpeakerWhitespace(_DocumentTest):
    """Collapse whitespace inside the captured speaker.
    """

    DAY = "CREC-1999-11-05"
    GRANULE = "CREC-1999-11-05-pt1-PgE2291-3"
    HEADER = "Mr. FARR  of California."
    OFFICER_DAY = "CREC-1994-07-21"
    OFFICER_GRANULE = "CREC-1994-07-21-pt1-PgH48"

    def test_double_spaced_name_is_stored_single_spaced(self):
        self.assert_heads_a_speech(
            self.DAY, self.GRANULE, self.HEADER, "Mr. FARR of California", "F000030"
        )

    def test_collapse_reaches_officer_headers_too(self):
        self.assert_heads_a_speech(
            self.OFFICER_DAY,
            self.OFFICER_GRANULE,
            "The SPEAKER pro tempore (Mr. Fields  of Louisiana).",
            "The SPEAKER pro tempore (Mr. Fields of Louisiana)",
        )


class testBulletNormalization(_DocumentTest):
    """Tests correct <bullet> preprocessing
    """


    DAY = "CREC-1997-01-28"
    GRANULE = "CREC-1997-01-28-pt1-PgS771-3"

    def test_bullet_header_starts_a_speech(self):
        speeches = [
            (i["speaker"], i["speaker_bioguide"])
            for i in self.items(self.DAY, self.GRANULE)
            if i["kind"] == "speech"
        ]
        self.assertEqual(speeches, [("Mr. ABRAHAM", "A000355")])

    def test_bullet_tag_does_not_leak_into_the_text(self):
        for item in self.items(self.DAY, self.GRANULE):
            self.assertFalse(
                "<bullet>" in item["text"],
                msg="a <bullet> marker survived into a {0} item".format(item["kind"]),
            )


class testParentheticalAfterName(_DocumentTest):
    DAY = "CREC-1994-02-03"
    GRANULE = "CREC-1994-02-03-pt1-PgH44"
    HEADER = "Mr. TRAFICANT (during the reading)."

    def test_parenthetical_header_starts_a_speech(self):
        self.assert_heads_a_speech(
            self.DAY, self.GRANULE, self.HEADER, "Mr. TRAFICANT", "T000350"
        )


class testGuestSpeakerTitles(_DocumentTest):

    DAY = "CREC-2024-04-11"
    GRANULE = "CREC-2024-04-11-pt1-PgH2294-4"
    HEADER = "Prime Minister KISHIDA."
    PROSE_DAY = "CREC-2020-01-21"
    PROSE_GRANULE = "CREC-2020-01-21-pt1-PgS406"

    def test_guest_address_starts_its_own_speech(self):
        self.assert_heads_a_speech(
            self.DAY, self.GRANULE, self.HEADER, "Prime Minister KISHIDA"
        )

    def test_prose_about_a_guest_is_not_a_header(self):
        self.assert_not_a_speech(
            self.PROSE_DAY,
            self.PROSE_GRANULE,
            "President Clinton himself gave testimony on camera and under oath.",
        )


class testSpeakerPatternGuards(_DocumentTest):


    def test_vote_change_annotation_is_not_a_speech(self):
        self.assert_not_a_speech(
            "CREC-2005-07-20",
            "CREC-2005-07-20-pt1-PgH6117-3",
            "Mr. DOYLE changed his vote",
        )


class testTagSpeechAsTitle(_DocumentTest):

    DAY = "CREC-1997-01-28"
    GRANULE = "CREC-1997-01-28-pt1-PgS771-3"

    # Original is commented out, I replaced it with the helper for consistency
    #
    # def setUp(self):
    #     input_string = "tests/test_files/CREC-1997-01-28"
    #     self.crdir = cr.ParseCRDir(input_string)
    #     input_dir = os.path.join(input_string, "html")
    #     input_file = "CREC-1997-01-28-pt1-PgS771-3.htm"
    #     self.input_path = os.path.join(input_dir, input_file)
    #
    # def test_speech_should_not_be_title(self):
    #     crfile = cr.ParseCRFile(self.input_path, self.crdir)
    #     titles = [i for i in crfile.crdoc["content"] if i["kind"] == "title"]
    #     pat = re.compile(r"[a-z]{5,}")
    #     for i in titles:
    #         self.assertNotRegex(i["text"], pat)

    def test_speech_should_not_be_title(self):
        titles = [i for i in self.items(self.DAY, self.GRANULE) if i["kind"] == "title"]
        pat = re.compile(r"[a-z]{5,}")
        for i in titles:
            self.assertNotRegex(i["text"], pat)
