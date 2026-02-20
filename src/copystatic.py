import os
import shutil

def directory_copy(src: str, dst: str):
    """
    Copies a directory from the static directory and recursively copies all subdirectories to the public directory in this directory.
    
    Args:
        src (str): The source directory path.
    """
    if not os.path.exists(dst):
        os.mkdir(dst)

    for filename in os.listdir(src):
        from_path = os.path.join(src, filename)
        dest_path = os.path.join(dst, filename)
        print(f" * {from_path} -> {dest_path}")
        if os.path.isfile(from_path):
            shutil.copy(from_path, dest_path)
        else:
            directory_copy(from_path, dest_path)