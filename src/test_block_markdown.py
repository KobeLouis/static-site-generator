import unittest
from block_markdown import BlockType, markdown_to_blocks, block_to_block_type, markdown_to_html_node

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

    # Test markdown_to_html_node function
    def test_markdown_to_html_node_paragraph(self):
        md = "This is a paragraph."
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><p>This is a paragraph.</p></div>")

    def test_markdown_to_html_node_heading(self):
        md = "# Heading"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h1>Heading</h1></div>")

    def test_markdown_to_html_node_quote(self):
        md = "> This is a quote."
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><blockquote>This is a quote.</blockquote></div>")

    def test_markdown_to_html_node_unordered_list(self):
        md = "- Item 1\n- Item 2\n- Item 3"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul></div>")

    def test_markdown_to_html_node_list_with_italics(self):
        md = "- _Item 1_\n- _Item 2_\n- _Item 3_"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ul><li><i>Item 1</i></li><li><i>Item 2</i></li><li><i>Item 3</i></li></ul></div>")


    def test_markdown_to_html_node_ordered_list(self):
        md = "1. Item 1\n2. Item 2\n3. Item 3"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ol><li>Item 1</li><li>Item 2</li><li>Item 3</li></ol></div>")

    def test_markdown_to_html_node_code_block(self):
        md = "```\nCode block\n```"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><pre><code>Code block\n</code></pre></div>")

    def test_markdown_to_html_node_mixed_multi_line(self):
        md = """# Heading

This is a paragraph.

- List item 1
- List item 2

```
Code block
```"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h1>Heading</h1><p>This is a paragraph.</p><ul><li>List item 1</li><li>List item 2</li></ul><pre><code>Code block\n</code></pre></div>")

if __name__ == "__main__":
    unittest.main()