import sys
import os

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from Component_ui.Register import Register
from Component_ui.Analyze import Analyze
from Component_ui.Show import Show
from Component_ui.Util import File
from Component_ui.Util import Print
from Component_ui.Error.Error import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 윈도우 설정
        self.setGeometry(300, 300, 400, 400)  # x, y, w, h
        self.setWindowTitle('손고운 사회문화 채점 분석 통합 시스템')

        # QButton 위젯 생성
        self.button1 = QPushButton('시험지 등록', self)
        self.button1.clicked.connect(self.dialog1_open)
        self.button1.setFixedSize(200, 50)
        self.button1.setGeometry(10, 10, 200, 50)

        self.button2 = QPushButton('제출 답안 등록', self)
        self.button2.clicked.connect(self.dialog2_open)
        self.button2.setFixedSize(200, 50)
        self.button2.setGeometry(10, 70, 200, 50)

        self.button3 = QPushButton('채점', self)
        self.button3.clicked.connect(self.dialog3_open)
        self.button3.setFixedSize(200, 50)
        self.button3.setGeometry(10, 130, 200, 50)

        self.button4 = QPushButton('채점 및 분석 결과 열람', self)
        self.button4.clicked.connect(self.dialog4_open)
        self.button4.setFixedSize(200, 50)
        self.button4.setGeometry(10, 190, 200, 50)

        self.button5 = QPushButton('채점 및 분석 결과 출력', self)
        self.button5.clicked.connect(self.dialog7_open)
        self.button5.setFixedSize(200, 50)
        self.button5.setGeometry(10, 250, 200, 50)


        self.myexam = ''


    # 버튼 이벤트 함수
    def dialog1_open(self):
        self.dialog1 = QDialog()
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
        self.dialog2 = QDialog()
        # 답안 등록할 모의고사 고르기
        vbox = QVBoxLayout(self)
        listWidget = QListWidget()
        item_list = File.select_exam_folder()
        listWidget.clear()
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
        self.dialog3 = QDialog()
        # 채점할 모의고사 고르기
        vbox = QVBoxLayout(self)
        listWidget = QListWidget()
        item_list = File.select_exam_folder()
        listWidget.clear()
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
        self.dialog4 = QDialog()
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

    def dialog7_open(self):
        self.dialog7 = QDialog()
        # 열람할 모의고사 고르기
        vbox = QVBoxLayout(self)
        listWidget = QListWidget()
        item_list = File.select_exam_folder()
        for i in item_list:
            listWidget.addItem(i)
        listWidget.itemDoubleClicked.connect(self.dialog7_close)

        vbox.addWidget(listWidget)
        self.setLayout(vbox)

        # QDialog 세팅
        self.dialog7.setWindowTitle('모의고사 출력')
        self.dialog7.setLayout(vbox)
        self.dialog7.setWindowModality(Qt.ApplicationModal)
        self.dialog7.setGeometry(300, 300, 350, 250)
        self.dialog7.show()

    # Dialog 닫기 이벤트
    def dialog1_close(self):
        text = self.dialog1.lineedit.text()
        if text == '':
            self.error_no_input()
            return

        try:
            Register.register_exam(text)
        except WrongFileNameError as wrong_file_name_error:
            self.pop_error_message(wrong_file_name_error)
        except FileExistsError as file_exists_error:
            self.pop_error_message(file_exists_error)
        finally:
            self.dialog1.close()

    # Dialog 닫기 이벤트
    def dialog2_close(self, item):
        exam = item.text()
        Register.register_students_submission(exam)
        self.dialog2.close()

    # Dialog 닫기 이벤트
    def dialog3_close(self, item):
        exam = item.text()
        try:
            Analyze.analyze_exam(exam)
            self.dialog5 = QDialog()
            self.dialog5_open()
        except GetExamDataError as get_exam_data_error:
            self.pop_error_message(get_exam_data_error)
        except GetStudentsDataError as get_students_data_error:
            self.pop_error_message(get_students_data_error)
        except ExcelNotClosedError as excel_not_closed_error:
            self.pop_error_message(excel_not_closed_error)
        except GetDataError as get_data_error:
            self.pop_error_message(get_data_error)

        finally:
            self.dialog3.close()

    # Dialog 닫기 이벤트
    def dialog4_close(self, item):
        exam = item.text()

        try:
            showed_exam = Show.show_exam(exam)
            self.dialog6 = QDialog()
            self.dialog6_open(exam, showed_exam)
        except NotScoredError as not_scored_error:
            not_scored_error.path = exam
            self.pop_error_message(not_scored_error)
        finally:
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
        btnDialog1.move(10, 320)
        btnDialog1.resize(200, 32)
        btnDialog1.clicked.connect(self.dialog6_close1)
        # 버튼 추가
        btnDialog2 = QPushButton("학생 전체 분석 엑셀보기", self.dialog6)
        btnDialog2.move(10, 360)
        btnDialog2.resize(200, 32)
        btnDialog2.clicked.connect(self.dialog6_close2)
        # 버튼 추가
        btnDialog3 = QPushButton("지점별 분석 폴더보기", self.dialog6)
        btnDialog3.move(10, 400)
        btnDialog3.resize(200, 32)
        btnDialog3.clicked.connect(self.dialog6_close3)

        # QDialog 세팅
        self.dialog6.setWindowTitle('분석 결과 열람')
        self.dialog6.setWindowModality(Qt.ApplicationModal)
        self.dialog6.resize(300, 460)
        self.dialog6.show()

    def dialog6_close1(self):
        path = './data/' + self.myexam + '/채점결과/' + self.myexam + ' 채점 결과 문항 분석.xlsx'
        File.open_file(path)

    def dialog6_close2(self):
        path = './data/' + self.myexam + '/채점결과/' + self.myexam + ' 전체 학생 채점 결과.xlsx'
        File.open_file(path)

    def dialog6_close3(self):
        path = os.path.realpath('./data/' + self.myexam + '/채점결과/')
        File.open_file(path, type='directory')

    def dialog7_close(self, item):
        exam = item.text()
        try:
            showed_exam = Show.show_exam(exam)
            self.dialog8 = QDialog()
            self.dialog8_open(exam, showed_exam)
        except NotScoredError as not_scored_error:
            not_scored_error.path = exam
            self.pop_error_message(not_scored_error)
        finally:
            self.dialog7.close()

    def dialog8_open(self, exam, showed_exam):
        self.myexam = exam

        self.dialog8.label = QLabel(showed_exam, self)
        self.dialog8.label.setAlignment(Qt.AlignTop)
        self.dialog8.layout = QVBoxLayout()
        self.dialog8.layout.addWidget(self.dialog8.label)

        self.dialog8.setLayout(self.dialog8.layout)

        # 버튼 추가
        btnDialog1 = QPushButton("시험 문제 분석 엑셀 출력", self.dialog8)
        btnDialog1.move(10, 320)
        btnDialog1.resize(200, 32)
        btnDialog1.clicked.connect(self.dialog8_close1)
        # 버튼 추가
        btnDialog2 = QPushButton("학생 전체 분석 엑셀 출력", self.dialog8)
        btnDialog2.move(10, 360)
        btnDialog2.resize(200, 32)
        btnDialog2.clicked.connect(self.dialog8_close2)
        # 버튼 추가
        btnDialog3 = QPushButton("지점별 분석 폴더 출력", self.dialog8)
        btnDialog3.move(10, 400)
        btnDialog3.resize(200, 32)
        btnDialog3.clicked.connect(self.dialog9_open)

        # QDialog 세팅
        self.dialog8.setWindowTitle('분석 결과 출력')
        self.dialog8.setWindowModality(Qt.ApplicationModal)
        self.dialog8.resize(300, 460)
        self.dialog8.show()

    def dialog8_close1(self):
        # Print.PrintExamInfo(self.myexam)
        print('done')
        self.dialog8.close()

    def dialog8_close2(self):
        # Print.PrintStudentInfo(self.myexam)
        print('done')
        self.dialog8.close()

    def dialog9_open(self):
        self.dialog9 = QDialog()
        # 지점 고르기
        vbox = QVBoxLayout(self)
        listWidget = QListWidget()
        item_list = File.select_branch_foler()
        listWidget.clear()
        for i in item_list:
            listWidget.addItem(i)
        listWidget.itemDoubleClicked.connect(self.dialog9_close)

        vbox.addWidget(listWidget)
        self.setLayout(vbox)

        # QDialog 세팅
        self.dialog9.setWindowTitle('출력할 지점 선택')
        self.dialog9.setLayout(vbox)
        self.dialog9.setWindowModality(Qt.ApplicationModal)
        self.dialog9.setGeometry(300, 300, 350, 250)
        self.dialog9.show()
        self.dialog8.close()

    def dialog9_close(self, item):
        # print(item)
        print('closed')


    # 오류 창 띄우기
    def pop_error_message(self, error):
        QMessageBox.warning(self, error.type, error.path + ': ' + error.message)

    def error_no_input(self):
        QMessageBox.warning(self, '모의고사 이름 오류', '모의고사 이름을 입력하지 않으셨습니다.')

if __name__ == '__main__':
    if getattr(sys, 'frozen', False):
        os.chdir(os.path.dirname(sys.executable))
    else:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
