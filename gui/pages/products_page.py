from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout


class ProductsPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        layout.addWidget(
            QLabel("صفحه محصولات")
        )






# gui/pages/products_page.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit, QLabel, QMessageBox, QHeaderView, QDialog,
    QFormLayout, QDialogButtonBox
)
from PySide6.QtCore import Qt
from database.product_repo import get_all_products, save_product, update_product, delete_product, get_product_by_code


class ProductDialog(QDialog):
    def __init__(self, product=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("ثبت/ویرایش محصول")
        self.setMinimumWidth(400)
        self.product = product

        layout = QVBoxLayout(self)
        form = QFormLayout()
        self.code_edit = QLineEdit()
        self.name_edit = QLineEdit()
        self.price_edit = QLineEdit()
        self.desc_edit = QLineEdit()

        form.addRow("کد کالا:", self.code_edit)
        form.addRow("نام کالا:", self.name_edit)
        form.addRow("قیمت (ریال):", self.price_edit)
        form.addRow("توضیحات:", self.desc_edit)

        if product:
            self.code_edit.setText(product[1])   # code
            self.name_edit.setText(product[2])   # name
            self.price_edit.setText(str(product[3]))  # price
            self.desc_edit.setText(product[4] if product[4] else "")  # description

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addLayout(form)
        layout.addWidget(buttons)

    def get_data(self):
        return {
            "code": self.code_edit.text().strip(),
            "name": self.name_edit.text().strip(),
            "price": int(self.price_edit.text().strip()),
            "description": self.desc_edit.text().strip()
        }


class ProductsPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        # نوار جستجو
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("جستجو بر اساس کد یا نام...")
        self.search_btn = QPushButton("جستجو")
        self.search_btn.clicked.connect(self.search_products)
        self.clear_btn = QPushButton("نمایش همه")
        self.clear_btn.clicked.connect(self.load_products)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_btn)
        search_layout.addWidget(self.clear_btn)
        layout.addLayout(search_layout)

        # جدول محصولات
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["شناسه", "کد", "نام", "قیمت", "توضیحات"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)

        # دکمه‌های عملیاتی
        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("افزودن محصول")
        self.edit_btn = QPushButton("ویرایش")
        self.delete_btn = QPushButton("حذف")
        self.refresh_btn = QPushButton("بازخوانی")

        self.add_btn.clicked.connect(self.add_product)
        self.edit_btn.clicked.connect(self.edit_product)
        self.delete_btn.clicked.connect(self.delete_product)
        self.refresh_btn.clicked.connect(self.load_products)

        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.edit_btn)
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addWidget(self.refresh_btn)
        layout.addLayout(btn_layout)

        self.load_products()

    def load_products(self):
        products = get_all_products()
        self.populate_table(products)

    def search_products(self):
        keyword = self.search_input.text().strip().lower()
        if not keyword:
            self.load_products()
            return
        all_products = get_all_products()
        filtered = [p for p in all_products if keyword in p[1].lower() or keyword in p[2].lower()]
        self.populate_table(filtered)

    def populate_table(self, products):
        self.table.setRowCount(0)
        for row, prod in enumerate(products):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(prod[0])))   # id
            self.table.setItem(row, 1, QTableWidgetItem(prod[1]))        # code
            self.table.setItem(row, 2, QTableWidgetItem(prod[2]))        # name
            self.table.setItem(row, 3, QTableWidgetItem(f"{prod[3]:,}")) # price
            self.table.setItem(row, 4, QTableWidgetItem(prod[4] if prod[4] else ""))  # desc

    def add_product(self):
        dialog = ProductDialog()
        if dialog.exec():
            data = dialog.get_data()
            # بررسی تکراری نبودن کد
            if get_product_by_code(data["code"]):
                QMessageBox.warning(self, "خطا", "کد کالا قبلاً ثبت شده است.")
                return
            try:
                save_product(data)
                QMessageBox.information(self, "موفق", "محصول با موفقیت افزوده شد.")
                self.load_products()
            except Exception as e:
                QMessageBox.critical(self, "خطا", f"خطا در ذخیره: {str(e)}")

    def edit_product(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "خطا", "لطفاً یک محصول را انتخاب کنید.")
            return
        product_id = int(self.table.item(current_row, 0).text())
        # برای ویرایش باید اطلاعات کامل محصول را بگیریم (شامل توضیحات)
        from database.product_repo import get_product_by_id  # نیاز به اضافه کردن این تابع
        product = get_product_by_id(product_id)
        if not product:
            QMessageBox.warning(self, "خطا", "محصول یافت نشد.")
            return
        dialog = ProductDialog(product)
        if dialog.exec():
            data = dialog.get_data()
            # بررسی اینکه کد جدید با کد قبلی متفاوت است و تکراری نباشد
            existing = get_product_by_code(data["code"])
            if existing and existing[0] != product_id:
                QMessageBox.warning(self, "خطا", "کد کالا تکراری است.")
                return
            try:
                update_product(product_id, data)
                QMessageBox.information(self, "موفق", "محصول با موفقیت ویرایش شد.")
                self.load_products()
            except Exception as e:
                QMessageBox.critical(self, "خطا", f"خطا در ویرایش: {str(e)}")

    def delete_product(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "خطا", "لطفاً یک محصول را انتخاب کنید.")
            return
        product_id = int(self.table.item(current_row, 0).text())
        product_name = self.table.item(current_row, 2).text()
        reply = QMessageBox.question(self, "تأیید حذف", f"آیا محصول '{product_name}' حذف شود؟",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                delete_product(product_id)
                QMessageBox.information(self, "موفق", "محصول حذف شد.")
                self.load_products()
            except Exception as e:
                QMessageBox.critical(self, "خطا", f"خطا در حذف: {str(e)}")