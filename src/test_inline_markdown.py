import unittest
from inline_markdown import (
    split_nodes_delimiter,
    split_nodes_images,
    split_nodes_links,
    text_to_textnodes,
    extract_markdown_links,
    extract_markdown_images,
)
from textnode import TextNode, TextType

class TestInlineMarkdown(unittest.TestCase):

    # Test cases for split_nodes_delimiter function
    def test_split_nodes_delimiter_bold(self):
        old_nodes = [TextNode("This is **bold** text", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_delimiter_unmatched(self):
        old_nodes = [TextNode("This is **bold text", TextType.TEXT)]
        with self.assertRaises(ValueError):
            split_nodes_delimiter(old_nodes, "**", TextType.BOLD)

    def test_split_nodes_delimiter_no_delimiter(self):
        old_nodes = [TextNode("This is plain text", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        expected_nodes = [TextNode("This is plain text", TextType.TEXT)]
        self.assertEqual(new_nodes, expected_nodes)
    
    def test_split_nodes_delimiter_multiple(self):
        old_nodes = [TextNode("**Bold** and **another bold**", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        expected_nodes = [
            TextNode("Bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("another bold", TextType.BOLD)
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_delimiter_multiple_nodes(self):
        old_nodes = [
            TextNode("This is **bold** text", TextType.TEXT),
            TextNode("And this is **another bold**", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
            TextNode("And this is ", TextType.TEXT),
            TextNode("another bold", TextType.BOLD)
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_delimiter_different_delimiters(self):
        old_nodes = [TextNode("This is *italic* and `code`", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, "*", TextType.ITALIC)
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and `code`", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_delimiter_delimiter_in_beginning(self):
        old_nodes = [TextNode("**Bold** text", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        expected_nodes = [
            TextNode("Bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_delimiter_delimiter_in_end(self):
        old_nodes = [TextNode("This is **bold**", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD)
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_delimiter_empty_text(self):
        old_nodes = [TextNode("", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        expected_nodes = []
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_delimiter_code(self):
        old_nodes = [TextNode("This is `code` text", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, "`", TextType.CODE)
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected_nodes)

    # Test cases for extract_markdown_images function
    def test_extract_markdown_images(self):
        text = "Here is an image: ![Alt text](image.jpg)"
        images = extract_markdown_images(text)
        expected_images = [("Alt text", "image.jpg")]
        self.assertEqual(images, expected_images)

    def test_extract_markdown_images_multiple(self):
        text = "Image 1: ![Alt1](image1.jpg) and Image 2: ![Alt2](image2.png)"
        images = extract_markdown_images(text)
        expected_images = [("Alt1", "image1.jpg"), ("Alt2", "image2.png")]
        self.assertEqual(images, expected_images)
    
    def test_extract_markdown_images_no_images(self):
        text = "This is a text without images"
        images = extract_markdown_images(text)
        expected_images = []
        self.assertEqual(images, expected_images)
    
    def test_extract_markdown_images_begins_with_image(self):
        text = "![Alt text](image.jpg) is at the beginning"
        images = extract_markdown_images(text)
        expected_images = [("Alt text", "image.jpg")]
        self.assertEqual(images, expected_images)

    def test_extract_markdown_images_ends_with_image(self):
        text = "This is a text ending with an image: ![Alt text](image.jpg)"
        images = extract_markdown_images(text)
        expected_images = [("Alt text", "image.jpg")]
        self.assertEqual(images, expected_images)

    # Test cases for extract_markdown_links function
    def test_extract_markdown_links(self):
        text = "Here is a link: [Link text](https://example.com)"
        links = extract_markdown_links(text)
        expected_links = [("Link text", "https://example.com")]
        self.assertEqual(links, expected_links)

    def test_extract_markdown_links_multiple(self):
        text = "Link 1: [Link1](https://example1.com) and Link 2: [Link2](https://example2.com)"
        links = extract_markdown_links(text)
        expected_links = [("Link1", "https://example1.com"), ("Link2", "https://example2.com")]
        self.assertEqual(links, expected_links)

    def test_extract_markdown_links_no_links(self):
        text = "This is a text without links"
        links = extract_markdown_links(text)
        expected_links = []
        self.assertEqual(links, expected_links)

    def test_extract_markdown_links_begins_with_link(self):
        text = "[Link text](https://example.com) is at the beginning"
        links = extract_markdown_links(text)
        expected_links = [("Link text", "https://example.com")]
        self.assertEqual(links, expected_links)

    def test_extract_markdown_links_ends_with_link(self):
        text = "This is a link at the end: [Link text](https://example.com)"
        links = extract_markdown_links(text)
        expected_links = [("Link text", "https://example.com")]
        self.assertEqual(links, expected_links)

    # Test cases for split_nodes_images
    def test_split_nodes_images(self):
        old_nodes = [TextNode("Here is an image: ![Alt text](image.jpg)", TextType.TEXT)]
        new_nodes = split_nodes_images(old_nodes)
        expected_nodes = [
            TextNode("Here is an image: ", TextType.TEXT),
            TextNode("Alt text", TextType.IMAGE, url="image.jpg")
        ]
        self.assertEqual(new_nodes, expected_nodes)
    
    def test_split_nodes_images_multiple(self):
        old_nodes = [TextNode("Image 1: ![Alt1](image1.jpg) and Image 2: ![Alt2](image2.png)", TextType.TEXT)]
        new_nodes = split_nodes_images(old_nodes)
        expected_nodes = [
            TextNode("Image 1: ", TextType.TEXT),
            TextNode("Alt1", TextType.IMAGE, url="image1.jpg"),
            TextNode(" and Image 2: ", TextType.TEXT),
            TextNode("Alt2", TextType.IMAGE, url="image2.png")
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_images_no_images(self):
        old_nodes = [TextNode("This is a text without images", TextType.TEXT)]
        new_nodes = split_nodes_images(old_nodes)
        expected_nodes = [TextNode("This is a text without images", TextType.TEXT)]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_images_begins_with_image(self):
        old_nodes = [TextNode("![Alt text](image.jpg) is at the beginning", TextType.TEXT)]
        new_nodes = split_nodes_images(old_nodes)
        expected_nodes = [
            TextNode("Alt text", TextType.IMAGE, url="image.jpg"),
            TextNode(" is at the beginning", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_images_ends_with_image(self):
        old_nodes = [TextNode("This is a text ending with an image: ![Alt text](image.jpg)", TextType.TEXT)]
        new_nodes = split_nodes_images(old_nodes)
        expected_nodes = [
            TextNode("This is a text ending with an image: ", TextType.TEXT),
            TextNode("Alt text", TextType.IMAGE, url="image.jpg")
        ]
        self.assertEqual(new_nodes, expected_nodes)

    # Test cases for split_nodes_links
    def test_split_nodes_links(self):
        old_nodes = [TextNode("Here is a link: [Link text](https://example.com)", TextType.TEXT)]
        new_nodes = split_nodes_links(old_nodes)
        expected_nodes = [
            TextNode("Here is a link: ", TextType.TEXT),
            TextNode("Link text", TextType.LINK, url="https://example.com")
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_links_multiple(self):
        old_nodes = [TextNode("Link 1: [Link1](https://example1.com) and Link 2: [Link2](https://example2.com)", TextType.TEXT)]
        new_nodes = split_nodes_links(old_nodes)
        expected_nodes = [
            TextNode("Link 1: ", TextType.TEXT),
            TextNode("Link1", TextType.LINK, url="https://example1.com"),
            TextNode(" and Link 2: ", TextType.TEXT),
            TextNode("Link2", TextType.LINK, url="https://example2.com")
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_links_no_links(self):
        old_nodes = [TextNode("This is a text without links", TextType.TEXT)]
        new_nodes = split_nodes_links(old_nodes)
        expected_nodes = [TextNode("This is a text without links", TextType.TEXT)]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_links_begins_with_link(self):
        old_nodes = [TextNode("[Link text](https://example.com) is at the beginning", TextType.TEXT)]
        new_nodes = split_nodes_links(old_nodes)
        expected_nodes = [
            TextNode("Link text", TextType.LINK, url="https://example.com"),
            TextNode(" is at the beginning", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_links_ends_with_link(self):
        old_nodes = [TextNode("This is a link at the end: [Link text](https://example.com)", TextType.TEXT)]
        new_nodes = split_nodes_links(old_nodes)
        expected_nodes = [
            TextNode("This is a link at the end: ", TextType.TEXT),
            TextNode("Link text", TextType.LINK, url="https://example.com")
        ]
        self.assertEqual(new_nodes, expected_nodes)

    # Test cases for text_to_textnodes
    def test_text_to_textnodes(self):
        text = "This is **bold** and *italic* and `code` text with a [link](https://example.com) and an image ![Alt](image.jpg)"
        text_nodes = text_to_textnodes(text)
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, url="https://example.com"),
            TextNode(" and an image ", TextType.TEXT),
            TextNode("Alt", TextType.IMAGE, url="image.jpg")
        ]
        self.assertEqual(text_nodes, expected_nodes)

    def test_text_to_textnodes_only_text(self):
        text = "This is plain text with no markdown."
        text_nodes = text_to_textnodes(text)
        expected_nodes = [TextNode("This is plain text with no markdown.", TextType.TEXT)]
        self.assertEqual(text_nodes, expected_nodes)

    def test_text_to_textnodes_only_markdown(self):
        text = "**Bold** *Italic* `Code` [Link](https://example.com) ![Alt](image.jpg)"
        text_nodes = text_to_textnodes(text)
        expected_nodes = [
            TextNode("Bold", TextType.BOLD),
            TextNode(" ", TextType.TEXT),
            TextNode("Italic", TextType.ITALIC),
            TextNode(" ", TextType.TEXT),
            TextNode("Code", TextType.CODE),
            TextNode(" ", TextType.TEXT),
            TextNode("Link", TextType.LINK, url="https://example.com"),
            TextNode(" ", TextType.TEXT),
            TextNode("Alt", TextType.IMAGE, url="image.jpg")
        ]
        self.assertEqual(text_nodes, expected_nodes)

    def test_text_to_textnodes_empty_string(self):
        text = ""
        text_nodes = text_to_textnodes(text)
        expected_nodes = []
        self.assertEqual(text_nodes, expected_nodes)


if __name__ == '__main__':
    unittest.main()