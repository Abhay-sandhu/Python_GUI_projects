from email.mime import image
from PIL import Image, ImageFilter, ImageEnhance
import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QKeyEvent, QPixmap
from PyQt5.QtWidgets import (
    QWidget,
    QApplication,
    QPushButton,
    QLabel,
    QListWidget,
    QComboBox,
    QVBoxLayout,
    QHBoxLayout,
    QVBoxLayout,
    QFileDialog,
)




class Image_Editor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Editor")
        self.resize(1200, 800)












# Execute application
if __name__ == "__main__":
    app = QApplication([])
    main = Image_Editor()
    main.show()
    app.exec_()
