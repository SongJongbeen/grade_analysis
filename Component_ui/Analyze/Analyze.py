import re
import json
import psutil
from openpyxl import load_workbook

from . import Student
from . import Exam
from ..Util.File import *
from ..Util.Excel import *


# 모의고사 채점/분석 페이지
# 모의고사의 정답 파일과 학생 제출 파일을 읽어 채점을 진행합니다.
# 채점된 데이터들을 result.json, /채점결과/시험 정보 열람.xlsx, /채점결과/학생 전체 점수 열람.xlsx 파일에 각각 저장합니다.


def analyze_exam(exam):
    exam_folder = "./data/" + exam
    exam_data = get_exam_data_from_excel(exam_folder + f'/{exam_folder.lstrip("./data")} 정답 및 배점.xlsx')
    if not exam_data:
        return
    students = get_students(exam_folder + f'/{exam_folder.lstrip("./data")} 학생 제출 답.xlsx', *exam_data)
    if not students:
        return

    exam = Exam.Exam(exam_folder, students, *exam_data)

    if not os.path.exists(exam_folder + '/채점결과'):
        os.mkdir(exam_folder + '/채점결과')

    create_excel_problem_analyzed_result(exam_folder+'/채점결과', exam)
    create_excel_total_students_score_result(exam_folder+'/채점결과', exam)
    create_json_exam_result(exam_folder, exam)
    print("채점되었습니다!")


def get_exam_data_from_excel(exam_path):
    exam_answers = exam_answers_from_excel(exam_path)
    exam_scores = exam_scores_from_excel(exam_path)

    if exam_answers and exam_scores:
        return exam_answers, exam_scores
    return False


def exam_answers_from_excel(exam_path):
    values = load_workbook(exam_path, data_only=True)['문항 정답 및 배점'].values
    answers = [value[1] for value in values if value and type(value[1]) == int]

    if len(answers) != 20:
        print("문제 정답 개수를 다시 확인해 주세요!")
        return False
    return answers


def exam_scores_from_excel(exam_path):
    values = load_workbook(exam_path, data_only=True)['문항 정답 및 배점'].values
    scores = [value[2] for value in values if value and type(value[2]) == int]

    if len(scores) != 20:
        print("문제 배점 개수를 다시 확인해 주세요!")
        return False

    return scores


# 학생 객체를 담은 학생들 배열을 반환합니다.
def get_students(students_path, exam_answers, exam_scores):
    students = {}
    records = load_workbook(students_path, data_only=True)['제출답안'].values


    next(records)
    for name, branch, submission in records:
        if is_valid_student_data(name, branch, submission):
            student = Student.Student(name, branch, submission, exam_answers, exam_scores)
            students[student.__hash__()] = student
        else:
            print("학생 제출 답안 엑셀 파일을 다시 확인해 주세요! 잘못된 값이 들어갔습니다.")
            return False

    if not students:
        print('학생이 없습니다!')
        return False
    return students


def is_valid_student_data(name, branch, submission):
    if name and branch and submission:
        # print(name, branch, submission)
        if type(name) == str and type(branch) == str and re.compile('[0-9]{20}').match(submission):
            return True
    return False


# 학생 전체 점수 열람 엑셀 생성
def create_excel_total_students_score_result(exam_path, exam):

    for proc in psutil.process_iter():
        if proc.name() == 'Microsoft Excel':
            print(proc.name(), proc.pid, proc.threads()) # proc.threads : 에러 남

    workbook, worksheet = create_worksheet('학생 전체 점수표')

    worksheet_write(worksheet, 1, '이름', '점수', '등급', '등수')
    for idx, student in enumerate(exam.students.values()):
        worksheet_write(worksheet, idx + 2, student.name, student.score, student.grade, student.rank)

    file_path = save_excel_file(workbook, exam_path, f'{exam.name} 전체 학생 채점 결과')
    return file_path


# 시험 정보 열람 엑셀 생성
def create_excel_problem_analyzed_result(exam_path, exam):
    workbook, worksheet = create_worksheet('학생 전체 점수표')
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

    return save_excel_file(workbook, exam_path, f'{exam.name} 채점 결과 문항 분석')


def create_json_exam_result(exam_path, exam):
    json_path = exam_path + '/result.json'
    data = {"name": exam.name, "students_number": exam.students_number, "average_score": exam.average_score(),
            "frequent5_wrong_answers": exam.frequent5_wrong_answers(),
            "grade_cut_line_scores": exam.grade_cut_line_scores}

    with open(json_path, 'w') as json_file:
        json.dump(data, json_file)
