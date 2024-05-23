import re

from textnode import (
    TextNode,
    type_text,
    type_bold,
    type_italic,
    type_code,
    type_link,
    type_image,
)


def split_nodes_delimiter_single(
        old_nodes: list[TextNode],
        delimiter: str, type_node: str) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != type_text:
            new_nodes.append(node)
            continue

        sections = node.text.split(delimiter)
        len_sections = len(sections)
        if len_sections % 2 == 0:
            raise ValueError(f"split_nodes_delimiter_single(): unenclosed markdown text: {sections}")
        
        sub_nodes: list[TextNode] = []
        for i in range(len_sections):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                sub_nodes.append(TextNode(sections[i], type_text))
            else:
                sub_nodes.append(TextNode(sections[i], type_node))
        new_nodes.extend(sub_nodes)
    return new_nodes


def extract_markdown_links(markdown: str) -> list[tuple[str, str]]:
    pattern: str =  r"\[(.*?)\]\((.*?)\)"
    return re.findall(pattern, markdown)


def extract_markdown_images(markdown: str) -> list[tuple[str, str]]:
    pattern = r"!\[(.*?)\]\((.*?)\)"
    return re.findall(pattern, markdown)


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != type_text:
            new_nodes.append(node)
            continue
        
        text: str = node.text
        links: list[tuple[str, str]] = extract_markdown_links(text)
        if len(links) == 0:
            new_nodes.append(node)
            continue
        
        link: tuple[str, str]
        for link in links:
            sections = text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError(f"split_nodes_link(): unenclosed markdown text: {sections}")
            
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], type_text))
            new_nodes.append(TextNode(link[0], type_link, link[1]))
            text = sections[1]
        if text != "":
            new_nodes.append(TextNode(text, type_text))
    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != type_text:
            new_nodes.append(node)
            continue
        
        text: str = node.text
        images: list[tuple[str, str]] = extract_markdown_images(text)
        if len(images) == 0:
            new_nodes.append(node)
            continue
        
        image: tuple[str, str]
        for image in images:
            sections = text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError(f"split_nodes_image(): unenclosed markdown text: {sections}")
            
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], type_text))
            new_nodes.append(TextNode(image[0], type_image, image[1]))
            text = sections[1]
        if text != "":
            new_nodes.append(TextNode(text, type_text))
    return new_nodes


def text_to_textnodes(text : str) -> list[TextNode]:
    list_nodes : list[TextNode] = [TextNode(text, type_text)]
    list_nodes = split_nodes_delimiter_single(list_nodes, "**", type_bold)
    list_nodes = split_nodes_delimiter_single(list_nodes, "*", type_italic)
    list_nodes = split_nodes_delimiter_single(list_nodes, "`", type_code)
    list_nodes = split_nodes_image(list_nodes)
    list_nodes = split_nodes_link(list_nodes)
    return list_nodes
