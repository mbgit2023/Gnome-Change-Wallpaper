import os
import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox

# Display a confirmation dialog to delete or not the picture
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        dlg = QMessageBox(self)
        dlg.setWindowTitle("Delete file")
        dlg.setStyleSheet("background-color: #292929; color: white;")
        dlg.setText("Are you sure you want to delete the file from the disk?")
        dlg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        dlg.setIcon(QMessageBox.Icon.Critical)
        button = dlg.exec()

        self.setCentralWidget(dlg)

        if button == QMessageBox.StandardButton.Yes:
            os.unlink(sys.argv[1])
        else:
            pass


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()