import re
import os
from openpyxl import load_workbook

from . import Student
from . import Exam
from . import Result
from ..Error.Error import GetExamDataError, GetStudentsDataError, GetDataError

# 모의고사 채점/분석 페이지

# 모의고사의 정답 파일과 학생 제출 파일을 읽어 채점을 진행합니다. 이후, 결과 파일들을 생성합니다.
def analyze_exam(exam):
    exam_folder = "./data/" + exam
    exam_data = get_exam_data_from_excel(exam_folder + f'/{exam} 정답 및 배점.xlsx')
    students = get_students(exam_folder + f'/{exam} 학생 제출 답.xlsx', *exam_data)

    exam = Exam.Exam(exam_folder, students, *exam_data)

    Result.create_result_files(exam_folder, exam)


def get_exam_data_from_excel(exam_path):
    if not os.path.exists(exam_path):
        raise GetDataError(exam_path, "해당 파일이 존재하지 않습니다!")
    return exam_answers_from_excel(exam_path), exam_scores_from_excel(exam_path)


def exam_answers_from_excel(exam_path):
    values = load_workbook(exam_path, data_only=True)['문항 정답 및 배점'].values
    next(values)
    answers = []

    for problem_num, value in enumerate(values, start=1):
        if not value or not (type(value[1]) == int) or not (0 < value[1] <= 5):
            raise GetExamDataError(exam_path, f"{problem_num}번째 문항의 정답이 올바르지 않습니다!")
        answers.append(value[1])

    if len(answers) != 20:
        raise GetExamDataError(exam_path, f"문항 정답이 20개가 아닌 {len(answers)}개 제출되었습니다.")
    return answers


def exam_scores_from_excel(exam_path):
    values = load_workbook(exam_path, data_only=True)['문항 정답 및 배점'].values
    next(values)
    scores = []

    for problem_num, value in enumerate(values, start=1):
        if not value or not (type(value[2]) == int):
            raise GetExamDataError(exam_path, f"{problem_num}번째 문항의 배점이 올바르지 않습니다!")
        scores.append(value[2])

    if len(scores) != 20:
        raise GetExamDataError(exam_path, f"문항 배점이 20개가 아닌 {len(scores)}개 제출되었습니다.")

    return scores


# 학생 객체를 담은 학생들 배열을 반환합니다.
def get_students(students_path, exam_answers, exam_scores):
    if not os.path.exists(students_path):
        raise GetDataError(students_path, "해당 파일이 존재하지 않습니다!")
    students = {}
    records = load_workbook(students_path, data_only=True)['제출답안'].values
    if not records:
        return False

    next(records)
    for record_id, (name, branch, submission) in enumerate(records, start=1):
        if is_valid_student_data(name, branch, submission):
            student = Student.Student(name, branch, submission, exam_answers, exam_scores)
            students[student.__hash__()] = student
        else:
            raise GetStudentsDataError(students_path, f"{record_id}번째 제출 답안 형식이 올바르지 않습니다.")


    return students


def is_valid_student_data(name, branch, submission):
    if name and branch and submission:
        if type(name) == str \
                and type(branch) == str \
                and type(submission) == str \
                and re.compile('[0-9]{20}').match(submission):
            return True
