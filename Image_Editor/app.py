from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QKeyEvent
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLabel, QListWidget, QComboBox, QVBoxLayout, QHBoxLayout, QVBoxLayout

class Image_Editor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Editor")
        self.resize(1200, 800)

        # App objects
        self.image_label = QLabel("NO IMAGE SELECTED")
        self.image_label.setBaseSize(800, 600)
        self.select_folder = QPushButton("Select Folder")
        self.image_list = QListWidget()
        self.filter_box = QComboBox()
        self.buttons = ["Left", "Right", "Mirror", "Sharpen", "B/W", "Color", "Contrast"]
        self.button_dict = {}
        # App Layout
        self.master_layout = QHBoxLayout()
        self.control_column = QVBoxLayout()
        self.image_column = QVBoxLayout()

        self.control_column.addWidget(self.select_folder)
        self.control_column.addWidget(self.image_list)
        self.control_column.addWidget(self.filter_box)
        self.filter_box.addItem("Original")
        self.add_buttons_to_column_and_filter_box()
        self.image_column.addWidget(self.image_label, alignment=Qt.AlignCenter)
        self.master_layout.addLayout(self.control_column, 20)
        self.master_layout.addLayout(self.image_column, 80)
        self.setLayout(self.master_layout)

    def add_buttons_to_column_and_filter_box(self):

        for btn_text in self.buttons:
            self.button_dict[btn_text] = QPushButton(btn_text)
            #self.button_dict[btn_text].setStyleSheet("QPushButton{font: 18pt Comic Sans MS; padding: 10px}")
            self.control_column.addWidget(self.button_dict[btn_text])
            self.filter_box.addItem(btn_text)




# Execute application
if __name__ == '__main__':
    app = QApplication([])
    main = Image_Editor()
    #main.setStyleSheet("QWidget{background-color: #f8f8f8}")
    main.show()
    app.exec_()