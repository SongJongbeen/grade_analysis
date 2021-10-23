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

        # 윈도우창 제목 및 사이즈 설정
        self.setGeometry(300, 300, 400, 400)  # x, y, w, h
        self.setWindowTitle('손고운 사회문화 채점 분석 통합 시스템')

        # 시험지 등록 버튼
        self.button1 = QPushButton('시험지 등록', self)
        self.button1.clicked.connect(self._RegiExam_)
        self.button1.setFixedSize(200, 50)
        self.button1.setGeometry(10, 10, 200, 50)

        # 제출답안 등록 버튼
        self.button2 = QPushButton('제출 답안 등록', self)
        self.button2.clicked.connect(self._ChooseExam_, 1)
        self.button2.setFixedSize(200, 50)
        self.button2.setGeometry(10, 70, 200, 50)

        # 채점 버튼
        self.button3 = QPushButton('채점', self)
        self.button3.clicked.connect(self._ChooseExam_, 2)
        self.button3.setFixedSize(200, 50)
        self.button3.setGeometry(10, 130, 200, 50)

        # 채점 및 분석결과 열람 버튼
        self.button4 = QPushButton('채점 및 분석 결과 열람', self)
        self.button4.clicked.connect(self._ChooseExam_, 3)
        self.button4.setFixedSize(200, 50)
        self.button4.setGeometry(10, 190, 200, 50)

        # 채점 및 분석 결과 출력 버튼
        self.button5 = QPushButton('채점 및 분석 결과 출력', self)
        self.button5.clicked.connect(self._ChooseExam_, 4)
        self.button5.setFixedSize(200, 50)
        self.button5.setGeometry(10, 250, 200, 50)

        # 데이터
        self.myexam = ''

    # 모의고사 등록창 (모의고사 이름 입력)
    def _RegiExam_(self):
        self.regiExam = QDialog()
        # 모의고사 이름 입력칸
        self.regiExam.lineedit = QLineEdit(self.regiExam)
        self.regiExam.lineedit.move(10, 10)

        # 버튼 추가
        self.regiExam.btnDialog = QPushButton("등록하기", self.regiExam)
        self.regiExam.btnDialog.move(10, 50)
        self.regiExam.btnDialog.clicked.connect(self._RegiExamExecute_)

        # QDialog 세팅
        self.regiExam.setWindowTitle('시험지 등록')
        self.regiExam.setWindowModality(Qt.ApplicationModal)
        self.regiExam.resize(300, 200)
        self.regiExam.show()

    # 모의고사 등록 실행
    def _RegiExamExecute_(self):
        text = self.regiExam.lineedit.text()
        if text == '':
            self._PopErrorMessage_('no_input')
            return

        try:
            Register.register_exam(text)
        except WrongFileNameError as wrong_file_name_error:
            self.pop_error_message(wrong_file_name_error)
        except FileExistsError as file_exists_error:
            self.pop_error_message(file_exists_error)
        finally:
            self.regiExam.close()

    # 모의고사 선택
    def _ChooseExam_(self, purpose):
        self.chooseExam = QDialog()
        # 모의고사 고르기
        vbox = QVBoxLayout(self)
        listWidget = QListWidget()
        item_list = File.select_exam_folder()
        listWidget.clear()
        for i in item_list:
            listWidget.addItem(i)
        if purpose == 1:
            listWidget.itemDoubleClicked.connect(self._RegiSubmission_)
        elif purpose == 2:
            listWidget.itemDoubleClicked.connect(self._AnalyzeExam_)
        elif purpose == 3:
            listWidget.itemDoubleClicked.connect(self._ShowAnalysis_, 1)
        elif purpose == 4:
            listWidget.itemDoubleClicked.connect(self._ShowAnalysis_, 2)

        vbox.addWidget(listWidget)
        self.setLayout(vbox)

        # QDialog 세팅
        self.chooseExam.setWindowTitle('모의고사 선택')
        self.chooseExam.setLayout(vbox)
        self.chooseExam.setWindowModality(Qt.ApplicationModal)
        self.chooseExam.setGeometry(300, 300, 350, 250)
        self.chooseExam.show()

    # 학생 제출 답안 등록
    def _RegiSubmssion_(self, item):
        exam = item.text()
        Register.register_students_submission(exam)
        self.chooseExam.close()

    # 채점
    def _AnalyzeExam_(self, item):
        exam = item.text()
        try:
            Analyze.analyze_exam(exam)
            self.popMessage = QDialog()
            self._PopMessage_(1)
        except GetExamDataError as get_exam_data_error:
            self._PopErrorMessage_(get_exam_data_error)
        except GetStudentsDataError as get_students_data_error:
            self._PopErrorMessage_(get_students_data_error)
        except ExcelNotClosedError as excel_not_closed_error:
            self._PopErrorMessage_(excel_not_closed_error)
        except GetDataError as get_data_error:
            self._PopErrorMessage_(get_data_error)

        finally:
            self.chooseExam.close()

    # 열람 및 출력을 위한 세팅
    def _ShowAnalysis_(self, item, purpose):
        exam = item.text()

        try:
            showed_exam = Show.show_exam(exam)
            self.showAnalysis = QDialog()
            self._ShowAnalysisExecute_(purpose, exam, showed_exam)
        except NotScoredError as not_scored_error:
            not_scored_error.path = exam
            self._PopErrorMessage_(not_scored_error)
        finally:
            self.chooseExam.close()

    # 열람 및 출력 기본창
    def _ShowAnalysisExecute_(self, purpose, exam, showed_exam):
        self.myexam = exam

        # 창 기본 레이아웃 설정값
        self.showAnalysis.label = QLabel(showed_exam, self)
        self.showAnalysis.label.setAlignment(Qt.AlignTop)
        self.showAnalysis.layout = QVBoxLayout()
        self.showAnalysis.layout.addWidget(self.showAnalysis.label)
        self.showAnalysis.setLayout(self.showAnalysis.layout)

        # 시험 문제 분석
        btnDialog1 = QPushButton("시험 문제 분석", self.showAnalysis)
        btnDialog1.move(10, 320)
        btnDialog1.resize(200, 32)
        if purpose == 1:
            btnDialog1.clicked.connect(self._ShowExmaAnalysis_)
        elif purpose == 2:
            btnDialog1.clicked.connect(self._PrintExamAnalysis_)

        # 학생 전체 분석
        btnDialog2 = QPushButton("학생 전체 분석", self.showAnalysis)
        btnDialog2.move(10, 360)
        btnDialog2.resize(200, 32)
        if purpose == 1:
            btnDialog2.clicked.connect(self._ShowStudentAnalysis_)
        elif purpose == 2:
            btnDialog2.clicked.connect(self._PrintStudentAnalysis_)

        # 지점별 분석
        btnDialog3 = QPushButton("지점별 분석", self.showAnalysis)
        btnDialog3.move(10, 400)
        btnDialog3.resize(200, 32)
        btnDialog3.clicked.connect(self._ChooseBranch_, purpose)

        # 목적에 맞게 창 제목 지정
        if purpose == 1:
            self.showAnalysis.setWindowTitle('분석 결과 열람')
        elif purpose == 2:
            self.showAnalysis.setWindowTitle('분석 결과 출력')
        # 창 기본 설정값
        self.showAnalysis.setWindowModality(Qt.ApplicationModal)
        self.showAnalysis.resize(300, 460)
        self.showAnalysis.show()

    # 시험 문제 분석 열람
    def _ShowExmaAnalysis_(self):
        path = './data/' + self.myexam + '/채점결과/' + self.myexam + ' 채점 결과 문항 분석.xlsx'
        File.open_file(path)
        self.showAnalysis.close()

    # 학생 전체 분석 열람
    def _ShowStudentAnalysis_(self):
        path = './data/' + self.myexam + '/채점결과/' + self.myexam + ' 채점 결과 문항 분석.xlsx'
        File.open_file(path)
        self.showAnalysis.close()

    # 시험 문제 분석 출력
    def _PrintExamAnalysis_(self):
        Print.PrintExamInfo(self.myexam)
        self.showAnalysis.close()

    # 학생 전체 분석 출력
    def _PrintStudentAnalysis_(self):
        Print.PrintStudentInfo(self.myexam)
        self.showAnalysis.close()

    # 지점을 선택합니다. (for 지점별 분석 열람 & 지점별 분석 출력)
    def _ChooseBranch_(self, purpose):
        self.chooseBranch = QDialog()
        # 지점 고르기
        vbox = QVBoxLayout(self)
        listWidget = QListWidget()
        item_list = File.select_branch_foler(self.myexam)
        listWidget.clear()
        for i in item_list:
            listWidget.addItem(i)
        if purpose == 1:
            listWidget.itemDoubleClicked.connect(self._ShowBranchAnalysis_)
        elif purpose == 2:
            listWidget.itemDoubleClicked.connect(self._PrintBranchAnalysis_)

        vbox.addWidget(listWidget)
        self.setLayout(vbox)

        # 목적에 맞게 창 제목 지정
        if purpose == 1:
            self.chooseBranch.setWindowTitle('열람할 지점 선택')
        elif purpose == 2:
            self.chooseBranch.setWindowTitle('출력할 지점 선택')
        # 창 기본 설정값
        self.chooseBranch.setLayout(vbox)
        self.chooseBranch.setWindowModality(Qt.ApplicationModal)
        self.chooseBranch.setGeometry(300, 300, 350, 250)
        self.chooseBranch.show()

    # 해당 지점의 채점 결과 폴더를 띄웁니다.
    def _ShowBranchAnalysis_(self, item):
        branch_name = item.text()
        path = os.path.realpath('./data/' + self.myexam + '/채점결과/' + branch_name + '/')
        File.open_file(path, type='directory')
        self.chooseBranch.close()
        self.showAnalysis.close()

    # 해당 지점 내 모든 학생의 성적표를 출력합니다.
    def _PrintBranchAnalysis_(self, item):
        branch_name = item.text()
        Print.PrintBranchInfo(self.myexam, branch_name)
        self.chooseBranch.close()
        self.showAnalysis.close()

    # 정보창을 띄웁니다.
    def _PopMessage_(self, content):
        # 채점이 완료되었음을 알리는 정보창
        if content == 1:
            QMessageBox.information(self, "채점이 완료되었습니다.", "채점이 완료되었습니다.")

    # 오류 메세지창을 띄웁니다.
    def _PopErrorMessage_(self, error):
        # 모의고사 등록 페이지에서 모의고사 이름을 입력하지 않았을 경우
        if error == 'no_input':
            QMessageBox.warning(self, '모의고사 이름 오류', '모의고사 이름을 입력하지 않으셨습니다.')
        # 그 외의 경우
        else:
            QMessageBox.warning(self, error.type, error.path + ': ' + error.message)

# 실행코드
if __name__ == '__main__':
    if getattr(sys, 'frozen', False):
        os.chdir(os.path.dirname(sys.executable))
    else:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

# 확인된 문제점
'''
1. 중복된 모의고사 오류메세지 출력 관련

'''