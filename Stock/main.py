from PyQt6 import QtWidgets, QtGui, QtCore
import csv
import os
import ctypes

class ManualWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("User Manual")
        self.setGeometry(100, 100, 1000, 500)

        # Load and display the manual image
        manual_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'manual.png')
        if os.path.exists(manual_path):
            manual_label = QtWidgets.QLabel(self)
            pixmap = QtGui.QPixmap(manual_path)
            manual_label.setPixmap(pixmap)
            manual_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        else:
            manual_label = QtWidgets.QLabel("Manual not found.", self)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(manual_label)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Set a smaller initial size for the window
        self.setGeometry(100, 100, 1000, 500)

        # Change the window title
        self.setWindowTitle("Stock and Sales Manager")

        # Set the window icon (assuming 'ssmanage.png' is in the same directory as your script)
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ssmanage.png')
        if os.path.exists(icon_path):
            self.setWindowIcon(QtGui.QIcon(icon_path))

            # Set the taskbar icon using ctypes on Windows
            try:
                myappid = 'mycompany.myproduct.subproduct.version'  # Change this to a unique identifier
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
            except Exception as e:
                print(f"Error setting taskbar icon: {e}")

        self.main_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.main_widget)

        # Create a banner QLabel and set text/image
        banner_label = QtWidgets.QLabel(self)
        banner_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        banner_label.setStyleSheet("background-color: #3498db; color: #ffffff; padding: 10px;")
        banner_label.setText("Stock and Sales Management System")  # You can also set an image using setPixmap()

        # Set layout for the main widget
        self.layout = QtWidgets.QVBoxLayout(self.main_widget)
        self.layout.addWidget(banner_label)

        # Open the manual window on startup
        manual_window = ManualWindow()
        manual_window.exec()

        self.left_side = QtWidgets.QVBoxLayout()
        self.layout.addLayout(self.left_side)

        self.stock_input = QtWidgets.QGroupBox("Product Input (Stock)")
        self.stock_layout = QtWidgets.QFormLayout(self.stock_input)
        self.stock_product_name = QtWidgets.QLineEdit()
        self.stock_quantity = QtWidgets.QLineEdit()
        self.stock_per_product_cp = QtWidgets.QLineEdit()
        self.stock_add_button = QtWidgets.QPushButton("Add")
        self.stock_edit_button = QtWidgets.QPushButton("Edit")
        self.stock_layout.addRow("Product Name", self.stock_product_name)
        self.stock_layout.addRow("Quantity", self.stock_quantity)
        self.stock_layout.addRow("Per Product CP", self.stock_per_product_cp)
        self.stock_layout.addRow(self.stock_add_button)
        self.stock_layout.addRow(self.stock_edit_button)
        self.left_side.addWidget(self.stock_input)

        self.sales_output = QtWidgets.QGroupBox("Product Output (Sales)")
        self.sales_layout = QtWidgets.QFormLayout(self.sales_output)
        self.sales_product_name = QtWidgets.QLineEdit()
        self.sales_quantity = QtWidgets.QLineEdit()
        self.sales_per_product_sp = QtWidgets.QLineEdit()
        self.sales_remove_button = QtWidgets.QPushButton("Remove")
        self.sales_edit_button = QtWidgets.QPushButton("Edit")
        self.sales_layout.addRow("Product Name", self.sales_product_name)
        self.sales_layout.addRow("Quantity", self.sales_quantity)
        self.sales_layout.addRow("Per Product SP", self.sales_per_product_sp)
        self.sales_layout.addRow(self.sales_remove_button)
        self.sales_layout.addRow(self.sales_edit_button)
        self.left_side.addWidget(self.sales_output)

        self.report_buttons = QtWidgets.QVBoxLayout()
        self.stock_report_button = QtWidgets.QPushButton("Stock Report")
        self.sales_report_button = QtWidgets.QPushButton("Sales Report")
        self.profit_report_button = QtWidgets.QPushButton("Profit Report")
        self.report_buttons.addWidget(self.stock_report_button)
        self.report_buttons.addWidget(self.sales_report_button)
        self.report_buttons.addWidget(self.profit_report_button)
        self.left_side.addLayout(self.report_buttons)

        self.right_side = QtWidgets.QVBoxLayout()
        self.layout.addLayout(self.right_side)

        self.stock_add_button.clicked.connect(self.add_stock_data)
        self.sales_remove_button.clicked.connect(self.remove_sales_data)
        self.stock_report_button.clicked.connect(self.generate_stock_report)
        self.sales_report_button.clicked.connect(self.generate_sales_report)
        self.profit_report_button.clicked.connect(self.generate_profit_report)
        self.stock_edit_button.clicked.connect(self.edit_stock_data)
        self.sales_edit_button.clicked.connect(self.edit_sales_data)

    def add_stock_data(self):
        product_name = self.stock_product_name.text()
        quantity = float(self.stock_quantity.text()) if self.stock_quantity.text() else 0.0
        per_product_cp = float(self.stock_per_product_cp.text()) if self.stock_per_product_cp.text() else 0.0

        script_dir = os.path.dirname(os.path.abspath(__file__))
        stock_csv_file_path = os.path.join(script_dir, 'stock_data.csv')

        header = ["Product Name", "Quantity", "Per Product CP"]

        # Check if the file exists, if not, write the header
        if not os.path.isfile(stock_csv_file_path):
            with open(stock_csv_file_path, 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(header)

        with open(stock_csv_file_path, 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow([product_name, quantity, per_product_cp])

        self.stock_product_name.clear()
        self.stock_quantity.clear()
        self.stock_per_product_cp.clear()

        QtWidgets.QMessageBox.information(self, "Success", "Stock data added successfully.")

    def remove_sales_data(self):
        product_name = self.sales_product_name.text()
        quantity = float(self.sales_quantity.text()) if self.sales_quantity.text() else 0.0
        per_product_sp = float(self.sales_per_product_sp.text()) if self.sales_per_product_sp.text() else 0.0

        script_dir = os.path.dirname(os.path.abspath(__file__))
        sales_csv_file_path = os.path.join(script_dir, 'sales_data.csv')
        stock_csv_file_path = os.path.join(script_dir, 'stock_data.csv')

        header = ["Product Name", "Quantity", "Per Product SP"]

        # Check if the file exists, if not, write the header
        if not os.path.isfile(sales_csv_file_path):
            with open(sales_csv_file_path, 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(header)

        with open(sales_csv_file_path, 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow([product_name, quantity, per_product_sp])

        # Update stock quantity in stock CSV
        stock_data = []
        try:
            with open(stock_csv_file_path, 'r') as csvfile:
                csv_reader = csv.reader(csvfile)
                next(csv_reader)  # Skip header
                stock_data = [row for row in csv_reader]
        except FileNotFoundError:
            pass

        updated_stock_data = []
        for row in stock_data:
            stock_product_name, stock_quantity, stock_per_product_cp = row
            if stock_product_name == product_name:
                stock_quantity = str(float(stock_quantity) - quantity)
            updated_stock_data.append([stock_product_name, stock_quantity, stock_per_product_cp])

        # Write back updated stock data
        with open(stock_csv_file_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["Product Name", "Quantity", "Per Product CP"])
            csv_writer.writerows(updated_stock_data)

        self.sales_product_name.clear()
        self.sales_quantity.clear()
        self.sales_per_product_sp.clear()

        QtWidgets.QMessageBox.information(self, "Success", "Sales data removed successfully.")

    def edit_stock_data(self):
        product_name = self.stock_product_name.text()
        new_quantity = float(self.stock_quantity.text()) if self.stock_quantity.text() else 0.0
        new_per_product_cp = float(self.stock_per_product_cp.text()) if self.stock_per_product_cp.text() else 0.0

        script_dir = os.path.dirname(os.path.abspath(__file__))
        stock_csv_file_path = os.path.join(script_dir, 'stock_data.csv')

        try:
            with open(stock_csv_file_path, 'r') as csvfile:
                csv_reader = csv.reader(csvfile)
                header = next(csv_reader)  # Skip header
                stock_data = [row for row in csv_reader]
        except FileNotFoundError:
            stock_data = []

        updated_stock_data = []
        for row in stock_data:
            stock_product_name, stock_quantity, stock_per_product_cp = row
            if stock_product_name == product_name:
                updated_stock_data.append([product_name, new_quantity, new_per_product_cp])
            else:
                updated_stock_data.append([stock_product_name, float(stock_quantity), float(stock_per_product_cp)])

        # Write back updated stock data
        with open(stock_csv_file_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(header)
            csv_writer.writerows(updated_stock_data)

        self.stock_product_name.clear()
        self.stock_quantity.clear()
        self.stock_per_product_cp.clear()

        QtWidgets.QMessageBox.information(self, "Success", "Stock data edited successfully.")

    def edit_sales_data(self):
        product_name = self.sales_product_name.text()
        new_quantity = float(self.sales_quantity.text()) if self.sales_quantity.text() else 0.0
        new_per_product_sp = float(self.sales_per_product_sp.text()) if self.sales_per_product_sp.text() else 0.0

        script_dir = os.path.dirname(os.path.abspath(__file__))
        sales_csv_file_path = os.path.join(script_dir, 'sales_data.csv')

        try:
            with open(sales_csv_file_path, 'r') as csvfile:
                csv_reader = csv.reader(csvfile)
                header = next(csv_reader)  # Skip header
                sales_data = [row for row in csv_reader]
        except FileNotFoundError:
            sales_data = []

        updated_sales_data = []
        for row in sales_data:
            sales_product_name, sales_quantity, sales_per_product_sp = row
            if sales_product_name == product_name:
                updated_sales_data.append([product_name, new_quantity, new_per_product_sp])
            else:
                updated_sales_data.append([sales_product_name, float(sales_quantity), float(sales_per_product_sp)])

        # Write back updated sales data
        with open(sales_csv_file_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(header)
            csv_writer.writerows(updated_sales_data)

        self.sales_product_name.clear()
        self.sales_quantity.clear()
        self.sales_per_product_sp.clear()

        QtWidgets.QMessageBox.information(self, "Success", "Sales data edited successfully.")

    def generate_stock_report(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        stock_csv_file_path = os.path.join(script_dir, 'stock_data.csv')

        try:
            with open(stock_csv_file_path, 'r') as csvfile:
                csv_reader = csv.reader(csvfile)
                next(csv_reader)  # Skip header
                stock_data = [(row[0], float(row[1]), float(row[2])) for row in csv_reader]
        except FileNotFoundError:
            stock_data = []

        stock_report_text = "Stock Report:\n\n"
        for product_name, stock_quantity, stock_per_product_cp in stock_data:
            stock_report_text += f"Product: {product_name}\nQuantity: {stock_quantity}\nPer Product CP: {stock_per_product_cp}\n\n"

        self.show_report_dialog(stock_report_text)

    def generate_sales_report(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        sales_csv_file_path = os.path.join(script_dir, 'sales_data.csv')

        try:
            with open(sales_csv_file_path, 'r') as csvfile:
                csv_reader = csv.reader(csvfile)
                next(csv_reader)  # Skip header
                sales_data = [(row[0], float(row[1]), float(row[2])) for row in csv_reader]
        except FileNotFoundError:
            sales_data = []

        sales_report_text = "Sales Report:\n\n"
        for product_name, quantity, per_product_sp in sales_data:
            sales_report_text += f"Product: {product_name}\nQuantity: {quantity}\nPer Product SP: {per_product_sp}\n\n"

        self.show_report_dialog(sales_report_text)

    def generate_profit_report(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        stock_csv_file_path = os.path.join(script_dir, 'stock_data.csv')
        sales_csv_file_path = os.path.join(script_dir, 'sales_data.csv')
        profit_csv_file_path = os.path.join(script_dir, 'profit_data.csv')

        # Read stock and sales data
        stock_data = {}
        try:
            with open(stock_csv_file_path, 'r') as stock_file:
                stock_reader = csv.DictReader(stock_file)
                for row in stock_reader:
                    stock_data[row['Product Name']] = (float(row['Quantity']), float(row['Per Product CP']))
        except FileNotFoundError:
            pass

        sales_data = {}
        try:
            with open(sales_csv_file_path, 'r') as sales_file:
                sales_reader = csv.DictReader(sales_file)
                for row in sales_reader:
                    sales_data[row['Product Name']] = (float(row['Quantity']), float(row['Per Product SP']))
        except FileNotFoundError:
            pass

        # Calculate profit and update profit data
        profit_data = {}
        for product_name, (stock_quantity, stock_per_product_cp) in stock_data.items():
            if product_name in sales_data:
                sales_quantity, per_product_sp = sales_data[product_name]
                profit = sales_quantity * (per_product_sp - stock_per_product_cp)
                profit_data[product_name] = profit

        # Write profit data to CSV
        header = ["Product Name", "Profit"]
        with open(profit_csv_file_path, 'w', newline='') as csvfile:
            csv_writer = csv.DictWriter(csvfile, fieldnames=header)
            csv_writer.writeheader()
            csv_writer.writerows([{'Product Name': product_name, 'Profit': profit} for product_name, profit in profit_data.items()])

        profit_report_text = "Profit Report:\n\n"
        for product_name, profit in profit_data.items():
            profit_report_text += f"Product: {product_name}\nProfit: {profit}\n\n"

        self.show_report_dialog(profit_report_text)

    def show_report_dialog(self, report_text):
        dialog = QtWidgets.QMessageBox()
        dialog.setWindowTitle("Report")
        dialog.setText(report_text)
        dialog.exec()

def show_manual(self):
        manual_window = ManualWindow()
        manual_window.exec()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
