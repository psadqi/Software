# وارد کردن ویجت‌های مورد نیاز از کتابخانه PyQt6
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QLineEdit, QLabel, QVBoxLayout
from PyQt6.QtGui import QFont, QIcon, QPixmap, QPainter, QPalette, QBrush
from PyQt6.QtCore import Qt

# وارد کردن صفحات ورود مالک و کارکن از فایل‌های جداگانه
from manager_login import ManagerLogin
from staff_login import StaffLogin

# تعریف کلاس اصلی پنجره که از QMainWindow ارث‌بری می‌کند
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # تنظیم عنوان پنجره
        self.setWindowTitle("گیم نت")

        # تنظیم آیکون پنجره (تصویر لوگو)
        self.setWindowIcon(QIcon("logo.png"))

        # تنظیم اندازه و موقعیت اولیه پنجره
        self.setGeometry(300, 200, 1000, 600)

        # تعیین تصویر پس‌زمینه برای پنجره
        self.set_background("main.jpg")

        # مقداردهی اولیه منوی اصلی
        self.init_main_menu()

    def set_background(self, image_path):
        """تنظیم تصویر پس‌زمینه با قابلیت تغییر اندازه خودکار با پنجره"""

        # گرفتن پالت رنگ فعلی پنجره
        palette = self.palette()

        # بارگذاری تصویر
        pixmap = QPixmap(image_path)

        # اگر تصویر بارگذاری نشد، خطا چاپ می‌شود
        if pixmap.isNull():
            print(f"Error: Could not load background image from {image_path}")
            return

        # تنظیم تصویر به عنوان پس‌زمینه با مقیاس مناسب
        palette.setBrush(QPalette.ColorRole.Window, QBrush(pixmap.scaled(
            self.size(),  # اندازه فعلی پنجره
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,  # حفظ نسبت تصویر
            Qt.TransformationMode.SmoothTransformation  # کیفیت بالا در تغییر اندازه
        )))

        # اعمال پالت به پنجره
        self.setPalette(palette)

    def resizeEvent(self, event):
        """به‌روزرسانی تصویر پس‌زمینه هنگام تغییر اندازه پنجره"""
        self.set_background("main.jpg")
        super().resizeEvent(event)

    def init_main_menu(self):
        """ایجاد منوی اصلی با دکمه‌های ورود برای مالک و کارکن"""

        # پاک‌سازی ویجت‌های موجود در صورت وجود
        self.clear_layout()

        # ایجاد یک ویجت مرکزی با پس‌زمینه شفاف
        central_widget = QWidget(self)
        central_widget.setStyleSheet("background: transparent;")
        self.setCentralWidget(central_widget)

        # ساخت دکمه ورود مالک
        self.manager_button = QPushButton("مالک", central_widget)
        self.manager_button.setFont(QFont('nazanintar', 20))
        self.manager_button.setStyleSheet("""
            QPushButton {
                background-color: #4a709b;
                border-radius: 5px;
                color: white;
                min-width: 300px;
                min-height: 50px;
            }
            QPushButton:hover {
                background-color: #6f86a1;
            }
        """)
        self.manager_button.clicked.connect(self.show_manager_login)

        # ساخت دکمه ورود کارکن
        self.staff_button = QPushButton("کارکن", central_widget)
        self.staff_button.setFont(QFont("nazanintar", 20))
        self.staff_button.setStyleSheet("""
            QPushButton {
                background-color: #4a709b;
                border-radius: 5px;
                color: white;
                min-width: 300px;
                min-height: 50px;
            }
            QPushButton:hover {
                background-color: #6f86a1;
            }
        """)
        self.staff_button.clicked.connect(self.show_staff_login)

        # ایجاد لایه عمودی برای چیدمان عناصر
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        # افزودن فاصله برای جای‌گیری بهتر دکمه‌ها در وسط
        layout.addStretch(2)  # فضای بالا
        layout.addStretch(1)  # فضای بین بالا و دکمه‌ها

        # افزودن دکمه‌ها به صورت وسط‌چین
        layout.addWidget(self.staff_button, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.manager_button, 0, Qt.AlignmentFlag.AlignCenter)

        layout.addStretch(1)  # فضای پایین

    def clear_layout(self):
        """حذف همه ویجت‌های دکمه، ورودی، و برچسب از پنجره هنگام تغییر صفحه"""
        for widget in self.findChildren(QPushButton):
            widget.deleteLater()
        for widget in self.findChildren(QLineEdit):
            widget.deleteLater()
        for widget in self.findChildren(QLabel):
            widget.deleteLater()

    def show_manager_login(self):
        """نمایش فرم ورود مالک"""
        self.clear_layout()
        self.manager_login = ManagerLogin(self)
        self.setCentralWidget(self.manager_login)

    def show_staff_login(self):
        """نمایش فرم ورود کارکن"""
        self.clear_layout()
        self.staff_login = StaffLogin(self)
        self.setCentralWidget(self.staff_login)

# اجرای برنامه در صورت اجرای مستقیم فایل
if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
