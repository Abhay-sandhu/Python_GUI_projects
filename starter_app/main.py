from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout
from random import choice
import csv
# app settings
app = QApplication([])
main = QWidget()
main.setWindowTitle("Starter App")
main.resize(600,600)

# Create app objects
title_text = QLabel('Random Word Generator')
text1 = QLabel("1?")
text2 = QLabel("2?")
text3 = QLabel("3?")

button1 = QPushButton("btn1")
button2 = QPushButton("btn2")
button3 = QPushButton("btn3")

# Design app
master = QVBoxLayout()
row1 = QHBoxLayout()
row2 = QHBoxLayout()
row3 = QHBoxLayout()

row1.addWidget(title_text, alignment=Qt.AlignCenter) # type: ignore

row2.addWidget(text1, alignment=Qt.AlignCenter)  # type: ignore
row2.addWidget(text2, alignment=Qt.AlignCenter) # type: ignore
row2.addWidget(text3, alignment=Qt.AlignCenter) # type: ignore

row3.addWidget(button1, alignment=Qt.AlignCenter)
row3.addWidget(button2, alignment=Qt.AlignCenter)
row3.addWidget(button3, alignment=Qt.AlignCenter)

master.addLayout(row1)
master.addLayout(row2)
master.addLayout(row3)

main.setLayout(master)

# App Functionality
with open("random_words_4000.csv", 'r') as words:
    word_list = list(csv.reader(words, delimiter=','))
def random_word1():
    word = choice(word_list)[0]
    #print(word)
    text1.setText(word)

def random_word2():
    word = choice(word_list)[0]
    #print(word)
    text2.setText(word)

def random_word3():
    word = choice(word_list)[0]
    #print(word)
    text3.setText(word)

button1.clicked.connect(random_word1)
button2.clicked.connect(random_word2)
button3.clicked.connect(random_word3)

# execute app
main.show()
app.exec_()