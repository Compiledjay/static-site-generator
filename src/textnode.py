from htmlnode import (
    LeafNode,
)


type_text   : str   = "text"
type_bold   : str   = "bold"
type_italic : str   = "italic"
type_code   : str   = "code"
type_link   : str   = "link"
type_image  : str   = "image"


class TextNode():
    def __init__(self, text: str, text_type: str, url: str = None) -> None:
        self.text       = text
        self.text_type  = text_type
        self.url        = url
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TextNode):
            return NotImplemented
        
        return (
            self.text           == other.text
            and self.text_type  == other.text_type
            and self.url        == other.url
        )
    
    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    if text_node.text_type == type_text:
        return LeafNode(None, text_node.text)
    if text_node.text_type == type_bold:
        return LeafNode("b", text_node.text)
    if text_node.text_type == type_italic:
        return LeafNode("i", text_node.text)
    if text_node.text_type == type_code:
        return LeafNode("code", text_node.text)
    if text_node.text_type == type_link:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == type_image:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    raise ValueError(f"Invalid text type: {text_node.text_type}")