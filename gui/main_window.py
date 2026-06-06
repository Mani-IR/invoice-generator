from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QStackedWidget
)

from gui.pages.create_invoice_page import CreateInvoicePage
from gui.pages.customers_page import CustomersPage
from gui.pages.products_page import ProductsPage
from gui.pages.invoices_page import InvoicesPage


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Invoice Generator")
        self.resize(1200, 700)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)

        menu_layout = QVBoxLayout()

        self.btn_invoice = QPushButton("ساخت فاکتور")
        self.btn_customers = QPushButton("مشتریان")
        self.btn_products = QPushButton("محصولات")
        self.btn_invoices = QPushButton("فاکتورها")
        self.btn_exit = QPushButton("خروج")

        menu_layout.addWidget(self.btn_invoice)
        menu_layout.addWidget(self.btn_customers)
        menu_layout.addWidget(self.btn_products)
        menu_layout.addWidget(self.btn_invoices)
        menu_layout.addStretch()
        menu_layout.addWidget(self.btn_exit)

        self.pages = QStackedWidget()

        self.page_invoice = CreateInvoicePage()
        self.page_customers = CustomersPage()
        self.page_products = ProductsPage()
        self.page_invoices = InvoicesPage()

        self.pages.addWidget(self.page_invoice)
        self.pages.addWidget(self.page_customers)
        self.pages.addWidget(self.page_products)
        self.pages.addWidget(self.page_invoices)

        main_layout.addLayout(menu_layout, 1)
        main_layout.addWidget(self.pages, 4)

        self.btn_invoice.clicked.connect(
            lambda: self.pages.setCurrentIndex(0)
        )

        self.btn_customers.clicked.connect(
            lambda: self.pages.setCurrentIndex(1)
        )

        self.btn_products.clicked.connect(
            lambda: self.pages.setCurrentIndex(2)
        )

        self.btn_invoices.clicked.connect(
            lambda: self.pages.setCurrentIndex(3)
        )

        self.btn_exit.clicked.connect(self.close)