import os

def solve_dir(dir_path):

    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

    return os.path.abspath(dir_path)

def solve_path(path, parent=None):

    if parent is not None:
        parent = solve_dir(parent)

        path = os.path.join(parent, path)

    return os.path.abspath(path)


def clean_extension(extension):

    extension = extension.lower()
    if not extension.startswith('.'):
        extension = '.' + extension
    
    return extension

def files_by_extension(folder, extension):

    folder = solve_path(folder)
    extension = clean_extension(extension)

    files = [os.path.abspath(os.path.join(folder, f))
        for f in os.listdir(folder)
        if f.lower().endswith(extension)]

    return files