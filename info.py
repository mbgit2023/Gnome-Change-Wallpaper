import sys
from PIL import Image
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QLabel



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Changes applied successfully')
        self.setFixedWidth(350)
        self.setFixedHeight(300)
        self.setStyleSheet("background-color: #292929; color: lightGreen;")
        screen = QApplication.primaryScreen().geometry()
        point = QPoint()
        point.setX(int(screen.width()/2-200))
        point.setY(int(screen.height()/2-200))
        self.move(point)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        lblInfo = QLabel("\nGnome Change Wallpaper v.1\n")
        lblInfo.setStyleSheet("font-weight: bold; font-size: 20px; color: blue;")
        lblBy = QLabel("@ 2024 CopyUp by\n")
        lblBy.setStyleSheet("font-weight: bold; font-size: 17px; color: blue;")
        lblAuthor = QLabel()
        pixmap = QPixmap("Icons/author.png")
        lblAuthor.setPixmap(pixmap)

        layout.addWidget(lblInfo, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(lblBy, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(lblAuthor, alignment=Qt.AlignmentFlag.AlignHCenter)
        container = QWidget()

        container.setLayout(layout)
        self.setCentralWidget(container)

    def close(self):
        app.exit(0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()