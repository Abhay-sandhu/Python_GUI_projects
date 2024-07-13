import os, sys
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import (
    QWidget,
    QApplication,
    QPushButton,
    QLabel,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QLineEdit,
    QDateEdit,
    QComboBox,
    QVBoxLayout,
    QHBoxLayout,
    QVBoxLayout,
    QHeaderView
)


class Expense_Tracker(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Editor")
        self.resize(800, 600)

        # App Objects
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.category_box = QComboBox()
        self.category_box.addItems(['Grocery', 'Transportation', 'Rent', 'Shopping' ,'Entertainment', 'Business', 'Bills' ,'Other'])
        
        self.amount_edit = QLineEdit()
        self.amount_edit.setText("0.00")
        self.description_edit = QLineEdit()
        self.description_edit.setText("None")
        self.add_expense_button = QPushButton("Add Expenses")
        self.delete_expense_button = QPushButton("Delete Expenses")
        
        self.expense_table = QTableWidget()
        self.expense_table.setColumnCount(5)
        self.expense_table.setHorizontalHeaderLabels(['ID', 'Date', 'Category','Amount','Description'])
        self.expense_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.expense_table.sortByColumn(1, Qt.DescendingOrder)

        # App Layout
        self.master_layout = QVBoxLayout()
        self.row1 = QHBoxLayout()
        self.row2 = QHBoxLayout()
        self.row3 = QHBoxLayout()

        self.row1.addWidget(QLabel("Date"))
        self.row1.addWidget(self.date_edit)
        self.row1.addWidget(QLabel("Category"))
        self.row1.addWidget(self.category_box)

        self.row2.addWidget(QLabel("Amount"))
        self.row2.addWidget(self.amount_edit)
        self.row2.addWidget(QLabel("Description"))
        self.row2.addWidget(self.description_edit)

        self.row3.addWidget(self.add_expense_button)
        self.row3.addWidget(self.delete_expense_button)

        self.master_layout.addLayout(self.row1)
        self.master_layout.addLayout(self.row2)
        self.master_layout.addLayout(self.row3)
        self.master_layout.addWidget(self.expense_table)
        self.setLayout(self.master_layout)
        
        # Load the database and table
        self.create_database()
        self.load_table()

        # Event handlers
        self.add_expense_button.clicked.connect(self.add_expense)
        self.delete_expense_button.clicked.connect(self.delete_expense)

    def create_database(self):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("expense_tracker.db")
        if not self.db.open():
            QMessageBox.critical(self, "Database Error", self.db.lastError().text())
            sys.exit(1)
        self.create_table()

    def create_table(self):
        query = QSqlQuery()
        query.exec_(
            """
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE,
                category TEXT,
                amount REAL,
                description TEXT
            )
            """
        )

    def load_table(self):
        self.expense_table.setRowCount(0)
        query = QSqlQuery("SELECT * FROM expenses")
        row = 0
        while query.next():        
            id = query.value(0)
            date = query.value(1)
            category = query.value(2)
            amount = query.value(3)
            description = query.value(4)

            self.expense_table.insertRow(row)
            self.expense_table.setItem(row, 0, QTableWidgetItem(str(id)))
            self.expense_table.setItem(row, 1, QTableWidgetItem(date))
            self.expense_table.setItem(row, 2, QTableWidgetItem(category))
            self.expense_table.setItem(row, 3, QTableWidgetItem(str(amount)))
            self.expense_table.setItem(row, 4, QTableWidgetItem(description))
            row += 1

    def add_expense(self):
        date = self.date_edit.date().toString("yyyy-MM-dd")
        category = self.category_box.currentText()
        amount = float(self.amount_edit.text())
        description = self.description_edit.text()

        query = QSqlQuery()
        query.prepare(
            """
            INSERT INTO expenses (date, category, amount, description)
            VALUES (:date, :category, :amount, :description)
            """
        )
        query.bindValue(":date", date)
        query.bindValue(":category", category)
        query.bindValue(":amount", amount)
        query.bindValue(":description", description)
        if query.exec_():
            #QMessageBox.information(self, "Success", "Expense added successfully.")
            self.load_table()
        
        self.date_edit.setDate(QDate.currentDate())
        self.category_box.setCurrentIndex(0)
        self.amount_edit.setText("0.00")
        self.description_edit.setText("None")

    def delete_expense(self):
        selected_row = self.expense_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Warning", "No expense selected.")
            return
        query = QSqlQuery()
        query.prepare("DELETE FROM expenses WHERE id = :id")
        query.bindValue(":id", self.expense_table.item(selected_row, 0).text())
        if query.exec_():
            self.load_table()

# Execute application
if __name__ == "__main__":
    app = QApplication([])
    main = Expense_Tracker()
    main.show()
    app.exec_()
