import unittest

from htmlnode import (
    HTMLNode,
    LeafNode,
    ParentNode
)

class TestHTMLNode(unittest.TestCase):
    def test_err_to_html(self):
        node = HTMLNode()
        self.assertRaises(NotImplementedError, node.to_html)
    
    def test_props_to_html(self):
        node = HTMLNode("p", "This is some text", None)
        self.assertEqual(node.props_to_html(), "")
        node.props = {"href": "style.css"}
        self.assertEqual(node.props_to_html(), " href=\"style.css\"")
        node.props["type"] = "class1"
        self.assertEqual(node.props_to_html(), " href=\"style.css\" type=\"class1\"")

    def test_repr(self):
        node = HTMLNode()
        self.assertEqual(repr(node), "HTMLNode(None, None, None, None)")
        node.tag = "p"
        node.value = "Some text"
        node.children = [LeafNode("p", "Txt"), LeafNode("p", "Abc", {"type": "class"})]
        node.props = {"id": "display"}
        self.assertEqual(repr(node), "HTMLNode(p, Some text, [LeafNode(p, Txt, None), LeafNode(p, Abc, {'type': 'class'})], {'id': 'display'})")

    def test_to_html_no_children(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )

if __name__ == "__main__":
    unittest.main()
