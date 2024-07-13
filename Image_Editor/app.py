from PIL import Image, ImageFilter, ImageEnhance
import os
from os import listdir
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QKeyEvent, QPixmap, QImage
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLabel, QListWidget, \
                            QComboBox, QVBoxLayout, QHBoxLayout, QVBoxLayout, QFileDialog

class Image_Editor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Editor")
        self.resize(1200, 800)

        # App objects
        self.image_label = QLabel("NO IMAGE SELECTED")
        self.select_folder = QPushButton("Select Folder")
        self.image_list = QListWidget()
        self.filter_box = QComboBox()
        self.buttons = ["Left", "Right", "Mirror", "Sharpen", "B/W", "Color Saturation", "Contrast"]
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

        # Image Properties
        self.original_pic = None
        self.pic = None
        self.image_path = ''
        self.image_file = ''
        self.working_directory = ''
        self.save_folder = 'Image_Editor/edits'
        
        # Event handlers
        self.select_folder.clicked.connect(self.select_folder_clicked)
        self.image_list.currentRowChanged.connect(self.image_list_changed)
        #self.filter_box.currentTextChanged.
        self.button_dict['Left'].clicked.connect(self.left_rotate)
        self.button_dict['Right'].clicked.connect(self.right_rotate)
        self.button_dict['Mirror'].clicked.connect(self.mirror_image)
        self.button_dict['Sharpen'].clicked.connect(self.sharpen_image)
        self.button_dict['B/W'].clicked.connect(self.black_and_white)
        self.button_dict['Color Saturation'].clicked.connect(self.color_saturation)
        self.button_dict['Contrast'].clicked.connect(self.contrast_image)
        
    def add_buttons_to_column_and_filter_box(self):

        for btn_text in self.buttons:
            self.button_dict[btn_text] = QPushButton(btn_text)
            #self.button_dict[btn_text].setStyleSheet("QPushButton{font: 18pt Comic Sans MS; padding: 10px}")
            self.control_column.addWidget(self.button_dict[btn_text])
            self.filter_box.addItem(btn_text)


    def select_folder_clicked(self):
        self.working_directory = QFileDialog.getExistingDirectory()
        extensions = ['.png', '.jpg', '.jpeg', '.svg', '.bmp']
        self.image_list.clear()
        filtered_images = [file for file in listdir(self.working_directory) if file.endswith(tuple(extensions))]
        self.image_list.addItems(filtered_images)

    def image_list_changed(self):
        if self.image_list.currentItem() is not None:
            self.image_file = self.image_list.currentItem().text() # type: ignore
            self.load_image(self.image_file)
            self.show_image(self.image_path)

    def load_image(self, file):
        self.image_path = os.path.join(self.working_directory, file)
        self.original_pic = Image.open(self.image_path)
        self.pic = self.original_pic.copy()
        
    def show_image(self, path):
        self.image_label.hide()
        Image = QPixmap(path)
        Image.scaled(self.image_label.width(), self.image_label.height(), Qt.KeepAspectRatio) # type: ignore
        self.image_label.setPixmap(Image)
        self.image_label.show()

    def save_image(self):
        if self.pic is not None:
            save_path = self.save_folder
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            self.save_file = os.path.join(save_path, self.image_file)
            self.pic.save(self.save_file)
    

    # FILTERS
    def original_image(self):
        self.save_image()
        self.image_path = os.path.join(self.working_directory, self.image_file)
        self.show_image(self.image_path)

    def left_rotate(self):
        if self.pic is not None:
            self.pic = self.pic.rotate(-90)
            self.save_image()
            self.image_path = os.path.join(self.save_folder, self.image_file)
            self.show_image(self.image_path)
    
    def right_rotate(self):
        if self.pic is not None:
            self.pic = self.pic.rotate(90)
            self.save_image()
            self.image_path = os.path.join(self.save_folder, self.image_file)
            self.show_image(self.image_path)

    def mirror_image(self):
        if self.pic is not None:
            self.pic = self.pic.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            self.save_image()
            self.image_path = os.path.join(self.save_folder, self.image_file)
            self.show_image(self.image_path)

    def sharpen_image(self):
        if self.pic is not None:
            self.pic = ImageEnhance.Sharpness(self.pic).enhance(1.2)
            self.save_image()
            self.image_path = os.path.join(self.save_folder, self.image_file)
            self.show_image(self.image_path)

    def black_and_white(self):
        if self.pic is not None:
            self.pic = self.pic.convert('L')
            self.save_image()
            self.image_path = os.path.join(self.save_folder, self.image_file)
            self.show_image(self.image_path)

    def color_saturation(self):
        if self.pic is not None:
            self.pic = ImageEnhance.Color(self.pic).enhance(1.2)
            self.save_image()
            self.image_path = os.path.join(self.save_folder, self.image_file)
            self.show_image(self.image_path)

    def contrast_image(self):
        if self.pic is not None:
            self.pic = ImageEnhance.Contrast(self.pic).enhance(1.2)
            self.save_image()
            self.image_path = os.path.join(self.save_folder, self.image_file)
            self.show_image(self.image_path)

# Execute application
if __name__ == '__main__':
    app = QApplication([])
    main = Image_Editor()
    #main.setStyleSheet("QWidget{background-color: #f8f8f8}")
    main.show()
    app.exec_()