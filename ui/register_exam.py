# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'register_exam.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_register_exam(object):
    def setupUi(self, register_exam):
        register_exam.setObjectName("register_exam")
        register_exam.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(register_exam)
        self.centralwidget.setObjectName("centralwidget")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(110, 260, 471, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(590, 260, 91, 31))
        self.pushButton.setObjectName("pushButton")
        register_exam.setCentralWidget(self.centralwidget)

        self.retranslateUi(register_exam)
        self.pushButton.clicked.connect(register_exam.registerExam)
        QtCore.QMetaObject.connectSlotsByName(register_exam)

    def retranslateUi(self, register_exam):
        _translate = QtCore.QCoreApplication.translate
        register_exam.setWindowTitle(_translate("register_exam", "시험지 등록"))
        self.lineEdit.setText(_translate("register_exam", "모의고사 이름을 입력하세요"))
        self.pushButton.setText(_translate("register_exam", "등록하기"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    register_exam = QtWidgets.QMainWindow()
    ui = Ui_register_exam()
    ui.setupUi(register_exam)
    register_exam.show()
    sys.exit(app.exec_())
