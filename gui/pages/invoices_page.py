from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit, QLabel, QMessageBox, QHeaderView
)
from PySide6.QtCore import Qt
from database.invoice_repo import get_all_invoices, get_invoice_items
from database.customer_repo import get_customer_by_id
from services.invoice_service import regenerate_pdf  # تابعی که می‌سازیم
import os

class InvoicesPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        layout.addWidget(
            QLabel("صفحه فاکتورها")
        )

class InvoicesPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        # جستجو
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("جستجو بر اساس شماره فاکتور یا نام مشتری...")
        self.search_btn = QPushButton("جستجو")
        self.search_btn.clicked.connect(self.search_invoices)
        self.refresh_btn = QPushButton("بازخوانی")
        self.refresh_btn.clicked.connect(self.load_invoices)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_btn)
        search_layout.addWidget(self.refresh_btn)
        layout.addLayout(search_layout)

        # جدول فاکتورها
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["شناسه", "شماره فاکتور", "تاریخ", "نام مشتری", "مبلغ نهایی", "عملیات"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)

        self.load_invoices()

    def load_invoices(self, invoices=None):
        if invoices is None:
            invoices = get_all_invoices()
        self.table.setRowCount(0)
        for row, inv in enumerate(invoices):
            # inv: (id, invoice_number, invoice_date, customer_id, total_price, tax, final_price)
            customer = get_customer_by_id(inv[3])
            customer_name = customer[1] if customer else "نامشخص"
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(inv[0])))
            self.table.setItem(row, 1, QTableWidgetItem(inv[1]))
            self.table.setItem(row, 2, QTableWidgetItem(inv[2]))
            self.table.setItem(row, 3, QTableWidgetItem(customer_name))
            self.table.setItem(row, 4, QTableWidgetItem(f"{inv[6]:,}"))
            # دکمه چاپ مجدد در ستون ۵
            btn = QPushButton("چاپ PDF")
            btn.clicked.connect(lambda checked, iid=inv[0]: self.reprint_pdf(iid))
            self.table.setCellWidget(row, 5, btn)

    def search_invoices(self):
        keyword = self.search_input.text().strip().lower()
        if not keyword:
            self.load_invoices()
            return
        all_invoices = get_all_invoices()
        filtered = []
        for inv in all_invoices:
            customer = get_customer_by_id(inv[3])
            customer_name = customer[1] if customer else ""
            if keyword in inv[1].lower() or keyword in customer_name.lower():
                filtered.append(inv)
        self.load_invoices(filtered)

    def reprint_pdf(self, invoice_id):
        try:
            pdf_path = regenerate_pdf(invoice_id)
            QMessageBox.information(self, "موفق", f"PDF مجدداً ساخته شد:\n{pdf_path}")
        except Exception as e:
            QMessageBox.critical(self, "خطا", f"خطا در ساخت PDF: {str(e)}")