import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    # Test cases for HTMLNode
    def test_default_values(self):
        node = HTMLNode()
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

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
        self.assertEqual(node.props_to_html(), ' class="my-class" id="my-id"')

    def test_repr(self):
        node = HTMLNode(tag="div", value="Hello", children=[HTMLNode(tag="span")], props={"class": "my-class"})
        expected_repr = "HTMLNode(tag='div', value='Hello', children=[HTMLNode(tag='span', value='None', children=None, props=None)], props={'class': 'my-class'})"
        self.assertEqual(repr(node), expected_repr)

    # Test cases for LeafNode
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

    def test_leaf_to_html_with_props(self):
        node = LeafNode("p", "This is a paragraph.", props={"class": "text"})
        self.assertEqual(node.to_html(), '<p class="text">This is a paragraph.</p>')

    def test_leaf_repr(self):
        node = LeafNode("p", "This is a paragraph.", props={"class": "text"})
        self.assertEqual(repr(node), "LeafNode(tag='p', value='This is a paragraph.', props={'class': 'text'})")

    # Test cases for ParentNode
    def test_parent_to_html_with_children(self):
        node = ParentNode("div", [
            LeafNode("p", "Hello"),
            LeafNode("span", "World")
        ])
        self.assertEqual(node.to_html(), "<div><p>Hello</p><span>World</span></div>")

    def test_parent_to_html_without_children(self):
        node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_parent_to_html_without_tag(self):
        node = ParentNode(None, [LeafNode("p", "Hello")])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_parent_to_html_with_props(self):
        node = ParentNode("div", [
            LeafNode("p", "Hello")
        ], props={"class": "container"})
        self.assertEqual(node.to_html(), '<div class="container"><p>Hello</p></div>')

    def test_parent_with_multiple_props(self):
        node = ParentNode("div", [
            LeafNode("p", "Hello")
        ], props={"class": "container", "id": "main"})
        self.assertEqual(node.to_html(), '<div class="container" id="main"><p>Hello</p></div>')

    def test_parent_to_html_with_grandchildren(self):
        node = ParentNode("div", [
            ParentNode("p", [
                LeafNode("span", "Hello")
            ])
        ])
        self.assertEqual(node.to_html(), "<div><p><span>Hello</span></p></div>")

    def test_parent_to_html_with_child_prop(self):
        node = ParentNode("div", [
            LeafNode("p", "Hello", props={"class": "text"})
        ])
        self.assertEqual(node.to_html(), '<div><p class="text">Hello</p></div>')

    def test_parent_to_html_with_many_children(self):
        node = ParentNode("ul", [
            LeafNode("li", "Item 1"),
            LeafNode("li", "Item 2"),
            LeafNode("li", "Item 3")
        ])
        self.assertEqual(node.to_html(), "<ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul>")

    def test_parent_to_html_heading(self):
        node = ParentNode("h1", [
            LeafNode(None, "This is a heading")
        ])
        self.assertEqual(node.to_html(), "<h1>This is a heading</h1>")

if __name__ == "__main__":
    unittest.main()