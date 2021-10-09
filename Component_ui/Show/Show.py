import os
import json
from ..Error.Error import NotScoredError


def show_exam(exam):
    exam_dir = './data/' + exam

    if not os.path.exists(exam_dir + '/result.json'):
        raise NotScoredError

    with open(exam_dir + '/result.json') as json_file:
        result = json.load(json_file)
        results = print_result(result)

    return results


def print_result(result):
    results = ''
    results += result["name"] + f'응시생: {result["students_number"]}명\n\n'
    results += f'평균 점수: {result["average_score"]}\n\n'
    results += '오답 1~5순위: ' + ', '.join(result["frequent5_wrong_answers"]) + '\n\n'
    results += '1~8등급 커트라인\n\n'

    for idx in range(1, 9):
        results += f'{idx}등급: {result["grade_cut_line_scores"][idx - 1]}점\n'

    return results
