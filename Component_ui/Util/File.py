import os

from ..Error.Error import WrongFileNameError, FileExistsError


def create_folder(path, text):
    folder_name = path + '/' + text
    if os.path.exists(folder_name):
        raise FileExistsError(text)
    if '/' in text or '\\' in text:
        raise WrongFileNameError(text)

    os.mkdir(folder_name)

    return folder_name


def select_exam_folder():
    path = './data'
    mtime = lambda f: -os.stat(os.path.join(path, f)).st_mtime
    sorted_exam_folders = [dir for dir in sorted(os.listdir(path), key=mtime) if dir != '.DS_Store']
    return sorted_exam_folders


def open_file(path, type="excel"):

    if os.name == 'nt':
        if type is 'directory':
            os.startfile(path)
        elif type is 'excel':
            os.system(f'start excel "{path}"')

    elif os.name == 'posix':
        os.system(f'open "{path}"')