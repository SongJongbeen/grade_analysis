import os
from openpyxl import Workbook

from ..Util.File import open_file
from ..Util.Excel import worksheet_write, create_worksheet

# 모의고사 등록 페이지
def register_exam():
    exam_folder_path = create_exam_folder()
    exam_excel_path = create_exam_excel(exam_folder_path)
    open_file(exam_excel_path)


# 모의고사 이름을 받고, 해당 모의고사 이름으로 된 폴더 생성
def create_exam_folder():
    exam_name = input('모의고사 이름을 입력: ')
    exam_folder_path = './data/' + exam_name
    # 이미 같은 이름의 모의고사가 존재하지 않는지 확인
    if not os.path.exists(exam_folder_path):
        try:
            os.mkdir(exam_folder_path)
        except:
            print('폴더명으로 쓸 수 있는 형식으로 모의고사 이름을 입력해주세요.')
            exam_folder_path = create_exam_folder()
    else:
        print('이미 존재하는 모의고사입니다.')
        print('이미 등록하신 모의고사의 정보를 수정하시려면, data 폴더 내에 있는 해당 시험의 엑셀파일에서 직접 수정하고 저장하시고 창을 닫으십시오.')
        exam_folder_path = create_exam_folder()
    return exam_folder_path


# 해당 폴더 안에 문제 정보 엑셀 파일 생성
def create_exam_excel(path):

    write_wb, write_ws = create_worksheet('문항 정답 및 배점')

    worksheet_write(write_ws, 1, '문항', '정답', '배점')
    for question_number in range(2, 22):
        worksheet_write(write_ws, question_number, question_number - 1)

    exam_excel_path = str(path) + '/문항및배점.xlsx'
    write_wb.save(exam_excel_path)
    return exam_excel_path
