import unittest

from textnode import (
    TextNode,
)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a text node", "text")
        node2 = TextNode("This is a text node", "text")
        self.assertEqual(node1, node2)

    def test_eq_url(self):
        node1 = TextNode("Link to the firefox browser", "link", "https://www.mozilla.org/firefox")
        node2 = TextNode("Link to the firefox browser", "link", "https://www.mozilla.org/firefox")
        self.assertEqual(node1, node2)
    
    def test_not_eq_text(self):
        node1 = TextNode("This is one text node", "text")
        node2 = TextNode("This is another text node", "text")
        self.assertNotEqual(node1, node2)

    def test_not_eq_type(self):
        node1 = TextNode("This is text", "bold")
        node2 = TextNode("This is text", "italic")
        self.assertNotEqual(node1, node2)
    
    def test_not_eq_url(self):
        node1 = TextNode("This has a url", "link", "https://www.archive.org")
        node2 = TextNode("This has a url", "link", "https://www.wikipedia.org")
        self.assertNotEqual(node1, node2)
    
    def test_repr(self):
        node = TextNode("This links to the python website", "link", "https://www.python.org")
        self.assertEqual(repr(node), "TextNode(This links to the python website, link, https://www.python.org)")


if __name__ == "__main__":
    unittest.main()
