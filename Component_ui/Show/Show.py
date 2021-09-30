import os
import json

from ..Util.File import select_exam_folder


def show_exam(exam):
    exam_dir = './data/' + exam

    if not os.path.exists(exam_dir + '/result.json'):
        print("채점을 먼저 진행해 주세요!")
        return

    with open(exam_dir + '/result.json') as json_file:
        result = json.load(json_file)
        print_result(result)

    return


def print_result(result):
    print(result["name"], f'응시생: {result["students_number"]}명') # 시험 이름, 응시생 수
    print(f'평균 점수: {result["average_score"]}')  # 평균 점수
    print('오답 1~5순위: ', *result["frequent5_wrong_answers"])  # 오답 1~5 순위
    print('1~9등급 커트라인')  # 각 등급 커트라인
    for idx in range(1, 9):
        print(f'{idx}등급: {result["grade_cut_line_scores"][idx - 1]}점')
