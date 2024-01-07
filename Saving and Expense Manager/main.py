import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QDialog, QTableWidget, QTableWidgetItem
from PyQt6.QtGui import QPixmap
import csv
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import QFileDialog
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime

class DataWindow(QDialog):
    def __init__(self, parent=None):
        super(DataWindow, self).__init__(parent)
        self.setWindowTitle("Data Window")

        # Add widgets and layout for the data window as needed
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Credit", "Amount", "Debit", "Amount"])

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addWidget(close_button)

        self.setLayout(layout)

        self.populate_table()
        self.print_pdf_button = QPushButton("Print PDF")
        self.print_pdf_button.clicked.connect(self.print_pdf)

        layout.addWidget(self.print_pdf_button)

    def populate_table(self):
        credit_data = self.load_data('credit.csv', 'Credit Title', 'Credit Amount')
        debit_data = self.load_data('debit.csv', 'Debit Title', 'Debit Amount')

        total_credit_amount = sum(credit_data.values())
        total_debit_amount = sum(debit_data.values())

        max_rows = max(len(credit_data), len(debit_data)) + 1

        self.table.setRowCount(max_rows)

        for row in range(max_rows - 1):  # Exclude the last row for the total
            if row < len(credit_data):
                title, amount = list(credit_data.items())[row]
                self.table.setItem(row, 0, QTableWidgetItem(title))
                self.table.setItem(row, 1, QTableWidgetItem(str(amount)))

            if row < len(debit_data):
                title, amount = list(debit_data.items())[row]
                self.table.setItem(row, 2, QTableWidgetItem(title))
                self.table.setItem(row, 3, QTableWidgetItem(str(amount)))

        self.table.setItem(max_rows - 1, 0, QTableWidgetItem("Total"))
        self.table.setItem(max_rows - 1, 1, QTableWidgetItem(str(total_credit_amount)))
        self.table.setItem(max_rows - 1, 2, QTableWidgetItem("Total"))
        self.table.setItem(max_rows - 1, 3, QTableWidgetItem(str(total_debit_amount)))

    def load_data(self, file_name, title_column, amount_column):
        data = {}
        try:
            with open(file_name, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    title = row.get(title_column)
                    amount = float(row[amount_column]) if amount_column in row else 0
                    data[title] = data.get(title, 0) + amount
        except FileNotFoundError:
            pass

        return data
    def print_pdf(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save PDF", "", "PDF files (*.pdf)")

        if file_path:
            pdf_canvas = canvas.Canvas(file_path, pagesize=letter)
            pdf_canvas.setFont("Helvetica", 12)

            # Print information at the top of the PDF
            pdf_canvas.drawString(72, 750, f"Printed by Sayem Billah")
            pdf_canvas.drawString(72, 730, f"Printed on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            pdf_canvas.drawString(72, 710, f"Subject: Monthly Income and Expense Statement")

            # Print table headers
            for col, header in enumerate(["Credit", "Amount", "Debit", "Amount"]):
                pdf_canvas.drawString(72 + col * 150, 690, header)

            # Print table data
            row_height = 20
            for row in range(self.table.rowCount()):
                for col in range(self.table.columnCount()):
                    item = self.table.item(row, col)
                    if item:
                        pdf_canvas.drawString(72 + col * 150, 670 - row * row_height, item.text())

            pdf_canvas.save()


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 654, 430)
        self.setWindowTitle("PyQt6 Form Example")

        self.image_label = QLabel(self)
        self.image_label.setGeometry(16, 16, 622, 110)
        self.load_image('banner.png')

        self.credit_label = QLabel("Credit title:")
        self.credit_title_textbox = QLineEdit()
        self.amount_label = QLabel("Amount:")
        self.amount_textbox = QLineEdit()
        self.submit_credit_button = QPushButton("Submit")
        self.submit_credit_button.clicked.connect(self.save_credit_data)

        self.debit_label = QLabel("Debit title:")
        self.debit_title_textbox = QLineEdit()
        self.debit_amount_label = QLabel("Amount:")
        self.debit_amount_textbox = QLineEdit()
        self.submit_debit_button = QPushButton("Submit")
        self.submit_debit_button.clicked.connect(self.save_debit_data)

        self.show_stat_button = QPushButton("Show Stat")
        self.show_stat_button.clicked.connect(self.show_statistics)

        self.current_balance_label = QLabel("Current Balance: $0.00")

        self.show_data_button = QPushButton("Show Data")
        self.show_data_button.clicked.connect(self.show_data_window)

        # Load existing data and update balance
        self.load_existing_data('credit.csv')
        self.load_existing_data('debit.csv')
        self.update_current_balance()

        central_layout = QVBoxLayout()
        central_layout.addWidget(self.image_label)

        central_layout.addWidget(self.credit_label)
        central_layout.addWidget(self.credit_title_textbox)
        central_layout.addWidget(self.amount_label)
        central_layout.addWidget(self.amount_textbox)
        central_layout.addWidget(self.submit_credit_button)

        central_layout.addWidget(self.debit_label)
        central_layout.addWidget(self.debit_title_textbox)
        central_layout.addWidget(self.debit_amount_label)
        central_layout.addWidget(self.debit_amount_textbox)
        central_layout.addWidget(self.submit_debit_button)

        central_layout.addWidget(self.show_stat_button)
        central_layout.addWidget(self.show_data_button)
        central_layout.addWidget(self.current_balance_label)

        central_widget = QWidget()
        central_widget.setLayout(central_layout)
        self.setCentralWidget(central_widget)

    def load_image(self, file_path):
        pixmap = QPixmap(file_path)
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)

    def load_existing_data(self, file_name):
        try:
            with open(file_name, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    print(row)
        except FileNotFoundError:
            pass

    def save_credit_data(self):
        credit_title = self.credit_title_textbox.text()
        credit_amount = self.amount_textbox.text()

        if credit_title and credit_amount:
            try:
                with open('credit.csv', 'a', newline='', encoding='utf-8') as csvfile:
                    fieldnames = ['Credit Title', 'Credit Amount']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                    if csvfile.tell() == 0:
                        writer.writeheader()

                    writer.writerow({'Credit Title': credit_title, 'Credit Amount': credit_amount})

                    print(f"Credit Data saved: {credit_title}, {credit_amount}")
            except Exception as e:
                print(f"Error saving credit data: {e}")

            self.update_current_balance()

    def save_debit_data(self):
        debit_title = self.debit_title_textbox.text()
        debit_amount = self.debit_amount_textbox.text()

        if debit_title and debit_amount:
            try:
                with open('debit.csv', 'a', newline='', encoding='utf-8') as csvfile:
                    fieldnames = ['Debit Title', 'Debit Amount']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                    if csvfile.tell() == 0:
                        writer.writeheader()

                    writer.writerow({'Debit Title': debit_title, 'Debit Amount': debit_amount})

                    print(f"Debit Data saved: {debit_title}, {debit_amount}")
            except Exception as e:
                print(f"Error saving debit data: {e}")

            self.update_current_balance()

    def update_current_balance(self):
        total_credit_amount = self.calculate_total_amount('credit.csv')
        total_debit_amount = self.calculate_total_amount('debit.csv')
        current_balance = total_credit_amount - total_debit_amount
        self.current_balance_label.setText(f"Current Balance: ${current_balance:.2f}")

    def calculate_total_amount(self, file_name):
        total_amount = 0
        try:
            with open(file_name, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    total_amount += float(row['Credit Amount']) if 'Credit Amount' in row else 0
                    total_amount += float(row['Debit Amount']) if 'Debit Amount' in row else 0
        except FileNotFoundError:
            pass

        return total_amount

    def show_statistics(self):
        self.show_credit_graph()
        self.show_debit_graph()

    def show_data_window(self):
        data_window = DataWindow(self)
        data_window.exec()

    def show_credit_graph(self):
        credit_data = self.load_amount_data('credit.csv', 'Credit Amount')
        plt.bar(credit_data.keys(), credit_data.values(), color='green')
        plt.title('Credit Amounts')
        plt.xlabel('Credit Title')
        plt.ylabel('Amount')
        plt.show()

    def show_debit_graph(self):
        debit_data = self.load_amount_data('debit.csv', 'Debit Amount')
        plt.bar(debit_data.keys(), debit_data.values(), color='red')
        plt.title('Debit Amounts')
        plt.xlabel('Debit Title')
        plt.ylabel('Amount')
        plt.show()

    def load_amount_data(self, file_name, column_name):
        amount_data = {}
        try:
            with open(file_name, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    title = row.get(column_name)
                    amount = float(row['Debit Amount']) if 'Debit Amount' in row else float(row['Credit Amount'])
                    amount_data[title] = amount_data.get(title, 0) + amount
        except FileNotFoundError:
            pass

        return amount_data

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())
