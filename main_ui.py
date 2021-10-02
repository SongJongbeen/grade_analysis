import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Component_ui.Register import Register
from Component_ui.Analyze import Analyze
from Component_ui.Show import Show
from Component_ui.Util import File


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # 윈도우 설정
        self.setGeometry(300, 300, 400, 300)  # x, y, w, h
        self.setWindowTitle('손고운 사회문화 채점 분석 통합 시스템')

        # QButton 위젯 생성
        self.button1 = QPushButton('시험지 등록', self)
        self.button1.clicked.connect(self.dialog1_open)
        self.button1.setGeometry(10, 10, 200, 50)

        self.button2 = QPushButton('제출 답안 등록', self)
        self.button2.clicked.connect(self.dialog2_open)
        self.button2.setGeometry(10, 70, 200, 50)

        self.button3 = QPushButton('채점', self)
        self.button3.clicked.connect(self.dialog3_open)
        self.button3.setGeometry(10, 130, 200, 50)

        self.button4 = QPushButton('채점 및 분석 결과 열람', self)
        self.button4.clicked.connect(self.dialog4_open)
        self.button4.setGeometry(10, 190, 200, 50)

        self.myexam = ''

        # QDialog 설정
        self.dialog1 = QDialog()
        self.dialog2 = QDialog()
        self.dialog3 = QDialog()
        self.dialog4 = QDialog()

    # 버튼 이벤트 함수
    def dialog1_open(self):
        # 모의고사 이름 입력칸
        self.dialog1.lineedit = QLineEdit(self.dialog1)
        self.dialog1.lineedit.move(10, 10)

        # 버튼 추가
        self.dialog1.btnDialog = QPushButton("등록하기", self.dialog1)
        self.dialog1.btnDialog.move(10, 50)
        self.dialog1.btnDialog.clicked.connect(self.dialog1_close)

        # QDialog 세팅
        self.dialog1.setWindowTitle('시험지 등록')
        self.dialog1.setWindowModality(Qt.ApplicationModal)
        self.dialog1.resize(300, 200)
        self.dialog1.show()

    def dialog2_open(self):
        # 답안 등록할 모의고사 고르기
        vbox = QVBoxLayout(self)
        listWidget = QListWidget()
        item_list = File.select_exam_folder()
        for i in item_list:
            listWidget.addItem(i)
        listWidget.itemDoubleClicked.connect(self.dialog2_close)

        vbox.addWidget(listWidget)
        self.setLayout(vbox)

        # QDialog 세팅
        self.dialog2.setWindowTitle('제출답안 등록')
        self.dialog2.setLayout(vbox)
        self.dialog2.setWindowModality(Qt.ApplicationModal)
        self.dialog2.setGeometry(300, 300, 350, 250)
        self.dialog2.show()

    def dialog3_open(self):
        # 채점할 모의고사 고르기
        vbox = QVBoxLayout(self)
        listWidget = QListWidget()
        item_list = File.select_exam_folder()
        for i in item_list:
            listWidget.addItem(i)
        listWidget.itemDoubleClicked.connect(self.dialog3_close)

        vbox.addWidget(listWidget)
        self.setLayout(vbox)

        # QDialog 세팅
        self.dialog3.setWindowTitle('모의고사 채점')
        self.dialog3.setLayout(vbox)
        self.dialog3.setWindowModality(Qt.ApplicationModal)
        self.dialog3.setGeometry(300, 300, 350, 250)
        self.dialog3.show()

    def dialog4_open(self):
        # 열람할 모의고사 고르기
        vbox = QVBoxLayout(self)
        listWidget = QListWidget()
        item_list = File.select_exam_folder()
        for i in item_list:
            listWidget.addItem(i)
        listWidget.itemDoubleClicked.connect(self.dialog4_close)

        vbox.addWidget(listWidget)
        self.setLayout(vbox)

        # QDialog 세팅
        self.dialog4.setWindowTitle('모의고사 열람')
        self.dialog4.setLayout(vbox)
        self.dialog4.setWindowModality(Qt.ApplicationModal)
        self.dialog4.setGeometry(300, 300, 350, 250)
        self.dialog4.show()

    # Dialog 닫기 이벤트
    def dialog1_close(self):
        text = self.dialog1.lineedit.text()
        if text == '':
            self.error_no_input()
        else:
            registered_exam = Register.register_exam(text)
            if registered_exam == 1:
                self.error_existing_folder()
            elif registered_exam == 2:
                self.error_folder_name()
            else:
                pass
        self.dialog1.close()

    # Dialog 닫기 이벤트
    def dialog2_close(self, item):
        exam = item.text()
        Register.register_students_submission(exam)
        self.dialog2.close()

    # Dialog 닫기 이벤트
    def dialog3_close(self, item):
        exam = item.text()
        analyzed_exam = Analyze.analyze_exam(exam)
        if analyzed_exam == 3:
            self.error_not_register_exam()
        elif analyzed_exam == 4:
            self.error_not_register_student_submission()
        elif analyzed_exam == 6:
            self.error_close_excel()
        elif analyzed_exam == 100:
            self.dialog5 = QDialog()
            self.dialog5_open()
        self.dialog3.close()


    # Dialog 닫기 이벤트
    def dialog4_close(self, item):
        exam = item.text()
        showed_exam = Show.show_exam(exam)
        if showed_exam == 5:
            self.error_not_analyzed()
        else:
            self.dialog6 = QDialog()
            self.dialog6_open(exam, showed_exam)
        self.dialog4.close()

    def dialog5_open(self):
        QMessageBox.information(self, "채점이 완료되었습니다.", "채점이 완료되었습니다.")

    def dialog5_close(self):
        self.dialog5.close()

    def dialog6_open(self, exam, showed_exam):
        self.myexam = exam

        self.dialog6.label = QLabel(showed_exam, self)
        self.dialog6.label.setAlignment(Qt.AlignTop)
        self.dialog6.layout = QVBoxLayout()
        self.dialog6.layout.addWidget(self.dialog6.label)

        self.dialog6.setLayout(self.dialog6.layout)

        # 버튼 추가
        btnDialog1 = QPushButton("시험 문제 분석 엑셀보기", self.dialog6)
        btnDialog1.move(10, 230)
        btnDialog1.resize(120, 32)
        btnDialog1.clicked.connect(self.dialog6_close1)
        # 버튼 추가
        btnDialog2 = QPushButton("학생 전체 분석 엑셀보기", self.dialog6)
        btnDialog2.move(10, 270)
        btnDialog2.resize(120, 32)
        btnDialog2.clicked.connect(self.dialog6_close2)
        # 버튼 추가
        btnDialog3 = QPushButton("지점별 분석 폴더보기", self.dialog6)
        btnDialog3.move(10, 310)
        btnDialog3.resize(120, 32)
        btnDialog3.clicked.connect(self.dialog6_close3)

        # QDialog 세팅
        self.dialog6.setWindowTitle('분석 결과 열람')
        self.dialog6.setWindowModality(Qt.ApplicationModal)
        self.dialog6.resize(300, 400)
        self.dialog6.show()

    def dialog6_close1(self):
        path = './data/' + self.myexam + '/채점결과/' + self.myexam + ' 채점 결과 문항 분석'
        File.open_file(path)

    def dialog6_close2(self):
        path = './data/' + self.myexam + '/채점결과/' + self.myexam + ' 전체 학생 채점 결과'
        File.open_file(path)

    def dialog6_close3(self):
        path = os.path.realpath('./data/' + self.myexam + '/채점결과/')
        os.startfile(path)


    # 오류 창 띄우기
    def error_no_input(self):
        QMessageBox.warning(self, '모의고사 이름 오류', '모의고사 이름을 입력하지 않으셨습니다.')

    def error_existing_folder(self):
        QMessageBox.warning(self, '중복되는 모의고사', '이미 존재하는 모의고사입니다. 수정하시려면 data 폴더 > 정답 및 배점에서 수정해주세요.')

    def error_folder_name(self):
        QMessageBox.warning(self, '모의고사 이름 오류', '폴더명으로 쓸 수 있는 형식으로 입력해주세요.')

    def error_not_register_exam(self):
        QMessageBox.warning(self, '채점 오류', '시험지가 정상적으로 등록되어있는지 확인해주세요.\n다음의 원인이 있을 수 있습니다.\n1.문제의 개수(20개)\n2.배점의 개수(20개)')

    def error_not_register_student_submission(self):
        QMessageBox.warning(self, '채점 오류', '학생 제출 답안이 정상적으로 등록되어있는지 확인해주세요.\n다음의 원인이 있을 수 있습니다.\n1.학생이 없음\n2.잘못된 값이 들어감.')

    def error_not_analyzed(self):
        QMessageBox.warning(self, '분석 열람 오류', '해당 모의고사에 대한 채점을 먼저 진행해주세요.')

    def error_close_excel(self):
        QMessageBox.warning(self, '채점 오류', '열려 있는 모의고사를 닫고 진행해주세요.')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
