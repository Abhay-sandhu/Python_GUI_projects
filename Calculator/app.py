from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLabel, QLineEdit, QGridLayout, QVBoxLayout, QHBoxLayout, QVBoxLayout

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Calculator")
        self.resize(200,400)

        # Calculator objects
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.buttons = [
                '1','2','3','/',
                '4','5','6','*',
                '7','8','9','-',
                '0','.','=','+'
                ]
        self.button_dict = {}
        self.clear = QPushButton("Clear")
        self.delete = QPushButton("<")
        
        # Calculator Layout
        self.master_layout = QVBoxLayout()
        self.cl_del_row = QHBoxLayout()
        self.cl_del_row.addWidget(self.clear)
        self.cl_del_row.addWidget(self.delete)
        self.grid = QGridLayout()
        self.master_layout.addWidget(self.display)
        self.master_layout.addLayout(self.grid)
        self.master_layout.addLayout(self.cl_del_row)
        self.setLayout(self.master_layout)

        # button event handlers
        self.add_buttons_to_grid()
        self.clear.clicked.connect(self.button_clicked)
        self.delete.clicked.connect(self.button_clicked)


    def button_clicked(self):
        button = app.sender()
        txt = button.text() # type: ignore

        if txt == 'Clear':
            self.display.clear()
        elif txt == '<':
            self.display.backspace()
        elif txt == '=':
            try:
                expression = str(eval(self.display.text()))
                self.display.setText(expression)
            except Exception as e:
                self.display.setText(f"Error:{e}")
        elif self.display.text().startswith("Error"):
            self.display.setText(txt)
        else:
            self.display.insert(txt)


    def add_buttons_to_grid(self):
        row, col = 0, 0
        for btn_text in self.buttons:
            self.button_dict[btn_text] = QPushButton(btn_text)
            self.button_dict[btn_text].clicked.connect(self.button_clicked)
            self.grid.addWidget(self.button_dict[btn_text], row, col)
            col += 1
            if col > 3:
                row +=1
                col = 0
    
    def keyPressEvent(self, event):
        key = event.key()
        num_pad_keys = [Qt.Key_1, Qt.Key_2, Qt.Key_3, Qt.Key_4, Qt.Key_5, Qt.Key_6, Qt.Key_7, # type: ignore
                   Qt.Key_8, Qt.Key_9, Qt.Key_0, Qt.Key_Period, Qt.Key_Plus, Qt.Key_Minus, # type: ignore
                   Qt.Key_Asterisk, Qt.Key_Slash] # type: ignore
        result_keys = [Qt.Key_Equal, Qt.Key_Return, Qt.Key_Enter] # type: ignore
        if key in num_pad_keys:
            self.button_dict[chr(key)].click()
        elif key in result_keys:
            self.button_dict['='].click() 
        elif key in [Qt.Key_Backspace, Qt.Key_Delete]: # type: ignore
            self.delete.click()
        elif key == Qt.Key_C: # type: ignore
            self.clear.click()
        else:
            super().keyPressEvent(event)



# Execute application
app = QApplication([])
main = Calculator()
main.show()
app.exec_()