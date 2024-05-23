import os
import shutil

from copy_directory import (
    copy_directory_recursive,
)

from generate_page import (
    generate_pages_recursive,
)

dir_path_public: str = "./public/"
dir_path_static: str = "./static/"
dir_path_content: str = "./content/"
path_template: str = "./template.html"


def main():
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)
    
    copy_directory_recursive(dir_path_static, dir_path_public)
    generate_pages_recursive(dir_path_content, path_template, dir_path_public)
    

main()
