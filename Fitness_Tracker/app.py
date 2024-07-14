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
        self.cal_edit.setPlaceholderText("Enter Calories Burned")

        self.km_label = QLabel("KM")
        self.km_edit = QLineEdit()
        self.km_edit.setPlaceholderText("Enter Distance(KMs) ran")

        self.desc_label = QLabel("Desc")
        self.desc_edit = QLineEdit()
        self.desc_edit.setPlaceholderText("Enter Activity Description")

        self.dark_mode = QCheckBox("Dark Mode")

        self.add_button = QPushButton("Add to Table")
        self.delete_button = QPushButton("Delete selected row")

        self.submit_button = QPushButton("Update Graph")
        self.clear_button = QPushButton("Clear all")

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.subplots()

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

        self.master_layout.addLayout(self.column1, 30)
        self.master_layout.addLayout(self.column2, 70)
        self.setLayout(self.master_layout)

        self.event_handler()
        self.load_table()
        self.calc_calories()
        self.apply_styles()

    def event_handler(self):
        self.add_button.clicked.connect(self.add_btn)
        self.delete_button.clicked.connect(self.del_btn)
        self.submit_button.clicked.connect(self.calc_calories)
        self.clear_button.clicked.connect(self.clear_btn)
        self.dark_mode.stateChanged.connect(self.dark_mode_toggle)

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

    def clear_btn(self):
        self.date_edit.setDate(QDate.currentDate())
        self.cal_edit.clear()
        self.km_edit.clear()
        self.desc_edit.clear()
        self.table.setRowCount(0)
        self.figure.clear()
        self.canvas.draw()

    def calc_calories(self):
        distances = []
        calories = []

        query = QSqlQuery()
        query.prepare("SELECT Distance, Calories FROM fitness ORDER BY Calories ASC")
        if query.exec_():
            while query.next():
                distances.append(query.value(0))
                calories.append(query.value(1))
        try:
            min_calories = min(calories)
            max_calories = max(calories)
            normalized_calories = [
                (calorie - min_calories) / (max_calories - min_calories)
                for calorie in calories
            ]

            # plt.style.use('seaborn-v0_8-darkgrid')
            self.ax.scatter(
                distances,
                calories,
                c=normalized_calories,
                cmap="viridis",
                label="Data points",
            )
            self.ax.grid()
            # self.ax.figure.set_facecolor('#f0f0f0')
            cbar = self.ax.figure.colorbar(self.ax.collections[0], label="Normalized Calories")
            self.ax.set_xlabel("Distance (KM)")
            self.ax.set_ylabel("Calories")
            self.ax.set_title("Calories Burnt VS Distance Run")
            self.ax.legend()
            self.canvas.draw()
        except Exception as e:
            print(f"Error: {e}")
            QMessageBox.warning(self, "Warning", "Please enter some data first")

    def dark_mode_toggle(self):
        self.apply_styles()

    def apply_styles(self):
        if self.dark_mode.isChecked():
            self.setStyleSheet("""
                QWidget {
                    background-color: #1e1e1e;
                    color: #d3d3d3;
                }
                QLineEdit, QDateEdit, QLabel, QTableWidget,{
                    background-color: #2d2d2d;
                    color: #d3d3d3;
                    border: 1px solid #444444;
                    padding: 5px;
                    border-radius: 5px;
                }
                QHeaderView::section {
                    background-color: #3d3d3d;
                    color: #d3d3d3;
                    padding: 5px;
                    border: none;
                    border-bottom: 1px solid #444444;
                }
                QCheckBox {
                    background-color: #1e1e1e;
                    color: #d3d3d3;
                }
                QPushButton {
                background-color: #3aafa9;
                color: #d3d3d3;
                border: 1px solid #444444;
                padding: 5px;
                border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #2b7a78;
                }
            """)
            self.figure.patch.set_facecolor('#1e1e1e')
            self.ax.set_facecolor('#1e1e1e')
            self.ax.tick_params(colors='#d3d3d3')
            self.ax.yaxis.label.set_color('#d3d3d3')
            self.ax.xaxis.label.set_color('#d3d3d3')
            self.ax.title.set_color('#d3d3d3')
            self.ax.spines['top'].set_color('#d3d3d3')
            self.ax.spines['bottom'].set_color('#d3d3d3')
            self.ax.spines['left'].set_color('#d3d3d3')
            self.ax.spines['right'].set_color('#d3d3d3')
        else:
            self.setStyleSheet("""
                QWidget {
                    background-color: #f0f0f0;
                    color: #2c2c2c;
                }
                QLineEdit, QDateEdit, QLabel, QTableWidget{
                    background-color: #ffffff;
                    color: #2c2c2c;
                    border: 1px solid #cccccc;
                    padding: 5px;
                    border-radius: 5px;
                }
                QHeaderView::section {
                    background-color: #e0e0e0;
                    color: #2c2c2c;
                    padding: 5px;
                    border: none;
                    border-bottom: 1px solid #cccccc;
                }
                QCheckBox {
                    background-color: #f0f0f0;
                    color: #2c2c2c;
                }
                QPushButton {
                background-color: #3aafa9;
                color: #ffffff;
                border: 1px solid #cccccc;
                padding: 5px;
                border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #2b7a78;
                }
            """)
            self.figure.patch.set_facecolor('#f0f0f0')
            self.ax.set_facecolor('#f0f0f0')
            self.ax.tick_params(colors='#2c2c2c')
            self.ax.yaxis.label.set_color('#2c2c2c')
            self.ax.xaxis.label.set_color('#2c2c2c')
            self.ax.title.set_color('#2c2c2c')
            self.ax.spines['top'].set_color('#2c2c2c')
            self.ax.spines['bottom'].set_color('#2c2c2c')
            self.ax.spines['left'].set_color('#2c2c2c')
            self.ax.spines['right'].set_color('#2c2c2c')

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
