import os
import json
from openpyxl.styles import Border, Side

from ..Util.Excel import create_worksheet, worksheet_write, save_excel_file


# 채점된 데이터들을 result.json, /채점결과/시험 정보 열람.xlsx, /채점결과/학생 전체 점수 열람.xlsx, 채점결과/지점명/학생이름.xlsx 파일에 각각 저장합니다.
def create_result_files(exam_path, exam):
    if not os.path.exists(exam_path + '/채점결과'):
        os.mkdir(exam_path + '/채점결과')

    create_excel_problem_analyzed_result(exam_path+'/채점결과', exam)
    create_excel_total_students_score_result(exam_path+'/채점결과', exam)
    create_json_exam_result(exam_path, exam)
    create_branch_reports(exam_path + '/채점결과', exam)


# 학생 전체 점수 열람 엑셀 생성
def create_excel_total_students_score_result(exam_path, exam):

    workbook, worksheet = create_worksheet('학생 전체 점수표')

    worksheet_write(worksheet, 1, '이름', '점수', '등급', '등수')
    for idx, student in enumerate(exam.students.values()):
        worksheet_write(worksheet, idx + 2, student.name, student.score, student.grade, student.rank)

    save_excel_file(workbook, exam_path, f'{exam.name} 전체 학생 채점 결과')


# 시험 정보 열람 엑셀 생성
def create_excel_problem_analyzed_result(exam_path, exam):
    workbook, worksheet = create_worksheet('시험 문제 분석')
    worksheet_write(worksheet, 1, '문항', '정답', '정답률', '선지선택비율')

    total_correct_ratio = exam.correct_ratio()
    total_chosen_ratio = exam.chosen_ratio()

    for column_number in range(2, 22):
        problem_number = column_number - 1
        worksheet_write(worksheet, column_number,
                        problem_number,
                        exam.answers[column_number - 2],
                        total_correct_ratio[problem_number],
                        total_chosen_ratio[problem_number]
                        )

    save_excel_file(workbook, exam_path, f'{exam.name} 채점 결과 문항 분석')


def create_json_exam_result(exam_path, exam):
    json_path = exam_path + '/result.json'
    data = {"name": exam.name, "students_number": exam.students_number, "average_score": exam.average_score(),
            "frequent5_wrong_answers": exam.frequent5_wrong_answers(),
            "grade_cut_line_scores": exam.grade_cut_line_scores}

    with open(json_path, 'w') as json_file:
        json.dump(data, json_file)


def create_branch_reports(exam_path, exam):
    create_branch_folders(exam_path, exam.branches.keys())

    for branch_name in exam.branches.keys():
        create_excel_student_reports(exam_path, branch_name, exam)


def create_branch_folders(exam_path, branches):
    for branch in branches:
        if not os.path.exists(exam_path + f'/{branch}'):
            os.mkdir(exam_path + f'/{branch}')


def create_excel_student_reports(exam_path, branch_name, exam):
    student_ids = exam.branches[branch_name]
    for student_id in student_ids:
        create_excel_student_report(exam_path + f'/{branch_name}', exam.students[student_id], exam)


def create_excel_student_report(branch_path, student, exam):
    workbook, worksheet = create_worksheet('점수 분석')
    worksheet.page_setup.orientation = worksheet.ORIENTATION_LANDSCAPE

    worksheet_write(worksheet, 1, '모의고사 이름', '', exam.name, '', '학생 이름', student.name, '점수', str(student.score), '등수',
                    str(student.rank), '등급', str(student.grade))
    worksheet_write(worksheet, 3, '문항번호', '', *(problem_num for problem_num in range(1, 21)))
    worksheet_write(worksheet, 4, '정답', '', *exam.answers)
    worksheet_write(worksheet, 5, '제출답', '', *[int(_) for _ in student.submission])
    worksheet_write(worksheet, 6, '정답률', '', *exam.correct_ratio().values())

    output_range_alphabet = ['C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V']
    for i in range(3, 7):
        for j in output_range_alphabet:
            output_range = worksheet[j+str(i)]
            output_range.border = Border(left=Side(border_style='thin', color='000000'),
                                         right=Side(border_style='thin', color='000000'),
                                         top=Side(border_style='thin', color='000000'),
                                         bottom=Side(border_style='thin', color='000000'))

    save_excel_file(workbook, branch_path, student.name)
