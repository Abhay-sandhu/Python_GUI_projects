from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout

# app settings
app = QApplication([])
main = QWidget()
main.setWindowTitle("Starter App")
main.resize(600,600)

# Create app objects

# execute app
main.show()
app.exec_()