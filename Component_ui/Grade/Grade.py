import os
from openpyxl import Workbook

from ..Util.File import open_file


def grade_exam():
    grade_exam_path = get_grade_exam_path()
    grade_excel_path = create_grade_excel(grade_exam_path)
    open_file(grade_excel_path)


# # 채점할 모의고사 이름 및 경로 받기
# def get_grade_exam_path():
#     # 모의고사 목록 출력
#     exam_list = os.listdir('./data')
#     for idx in range(len(exam_list)):
#         print(str(idx+1) + '.', exam_list[idx])
#     # 채점할 모의고사 이름 받기
#     grade_exam_idx = input('몇번째 모의고사를 채점하시겠습니까? ')
#     grade_exam_name = exam_list[int(grade_exam_idx)-1]
#     # 해당 모의고사 경로 return
#     grade_exam_path = './data/' + grade_exam_name
#     return grade_exam_path


# 해당 모의고사 폴더 안에 제출답안 엑셀 파일 생성
def create_grade_excel(grade_exam_path):
    # 엑셀 시트 활성화
    write_wb = Workbook()
    write_ws = write_wb.create_sheet('제출답안')
    # 엑셀에 기본 값 넣어두기
    write_ws['A1'] = '학생 이름'
    write_ws['B1'] = '지점명'
    write_ws['C1'] = '제출답안'
    # 엑셀 파일이 저장될 경로
    grade_excel_path = str(grade_exam_path) + '/제출답안.xlsx'
    # 엑셀 파일 저장 및 경로 return
    write_wb.save(grade_excel_path)
    return grade_excel_path
