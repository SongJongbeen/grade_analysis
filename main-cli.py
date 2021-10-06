from Component.Register import Register
from Component.Analyze import Analyze
from Component.Show import Show


# 커맨드를 입력 받아, 그에 해당하는 기능들을 실행시킵니다.
def run_feature_by_command(command):
    if command == '1':
        Register.register_exam()
    elif command == '2':
        Register.register_students_submission()
    elif command == '3':
        Analyze.analyze_exam()
    elif command == '4':
        Show.show_exam()
    else:
        print('프로그램 종료')
        exit()


if __name__ == '__main__':
    while True:
        print('1.모의고사 등록 2.학생 제출 답안 등록 3.채점/분석 4.모의고사 열람')
        command = input('원하는 기능: ')
        run_feature_by_command(command)
        print()
