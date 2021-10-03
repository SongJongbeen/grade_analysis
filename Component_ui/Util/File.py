import os


def create_folder(path, reference_name, text):
    folder_name = path + '/' + text
    if os.path.exists(folder_name):
        return 1
    try:
        os.mkdir(folder_name)
    except:
        return 2
    return folder_name


def select_exam_folder():
    path = './data'
    mtime = lambda f: -os.stat(os.path.join(path, f)).st_mtime
    sorted_exam_folders = [dir for dir in sorted(os.listdir(path), key=mtime) if dir != '.DS_Store']
    return sorted_exam_folders
    # for idx in range(len(sorted_exam_folders)):
    #     print(str(idx + 1) + '.', sorted_exam_folders[idx])
    # # 채점할 모의고사 이름 받기
    # selected_idx = int(input('몇번째 모의고사를 선택하시겠습니까? '))
    # selected_name = sorted_exam_folders[selected_idx - 1]
    # # 해당 모의고사 경로 return
    # directory_path = './data/' + selected_name
    # return directory_path


def open_file(path, type="excel"):

    if os.name == 'nt':
        if type is 'directory':
            os.startfile(path)
        elif type is 'excel':
            os.system(f'start excel "{path}"')

    elif os.name == 'posix':
        os.system(f'open "{path}"')