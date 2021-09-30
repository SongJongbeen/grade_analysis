import sys
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
        self.setWindowTitle('Status Window')

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
        self.dialog3.setWindowTitle('제출답안 등록')
        self.dialog3.setLayout(vbox)
        self.dialog3.setWindowModality(Qt.ApplicationModal)
        self.dialog3.setGeometry(300, 300, 350, 250)
        self.dialog3.show()

    def dialog4_open(self):
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
        self.dialog3.setWindowTitle('제출답안 등록')
        self.dialog3.setLayout(vbox)
        self.dialog3.setWindowModality(Qt.ApplicationModal)
        self.dialog3.setGeometry(300, 300, 350, 250)
        self.dialog3.show()

    # Dialog 닫기 이벤트
    def dialog1_close(self):
        text = self.dialog1.lineedit.text()     # 이 부분 문제 있음.
        Register.register_exam(text)
        self.dialog1.close()

    # Dialog 닫기 이벤트
    def dialog2_close(self):
        exam = self.dialog2.item.text()     # 이 부분 문제 있음.
        Register.register_students_submission(exam)
        self.dialog2.close()

    # Dialog 닫기 이벤트
    def dialog3_close(self):
        exam = self.dialog3.item.text()  # 이 부분 문제 있음.
        Analyze.analyze_exam(exam)
        self.dialog3.close()

    # Dialog 닫기 이벤트
    def dialog4_close(self):
        exam = self.dialog4.item.text()  # 이 부분 문제 있음.
        Show.show_exam(exam)
        self.dialog4.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())