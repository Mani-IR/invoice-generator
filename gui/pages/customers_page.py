from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout


class CustomersPage(QWidget):
    
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(
            QLabel("صفحه مشتریان")
        )
# gui/pages/customers_page.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit, QLabel, QMessageBox, QHeaderView, QDialog,
    QFormLayout, QDialogButtonBox, QTabWidget, QGroupBox
)
from PySide6.QtCore import Qt
from database.customer_repo import (
    get_all_customers, save_customer, update_customer, delete_customer,
    get_customer_by_phone, get_customer_invoices
)

class CustomerDialog(QDialog):
    def __init__(self, customer=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("ثبت/ویرایش مشتری")
        self.setMinimumWidth(450)
        self.customer = customer

        layout = QVBoxLayout(self)
        form = QFormLayout()
        self.name_edit = QLineEdit()
        self.phone_edit = QLineEdit()
        self.national_edit = QLineEdit()
        self.economic_edit = QLineEdit()
        self.postal_edit = QLineEdit()
        self.address_edit = QLineEdit()

        form.addRow("نام و نام خانوادگی:", self.name_edit)
        form.addRow("شماره تلفن:", self.phone_edit)
        form.addRow("کد ملی:", self.national_edit)
        form.addRow("شماره اقتصادی:", self.economic_edit)
        form.addRow("کد پستی:", self.postal_edit)
        form.addRow("آدرس:", self.address_edit)

        if customer:
            self.name_edit.setText(customer[1])
            self.phone_edit.setText(customer[2])
            self.national_edit.setText(customer[3] if customer[3] else "")
            self.economic_edit.setText(customer[4] if customer[4] else "")
            self.postal_edit.setText(customer[5] if customer[5] else "")
            self.address_edit.setText(customer[6] if customer[6] else "")

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addLayout(form)
        layout.addWidget(buttons)

    def get_data(self):
        return {
            "name": self.name_edit.text().strip(),
            "phone": self.phone_edit.text().strip(),
            "national_code": self.national_edit.text().strip(),
            "economic_code": self.economic_edit.text().strip(),
            "postal_code": self.postal_edit.text().strip(),
            "address": self.address_edit.text().strip()
        }

class CustomersPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        # نوار جستجو
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("جستجو بر اساس نام یا تلفن...")
        self.search_btn = QPushButton("جستجو")
        self.search_btn.clicked.connect(self.search_customers)
        self.clear_btn = QPushButton("نمایش همه")
        self.clear_btn.clicked.connect(self.load_customers)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_btn)
        search_layout.addWidget(self.clear_btn)
        layout.addLayout(search_layout)

        # جدول مشتریان
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["شناسه", "نام", "تلفن", "کد ملی", "کد اقتصادی", "عملیات"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)

        # دکمه‌های عملیاتی
        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("افزودن مشتری")
        self.edit_btn = QPushButton("ویرایش")
        self.delete_btn = QPushButton("حذف")
        self.refresh_btn = QPushButton("بازخوانی")
        self.invoices_btn = QPushButton("مشاهده فاکتورها")

        self.add_btn.clicked.connect(self.add_customer)
        self.edit_btn.clicked.connect(self.edit_customer)
        self.delete_btn.clicked.connect(self.delete_customer)
        self.refresh_btn.clicked.connect(self.load_customers)
        self.invoices_btn.clicked.connect(self.show_invoices)

        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.edit_btn)
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addWidget(self.invoices_btn)
        btn_layout.addWidget(self.refresh_btn)
        layout.addLayout(btn_layout)

        self.load_customers()

    def load_customers(self, customers=None):
        if customers is None:
            customers = get_all_customers()
        self.table.setRowCount(0)
        for row, cust in enumerate(customers):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(cust[0])))  # id
            self.table.setItem(row, 1, QTableWidgetItem(cust[1]))       # name
            self.table.setItem(row, 2, QTableWidgetItem(cust[2]))       # phone
            self.table.setItem(row, 3, QTableWidgetItem(cust[3] if cust[3] else ""))
            self.table.setItem(row, 4, QTableWidgetItem(cust[4] if cust[4] else ""))

            # دکمه مشاهده فاکتورها در ستون ۵
            btn = QPushButton("فاکتورها")
            btn.clicked.connect(lambda checked, cid=cust[0]: self.show_customer_invoices(cid))
            self.table.setCellWidget(row, 5, btn)

    def search_customers(self):
        keyword = self.search_input.text().strip().lower()
        if not keyword:
            self.load_customers()
            return
        all_customers = get_all_customers()
        filtered = [c for c in all_customers if keyword in c[1].lower() or keyword in c[2].lower()]
        self.load_customers(filtered)

    def add_customer(self):
        dialog = CustomerDialog()
        if dialog.exec():
            data = dialog.get_data()
            if not data["name"] or not data["phone"]:
                QMessageBox.warning(self, "خطا", "نام و تلفن الزامی است")
                return
            # بررسی تکراری نبودن تلفن
            if get_customer_by_phone(data["phone"]):
                QMessageBox.warning(self, "خطا", "این شماره تلفن قبلاً ثبت شده است")
                return
            try:
                save_customer(data)  # توجه: تابع save_customer موجود باید به روز شود تا نام فیلدها مطابق باشد
                QMessageBox.information(self, "موفق", "مشتری با موفقیت افزوده شد")
                self.load_customers()
            except Exception as e:
                QMessageBox.critical(self, "خطا", f"خطا در ذخیره: {str(e)}")

    def edit_customer(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "خطا", "لطفاً یک مشتری را انتخاب کنید")
            return
        cust_id = int(self.table.item(current_row, 0).text())
        customer = get_customer_by_id(cust_id)
        if not customer:
            QMessageBox.warning(self, "خطا", "مشتری یافت نشد")
            return
        dialog = CustomerDialog(customer)
        if dialog.exec():
            data = dialog.get_data()
            # بررسی تلفن تکراری (به غیر از خودش)
            existing = get_customer_by_phone(data["phone"])
            if existing and existing[0] != cust_id:
                QMessageBox.warning(self, "خطا", "این شماره تلفن قبلاً برای مشتری دیگری ثبت شده است")
                return
            try:
                update_customer(cust_id, data)
                QMessageBox.information(self, "موفق", "اطلاعات مشتری به روز شد")
                self.load_customers()
            except Exception as e:
                QMessageBox.critical(self, "خطا", f"خطا در به روزرسانی: {str(e)}")

    def delete_customer(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "خطا", "لطفاً یک مشتری را انتخاب کنید")
            return
        cust_id = int(self.table.item(current_row, 0).text())
        cust_name = self.table.item(current_row, 1).text()
        reply = QMessageBox.question(self, "تأیید حذف", f"آیا مشتری '{cust_name}' حذف شود؟\n(فاکتورهای این مشتری حذف نخواهند شد)", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                delete_customer(cust_id)
                QMessageBox.information(self, "موفق", "مشتری حذف شد")
                self.load_customers()
            except Exception as e:
                QMessageBox.critical(self, "خطا", f"خطا در حذف: {str(e)}")

    def show_customer_invoices(self, customer_id):
        """نمایش فاکتورهای مشتری در یک دیالوگ جدا"""
        invoices = get_customer_invoices(customer_id)
        if not invoices:
            QMessageBox.information(self, "اطلاعات", "این مشتری هیچ فاکتوری ندارد")
            return
        dialog = QDialog(self)
        dialog.setWindowTitle("فاکتورهای مشتری")
        dialog.resize(700, 400)
        layout = QVBoxLayout(dialog)
        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["شماره فاکتور", "تاریخ", "جمع کل", "مالیات", "مبلغ نهایی"])
        table.setRowCount(len(invoices))
        for row, inv in enumerate(invoices):
            table.setItem(row, 0, QTableWidgetItem(inv[1]))
            table.setItem(row, 1, QTableWidgetItem(inv[2]))
            table.setItem(row, 2, QTableWidgetItem(f"{inv[3]:,}"))
            table.setItem(row, 3, QTableWidgetItem(f"{inv[4]:,}"))
            table.setItem(row, 4, QTableWidgetItem(f"{inv[5]:,}"))
        layout.addWidget(table)
        close_btn = QPushButton("بستن")
        close_btn.clicked.connect(dialog.accept)
        layout.addWidget(close_btn)
        dialog.exec()

    def show_invoices(self):
        """نمایش فاکتورهای مشتری انتخاب شده (دکمه جداگانه)"""
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "خطا", "لطفاً یک مشتری را انتخاب کنید")
            return
        cust_id = int(self.table.item(current_row, 0).text())
        self.show_customer_invoices(cust_id)