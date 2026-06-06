from PySide6.QtWidgets import (
    QDialog,
    QFormLayout,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLabel
)
from PySide6.QtCore import Qt


class AddProductDialog(QDialog):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("افزودن کالا جدید")
        self.setMinimumWidth(400)   # افزایش عرض
        self.setMinimumHeight(250)  # افزایش ارتفاع
        self.resize(450, 300)       # اندازه پیش‌فرض

        # لایه اصلی عمودی
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # فرم ورودی
        form = QFormLayout()
        form.setSpacing(10)
        form.setLabelAlignment(Qt.AlignLeft)

        self.code = QLineEdit()
        self.code.setPlaceholderText("مثال: 12345")
        self.name = QLineEdit()
        self.name.setPlaceholderText("نام کالا")
        self.qty = QLineEdit()
        self.qty.setPlaceholderText("عدد")
        self.price = QLineEdit()
        self.price.setPlaceholderText("ریال")

        form.addRow("کد کالا :", self.code)
        form.addRow("نام کالا :", self.name)
        form.addRow("تعداد :", self.qty)
        form.addRow("قیمت :", self.price)

        layout.addLayout(form)

        # دکمه‌ها در پایین
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        self.btn_save = QPushButton("ثبت کالا")
        self.btn_save.setFixedWidth(100)
        self.btn_cancel = QPushButton("انصراف")
        self.btn_cancel.setFixedWidth(100)

        btn_layout.addWidget(self.btn_save)
        btn_layout.addWidget(self.btn_cancel)
        layout.addLayout(btn_layout)

        # اتصال رویدادها
        self.btn_save.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)

        # فوکوس اول روی کد کالا
        self.code.setFocus()