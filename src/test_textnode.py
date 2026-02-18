import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_init(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://example.com")
        self.assertEqual(node.text, "This is a text node")
        self.assertEqual(node.text_type, TextType.BOLD)
        self.assertEqual(node.url, "https://example.com")

    def test_eq_with_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://example.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://example.com")
        self.assertEqual(node, node2)

    def test_eq_without_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_dif_text_type(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://example.com")
        node2 = TextNode("This is a text node", TextType.ITALIC, "https://example.com")
        self.assertNotEqual(node, node2)

    def test_dif_text(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://example.com")
        node2 = TextNode("This is a different text node", TextType.BOLD, "https://example.com")
        self.assertNotEqual(node, node2)

    def test_dif_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://example.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://different-example.com")
        self.assertNotEqual(node, node2)

    def test_one_node_without_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://example.com")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://example.com")
        self.assertEqual(repr(node), "TextNode(This is a text node, bold, https://example.com)")

if __name__ == "__main__":
    unittest.main()