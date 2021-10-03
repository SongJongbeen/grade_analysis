import os

from ..Util.File import open_file, create_folder, select_exam_folder
from ..Util.Excel import worksheet_write, create_worksheet, save_excel_file


# 모의고사 폴더를 생성 후, 문제 정답 및 배점 정보가 초기화된 엑셀 파일 하나를 생성합니다.
def register_exam(text):
    exam_folder = create_folder('./data', text)
    exam_excel_path = exam_folder + f'{exam_folder.replace("./data", "")} 정답 및 배점.xlsx'
    if not os.path.exists(exam_excel_path):
        create_exam_excel(exam_folder)
    open_file(exam_excel_path)


def create_exam_excel(path):
    workbook, worksheet = create_worksheet('문항 정답 및 배점')

    worksheet_write(worksheet, 1, '문항', '정답', '배점')
    for question_number in range(2, 22):
        worksheet_write(worksheet, question_number, question_number - 1)

    return save_excel_file(workbook, path, f'{path.replace("./data", "")} 정답 및 배점')


# 모의고사 폴더를 선택하여 학생들의 제출 답안 엑셀 파일을 생성하고, 파일을 엽니다.
def register_students_submission(exam):
    exam_folder = "./data/" + exam
    submission_file = exam_folder + f'{exam_folder.replace("./data", "")} 학생 제출 답.xlsx'
    if not os.path.exists(submission_file):
        create_students_submission_excel(exam_folder)
    open_file(submission_file)


# 해당 모의고사 폴더 안에 제출답안 엑셀 파일 생성
def create_students_submission_excel(exam_path):
    workbook, worksheet = create_worksheet('제출답안')
    worksheet_write(worksheet, 1, '학생 이름', '지점명', '제출답안')

    return save_excel_file(workbook, exam_path, f'{exam_path.replace("./data", "")} 학생 제출 답')
