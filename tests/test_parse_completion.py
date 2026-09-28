import unittest
from unittest.mock import patch

from congressionalrecord.govinfo.cr_parser import ParseCRDir, ParseCRFile


class TestParseCompletion(unittest.TestCase):
    def setUp(self):
        self.folder = "tests/test_files/CREC-2005-07-20"
        self.path = self.folder + "/html/CREC-2005-07-20-pt1-PgH6115-2.htm"

    def parse(self):
        return ParseCRFile(self.path, ParseCRDir(self.folder))

    def test_complete(self):
        result = self.parse()
        self.assertEqual(result.crdoc["parse_status"], "complete")
        self.assertNotIn("parse_error", result.crdoc)
        self.assertFalse(result.lines_remaining)
        self.assertGreater(len(result.crdoc["content"]), 0)

    def test_failure_is_not_successful_empty_content(self):
        with patch(
            "congressionalrecord.govinfo.cr_parser.crItem",
            side_effect=ValueError("bad item"),
        ):
            result = self.parse()
        self.assertEqual(result.crdoc["parse_status"], "partial")
        self.assertEqual(result.crdoc["parse_error"]["type"], "ValueError")
        self.assertEqual(result.crdoc["content"], [])
        self.assertTrue(result.lines_remaining)

    def test_failure_preserves_prior_items_and_failure_location(self):
        from congressionalrecord.govinfo.cr_parser import crItem

        calls = 0

        def fail_second(parser):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise ValueError("second item refused")
            return crItem(parser)

        with patch(
            "congressionalrecord.govinfo.cr_parser.crItem", side_effect=fail_second
        ):
            result = self.parse()
        self.assertEqual(result.crdoc["parse_status"], "partial")
        self.assertEqual(len(result.crdoc["content"]), 1)
        self.assertEqual(result.crdoc["parse_error"]["line"], result.cur_line)
