import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

class Ui_MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(620, 200)

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        # Warning_button
        self.warning_button = QtWidgets.QPushButton(self.centralwidget)
        self.warning_button.setGeometry(QtCore.QRect(260, 90, 100, 30))
        self.warning_button.setObjectName("warning_button")
        self.warning_button.setText("Warning")
        self.warning_button.clicked.connect(self.Warning_event)

        self.show()

    # Warning 버튼 클릭 이벤트
    def Warning_event(self):
        QMessageBox.warning(self, 'Warning Title', 'Warning Message')


import sys
app = QtWidgets.QApplication(sys.argv)
ui = Ui_MainWindow()
sys.exit(app.exec_())