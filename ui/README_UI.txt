메인 윈도우 (MainWindow)

시험지등록 (pushButton_1) --> clicked() --> openRegisterExam()
제출 답안 등록 (pushButton_2) --> clicked() --> openRegisterStudentsSubmission()
채점 (pushButton_3) --> clicked() --> openAnalyzeExam()
채점 및 분석 결과 열람 (pushButton_4) --> clicked() --> openShowExam()
=====
시험지 등록 (register_exam)

등록하기 (pushButton) --> clicked() --> registerExam()
=====
제출 답안 등록 (register_students_submission)

시험 리스트 (exam_list_register_exam)
등록하기 (pushButton) --> clicked() --> registerStudentsSubmission()
=====
채점 (analyze_exam)

시험 리스트 (exam_list_analyze_exam)
채점하기 (pushButton) --> clicked() --> analyzeExam()
=====
채점 및 분석 결과 열람 (show_exam)

시험 리스트 (exam_list_show_exam)
열람하기  (pushButton) --> clicked() --> openShowExam2()
=====
채점 및 분석 결과 열람 2 (show_exam_2)

기본 정보 (textBrowser)
모의고사 문항 분석 (pushButton_1) --> clicked() --> showAnalyzedExam()
학생 전체 점수 열람 (pushButton_2) --> clicked() --> showAnalyzedStudents()
학생별 성적표 열람 (pushButton_3) --> clicked() --> showAnalyzedBranches()
