import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import (
    QWidget,
    QApplication,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
)

class Fitness_Tracker(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fitness Tracker")
        self.resize(1200, 1000)

        # App Objects
        # App Layout
        # Event Handlers
        # Database Creation and Operations
        # Plot Data with mpl

if __name__ == "__main__":
    app = QApplication([])
    window = Fitness_Tracker()
    window.show()
    app.exec_()