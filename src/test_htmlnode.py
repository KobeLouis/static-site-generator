import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_default_values(self):
        node = HTMLNode()
        self.assertEqual(node.tag, "")
        self.assertEqual(node.value, "")
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {})

    def test_custom_values(self):
        node = HTMLNode(tag="div", value="Hello", children=[HTMLNode(tag="span")], props={"class": "my-class"})
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello")
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].tag, "span")
        self.assertEqual(node.props, {"class": "my-class"})
    
    def test_to_html(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_props_to_html_empty(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_with_props(self):
        node = HTMLNode(props={"class": "my-class", "id": "my-id"})
        self.assertEqual(node.props_to_html(), 'class="my-class" id="my-id"')

    def test_repr(self):
        node = HTMLNode(tag="div", value="Hello", children=[HTMLNode(tag="span")], props={"class": "my-class"})
        expected_repr = "HTMLNode(tag='div', value='Hello', children=[HTMLNode(tag='span', value='', children=[], props={})], props={'class': 'my-class'})"
        self.assertEqual(repr(node), expected_repr)

    def test_leaf_to_html_with_tag(self):
        node = LeafNode("p", "This is a paragraph.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph.</p>")

    def test_leaf_to_html_without_tag(self):
        node = LeafNode(None, "Just some text.")
        self.assertEqual(node.to_html(), "Just some text.")

    def test_leaf_to_html_with_none_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_repr(self):
        node = LeafNode("p", "This is a paragraph.", props={"class": "text"})
        self.assertEqual(repr(node), "LeafNode(tag='p', value='This is a paragraph.', props={'class': 'text'})")

if __name__ == "__main__":
    unittest.main()