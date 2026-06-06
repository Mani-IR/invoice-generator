# import sys

# from PySide6.QtWidgets import QApplication

# from gui.main_window import MainWindow


# def main():

#     app = QApplication(sys.argv)

#     window = MainWindow()
#     window.show()

#     sys.exit(app.exec())


# if __name__ == "__main__":
#     main()





# gui/app.py
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from gui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setLayoutDirection(Qt.RightToLeft)  # کل برنامه راست‌چین می‌شود

    # تنظیم فونت فارسی (اگر فونت مورد نظر روی سیستم باشد)
    from PySide6.QtGui import QFont
    font = QFont("Vazirmatn", 10)  # یا "B Nazanin", "Tahoma"
    app.setFont(font)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()