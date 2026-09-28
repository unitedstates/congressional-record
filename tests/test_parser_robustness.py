import copy
import os
import tempfile
import unittest
import warnings
from functools import lru_cache
from importlib.util import find_spec
from unittest.mock import patch

from bs4 import BeautifulSoup

from congressionalrecord.govinfo import cr_parser as cr

DAY = "tests/test_files/CREC-2005-07-20"


def granule(name):
    return os.path.join(DAY, "html", name + ".htm")


@lru_cache(maxsize=None)
def day():
    """The fixture day's MODS, read once; the parser never modifies it."""
    return cr.ParseCRDir(DAY)


def speeches(parser):
    return [
        (item["speaker"], item["text"])
        for item in parser.crdoc["content"]
        if item["kind"] == "speech"
    ]


def none_strings(node, path=()):
    """Where a parsed document holds the string "None"."""
    if isinstance(node, dict):
        children = node.items()
    elif isinstance(node, list):
        children = enumerate(node)
    else:
        return [path] if node == "None" else []
    return [p for key, child in children for p in none_strings(child, path + (key,))]


class testBeautifulSoupArguments(unittest.TestCase):
    def test_parse_uses_no_deprecated_argument(self):
        crdir = day()
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            cr.ParseCRFile(granule("CREC-2005-07-20-pt1-PgH6115-2"), crdir)
        ours = [
            str(w.message)
            for w in caught
            if issubclass(w.category, DeprecationWarning)
            and os.path.realpath(w.filename) == os.path.realpath(cr.__file__)
        ]
        self.assertEqual(ours, [])


class testSpeakerPatternPerDocument(unittest.TestCase):
    """Each document matches speeches against its own MODS speaker list."""

    # Four of its speeches are Ms. MILLENDER-McDONALD's, which only its
    # speaker list matches; OTHER's list names someone else.
    DOC = granule("CREC-2005-07-20-pt1-PgH6115-2")
    OTHER = granule("CREC-2005-07-20-pt1-PgE1539-3")

    def setUp(self):
        self.crdir = day()

    def test_parse_leaves_the_class_table_unchanged(self):
        before = copy.deepcopy(cr.ParseCRFile.item_types)
        # Two different speaker lists, so a write cannot match by chance.
        for path in (self.DOC, self.OTHER):
            cr.ParseCRFile(path, self.crdir)
            self.assertEqual(cr.ParseCRFile.item_types, before)

    def test_documents_parsed_in_sequence_keep_their_own_patterns(self):
        doc = cr.ParseCRFile(self.DOC, self.crdir)
        other = cr.ParseCRFile(self.OTHER, self.crdir)
        self.assertNotEqual(doc.re_newspeaker, other.re_newspeaker)
        self.assertEqual(doc.item_types["speech"]["patterns"], [doc.re_newspeaker])
        self.assertEqual(other.item_types["speech"]["patterns"], [other.re_newspeaker])

    def test_document_begun_mid_parse_leaves_the_speakers_alone(self):
        alone = speeches(cr.ParseCRFile(self.DOC, self.crdir))
        self.assertIn("Ms. MILLENDER-McDONALD", [s for s, _ in alone])
        item, other = cr.crItem, []

        def other_document_first(parser):
            # What a second thread does: start another document mid-parse.
            if not other:
                other.append(None)
                other[0] = cr.ParseCRFile(self.OTHER, self.crdir)
            return item(parser)

        with patch(
            "congressionalrecord.govinfo.cr_parser.crItem",
            side_effect=other_document_first,
        ):
            interleaved = cr.ParseCRFile(self.DOC, self.crdir)
        self.assertIsNotNone(other[0])
        self.assertEqual(speeches(interleaved), alone)


class testAbsentValues(unittest.TestCase):
    """A value the source lacks is None, never the string "None"."""

    # Its MODS search title lacks "; Congressional Record Vol. N, No. N".
    UNTITLED = granule("CREC-2005-07-20-pt1-PgH6176-5")
    TITLED = granule("CREC-2005-07-20-pt1-PgH6115-2")

    def setUp(self):
        self.crdir = day()

    def test_member_without_attributes(self):
        member = BeautifulSoup(
            '<congmember><name type="parsed">Mr. DOE</name></congmember>', "lxml"
        ).congmember
        parser = cr.ParseCRFile.__new__(cr.ParseCRFile)
        self.assertEqual(
            parser.people_helper(member),
            dict.fromkeys(
                ["bioguideid", "chamber", "congress", "party", "state", "role"]
                + ["name_full"]
            ),
        )

    def test_untitled_document(self):
        doc = cr.ParseCRFile(self.UNTITLED, self.crdir).crdoc
        self.assertIsNone(doc["doc_title"])

    def test_kinds_without_a_speaker(self):
        content = cr.ParseCRFile(self.TITLED, self.crdir).crdoc["content"]
        unspoken = {i["kind"] for i in content if i["speaker"] is None}
        self.assertIn("linebreak", unspoken)
        self.assertNotIn("speech", unspoken)

    def test_no_value_is_the_string_none(self):
        for path in (self.UNTITLED, self.TITLED):
            with self.subTest(path=path):
                doc = cr.ParseCRFile(path, self.crdir).crdoc
                self.assertEqual(none_strings(doc), [])

    @unittest.skipUnless(find_spec("pydantic"), "pydantic is not installed")
    def test_documents_validate(self):
        from congressionalrecord.schema import CongressionalRecordDocument

        for path in (self.UNTITLED, self.TITLED):
            with self.subTest(path=path):
                doc = cr.ParseCRFile(path, self.crdir).crdoc
                CongressionalRecordDocument(**doc)


