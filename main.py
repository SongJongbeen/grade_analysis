from Component.Register import Register
from Component.Grade import Grade
from Component.Analyze import Analyze


# 커맨드를 입력 받아, 그에 해당하는 기능들을 실행시킵니다.
def run_feature_by_command(command):
    if command == '1':
        Register.register_exam()
    elif command == '2':
        Grade.grade_exam()
    elif command == '3':
        Analyze.analyze_exam()
    else:
        print('프로그램 종료')
        exit()


if __name__ == '__main__':
    print('1. 모의고사 등록 2. 모의고사 채점 3. 모의고사 열람')

    while True:
        command = input('원하는 기능: ')
        run_feature_by_command(command)
