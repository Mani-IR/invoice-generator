from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QLabel,
    QGroupBox, QTableWidget, QPushButton, QHBoxLayout,
    QTableWidgetItem, QMessageBox, QHeaderView, QDateEdit
)
from PySide6.QtCore import Qt, QDate
import jdatetime
from services.invoice_service import create_invoice_from_gui
from gui.dialogs.add_product_dialog import AddProductDialog
from gui.dialogs.select_product_dialog import SelectProductDialog
from database.invoice_repo import is_invoice_number_exists
from config.settings import TAX_RATE


class CreateInvoicePage(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout(self)

        # ========== اطلاعات مشتری (بدون تغییر) ==========
        customer_group = QGroupBox("اطلاعات مشتری")
        customer_form = QFormLayout()
        self.customer_name = QLineEdit()
        self.customer_phone = QLineEdit()
        self.customer_national_code = QLineEdit()
        self.customer_economic_code = QLineEdit()
        self.customer_postal_code = QLineEdit()
        self.customer_address = QLineEdit()
        customer_form.addRow("نام مشتری :", self.customer_name)
        customer_form.addRow("شماره مشتری :", self.customer_phone)
        customer_form.addRow("کد ملی :", self.customer_national_code)
        customer_form.addRow("کد اقتصادی :", self.customer_economic_code)
        customer_form.addRow("کد پستی :", self.customer_postal_code)
        customer_form.addRow("آدرس :", self.customer_address)
        customer_group.setLayout(customer_form)

        # ========== اطلاعات فاکتور و تاریخ ==========
        invoice_group = QGroupBox("اطلاعات فاکتور")
        invoice_form = QFormLayout()
        self.invoice_number = QLineEdit()
        # تاریخ فاکتور (شمسی)
        self.invoice_date = QDateEdit()
        today = jdatetime.date.today()
        self.invoice_date.setDate(QDate(today.year, today.month, today.day))
        self.invoice_date.setDisplayFormat("yyyy/MM/dd")
        self.invoice_date.setCalendarPopup(True)
        invoice_form.addRow("شماره فاکتور :", self.invoice_number)
        invoice_form.addRow("تاریخ فاکتور :", self.invoice_date)
        invoice_group.setLayout(invoice_form)

        # ========== کالاها (با قابلیت انتخاب از لیست) ==========
        products_group = QGroupBox("کالاها")
        products_layout = QVBoxLayout()
        self.products_table = QTableWidget()
        self.products_table.setColumnCount(5)
        self.products_table.setHorizontalHeaderLabels(["کد کالا", "نام کالا", "تعداد", "قیمت", "جمع"])
        self.products_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # فعال کردن ویرایش با دابل کلیک روی ستون تعداد و قیمت
        self.products_table.setEditTriggers(QTableWidget.DoubleClicked)
        self.products_table.itemDoubleClicked.connect(self.on_item_double_clicked)
        products_layout.addWidget(self.products_table)

        buttons_layout = QHBoxLayout()
        self.btn_add_product = QPushButton("افزودن دستی کالا")
        self.btn_select_product = QPushButton("انتخاب از محصولات")
        self.btn_remove_product = QPushButton("حذف کالا")
        buttons_layout.addWidget(self.btn_add_product)
        buttons_layout.addWidget(self.btn_select_product)
        buttons_layout.addWidget(self.btn_remove_product)
        products_layout.addLayout(buttons_layout)
        products_group.setLayout(products_layout)

        # ========== خلاصه فاکتور ==========
        totals_group = QGroupBox("خلاصه فاکتور")
        totals_layout = QVBoxLayout()
        self.lbl_total = QLabel("جمع کل : 0")
        self.lbl_tax = QLabel("مالیات : 0")
        self.lbl_final = QLabel("مبلغ نهایی : 0")
        totals_layout.addWidget(self.lbl_total)
        totals_layout.addWidget(self.lbl_tax)
        totals_layout.addWidget(self.lbl_final)
        totals_group.setLayout(totals_layout)

        self.btn_create_invoice = QPushButton("ساخت فاکتور")

        # اتصال رویدادها
        self.btn_add_product.clicked.connect(self.add_product_manual)
        self.btn_select_product.clicked.connect(self.select_product_from_db)
        self.btn_remove_product.clicked.connect(self.remove_product)
        self.btn_create_invoice.clicked.connect(self.create_invoice)
        # اتصال تغییرات جدول برای به‌روزرسانی مجموع
        self.products_table.itemChanged.connect(self.on_item_changed)

        # اضافه کردن ویجت‌ها به لایه اصلی
        main_layout.addWidget(customer_group)
        main_layout.addWidget(invoice_group)
        main_layout.addWidget(products_group)
        main_layout.addWidget(totals_group)
        main_layout.addWidget(self.btn_create_invoice)
        main_layout.addStretch()

    # ---------- توابع کمکی ----------
    def update_totals(self):
        total = 0
        for row in range(self.products_table.rowCount()):
            qty = int(self.products_table.item(row, 2).text())
            price = int(self.products_table.item(row, 3).text())
            total += qty * price
        tax = int(total * TAX_RATE)
        final = total + tax
        self.lbl_total.setText(f"جمع کل : {total:,}")
        self.lbl_tax.setText(f"مالیات ({int(TAX_RATE*100)}%) : {tax:,}")
        self.lbl_final.setText(f"مبلغ نهایی : {final:,}")

    def add_product_to_table(self, code, name, qty, price):
        # جلوگیری از سیگنال دائم
        self.products_table.blockSignals(True)
        row = self.products_table.rowCount()
        self.products_table.insertRow(row)
        self.products_table.setItem(row, 0, QTableWidgetItem(code))
        self.products_table.setItem(row, 1, QTableWidgetItem(name))
        self.products_table.setItem(row, 2, QTableWidgetItem(str(qty)))
        self.products_table.setItem(row, 3, QTableWidgetItem(str(price)))
        total = qty * price
        self.products_table.setItem(row, 4, QTableWidgetItem(str(total)))
        self.products_table.blockSignals(False)
        self.update_totals()

    def add_product_manual(self):
        dialog = AddProductDialog()
        if dialog.exec():
            code = dialog.code.text().strip()
            name = dialog.name.text().strip()
            try:
                qty = int(dialog.qty.text())
                price = int(dialog.price.text())
            except ValueError:
                QMessageBox.warning(self, "خطا", "تعداد و قیمت باید عدد باشند")
                return
            self.add_product_to_table(code, name, qty, price)

    def select_product_from_db(self):
        dialog = SelectProductDialog(self)
        if dialog.exec() and dialog.selected_product:
            prod = dialog.selected_product  # (id, code, name, price, description)
            code = prod[1]
            name = prod[2]
            price = prod[3]
            # گرفتن تعداد از کاربر
            from PySide6.QtWidgets import QInputDialog
            qty, ok = QInputDialog.getInt(self, "تعداد", f"تعداد {name} را وارد کنید:", 1, 1, 10000)
            if ok:
                self.add_product_to_table(code, name, qty, price)

    def remove_product(self):
        current_row = self.products_table.currentRow()
        if current_row >= 0:
            self.products_table.removeRow(current_row)
            self.update_totals()

    def on_item_double_clicked(self, item):
        # اجازه ویرایش فقط برای ستون تعداد (2) و قیمت (3)
        if item.column() in (2, 3):
            self.products_table.editItem(item)

    def on_item_changed(self, item):
        if item.column() in (2, 3):
            # اعتبارسنجی
            try:
                new_val = int(item.text())
                if new_val <= 0:
                    raise ValueError
                # بروزرسانی جمع آن ردیف
                row = item.row()
                qty_item = self.products_table.item(row, 2)
                price_item = self.products_table.item(row, 3)
                if qty_item and price_item:
                    qty = int(qty_item.text())
                    price = int(price_item.text())
                    total = qty * price
                    self.products_table.blockSignals(True)
                    self.products_table.setItem(row, 4, QTableWidgetItem(str(total)))
                    self.products_table.blockSignals(False)
                    self.update_totals()
            except ValueError:
                # اگر مقدار نامعتبر بود، مقدار قبلی را برگردانیم (کاربر باید اصلاح کند)
                QMessageBox.warning(self, "خطا", "تعداد و قیمت باید اعداد مثبت باشند")
                # ساده: دوباره مقدار قبلی را از حافظه می‌خوانیم (می‌توان قبلی را ذخیره کرد)
                self.update_totals()

    def create_invoice(self):
        # اعتبارسنجی شماره فاکتور تکراری
        invoice_number = self.invoice_number.text().strip()
        if not invoice_number:
            QMessageBox.warning(self, "خطا", "شماره فاکتور را وارد کنید")
            return
        if is_invoice_number_exists(invoice_number):
            QMessageBox.warning(self, "خطا", "این شماره فاکتور قبلاً ثبت شده است")
            return

        # جمع‌آوری اطلاعات مشتری
        customer_data = {
            "customer_name": self.customer_name.text(),
            "customer_phone": self.customer_phone.text(),
            "customer_national_code": self.customer_national_code.text(),
            "customer_economic_code": self.customer_economic_code.text(),
            "customer_postal_code": self.customer_postal_code.text(),
            "customer_address": self.customer_address.text(),
        }
        if not customer_data["customer_name"] or not customer_data["customer_phone"]:
            QMessageBox.warning(self, "خطا", "نام و شماره تلفن مشتری الزامی است")
            return

        # تاریخ (تبدیل به رشته شمسی)
        qdate = self.invoice_date.date()
        greg_date = QDate(qdate.year(), qdate.month(), qdate.day())
        # تبدیل به شمسی - ساده: چون QDate تاریخ میلادی می‌دهد، ما از jdatetime استفاده می‌کنیم
        # اما QDateEdit میلادی است. بهتر است از یک ویجت سفارشی استفاده کنیم. برای سادگی، تاریخ میلادی را به شمسی تبدیل می‌کنیم.
        # روش: از کتابخانه jdatetime برای تبدیل استفاده می‌کنیم. ابتدا تاریخ میلادی را به tuple تبدیل می‌کنیم.
        from datetime import date
        g_date = date(greg_date.year(), greg_date.month(), greg_date.day())
        shamsi = jdatetime.date.fromgregorian(date=g_date)
        invoice_date_str = shamsi.strftime("%Y/%m/%d")

        # جمع‌آوری کالاها
        items = []
        for row in range(self.products_table.rowCount()):
            item = {
                "code": self.products_table.item(row, 0).text(),
                "name": self.products_table.item(row, 1).text(),
                "qty": int(self.products_table.item(row, 2).text()),
                "price": int(self.products_table.item(row, 3).text()),
            }
            items.append(item)
        if not items:
            QMessageBox.warning(self, "خطا", "حداقل یک کالا باید اضافه شود")
            return

        try:
            pdf_path = create_invoice_from_gui(customer_data, items, invoice_number, invoice_date_str)
            QMessageBox.information(self, "موفق", f"فاکتور با موفقیت ساخته شد\nPDF: {pdf_path}")
            # پاک کردن فرم پس از موفقیت
            self.clear_form()
        except Exception as e:
            QMessageBox.critical(self, "خطا", f"خطا در ساخت فاکتور:\n{str(e)}")

    def clear_form(self):
        self.customer_name.clear()
        self.customer_phone.clear()
        self.customer_national_code.clear()
        self.customer_economic_code.clear()
        self.customer_postal_code.clear()
        self.customer_address.clear()
        self.invoice_number.clear()
        self.products_table.setRowCount(0)
        self.update_totals()
        # تاریخ را به امروز تنظیم کنید
        today = jdatetime.date.today()
        self.invoice_date.setDate(QDate(today.year, today.month, today.day))