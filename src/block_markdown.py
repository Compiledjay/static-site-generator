from textnode import (
    TextNode,
    text_node_to_html_node,
)

from htmlnode import (
    LeafNode,
    ParentNode,
)

from inline_markdown import (
    text_to_textnodes,
)

block_paragraph:      str = "paragraph"
block_heading:        str = "heading"
block_code:           str = "code"
block_quote:          str = "quote"
block_unordered_list: str = "unordered_list"
block_ordered_list:   str = "ordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks: list[str] = markdown.split("\n\n")
    valid_blocks: list[str] = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip(" \n")
        valid_blocks.append(block)
    return valid_blocks


def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks: list[str] = markdown_to_blocks(markdown)
    child_nodes: list[ParentNode] = []
    for block in blocks:
        child_nodes.append(block_to_html_node(block))
    return ParentNode("div", child_nodes, None)


def block_to_html_node(block: str) -> ParentNode:
    block_type: str = block_to_block_type(block)
    if block_type == block_paragraph:
        return paragraph_to_html_node(block)
    elif block_type == block_heading:
        return heading_to_html_node(block)
    elif block_type == block_code:
        return code_to_html_node(block)
    elif block_type == block_quote:
        return quote_to_html_node(block)
    elif block_type == block_unordered_list:
        return unordered_list_to_html_node(block)
    elif block_type == block_ordered_list:
        return ordered_list_to_html_node(block)
    raise ValueError(f"block_to_html_node(): unknown block_type: {block_type}")


def block_to_block_type(block: str) -> str:
    if block.startswith('#'):
        for i in range(0, 6):
            if block[i] != '#':
                return block_heading
        return block_paragraph
    
    len_block = len(block)
    if len_block >= 6 and block.startswith("```") and block.endswith("```"):
        return block_code
    
    lines: list[str] = block.split('\n')
    if block.startswith('>'):
        for line in lines:
            if not line.startswith('>'):
                return block_paragraph
        return block_quote
    
    if block.startswith("* ") or block.startswith("- "):
        for line in lines:
            if not line.startswith("* ") and not block.startswith("- "):
                return block_paragraph
        return block_unordered_list
    
    if block.startswith("1. "):
        i: int = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return block_paragraph
            i += 1
        return block_ordered_list
    
    return block_paragraph


def paragraph_to_html_node(paragraph: str) -> ParentNode:
    lines: list[str] = paragraph.split('\n')
    text: str = ' '.join(lines)
    old_nodes: list[TextNode] = text_to_textnodes(text)
    child_nodes: list[LeafNode] = []
    for node in old_nodes:
        child_nodes.append(text_node_to_html_node(node))
    return ParentNode("p", child_nodes)


def heading_to_html_node(heading: str) -> ParentNode:
    heading_size: int = 0
    for char in heading:
        if char != '#':
            break
        heading_size += 1
    
    if heading_size + 1 > len(heading):
        raise ValueError(f"heading_to_html_node(): heading size not permitted: {heading_size}, text: {heading}")
    
    text = heading[heading_size + 1: ]
    old_nodes: list[TextNode] = text_to_textnodes(text)
    child_nodes: list[LeafNode] = []

    node: TextNode
    for node in old_nodes:
        child_nodes.append(text_node_to_html_node(node))
    
    return ParentNode(f"h{heading_size}", child_nodes)


def code_to_html_node(code_block: str) -> ParentNode:
    if (len(code_block) <= 6 
            or not code_block.startswith("```")
            or not code_block.endswith("```")):
        raise ValueError(f"code_to_html_node(): invalid code: {code_block}")
    
    code_nodes: list[ParentNode] = []
    child_nodes: list[TextNode] = []
    text_nodes: list[TextNode] = text_to_textnodes(code_block)
    for node in text_nodes:
        child_nodes.append(text_node_to_html_node(node))
    code_nodes.append(ParentNode("code", child_nodes))
        
    return ParentNode("pre", code_nodes)


def quote_to_html_node(quote_block: str) -> ParentNode:
    lines = quote_block.split('\n')
    text: list[str] = []
    for line in lines:
        if not line.startswith('>'):
            raise ValueError(f"quote_to_html_node(): invalid line for quotes: {line}")
        text.append(line.lstrip('>').strip())
    
    quotes = ' '.join(text)
    quote_nodes: list[TextNode] = text_to_textnodes(quotes)
    child_nodes: list[LeafNode] = []
    
    node: TextNode
    for node in quote_nodes:
        child_nodes.append(text_node_to_html_node(node))
    
    return ParentNode("blockquote", child_nodes)


def unordered_list_to_html_node(unordered_list: str) -> ParentNode:
    lines = unordered_list.split('\n')
    list_nodes: list[ParentNode] = []
    for line in lines:
        if len(line) <= 2:
            raise IndexError(f"unordered_list_to_html_node(): empty or invalid ulist element: {line}")
        
        text = line[2:]
        text_nodes: list[TextNode] = text_to_textnodes(text)
        child_nodes: list[LeafNode] = []

        node: TextNode
        for node in text_nodes:
            child_nodes.append(text_node_to_html_node(node))
        
        list_nodes.append(ParentNode("li", child_nodes))
    
    return ParentNode("ul", list_nodes)


def ordered_list_to_html_node(ordered_list: str) -> ParentNode:
    lines = ordered_list.split('\n')
    list_nodes: list[ParentNode] = []
    for line in lines:
        if len(line) <= 3:
            raise IndexError(f"ordered_list_to_html_node(): empty or invalid olist element: {line}")
        
        text = line[3:]
        text_nodes: list[TextNode] = text_to_textnodes(text)
        child_nodes: list[LeafNode] = []

        node: TextNode
        for node in text_nodes:
            child_nodes.append(text_node_to_html_node(node))
        
        list_nodes.append(ParentNode("li", child_nodes))
    
    return ParentNode("ol", list_nodes)
