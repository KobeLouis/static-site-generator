import unittest
from block_markdown import BlockType, markdown_to_blocks, block_to_block_type

class TestBlockMarkdown(unittest.TestCase):
    # Test cases for markdown_to_blocks function
    def test_block_markdown_heading(self):
        markdown = """# Heading 1

## Heading 2

### Heading 3"""
        expected = [
            "# Heading 1",
            "## Heading 2",
            "### Heading 3"
        ]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_block_markdown_paragraphs(self):
        markdown = """This is a paragraph.
And this is another paragraph."""
        expected = [
            "This is a paragraph.\nAnd this is another paragraph."
        ]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_block_markdown_list(self):
        markdown = """- Item 1
- Item 2
- Item 3"""
        expected = [
            "- Item 1\n- Item 2\n- Item 3"
        ]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_block_markdown_mixed(self):
        markdown = """# Heading block

## Another heading

This is a paragraph.

- List item 1
- List item 2"""
        expected = [
            "# Heading block",
            "## Another heading",
            "This is a paragraph.",
            "- List item 1\n- List item 2"
        ]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_block_markdown_empty_lines(self):
        markdown = """# Heading 1

## Heading 2

### Heading 3"""
        expected = [
            "# Heading 1",
            "## Heading 2",
            "### Heading 3"
        ]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    # Test block_to_block_type function
    def test_block_to_block_type(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("> Quote\n> another quote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("- List item\n- List item 2"), BlockType.ULIST)
        self.assertEqual(block_to_block_type("1. List item\n2. Another list item"), BlockType.OLIST)
        self.assertEqual(block_to_block_type("```\nCode block\n```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("Just a paragraph"), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()