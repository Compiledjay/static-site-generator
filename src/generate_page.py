import os
import pathlib

from htmlnode import (
    ParentNode,
)

from block_markdown import (
    markdown_to_html_node,
)


def extract_title(markdown: str) -> str:
    lines = markdown.split('\n')
    for line in lines:
        if line.startswith("# ") and len(line) > 2:
            return line[2:]
    raise ValueError("extract_title(): no h1 element in markdown")


def generate_page(file_from_path: pathlib.Path, template_path: pathlib.Path, dir_dest_path: pathlib.Path) -> None:
    if not os.path.exists(file_from_path):
        raise ValueError(f"generate_page(): dir_from_path is invalid: {file_from_path}")
    if not os.path.exists(template_path):
        raise ValueError(f"generate_page(): template_path is invalid: {template_path}")
    
    print(f"Generating page from {file_from_path} to {dir_dest_path} using {template_path}")

    markdown: str = ""
    with open(file_from_path, 'r') as markdown_file:
        markdown = markdown_file.read()

    html_node: ParentNode = markdown_to_html_node(markdown)
    title: str = extract_title(markdown)

    template: str = ""
    with open(template_path, 'r') as template_file:
        template = template_file.read()
        template = template.replace("{{ Title }}", title)
        template = template.replace("{{ Content }}", html_node.to_html())
    
    if not os.path.exists(dir_dest_path):
        os.makedirs(dir_dest_path)

    file_name = file_from_path.name.split('.')[0]
    with open(os.path.join(dir_dest_path, file_name + ".html"), 'w') as site_html:
        site_html.write(template)


def generate_pages_recursive(dir_path_content: str, template_path: str, dir_path_dest: str):
    """Generates the .html pages for the site using .md files.
        copies the file structure from the dir_path_content directory when converting files
    
    Arguments:
    dir_path_content : path to directory of .md files for conversion
        main.py default: content/
    template_path : path to .html template for the site
        main.py default: project root
    dir_path_dest : path to where generated .html files are stored
        must be in same directory with non-html files and where server.py looks for files
        main.sh/main.py default: public/
    """
    if not os.path.exists(template_path):
        raise ValueError(f"generate_pages_recursive(): template_path is invalid: {template_path}")

    for path in os.listdir(dir_path_content):
        full_path = os.path.join(dir_path_content, path)

        if not os.path.isfile(full_path):
            generate_pages_recursive(full_path, template_path, os.path.join(dir_path_dest, path))
        else:
            generate_page(pathlib.Path(full_path), pathlib.Path(template_path), pathlib.Path(dir_path_dest))