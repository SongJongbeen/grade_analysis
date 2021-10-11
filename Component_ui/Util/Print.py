import os

def PrintExamInfo(exam_name):
    path = './data/' + exam_name + '/채점결과/' + exam_name + ' 채점 결과 문항 분석.xlsx'
    print(path)
    # os.startfile(path, 'print')

def PrintStudentInfo(exam_name):
    path = './data/' + exam_name + '/채점결과/' + exam_name + ' 전체 학생 채점 결과.xlsx'
    print(path)
    # os.startfile(path, 'print')

def PrintBranchInfo(exam_name, branch_name):
    dir_path = './data/' + exam_name + '/채점결과/' + branch_name + '/'
    file_list = os.listdir(dir_path)
    for file in file_list:
        path = dir_path + file
        print(path)
        # os.startfile(path, 'print')
