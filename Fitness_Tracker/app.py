import matplotlib.pyplot as plt
import sys
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import (
    QWidget,
    QApplication,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QDateEdit,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QCheckBox,
    QMessageBox,
)


class Fitness_Tracker(QWidget):
    def __init__(self):
        super().__init__()
        self.init_UI()

    def init_UI(self):
        self.setWindowTitle("Fitness Tracker")
        self.resize(1200, 1000)

        # App Objects
        self.date_label = QLabel("Date")
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())

        self.cal_label = QLabel("Cal")
        self.cal_edit = QLineEdit()

        self.km_label = QLabel("KM")
        self.km_edit = QLineEdit()

        self.desc_label = QLabel("Desc")
        self.desc_edit = QLineEdit()

        self.dark_mode = QCheckBox("Dark Mode")

        self.add_button = QPushButton("Add")
        self.delete_button = QPushButton("Delete")

        self.submit_button = QPushButton("Submit")
        self.clear_button = QPushButton("Clear")

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Date", "Calories", "Distance (KM)", "Description"]
        )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # App Layout
        self.master_layout = QHBoxLayout()
        self.column1 = QVBoxLayout()
        self.column2 = QVBoxLayout()
        self.row11 = QHBoxLayout()
        self.row12 = QHBoxLayout()
        self.row13 = QHBoxLayout()
        self.row14 = QHBoxLayout()
        self.row15 = QHBoxLayout()
        self.row16 = QHBoxLayout()
        self.row17 = QHBoxLayout()

        self.row11.addWidget(self.date_label)
        self.row11.addWidget(self.date_edit)

        self.row12.addWidget(self.cal_label)
        self.row12.addWidget(self.cal_edit)

        self.row13.addWidget(self.km_label)
        self.row13.addWidget(self.km_edit)

        self.row14.addWidget(self.desc_label)
        self.row14.addWidget(self.desc_edit)

        self.row15.addWidget(self.dark_mode)

        self.row16.addWidget(self.add_button)
        self.row16.addWidget(self.delete_button)

        self.row17.addWidget(self.submit_button)
        self.row17.addWidget(self.clear_button)

        self.column1.addLayout(self.row11)
        self.column1.addLayout(self.row12)
        self.column1.addLayout(self.row13)
        self.column1.addLayout(self.row14)
        self.column1.addLayout(self.row15)
        self.column1.addLayout(self.row16)
        self.column1.addLayout(self.row17)

        self.column2.addWidget(self.canvas, 70)
        self.column2.addWidget(self.table, 30)

        self.master_layout.addLayout(self.column1, 25)
        self.master_layout.addLayout(self.column2, 75)
        self.setLayout(self.master_layout)

        self.event_handler()
        self.load_table()

    def event_handler(self):
        self.add_button.clicked.connect(self.add_btn)
        self.delete_button.clicked.connect(self.del_btn)
        self.submit_button.clicked.connect(self.submit_btn)
        self.clear_button.clicked.connect(self.clear_btn)

    def load_table(self):
        self.table.setRowCount(0)
        query = QSqlQuery("SELECT * FROM fitness")
        row = 0
        while query.next():
            id = query.value(0)
            date = query.value(1)
            calories = query.value(2)
            distance = query.value(3)
            description = query.value(4)

            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(id)))
            self.table.setItem(row, 1, QTableWidgetItem(date))
            self.table.setItem(row, 2, QTableWidgetItem(str(calories)))
            self.table.setItem(row, 3, QTableWidgetItem(str(distance)))
            self.table.setItem(row, 4, QTableWidgetItem(description))
            row += 1

    def add_btn(self):
        try:
            date = self.date_edit.date().toString("yyyy-MM-dd")
            calories = float(self.cal_edit.text())
            distance = float(self.km_edit.text())
            description = self.desc_edit.text()
        except ValueError:
            QMessageBox.warning(
                self, "Warning", "Invalid input. Please enter numeric values."
            )
            return

        query = QSqlQuery()
        query.prepare(
            """
            INSERT INTO fitness (Date, Calories, Distance, Description) 
            VALUES (:date,:cal,:km,:desc)
            """
        )
        query.bindValue(":date", date)
        query.bindValue(":cal", calories)
        query.bindValue(":km", distance)
        query.bindValue(":desc", description)
        if query.exec_():
            # QMessageBox.information(self, "Addition Successful", "Data added successfully")
            self.load_table()

        self.load_table()

    def del_btn(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Warning", "No expense selected.")
            return
        if self.table.item(selected_row, 0):
            query = QSqlQuery()
            query.prepare("DELETE FROM fitness WHERE id = :ID")
            query.bindValue(":ID", self.table.item(selected_row, 0).text())
            if query.exec_():
                # QMessageBox.information(self, "Delete Successful", "Data deleted successfully")
                self.load_table()

    def submit_btn(self):
        pass

    def clear_btn(self):
        self.date_edit.setDate(QDate.currentDate())
        self.cal_edit.clear()
        self.km_edit.clear()
        self.desc_edit.clear()
        self.table.setRowCount(0)
        self.figure.clear()
        self.canvas.draw()


# Database Instantiation and Connection
db = QSqlDatabase.addDatabase("QSQLITE")
db.setDatabaseName("fitness_tracker.db")
if not db.open():
    print("Error: Failed to connect to the database.")
    sys.exit(1)
query = QSqlQuery()
query.prepare(
    """
    CREATE TABLE IF NOT EXISTS fitness (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Date TEXT,
        Calories REAL,
        Distance REAL,
        Description TEXT
    )
    """
)
query.exec_()


if __name__ == "__main__":
    app = QApplication([])
    window = Fitness_Tracker()
    window.show()
    app.exec_()
