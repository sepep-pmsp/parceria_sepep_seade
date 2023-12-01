import os


def solve_dir(folder):

    if not os.path.exists(folder):
        os.mkdir(folder)
    
    return os.path.abspath(folder)

def solve_path(path, parent = None):

    if parent:
        parent = solve_dir(parent)
        path = os.path.join(parent, path)

    return os.path.abspath(path)

def check_file_exists(file, parent=None):

    if parent:
        file = solve_path(file, parent)

    return os.path.exists(file) and os.path.isfile(file)

def check_dir_exists(folder, parent=None):

    if parent:
        folder = solve_path(folder, parent)

    return os.path.exists(folder)

def solve_path_relative(path, parent):

    if not os.path.exists(parent):
        os.mkdir(parent)

    return os.path.join(parent, path)

def list_files(folder, extension=None):

    folder = solve_path(folder)
    files = [os.path.join(folder, file) for file in os.listdir(folder)]
    
    if extension is not None:
        return [f for f in files if f.endswith(extension)]
    
    return files

def list_files_recursive(root_folder, extension):

    root_folder = solve_path(root_folder)
    files = []
    for root, folder, folder_files in os.walk(root_folder):
        root_files = [
            solve_path(f, parent=root)
            for f in folder_files 
            if f.lower().endswith(extension)
            ]
        files.extend(root_files)
    return files

def delete_existing_files(folder, extension=None):

    folder = solve_dir(folder)

    files = list_files(folder, extension)
    if files:
        print('Found existing files')
    for file in files:
        os.remove(file)
        print(f'File {file} deleted.')

