import sys
import os.path
import requests
import subprocess
from PIL import Image
from urllib.parse import urlparse
from urllib.request import urlretrieve
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QPixmap, QMouseEvent
from PyQt6.QtWidgets import QApplication, QFileDialog, QMainWindow, QPushButton, QWidget, QVBoxLayout, \
    QLabel, QHBoxLayout, QGridLayout, QLayout, QFrame, QRadioButton, QButtonGroup, QScrollArea, QMenu, QLineEdit, QMessageBox, QSpinBox



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        if not os.path.isdir("./Images"):
            os.mkdir("./Images")

        self.setWindowTitle('Gnome Change Wallpaper')
        self.showMaximized()
        self.setStyleSheet("background-color: #292929; color: white;")
        screen = QApplication.primaryScreen().geometry()

        container = QWidget()
        layout = QHBoxLayout()

        # Right Layout and Frame
        self.rightLayout = QGridLayout()
        self.rightLayout.setSpacing(20)
        self.rightLayout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)

        self.rightFrame = QFrame()
        self.rightFrame.setLayout(self.rightLayout)
        self.rightFrame.setFixedWidth(1300)

        self.scroll = QScrollArea()
        self.scroll.setWidget(self.rightFrame)
        self.scroll.setWidgetResizable(True)

        # Left Layout and Frame
        self.leftLayout = QVBoxLayout()
        self.leftLayout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        self.lblSelect = QLabel("Select a folder")
        self.lblSelect.setStyleSheet("font-size: 19px; font-weight: bold;")
        self.btnSelect = QPushButton()
        self.btnSelect.setFixedWidth(60)
        self.btnSelect.setIcon(QIcon("./Icons/folder-grey.svg"))
        self.btnSelect.setIconSize(QSize(28, 28))
        self.btnSelect.clicked.connect(self.get_folder)
        self.btnReload = QPushButton()
        self.btnReload.setFixedWidth(60)
        self.btnReload.setIcon(QIcon("./Icons/reload.png"))
        self.btnReload.setIconSize(QSize(28, 28))
        self.btnReload.clicked.connect(self.reload_folder)
        self.btnReload.setDisabled(True)

        self.selectLayout = QHBoxLayout()
        self.selectLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.selectLayout.addWidget(self.lblSelect)
        self.selectLayout.addWidget(self.btnSelect)
        self.selectLayout.addWidget(self.btnReload)

        selectframe = QFrame()
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

        currentConfLayout = QVBoxLayout()
        currentConf = QLabel("Current configuration\n")
        currentConf.setStyleSheet("font-weight: bold; font-size: 18px; margin-top: 90px;")
        self.currentDir = QLabel()
        self.currentTime = QLabel()
        currentConfLayout.addWidget(currentConf)
        currentConfLayout.addWidget(self.currentDir)
        currentConfLayout.addWidget(self.currentTime)
        currentConfFrame = QFrame()
        currentConfFrame.setLayout(currentConfLayout)

        self.getCurrentConf()

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
        buttonFrame.setStyleSheet("margin-top: 50px")

        self.leftLayout.addWidget(selectframe)
        self.leftLayout.addWidget(folderFrame)
        self.leftLayout.addWidget(timeFrame)
        self.leftLayout.addWidget(currentConfFrame)
        self.leftLayout.addWidget(buttonFrame)

        self.leftFrame = QFrame()
        self.leftFrame.setLayout(self.leftLayout)
        self.leftFrame.setFixedWidth(430)
        self.leftFrame.setFixedHeight(900)
        self.leftFrame.setStyleSheet("background-color: #323232; color: white;")

        # Add left and right layouts to the layout
        layout.addWidget(self.leftFrame)
        layout.addWidget(self.scroll)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        # Top layout and frame
        topLayout = QHBoxLayout()
        lblTip = QLabel("Enter an URL or select a folder")
        lblTip.setAlignment(Qt.AlignmentFlag.AlignLeft)
        lblTip.setFixedWidth(220)
        lblTip.setStyleSheet("color: blue; font-weight: bold; font-size: 16px;")
        self.lineUrl = QLineEdit()
        self.lineUrl.setPlaceholderText("Enter the URL of the image")
        self.lineUrl.setFixedWidth(1450)
        self.lineUrl.setFixedHeight(25)
        self.lineUrl.setStyleSheet("background-color: white; color: black; border-radius: 3px;")
        downButton = QPushButton("Set as Wallpaper")
        downButton.setFixedWidth(160)
        downButton.clicked.connect(self.download)

        topLayout.addWidget(lblTip)
        topLayout.addWidget(self.lineUrl, Qt.AlignmentFlag.AlignLeft)
        topLayout.addWidget(downButton, Qt.AlignmentFlag.AlignLeft)

        topFrame = QFrame()
        topFrame.setLayout(topLayout)

        # Add the top frame and the layout to the main layout
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(topFrame)
        mainLayout.addLayout(layout)

        container.setLayout(mainLayout)
        self.setCentralWidget(container)


    # Retrieve the current configuration from the file
    def getCurrentConf(self):
        if os.path.isfile("./changewallpaper"):
            f = open("./changewallpaper", "r")
            current = f.readline().split("'")
            self.currentDir.setText(fr" Folder '{current[1]}'")
            self.currentDir.setStyleSheet("color: white; font-weight: bold; font-size: 17px;")
            self.currentTime.setText(fr" Change every: {current[2]}")
            self.currentTime.setStyleSheet("color: white; font-weight: bold; font-size: 17px;")
            f.close()

    # Select the folder's pictures
    def get_folder(self):
        caption = "Select folder"
        initial_dir = ''
        folder_path = QFileDialog.getExistingDirectory(self, caption=caption, directory=initial_dir)

        if not folder_path:
            return False

        if len(os.listdir(folder_path)) == 0:
            subprocess.run(["python3", "./popup.py", "The folder is empty", "", "red"])
            return False

        p = subprocess.run(["zsh", "./listimagefiles.sh", folder_path], capture_output=True)

        if not p.returncode == 0:
            subprocess.run(['python3', "./popup.py", "The folder doesn't contain image files", "", "red"])
            return False

        self.loadfilefromfolder(folder_path)

    # Load the image files from the selected folder
    def loadfilefromfolder(self, folder_path):
        os.system("sync")
        while self.rightLayout.count():
            child = self.rightLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        subprocess.Popen(["python3", "dolist.py", folder_path])

        i = 0
        j = 0

        for file in os.listdir(folder_path):
            included_extensions = ['jpg', 'jpeg', 'bmp', 'png', 'gif', 'webp']
            if any(file.endswith(ext) for ext in included_extensions):

                self.lblImage = QLabel()
                base_width = 200
                img = Image.open(fr'{folder_path}/{file}')
                wpercent = (base_width / float(img.size[0]))
                hsize = int((float(img.size[1]) * float(wpercent)))
                img = img.resize((base_width, hsize), Image.Resampling.LANCZOS)
                img.save(fr'./Images/{file}')

                img = QPixmap(fr'./Images/{file}')
                self.lblImage.setPixmap(img)
                self.lblImage.testo = str(fr".{folder_path}/{file}")
                self.lblImage.mousePressEvent = self.pictureClicked
                self.lblImage.setStyleSheet("border: 1px solid #EEEEEE; border-radius: 5px;")

                item = QHBoxLayout()
                item.addWidget(self.lblImage)
                self.rightLayout.addLayout(item, i, j)

                if j == 5:
                    j = 0
                    i = i + 1
                else:
                    j = j+1

        self.lblFolder.setText(str(folder_path))
        self.rightFrame.setStyleSheet("background-color: #292929; border: 0px solid black; border-radius: 10px; margin-left: 10px;")
        self.btnReload.setDisabled(False)

    def reload_folder(self):
        self.loadfilefromfolder(self.lblFolder.text())

    # Retrieve the filename of the clicked picture
    def pictureClicked(self, event):
        if QMouseEvent.button(event) == Qt.MouseButton.RightButton:

            # Add a check if testo exists and is not null
            filename = self.childAt(QMouseEvent.globalPosition(event).toPoint()).testo
            self.showPopup(filename, QMouseEvent.globalPosition(event).toPoint())
        elif QMouseEvent.button(event) == Qt.MouseButton.LeftButton:
            pass

    # Display the popup menu
    def showPopup(self, filename, pos):
        self.fileimg = filename
        self.context_menu = QMenu(self)
        action1 = self.context_menu.addAction("Set as wallpaper")
        action2 = self.context_menu.addAction("View")
        action3 = self.context_menu.addAction("Delete")

        action1.triggered.connect(self.setWallpaper)
        action2.triggered.connect(self.View)
        action3.triggered.connect(self.Delete)

        self.context_menu.exec(pos)

    # Set the selected picture as background
    def setWallpaper(self):
        print(self.fileimg)
        uri = fr"file:///{self.fileimg}"
        print(uri)
        p = subprocess.run(["/usr/bin/gsettings", "set", "org.gnome.desktop.background", "picture-uri", fr"'{uri}'"],
                           capture_output=True)

    # Open the selected picture in the viewer
    def View(self, event):
        ext = str(self.fileimg).split(".")[2]
        name = str(self.fileimg).split(".")[1]
        subprocess.Popen(["python3", "./viewer.py", fr"{name}.{ext}", self.lblFolder.text()])

    # Delete the selected picture from the hard disk
    def Delete(self):
        ext = str(self.fileimg).split(".")[2]
        name = str(self.fileimg).split(".")[1]
        filename = fr"{name}.{ext}"

        dlg = QMessageBox(self)
        dlg.setWindowTitle("Delete file")
        dlg.setStyleSheet("background-color: #292929; color: white;")
        dlg.setText(fr"Are you sure you want to delete the file '{filename}' from the disk?")
        dlg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        dlg.setIcon(QMessageBox.Icon.Critical)
        button = dlg.exec()

        if button == QMessageBox.StandardButton.Yes:
            subprocess.run(["mv", filename, fr"{os.environ['HOME']}/.local/share/Trash/files"])
            subprocess.run(["python3", "./popup.py", "The file has been moved to the Trash", "", "lightGreen"])
        else:
            pass

    # Download the picture file from the entered URL
    def download(self):
        url = self.lineUrl.text()
        if url == "":
            subprocess.run(["python3", "popup.py", "Enter a valid URL", "", "lightGreen"])
            return False

        parsedurl = urlparse(url)
        if not parsedurl.scheme == 'http' and not parsedurl.scheme == 'https' and not parsedurl.scheme == 'ftp':
            subprocess.run(["python3", "popup.py", fr"The URL is not valid", "", "red"])
            return False

        try:
            req = requests.get(url)
            if not req.status_code == 200:
                subprocess.run(["python3", "./popup.py", "Error downloading the file", fr"Server response: {req.status_code}", "red"])
                return False
        except:
            subprocess.run(
                ["python3", "./popup.py", f"Check the internet connection and try again", "", "red"])
            return False


        print(parsedurl.path.split("/"))
        for name in parsedurl.path.split("/"):
            pass

        urlretrieve(url, name)
        subprocess.run(["mv", fr"./{name}", fr"{os.environ['HOME']}/{name}"])

        subprocess.run(["zsh", "./clearcrontab.sh"])

        self.currentDir.setText("")
        self.currentTime.setText("")

        uri = fr"file://{os.environ['HOME']}/{name}"
        p = subprocess.run(["/usr/bin/gsettings", "set", "org.gnome.desktop.background", "picture-uri", fr"'{uri}'"], capture_output=True)
        q = subprocess.run(["/usr/bin/gsettings", "set", "org.gnome.desktop.background", "picture-uri-dark", fr"'{uri}'"],capture_output=True)

        while self.rightLayout.count():
            child = self.rightLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        self.lblImage = QLabel()
        img = QPixmap(fr"{os.environ['HOME']}/{name}")
        self.lblImage.setPixmap(img)
        item = QHBoxLayout()
        item.addWidget(self.lblImage)
        self.rightLayout.addLayout(item, 0, 0)

        subprocess.run(["python3", "popup.py", fr"The image: {name} ", "has been set as wallpaper", "lightGreen"])


    # Apply the settings (selected folder and interval)
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
        self.currentDir.setText(fr"Folder '{self.lblFolder.text()}'")
        self.currentTime.setText(fr"Change every: {text}")
        subprocess.run(["python3", "./popup.py", "The wallpaper will be updated every:", text, "lightGreen"])

    # Display the about popup
    def showInfo(self):
        subprocess.run(["python3", "info.py"])


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
