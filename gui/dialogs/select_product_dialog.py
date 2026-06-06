from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QHBoxLayout, QLabel, QHeaderView
)
from PySide6.QtCore import Qt
from database.product_repo import get_all_products


class SelectProductDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("انتخاب کالا از لیست")
        self.setMinimumSize(600, 400)
        self.selected_product = None
        self.current_products = []  # لیست محصولات در حال نمایش

        layout = QVBoxLayout(self)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("جستجو بر اساس کد یا نام...")
        self.search_input.textChanged.connect(self.search_products)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["کد", "نام", "قیمت"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.doubleClicked.connect(self.accept_selection)

        btn_layout = QHBoxLayout()
        self.btn_select = QPushButton("انتخاب")
        self.btn_cancel = QPushButton("انصراف")
        self.btn_select.clicked.connect(self.accept_selection)
        self.btn_cancel.clicked.connect(self.reject)

        btn_layout.addWidget(self.btn_select)
        btn_layout.addWidget(self.btn_cancel)

        layout.addWidget(QLabel("جستجو:"))
        layout.addWidget(self.search_input)
        layout.addWidget(self.table)
        layout.addLayout(btn_layout)

        self.load_all_products()

    def load_all_products(self):
        self.current_products = get_all_products()
        self.populate_table(self.current_products)

    def populate_table(self, products):
        self.table.setRowCount(0)
        for row, prod in enumerate(products):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(prod[1]))
            self.table.setItem(row, 1, QTableWidgetItem(prod[2]))
            self.table.setItem(row, 2, QTableWidgetItem(f"{prod[3]:,}"))

    def search_products(self):
        keyword = self.search_input.text().strip().lower()
        if not keyword:
            self.current_products = get_all_products()
        else:
            all_prods = get_all_products()
            self.current_products = [p for p in all_prods if keyword in p[1].lower() or keyword in p[2].lower()]
        self.populate_table(self.current_products)

    def accept_selection(self):
        current_row = self.table.currentRow()
        if current_row >= 0 and current_row < len(self.current_products):
            self.selected_product = self.current_products[current_row]
            self.accept()
        else:
            self.reject()