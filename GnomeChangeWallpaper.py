import sys
import os.path
import subprocess
from PIL import Image
from PyQt6.QtCore import Qt, QSize, QPoint
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QApplication, QFileDialog, QMainWindow, QPushButton, QWidget, QVBoxLayout, \
    QLabel, QHBoxLayout, QGridLayout, QLayout, QFrame, QRadioButton, QButtonGroup, QScrollArea



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Gnome Change Wallpaper')
        self.setFixedWidth(1600)
        self.setFixedHeight(900)
        self.setStyleSheet("background-color: #292929; color: white;")
        screen = QApplication.primaryScreen().geometry()
        point = QPoint()
        point.setX(int((screen.width()-1600)/2))
        point.setY(int((screen.height()-900)/2))
        self.move(point)

        container = QWidget()
        layout = QHBoxLayout()

        # Right Layout
        self.rightLayout = QGridLayout()
        self.rightLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.rightLayout.setSpacing(20)
        self.rightLayout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)

        self.rightFrame = QFrame()
        self.rightFrame.setLayout(self.rightLayout)
        self.rightFrame.setFixedWidth(1100)
        self.rightFrame.setFixedWidth(900)

        self.scroll = QScrollArea()
        #self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setWidget(self.rightFrame)
        self.scroll.setWidgetResizable(True)


        # Left Layout
        self.leftLayout = QVBoxLayout()
        self.leftLayout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        self.lblSelect = QLabel("Select a folder")
        self.lblSelect.setStyleSheet("font-size: 19px; font-weight: bold;")
        self.btnSelect = QPushButton()
        self.btnSelect.setFixedWidth(60)
        # self.btnSelect.setIcon(QIcon.fromTheme('folder-open'))
        self.btnSelect.setIcon(QIcon("./Icons/folder-grey.svg"))
        self.btnSelect.setIconSize(QSize(28, 28))
        self.btnSelect.clicked.connect(self.get_folder)

        self.selectLayout = QHBoxLayout()
        self.selectLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.selectLayout.addWidget(self.lblSelect)
        self.selectLayout.addWidget(self.btnSelect)

        selectframe = QFrame()
        #selectframe.setStyleSheet("margin-bottom: 10px;")
        selectframe.setLayout(self.selectLayout)

        self.folderLayout = QHBoxLayout()
        self.folderLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        folderFrame = QFrame()
        folderFrame.setLayout(self.folderLayout)
        folderFrame.setStyleSheet("margin-bottom: 30px;")
        self.lblFolder = QLabel()
        self.lblFolder.setStyleSheet("font-size: 14px;")
        self.folderLayout.addWidget(self.lblFolder)

        timeLayout = QVBoxLayout()
        lblChange = QLabel("Change the wallpaper every\n")
        lblChange.setStyleSheet("font-weight: bold; font-size: 18px")
        timeLayout.addWidget(lblChange)

        buttonGroup = QButtonGroup()
        self.radio1min = QRadioButton("1 min")
        self.radio5min = QRadioButton("5 mim")
        self.radio15min = QRadioButton("15 mim")
        self.radio30min = QRadioButton("30 min")
        self.radio1h = QRadioButton("1 hour")
        self.radio3h = QRadioButton("3 hours")
        self.radio6h = QRadioButton("6 hours")
        self.radio12h = QRadioButton("12 hours")
        self.radio1d = QRadioButton("1 day")
        self.radio1w = QRadioButton("1 Week")

        buttonGroup.addButton(self.radio1min)
        buttonGroup.addButton(self.radio5min)
        buttonGroup.addButton(self.radio15min)
        buttonGroup.addButton(self.radio30min)
        buttonGroup.addButton(self.radio1h)
        buttonGroup.addButton(self.radio3h)
        buttonGroup.addButton(self.radio6h)
        buttonGroup.addButton(self.radio12h)
        buttonGroup.addButton(self.radio1d)
        buttonGroup.addButton(self.radio1w)

        timeLayout.addWidget(self.radio1min)
        timeLayout.addWidget(self.radio5min)
        timeLayout.addWidget(self.radio15min)
        timeLayout.addWidget(self.radio30min)
        timeLayout.addWidget(self.radio1h)
        timeLayout.addWidget(self.radio3h)
        timeLayout.addWidget(self.radio6h)
        timeLayout.addWidget(self.radio12h)
        timeLayout.addWidget(self.radio1d)
        timeLayout.addWidget(self.radio1w)

        timeFrame = QFrame()
        timeFrame.setLayout(timeLayout)

        buttonLayout = QHBoxLayout()
        btnApply = QPushButton("Apply")
        btnApply.setFixedWidth(100)
        btnApply.setStyleSheet("border: 3px solid lightGrey; border-radius: 5px; background-color: #e8e8e8; color: black;")
        btnApply.clicked.connect(self.apply)
        self.statusLabel = QLabel()
        self.statusLabel.setFixedWidth(220)
        btnInfo = QPushButton("?")
        btnInfo.setFixedWidth(30)
        btnInfo.clicked.connect(self.showInfo)
        buttonLayout.addWidget(btnApply, alignment=Qt.AlignmentFlag.AlignLeft)
        buttonLayout.addWidget(self.statusLabel, alignment=Qt.AlignmentFlag.AlignLeft)
        buttonLayout.addWidget(btnInfo, alignment=Qt.AlignmentFlag.AlignRight)
        buttonLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        buttonFrame = QFrame()
        buttonFrame.setLayout(buttonLayout)
        buttonFrame.setStyleSheet("margin-top: 160px")

        self.leftLayout.addWidget(selectframe)
        self.leftLayout.addWidget(folderFrame)
        self.leftLayout.addWidget(timeFrame)
        self.leftLayout.addWidget(buttonFrame)

        self.leftFrame = QFrame()
        self.leftFrame.setLayout(self.leftLayout)
        self.leftFrame.setFixedWidth(400)
        self.leftFrame.setFixedHeight(900)
        self.leftFrame.setStyleSheet("background-color: #323232; color: white;")

        layout.addWidget(self.leftFrame)
        layout.addWidget(self.scroll)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        container.setLayout(layout)
        self.setCentralWidget(container)

    def get_folder(self):
        caption = "Select folder"
        initial_dir = ''
        folder_path = QFileDialog.getExistingDirectory(self, caption=caption, directory=initial_dir)

        i = 0
        j = 0

        for file in os.listdir(folder_path):

            lblImage = QLabel()
           # pixmap = QPixmap(rf"{folder_path}/{file}")
           # lblImage.setPixmap(pixmap.scaledToWidth(200, Qt.TransformationMode.FastTransformation))

            img = Image.open(fr'{folder_path}/{file}')
            img = img.resize((200, 200), Image.HAMMING)
            img.save(fr'./Images/{file}')

            img = QPixmap(fr'./Images/{file}')
            lblImage.setPixmap(img)

            item = QHBoxLayout()
            item.addWidget(lblImage)
            self.rightLayout.addLayout(item, i, j)

            if j == 4:
                j = 0
                i = i + 1
            else:
                j = j+1

        self.lblFolder.setText(str(folder_path))
        self.rightFrame.setStyleSheet("background-color: #292929; border: 2px solid black; border-radius: 10px;")

    def apply(self):
        if self.lblFolder.text() == '':
            self.statusLabel.setText("Select a folder")
            self.statusLabel.setStyleSheet("color: red;")
            return

        if self.radio1min.isChecked() is False and self.radio5min.isChecked() is False and  self.radio15min.isChecked() is False and self.radio30min.isChecked() is False and self.radio1h.isChecked() is False \
                and self.radio3h.isChecked() is False and self.radio6h.isChecked() is False and self.radio12h.isChecked() is False \
                and self.radio1d.isChecked() is False and self.radio1w.isChecked() is False:
            self.statusLabel.setText("Select a period of time")
            self.statusLabel.setStyleSheet("color: red;")
            return

        if self.radio1min.isChecked():
            time = 60
            text = "1 min"
        if self.radio5min.isChecked():
            time = 5
            text = "5 min"
        if self.radio15min.isChecked():
            time = 15
            text = "15 min"
        if self.radio30min.isChecked():
            time = 30
            text = "30 min"
        elif self.radio1h.isChecked():
            time = 1
            text = "1 hour"
        elif self.radio3h.isChecked():
            time = 3
            text = "3 hours"
        elif self.radio6h.isChecked():
            time = 6
            text = "6 hours"
        elif self.radio12h.isChecked():
            time = 12
            text = "12 hours"
        elif self.radio1d.isChecked():
            time = 24
            text = "1 day"
        elif self.radio1w.isChecked():
            time = 148
            text = "1 week"

        f = open("./changewallpaper", "w")
        f.write(fr"'{self.lblFolder.text()}' {text}")
        f.close()

        if os.path.isfile('./fileList'):
            os.unlink('./fileList')

        subprocess.Popen(["python3", "./setcron.py"])
        subprocess.run(["python3", "./popup.py", text])

    def showInfo(self):
        subprocess.run(["python3", "info.py"])

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
