import os
import re
from openpyxl import Workbook, load_workbook

from . import Student
from . import Exam
from ..Util.File import open_file
from ..Util.Excel import worksheet_write, create_worksheet


# 모의고사 분석 페이지
def analyze_exam():
    analysis_exam_path = get_analysis_exam_path()
    exam_answers = exam_answers_from_excel(analysis_exam_path)
    exam_scores = exam_scores_from_excel(analysis_exam_path)

    students = get_students(analysis_exam_path + str('/제출답안.xlsx'), exam_answers, exam_scores)
    exam = Exam.Exam(analysis_exam_path, students, exam_answers, exam_scores)

    show_exam_info(exam)

    print('1. 학생 전체 점수 열람 2. 각 문항별 분석 3. 학생 성적표 열람')
    cmd = receive_command()
    run_with_command(analysis_exam_path, cmd, exam)


# 분석할 모의고사 이름 및 경로 받기
def get_analysis_exam_path():
    # 모의고사 목록 출력
    exam_list = os.listdir('./data')
    for idx in range(len(exam_list)):
        print(str(idx + 1) + '.', exam_list[idx])
    # 채점할 모의고사 이름 받기
    analysis_exam_idx = input('몇번째 모의고사를 분석/열람하시겠습니까? ')
    analysis_exam_name = exam_list[int(analysis_exam_idx) - 1]
    # 해당 모의고사 경로 return
    analysis_exam_path = './data/' + analysis_exam_name
    return analysis_exam_path


def exam_answers_from_excel(exam_path):
    values = load_workbook(exam_path, data_only=True)['문항 정답 및 배점'].values
    answers = [value[1] for value in values if value and type(value[1]) == int]
    return answers


def exam_scores_from_excel(exam_path):
    values = load_workbook(exam_path, data_only=True)['문항 정답 및 배점'].values
    scores = [value[2] for value in values if value and type(value[2]) == int]
    return scores


# 학생 객체를 담은 학생들 배열을 반환합니다.
def get_students(students_path, exam_answers, exam_scores):
    students = {}
    records = load_workbook(students_path, data_only=True)['제출답안'].values

    for name, branch, submission in records:
        if is_valid_student_data(name, branch, submission):
            student = Student.Student(name, branch, submission, exam_answers, exam_scores)
            students[student.__hash__()] = student

    return students


def is_valid_student_data(name, branch, submission):
    if name and branch and submission:
        if type(name) == str and type(branch) == str and re.compile('[0-9]{20}').match(submission):
            return True
    return False


# 모의고사 정보 보여줌
def show_exam_info(exam):
    print(exam.name, f'(응시생: {exam.students_number}명)')  # 시험 이름, 응시생 수
    print(f'평균 점수: {exam.average_score()}')  # 평균 점수
    print('오답 1~5순위: ', *exam.frequent5_wrong_answers())  # 오답 1~5 순위
    print('1~9등급 커트라인')  # 각 등급 커트라인
    for idx in range(1, 9):
        print(f'{idx}등급: {exam.grade_cut_line_scores[idx - 1]}점')


def receive_command():
    return input('열람할 자료를 고르세요: ')


def run_with_command(analysis_exam_path, cmd, exam):
    if cmd == '1':
        file_path = write_excel_total_students_score(analysis_exam_path, exam)
    elif cmd == '2':
        file_path = write_excel_exam_analyze(analysis_exam_path, exam)
    elif cmd == '3':
        file_path = create_branch_folder(analysis_exam_path)
        write_student_reports(file_path, exam)
    else:
        print('명령 종료')
        return

    open_file(file_path)


# 학생 전체 점수 열람 엑셀 생성
def write_excel_total_students_score(analysis_exam_path, exam):
    write_wb = Workbook()
    write_ws = write_wb.create_sheet('학생 전체 점수표')

    worksheet_write(write_ws, 1, '이름', '점수', '등급', '등수')

    for idx, student in enumerate(exam.students.values()):
        worksheet_write(write_ws, idx + 2, student.name, student.score, student.grade, student.rank)

    # 엑셀 파일 저장
    students_info_excel_path = str(analysis_exam_path) + '/학생 전체 점수 열람.xlsx'
    write_wb.save(students_info_excel_path)
    return students_info_excel_path


# 시험 정보 열람 엑셀 생성
def write_excel_exam_analyze(analysis_exam_path, exam):
    # 엑셀 시트 활성화
    write_wb = Workbook()
    write_ws = write_wb.create_sheet('학생 전체 점수표')

    worksheet_write(write_ws, 1, '문항', '정답', '정답률', '선지선택비율')

    total_correct_ratio = exam.correct_ratio()
    total_chosen_ratio = exam.chosen_ratio()

    for column_number in range(2, 22):
        problem_number = column_number - 1
        worksheet_write(write_ws, column_number,
                        problem_number,
                        exam.answers[column_number - 2],
                        total_correct_ratio[problem_number],
                        total_chosen_ratio[problem_number]
                        )

    # 엑셀 파일이 저장될 경로
    exam_info_excel_path = str(analysis_exam_path) + '/시험 정보 열람.xlsx'
    # 엑셀 파일 저장 및 경로 return
    write_wb.save(exam_info_excel_path)
    return exam_info_excel_path


# 지점의 폴더를 만드는 기능
def create_branch_folder(analysis_exam_path):
    branch_name = input('지점명을 입력: ')
    branch_folder_path = analysis_exam_path + '/' + branch_name
    if not os.path.exists(branch_folder_path):
        try:
            os.mkdir(branch_folder_path)
        except:
            print('폴더명으로 쓸 수 있는 형식으로 지점 이름을 입력해주세요.')
            branch_folder_path = create_branch_folder(analysis_exam_path)
    else:
        print('이미 존재하는 지점입니다. \n이미 등록하신 지점의 정보를 수정하시려면, data 폴더 내에 있는 해당 모의고사 폴더 내에 있는 지점 폴더를 삭제하십시오.')
        create_branch_folder(analysis_exam_path)

    return branch_folder_path


def write_student_report(branch_folder_path, student, exam):
    write_wb, write_ws = create_worksheet('해당 학생 점수표')

    worksheet_write(write_ws, 1, '모의고사 이름', str(exam.name), '학생 이름', student.name, '점수', student.score, '등수',
                    student.rank, '등급', student.grade)
    worksheet_write(write_ws, 3, '문항번호', '', *(problem_num for problem_num in range(1, 21)))
    worksheet_write(write_ws, 4, '정답', '', *exam.answers)
    worksheet_write(write_ws, 5, '제출답', '', *student.submission)
    worksheet_write(write_ws, 6, '정답률', '', *exam.correct_ratio())

    branch_info_excel_path = str(branch_folder_path) + '/' + student.name + '.xlsx'
    write_wb.save(branch_info_excel_path)


def write_student_reports(branch_folder_path, exam):
    for student in exam.students.values():
        write_student_report(branch_folder_path, student, exam)
