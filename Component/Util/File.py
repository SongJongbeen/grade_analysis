import os


def open_file(path):
    print(path)
    if os.name == 'nt':
        os.system("start " + path)
    elif os.name == 'posix':
        os.system("open " + path)
