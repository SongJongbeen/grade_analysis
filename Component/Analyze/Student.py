class Student:
    # 초기값
    def __init__(self, name, branch, submission, exam_answers, exam_scores):
        self.name = name
        self.branch = branch
        self.submission = submission
        self.correct_answers = []
        self.wrong_answers = []
        self.score = -1
        self.grade = -1
        self.rank = -1

        self.set_correct_answers(exam_answers)
        self.set_wrong_answers()
        self.set_score(exam_scores)

    def set_correct_answers(self, exam_answers):
        for idx in range(0, 20):
            if exam_answers[idx] == int(self.submission[idx]):
                self.correct_answers.append(idx + 1)

    def set_wrong_answers(self):
        self.wrong_answers = [idx + 1 for idx in range(1, 21) if idx + 1 not in self.correct_answers]

    def set_score(self, exam_scores):
        for idx in self.correct_answers:
            self.score += exam_scores[idx - 1]

    def is_correct(self, problem_number):
        return True if problem_number in self.correct_answers else False
