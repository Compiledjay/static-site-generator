import os
import shutil


def copy_directory_recursive(src_path: str, dest_path: str) -> None:
    """Copies all files from the 'src_path' to the 'dest_path' directory.
    
    Arguments:
    src_path : directory path to all non-html files
    dest_path : directory path to copy src_path files to
        Must be same directory where .html files rendered by server.py are stored
        main.sh/main.py default: public/
    """
    if not os.path.exists(src_path):
        raise FileExistsError(f"copy_directory_recursive(): src_path invalid: {src_path}")
    if not os.path.exists(dest_path):
        os.mkdir(dest_path)
    
    for path in os.listdir(src_path):
        src_filepath: str = os.path.join(src_path, path)
        dest_filepath: str = os.path.join(dest_path, path)
        if not os.path.isfile(src_filepath):
            copy_directory_recursive(src_filepath, dest_filepath)
        else:
            shutil.copy(src_filepath, dest_filepath)