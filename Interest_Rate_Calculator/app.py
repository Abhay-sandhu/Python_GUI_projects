import csv, os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import (
    QWidget,
    QApplication,
    QPushButton,
    QLabel,
    QMessageBox,
    QFileDialog,
    QLineEdit,
    QCheckBox,
    QTreeView,
    QVBoxLayout,
    QHBoxLayout,
    QVBoxLayout,
)


class Interest_Rate_Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Editor")
        self.resize(1000, 800)

        # App Objects
        self.interest_rate = QLineEdit()
        self.interest_rate.setText("10")
        self.investment_edit = QLineEdit()
        self.investment_edit.setText("10000")
        self.time_edit = QLineEdit()
        self.time_edit.setText("10")
        self.dark_mode = QCheckBox()
        self.dark_mode.setText("Dark Mode")

        self.interest_viewer = QTreeView()
        self.interest_model = QStandardItemModel()
        self.interest_viewer.setModel(self.interest_model)
        self.interest_model.setColumnCount(2)
        self.interest_model.setHorizontalHeaderLabels(["Years", "Interest"])

        self.calculate = QPushButton("Calculate")
        self.reset = QPushButton("Reset")
        self.save = QPushButton("Save")
        self.save.setVisible(False)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        # App Layout
        self.master_layout = QVBoxLayout()
        self.row1 = QHBoxLayout()
        self.row2 = QHBoxLayout()
        self.column11 = QVBoxLayout()
        self.column21 = QVBoxLayout()

        self.row1.addWidget(QLabel("Interest Rate(%)"))
        self.row1.addWidget(self.interest_rate)
        self.row1.addWidget(QLabel("Initial Investment($)"))
        self.row1.addWidget(self.investment_edit)
        self.row1.addWidget(QLabel("Number of years"))
        self.row1.addWidget(self.time_edit)
        self.row1.addWidget(self.dark_mode)

        self.column11.addWidget(self.interest_viewer)
        self.column11.addWidget(self.calculate)
        self.column11.addWidget(self.reset)
        self.column11.addWidget(self.save)

        self.column21.addWidget(self.canvas)

        self.master_layout.addLayout(self.row1, 3)
        self.master_layout.addLayout(self.row2, 97)
        self.row2.addLayout(self.column11, 30)
        self.row2.addLayout(self.column21, 70)
        self.setLayout(self.master_layout)

        # Event handlers
        self.calculate.clicked.connect(self.calculate_btn)
        self.reset.clicked.connect(self.reset_btn)
        self.save.clicked.connect(self.save_btn)

    def plot_interest(self, years, interests):
        plt.plot(years, interests)
        plt.xlabel("Years")
        plt.ylabel("Interest")
        plt.title("Yearly Interest")
        self.canvas.draw()

    def calculate_btn(self):
        self.interest_model.clear()
        self.figure.clear()
        try:
            interest_rate = float(self.interest_rate.text())
            investment = float(self.investment_edit.text())
            years = int(self.time_edit.text())
        except ValueError:
            QMessageBox.warning(self, "Warning", "Please enter valid numbers.")
            return
        total = investment
        for year in range(1, years + 1):
            interest = total * (interest_rate / 100.00)
            total += interest
            item_year = QStandardItem(str(year))
            item_interest = QStandardItem(f"{interest:.2f}")
            self.interest_model.appendRow([item_year, item_interest])
        self.interest_model.setHorizontalHeaderLabels(["Years", "Interest"])

        years = list(range(1, years + 1))
        interests = [
            investment * (1 + (interest_rate / 100.00)) ** year for year in years
        ]
        self.plot_interest(years, interests)
        self.save.setVisible(True)

    def reset_btn(self):
        self.save.setVisible(False)
        self.time_edit.setText("0")
        self.interest_rate.setText("0.00")
        self.investment_edit.setText("0.00")
        self.interest_model.clear()
        self.figure.clear()
        self.canvas.draw()

    def save_btn(self):
        dir = QFileDialog.getExistingDirectory(self, "Select Save Destination")
        if dir:
            save_folder = os.path.join(dir, "saved")
        if not os.path.exists(save_folder):
            os.mkdir(save_folder)
        save_file = os.path.join(save_folder, "interest_per_annum.csv")
        try:
            with open(save_file, "w") as file:
                writer = csv.writer(file, delimiter=",")
                writer.writerow(["Years", "Interest"])
                for row in range(self.interest_model.rowCount()):
                    year = self.interest_model.item(row, 0).text()
                    interest = self.interest_model.item(row, 1).text()
                    writer.writerow([year, interest])
        except Exception as e:
            print(f"ERROR: {e}")
        plt.savefig(os.path.join(save_folder, "interest_chart.png"))
        QMessageBox.information(self, "Information", "Interest data and chart saved")


# Execute application
if __name__ == "__main__":
    app = QApplication([])
    main = Interest_Rate_Calculator()
    main.show()
    app.exec_()
