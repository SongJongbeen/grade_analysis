# 현재 쓰이진 않지만, 추가될 여지가 있는 기능들.

# Analyze.py

# 지점별 학생 성적표 엑셀 파일 생성
# def create_excel_student_reports(branch_folder_path, exam):
#     for student in exam.students.values():
#         create_excel_student_report(branch_folder_path, student, exam)
#
#
# def create_excel_student_report(branch_folder_path, student, exam):
#     workbook, worksheet = create_worksheet('해당 학생 점수표')
#
#     worksheet_write(worksheet, 1, '모의고사 이름', str(exam.name), '학생 이름', student.name, '점수', student.score, '등수',
#                     student.rank, '등급', student.grade)
#     worksheet_write(worksheet, 3, '문항번호', '', *(problem_num for problem_num in range(1, 21)))
#     worksheet_write(worksheet, 4, '정답', '', *exam.answers)
#     worksheet_write(worksheet, 5, '제출답', '', *student.submission)
#     worksheet_write(worksheet, 6, '정답률', '', *exam.correct_ratio())
#
#     save_excel_file(workbook, branch_folder_path, student.name)



# print('1. 모의고사 정보 열람 2. 각 문항별 분석 3. 학생 성적표 열람')


# # 모의고사 정보 보여줌
# def show_exam_info(exam):
#     print(exam.name, f'(응시생: {exam.students_number}명)')  # 시험 이름, 응시생 수
#     print(f'평균 점수: {exam.average_score()}')  # 평균 점수
#     print('오답 1~5순위: ', *exam.frequent5_wrong_answers())  # 오답 1~5 순위
#     print('1~9등급 커트라인')  # 각 등급 커트라인
#     for idx in range(1, 9):
#         print(f'{idx}등급: {exam.grade_cut_line_scores[idx - 1]}점')
#
# def receive_command():
#     return input('열람할 자료를 고르세요: ')
#
#
# def run_with_command(exam_path, cmd, exam):
#     # 1. 학생 전체 점수 열람 2. 각 문항별 분석 3. 학생 성적표 열람
#
#     if cmd == '1':
#         open_file(create_excel_total_students_score(exam_path, exam))
#     elif cmd == '2':
#         open_file(create_excel_exam_analyze(exam_path, exam))
#     elif cmd == '3':
#         file_path = create_folder(exam_path, '지점')
#         create_excel_student_reports(file_path, exam)
#         open_file(file_path)
#     else:
#         print('명령 종료')
#         return
