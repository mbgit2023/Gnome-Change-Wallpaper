# Simple image viewer

import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QHBoxLayout, QWidget, QPushButton


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(sys.argv[1])
        self.setFixedWidth(1500)
        self.setFixedHeight(900)
        self.setStyleSheet("background-color: #292929;")

        self.imgfile = sys.argv[1]

        layout = QHBoxLayout()
        lbutton = QPushButton("<-")
        lbutton.clicked.connect(self.prev)
        rbutton = QPushButton("->")
        rbutton.clicked.connect(self.next)
        lbutton.setFixedWidth(100)
        rbutton.setFixedWidth(100)
        self.image = QLabel()
        self.image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.img = QPixmap(self.imgfile)
        self.image.setPixmap(self.img)
        layout.addWidget(lbutton)
        layout.addWidget(self.image)
        layout.addWidget(rbutton)

        f = open("./foldercontent.lst", "r")
        self.list = []
        while f.readline():
            self.list.append(f.readline().split("\n")[0])
        f.close()

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    # Display the previous image in the list
    def prev(self):
        for name in self.imgfile.split("/"):
            pass
        name = name
        current = self.list.index(name)

        if not current == 0:
            self.imgfile = fr"{sys.argv[2]}/{self.list[current - 1]}"
        else:
            index = len(self.list) - 1
            self.imgfile = fr"{sys.argv[2]}/{self.list[index]}"
        self.img = QPixmap(self.imgfile)
        self.image.setPixmap(self.img)
        self.setWindowTitle(self.imgfile)


    # Display the next image in the list
    def next(self):
        for name in self.imgfile.split("/"):
            pass

        current = self.list.index(name)
        if not current == len(self.list)-1:
            self.imgfile = fr"{sys.argv[2]}/{self.list[current + 1]}"
        else:
            self.imgfile = fr"{sys.argv[2]}/{self.list[0]}"

        self.img = QPixmap(self.imgfile)
        self.image.setPixmap(self.img)
        self.setWindowTitle(self.imgfile)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()