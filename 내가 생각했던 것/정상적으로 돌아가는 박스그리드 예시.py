import sys

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout


class QtGUI(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Appia Qt GUI")

        self.resize(300, 300)

        self.intialL1 = 'First Label'

        self.intialL2 = 'Two Label'

        label1 = QLabel(self.intialL1, self)

        # label1.move(10,10)

        label2 = QLabel(self.intialL2, self)

        # label2.move(10, 50)

        button = QPushButton('Button', self)

        # button.move(50, 110)

        button.clicked.connect(lambda: self.print_label(button, label1))

        button1 = QPushButton('Button1', self)

        # button1.move(50, 140)

        button1.clicked.connect(lambda: self.print_label(button1, label2))

        qhbox = QHBoxLayout()

        qhbox.addStretch(2)

        qhbox.addWidget(label1)

        qhbox.addWidget(button)

        qhbox.addStretch(1)

        qhbox1 = QHBoxLayout()

        qhbox1.addStretch(1)

        qhbox1.addWidget(label2)

        qhbox1.addWidget(button1)

        qhbox1.addStretch(2)

        qvbox = QVBoxLayout()

        qvbox.addStretch(1)

        qvbox.addLayout(qhbox)

        qvbox.addLayout(qhbox1)

        qvbox.addStretch(2)

        self.setLayout(qvbox)

        self.show()

    def print_label(self, vbutton, vlabel):
        vlabel.setText(vbutton.text())


if __name__ == '__main__':
    app = QApplication(sys.argv)

    ex = QtGUI()

    app.exec_()