class RewrittenGranule(unittest.TestCase):
    """A fixture granule whose <pre> lines a test rewrites and parses."""

    SOURCE = granule("CREC-2005-07-20-pt1-PgH6115-2")

    def setUp(self):
        self.crdir = day()
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.path = os.path.join(tmp.name, os.path.basename(self.SOURCE))
        with open(self.SOURCE) as source:
            html = source.read()
        start = html.index("<pre>") + len("<pre>")
        self.head, self.lines = html[:start], html[start:].split("\n")

    def parse(self, lines):
        with open(self.path, "w") as body:
            body.write(self.head + "\n".join(lines) + "</pre></body></html>")
        return cr.ParseCRFile(self.path, self.crdir)


class testShortBody(RewrittenGranule):
    """A text that stops or strays inside its header raises CRParseError."""

    ID = "CREC-2005-07-20-pt1-PgH6115-2"
    # The <pre> text starts with a blank line, then the volume, chamber,
    # pages and source lines.
    PARTS = ["volume", "volume", "chamber", "pages", "source"]

    def test_truncated_inside_the_header(self):
        for kept, part in enumerate(self.PARTS):
            with self.subTest(lines=kept):
                with self.assertRaisesRegex(
                    cr.CRParseError,
                    "{0} ends before its header's {1} line".format(self.ID, part),
                ):
                    self.parse(self.lines[:kept])

    def test_truncated_after_the_header(self):
        doc = self.parse(self.lines[: len(self.PARTS)]).crdoc
        self.assertEqual(doc["header"]["pages"], "H6115-H6117")
        self.assertEqual(doc["content"], [])

    def test_header_line_that_does_not_match(self):
        lines = list(self.lines)
        self.assertEqual(lines[2], "[House]")
        lines[2] = "House"
        with self.assertRaisesRegex(cr.CRParseError, "header's chamber line"):
            self.parse(lines)

    def test_is_a_value_error(self):
        self.assertTrue(issubclass(cr.CRParseError, ValueError))


class testMarkerLines(RewrittenGranule):
    """A [[Page]] or {time} marker is not text; the rest of its line is."""

    # Each alone on its line in the fixture.
    MARKERS = {118: "[[Page H6116]]", 174: " " * 30 + "{time}  1100"}

    def content(self, lines):
        return self.parse(lines).crdoc["content"]

    def test_marker_alone_on_its_line_is_dropped(self):
        for index, marker in self.MARKERS.items():
            with self.subTest(marker=marker):
                self.assertEqual(self.lines[index], marker)
                without = self.lines[:index] + self.lines[index + 1 :]
                trailing = list(self.lines)
                trailing[index] = marker + "  "
                self.assertEqual(self.content(self.lines), self.content(without))
                self.assertEqual(self.content(trailing), self.content(without))

    def test_words_after_a_marker_are_kept(self):
        # GovInfo's 1995 text sets some page markers at the start of a line
        # of prose: "[[Page H2736]] flagrant case, the judge has the ...".
        for index, marker in self.MARKERS.items():
            with self.subTest(marker=marker):
                words, marked = list(self.lines), list(self.lines)
                words[index] = " the words after the marker"
                marked[index] = marker + words[index]
                content = self.content(marked)
                self.assertEqual(content, self.content(words))
                self.assertEqual(
                    sum(words[index] in i["text"].split("\n") for i in content), 1
                )


class testAccessIdIndex(unittest.TestCase):
    """A granule's MODS record is looked up in an index built once per MODS."""

    def setUp(self):
        self.crdir = day()

    def test_index_holds_the_tag_find_returns(self):
        tags = self.crdir.mods.find_all("accessid")
        ids = {t.string for t in tags} - {None}
        self.assertEqual(set(self.crdir.access_ids), ids)
        for tag in (tags[0], tags[1], tags[len(tags) // 2], tags[-1]):
            with self.subTest(access_id=tag.string):
                self.assertIs(
                    self.crdir.access_ids[tag.string],
                    self.crdir.mods.find("accessid", string=tag.string),
                )

    def test_granule_absent_from_the_mods(self):
        with self.assertRaisesRegex(RuntimeError, "doesn't have accessid tag"):
            cr.ParseCRFile(granule("CREC-2005-07-20-pt1-Pgnull-2"), self.crdir)
