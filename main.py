from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QPainter, QColor
from PyQt5 import uic
import sys
from random import randint

SCREEN_SIZE = [400, 450]


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('UI.ui', self)
        self.flag = False
        # p = QPushButton()
        # p.clicked()
        self.pushButton.clicked.connect(self.draw)

    def draw(self):

        self.flag = True
        self.update()
        # self.paintEvent(self.event)

    def paintEvent(self, event):
        if self.flag:
            qp = QPainter()
            qp.begin(self)
            qp.setBrush(QColor(255, 255, 0))
            # self.x, self.y = SCREEN_SIZE[0] // 2 - self.side // 2, SCREEN_SIZE[1] - self.side - 20
            self.drawSquare(qp)
            qp.end()

    def drawSquare(self, qp):
        r = randint(50, 350)
        qp.drawEllipse(100, 100, r, r)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())
