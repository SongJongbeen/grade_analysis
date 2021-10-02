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
                self.error_foler_name()
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
        elif analyzed_exam:
            self.dialog5 = QDialog()
            self.dialog5_open()


    # Dialog 닫기 이벤트
    def dialog4_close(self, item):
        exam = item.text()
        showed_exam = Show.show_exam(exam)
        if showed_exam == 5:
            self.error_not_analyzed()
        self.dialog4.close()

    def dialog5_open(self):
        QMessageBox.information(self, "채점이 완료되었습니다.", "채점이 완료되었습니다.")

    def dialog5_close(self):
        self.dialog5.close()


    # 오류 창 띄우기
    def error_no_input(self):
        QMessageBox.warning(self, '모의고사 이름 오류', '모의고사 이름을 입력하지 않으셨습니다.')

    def error_existing_folder(self):
        QMessageBox.warning(self, '중복되는 모의고사', '이미 존재하는 모의고사입니다. 수정하시려면 data 폴더 > 정답 및 배점에서 수정해주세요.')

    def error_foler_name(self):
        QMessageBox.warning(self, '모의고사 이름 오류', '폴더명으로 쓸 수 있는 형식으로 입력해주세요.')

    def error_not_register_exam(self):
        QMessageBox.warning(self, '채점 오류', '시험지가 정상적으로 등록되어있는지 확인해주세요.\n다음의 원인이 있을 수 있습니다.\n1.문제의 개수(20개)\n2.배점의 개수(20개)')

    def error_not_register_student_submission(self):
        QMessageBox.warning(self, '채점 오류', '학생 제출 답안이 정상적으로 등록되어있는지 확인해주세요.\n다음의 원인이 있을 수 있습니다.\n1.학생이 없음\n2.잘못된 값이 들어감.')

    def error_not_anlayzed(self):
        QMessageBox.warning(self, '분석 열람 오류', '해당 모의고사에 대한 채점을 먼저 진행해주세요.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
