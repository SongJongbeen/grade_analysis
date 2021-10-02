from collections import Counter,defaultdict


class Exam:
    def __init__(self, path, students, answers, scores):
        self.name = path.strip('./data/')
        self.students = students
        self.answers = answers
        self.scores = scores
        self.sorted_students_by_score = []
        self.students_number = 0
        self.students_total_score = 0
        self.grade_cut_line_scores = []
        self.grade_cut_lines_proportion = [0.04, 0.11, 0.23, 0.40, 0.60, 0.77, 0.89, 0.96]
        self.branches = defaultdict(list)

        self.set_students_number()
        self.set_students_total_score()
        self.set_sort_students_by_score()
        self.set_grade_cut_lines()
        self.set_student_ranks()
        self.set_student_grades()
        self.set_branches()

    # 학생 수 받아오기
    def set_students_number(self):
        self.students_number = len(self.students)

    # 총점 구하기
    def set_students_total_score(self):
        self.students_total_score = sum([student.score for student in self.students.values()])

    # 등급 커트라인에 해당하는 점수 set.
    def set_grade_cut_lines(self):
        for proportion in self.grade_cut_lines_proportion:
            student_rank = int(self.students_number * proportion)
            self.grade_cut_line_scores.append(self.sorted_students_by_score[student_rank].score)

    def set_sort_students_by_score(self):
        self.sorted_students_by_score = sorted(self.students.values(), key=lambda student: -student.score)

    def set_student_ranks(self):
        if not self.sorted_students_by_score:
            print("학생들이 정렬되지 않았습니다!")

        for rank, student in enumerate(self.sorted_students_by_score):
            self.students[student.__hash__()].rank = rank + 1

    def set_student_grades(self):
        proportion_idx = 0
        for student in self.sorted_students_by_score:
            self.students[student.__hash__()].grade = proportion_idx + 1
            if student.score < self.grade_cut_line_scores[proportion_idx]:
                proportion_idx += 1

    def set_branches(self):
        for student_id, student_info in self.students.items():
            self.branches[student_info.branch].append(student_id)

    # 틀린 답안 리스트 만들기 (전체 학생)
    def total_students_wrong_answers(self):
        return [wrong_answer for student in self.students.values() for wrong_answer in student.wrong_answers]

    # 가장 많이 틀린 답안 찾기
    def frequent5_wrong_answers(self):
        total_wrong_answers = self.total_students_wrong_answers()
        counter = Counter(total_wrong_answers)

        return [str(number) + '번' for number, value in counter.most_common(5)]

    # 각 문항별로 정답률을 문자열로 리턴
    def correct_ratio(self):
        correct_ratio = {number: '' for number in range(1, 21)}

        for number in range(1, 21):
            count = 0
            for student in self.students.values():
                if student.is_correct(number):
                    count += 1
            correct_ratio[number] = str(round(count / self.students_number, 2) * 100) + '%'

        return correct_ratio

    # 소수 넷째 자리에서 반올림된 평균 값 리턴.
    def average_score(self):
        return round(self.students_total_score / self.students_number, 3)

    # 각 문항별로 선택된 선지 순위
    def chosen_ratio(self):
        total_submissions = [student.submission for student in self.students.values()]
        chosen_ratio = {}

        for number in range(20):
            counter = Counter([total_submissions[col][number] for col in range(len(total_submissions))])
            chosen_ratio[number + 1] = change_chosen_answer_counter_to_str(counter, self.students_number)
        return chosen_ratio


def change_chosen_answer_counter_to_str(counter, students_number):
    changed_str = ''
    for number in range(1, 6):
        selected_ratio = round(100 * counter[str(number)] / students_number ,1)
        changed_str += f'{number}: {selected_ratio}% / '

    return changed_str