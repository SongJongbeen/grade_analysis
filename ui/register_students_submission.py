# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'register_students_submission.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_register_students_submission(object):
    def setupUi(self, register_students_submission):
        register_students_submission.setObjectName("register_students_submission")
        register_students_submission.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(register_students_submission)
        self.centralwidget.setObjectName("centralwidget")
        self.exam_list_register_students_submission = QtWidgets.QListWidget(self.centralwidget)
        self.exam_list_register_students_submission.setGeometry(QtCore.QRect(30, 90, 721, 421))
        self.exam_list_register_students_submission.setObjectName("exam_list_register_students_submission")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(200, 40, 371, 31))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(660, 530, 91, 31))
        self.pushButton.setObjectName("pushButton")
        register_students_submission.setCentralWidget(self.centralwidget)

        self.retranslateUi(register_students_submission)
        self.pushButton.clicked.connect(register_students_submission.registerStudentsSubmission)
        QtCore.QMetaObject.connectSlotsByName(register_students_submission)

    def retranslateUi(self, register_students_submission):
        _translate = QtCore.QCoreApplication.translate
        register_students_submission.setWindowTitle(_translate("register_students_submission", "제출 답안 등록"))
        self.label.setText(_translate("register_students_submission", "답안을 제출할 모의고사를 선택하세요"))
        self.pushButton.setText(_translate("register_students_submission", "등록하기"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    register_students_submission = QtWidgets.QMainWindow()
    ui = Ui_register_students_submission()
    ui.setupUi(register_students_submission)
    register_students_submission.show()
    sys.exit(app.exec_())
