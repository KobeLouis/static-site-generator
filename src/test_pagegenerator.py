import unittest
from pagegenerator import extract_title

class TestPageGenerator(unittest.TestCase):
    def test_extract_title_valid(self):
        markdown = "# This is a title\n\nThis is some content."
        expected_title = "This is a title"
        self.assertEqual(extract_title(markdown), expected_title)

    def test_extract_title_no_title(self):
        markdown = "This is some content without a title."
        with self.assertRaises(ValueError):
            extract_title(markdown)

    def test_extract_title_multiple_titles(self):
        markdown = "# Title 1\n\n# Title 2\n\nThis is some content."
        expected_title = "Title 1"
        self.assertEqual(extract_title(markdown), expected_title)

    def test_extract_title_empty_title(self):
        markdown = "# \n\nThis is some content."
        expected_title = ""
        self.assertEqual(extract_title(markdown), expected_title)
        
    def test_extract_title_title_long(self):
        markdown = "# This is a very long title that spans multiple lines\n\nThis is some content."
        expected_title = "This is a very long title that spans multiple lines"
        self.assertEqual(extract_title(markdown), expected_title)