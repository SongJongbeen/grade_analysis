import os

def create_folder(path, reference_name):
    folder_name = path + '/' + input(f'{reference_name}명을 입력: ')

    if os.path.exists(folder_name):
        print('이미 존재하는 폴더입니다.')
        return False
    try:
        os.mkdir(folder_name)
    except:
        print('폴더명으로 쓸 수 있는 형식으로 입력해 주세요.')
        folder_name = create_folder(path, reference_name)
    return folder_name


def select_exam_folder():
    path = './data'
    mtime = lambda f: -os.stat(os.path.join(path, f)).st_mtime
    sorted_exam_folders = list(sorted(os.listdir(path), key=mtime))

    for idx in range(len(sorted_exam_folders)):
        print(str(idx + 1) + '.', sorted_exam_folders[idx])
    # 채점할 모의고사 이름 받기
    selected_idx = int(input('몇번째 모의고사를 선택하시겠습니까? '))
    selected_name = sorted_exam_folders[selected_idx - 1]
    # 해당 모의고사 경로 return
    directory_path = './data/' + selected_name
    return directory_path


def open_file(path):
    print(path)
    if os.name == 'nt':
        os.system(f'start excel "{path}"')
    elif os.name == 'posix':
        os.system(f'open "{path}"')
