import os
import json

from ..Util.File import select_exam_folder


def show_exam(exam):
    exam_dir = './data/' + exam

    if not os.path.exists(exam_dir + '/result.json'):
        return 5

    with open(exam_dir + '/result.json') as json_file:
        result = json.load(json_file)
        results = print_result(result)

    return results


def print_result(result):
    results = ''
    results += result["name"] + f'응시생: {result["students_number"]}명\n'
    results += f'평균 점수: {result["average_score"]}\n'
    results += '오답 1~5순위: ' + ', '.join(result["frequent5_wrong_answers"]) + '\n'
    results += '1~9등급 커트라인\n'

    for idx in range(1, 9):
        results += f'{idx}등급: {result["grade_cut_line_scores"][idx - 1]}점\n'

    return results
