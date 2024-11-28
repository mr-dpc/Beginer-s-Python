import csv
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QDialog, QFormLayout, QTextEdit, QMessageBox, QHBoxLayout, QFrame
from PyQt6.QtCore import QDateTime, Qt

class ProductDetailsDialog(QDialog):
    # Class-level variable to keep track of the product serial
    product_serial = 1

    def __init__(self, customer_info):
        super().__init__()

        # Instance variables for the current product serial and customer information
        self.current_product_serial = ProductDetailsDialog.product_serial
        self.customer_info = customer_info

        # Instance variables for product details
        self.product_name_entry = None
        self.product_description_entry = None
        self.product_selling_type_entry = None
        self.quantity_entry = None
        self.per_product_price_entry = None
        self.total_product_price_entry = None
        self.discount_percentage_entry = None
        self.discount_amount_entry = None
        self.vat_percentage_entry = None
        self.vat_amount_entry = None
        self.total_price_entry = None

        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()

        # Display current product serial
        serial_label = QLabel(f"Product Serial: {self.current_product_serial}")
        layout.addRow(serial_label)

        # Fields for product details
        self.product_name_entry = QLineEdit()
        self.product_description_entry = QTextEdit()
        self.product_selling_type_entry = QLineEdit()
        self.quantity_entry = QLineEdit()
        self.per_product_price_entry = QLineEdit()
        self.total_product_price_entry = QLineEdit()
        self.discount_percentage_entry = QLineEdit()
        self.discount_amount_entry = QLineEdit()
        self.vat_percentage_entry = QLineEdit()
        self.vat_amount_entry = QLineEdit()
        self.total_price_entry = QLineEdit()

        layout.addRow("Product Name:", self.product_name_entry)
        layout.addRow("Product Description:", self.product_description_entry)
        layout.addRow("Product Selling Type:", self.product_selling_type_entry)
        layout.addRow("Quantity:", self.quantity_entry)
        layout.addRow("Per Product Price:", self.per_product_price_entry)
        layout.addRow("Total Product Price:", self.total_product_price_entry)
        layout.addRow("Percentage of Discount:", self.discount_percentage_entry)
        layout.addRow("Amount of Discount:", self.discount_amount_entry)
        layout.addRow("Percentage of VAT:", self.vat_percentage_entry)
        layout.addRow("Amount of VAT:", self.vat_amount_entry)
        layout.addRow("Total Price:", self.total_price_entry)

        # Buttons
        confirm_button = QPushButton("Confirm Sell")
        sell_another_button = QPushButton("Sell Another Product")

        # Connect buttons to their respective functions
        confirm_button.clicked.connect(self.confirm_sell)
        sell_another_button.clicked.connect(self.sell_another_product)

        button_layout = QHBoxLayout()
        button_layout.addWidget(confirm_button)
        button_layout.addWidget(sell_another_button)

        layout.addRow(button_layout)

        self.setLayout(layout)
        self.setWindowTitle("Product Details")

    def confirm_sell(self):
        # Get the product details
        product_details = {
            "Product Serial": self.current_product_serial,
            "Product Name": self.product_name_entry.text(),
            "Product Description": self.product_description_entry.toPlainText(),
            "Product Selling Type": self.product_selling_type_entry.text(),
            "Quantity": self.quantity_entry.text(),
            "Per Product Price": self.per_product_price_entry.text(),
            "Total Product Price": self.total_product_price_entry.text(),
            "Discount Percentage": self.discount_percentage_entry.text(),
            "Discount Amount": self.discount_amount_entry.text(),
            "VAT Percentage": self.vat_percentage_entry.text(),
            "VAT Amount": self.vat_amount_entry.text(),
            "Total Price": self.total_price_entry.text(),
        }

        # Append the product details to the CSV file
        with open("sales_record.csv", mode="a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=product_details.keys())

            # If the file is empty, write the header
            if file.tell() == 0:
                writer.writeheader()

            writer.writerow(product_details)

        # Call the parent confirm_sell method to close the dialog and update the product serial
        super().accept()

    def sell_another_product(self):
        # Implement your logic for selling another product
        self.clear_fields()
        # Update the product serial for the new product
        self.current_product_serial = ProductDetailsDialog.product_serial
        # Update the displayed serial label
        self.findChild(QLabel, f"Product Serial: {self.current_product_serial}").setText(f"Product Serial: {self.current_product_serial}")

    def clear_fields(self):
        # Clear all input fields for the next product
        for field in [self.product_name_entry, self.product_description_entry,
                      self.product_selling_type_entry, self.quantity_entry,
                      self.per_product_price_entry, self.total_product_price_entry,
                      self.discount_percentage_entry, self.discount_amount_entry,
                      self.vat_percentage_entry, self.vat_amount_entry, self.total_price_entry]:
            field.clear()

class ReceiptProgram(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # Customer Information Entry
        customer_labels = ["Customer's Name:", "Customer's BIN/NID:", "Customer's Address:",
                           "Customer's Delivery Address:", "Delivery Transport Type and Number:",
                           "Receipt No:", "Issue Date:", "Issue Time:"]

        self.customer_info = {label: QLineEdit(self) for label in customer_labels}

        vbox = QVBoxLayout(self)
        for label_text, entry in zip(customer_labels, self.customer_info.values()):
            hbox = QVBoxLayout()
            hbox.addWidget(QLabel(label_text))
            hbox.addWidget(entry)
            vbox.addLayout(hbox)

        # Set real-time value for "Issue Date" without time
        current_date = QDateTime.currentDateTime().date()
        self.customer_info["Issue Date:"].setText(current_date.toString(Qt.DateFormat.ISODate))
        self.customer_info["Issue Date:"].setReadOnly(True)  # Make it uneditable

        # Set real-time value for "Issue Time" in 12-hour format with AM/PM
        current_time = QDateTime.currentDateTime().time()
        issue_time_label = QLabel(current_time.toString("hh:mm AP"), self)
        vbox.addWidget(issue_time_label)

        # Buttons
        sell_button = QPushButton("Sell", self)
        sell_button.clicked.connect(self.sell_button_clicked)

        search_button = QPushButton("Search", self)
        search_button.clicked.connect(self.search_button_clicked)

        vbox.addWidget(sell_button)
        vbox.addWidget(search_button)

        self.setLayout(vbox)
        self.setWindowTitle("Receipt Program")


    def sell_button_clicked(self):
        # Function to handle "Sell" button click
        product_details_dialog = ProductDetailsDialog(self.customer_info)
        result = product_details_dialog.exec()

        if result == QDialog.Accepted:
            QMessageBox.information(self, "Sell Completed", "Sell completed successfully.")
        else:
            QMessageBox.warning(self, "Sell Canceled", "Sell was canceled.")

    def search_button_clicked(self):
        # Function to handle "Search" button click
        # This is where you can add code for window no 3
        QMessageBox.information(self, "Search Button Clicked", "Implement the functionality for searching here.")

if __name__ == '__main__':
    app = QApplication([])
    window = ReceiptProgram()
    window.show()
    app.exec()
