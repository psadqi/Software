# ایمپورت کلاس‌ها و توابع موردنیاز از PyQt6
from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QMessageBox, QVBoxLayout, QHBoxLayout
)
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt
from data_base import DataBase  # ایمپورت کلاس پایگاه داده برای بررسی اطلاعات

# تعریف کلاس ورود کارکن
class StaffLogin(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent  # نگهداری ارجاع به پنجره والد
        self.setup_ui()       # راه‌اندازی رابط کاربری

    # متد راه‌اندازی رابط گرافیکی
    def setup_ui(self):
        self.setStyleSheet("background-color: white;border-radius: 20px;")  # تنظیم ظاهر کلی ویجت

        # لایه بیرونی افقی شامل بخش‌های چپ و راست
        outer_layout = QHBoxLayout(self)

        # === ویجت ثابت سمت چپ ===
        fixed_left_widget = QWidget()
        fixed_left_widget.setFixedSize(400, 600)  # اندازه ثابت برای بخش چپ
        fixed_left_layout = QVBoxLayout(fixed_left_widget)
        fixed_left_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # تراز وسط چین

        # عنوان صفحه "ورود کارکن"
        self.label = QLabel("ورود کارکن")
        self.label.setFont(QFont('nazanintar', 28))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet(""" 
            QLabel {
                color: white;
                font-size: 28px;
                font-weight: bold;
                border-radius: 15px;
                padding: 8px 20px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(150, 150, 150, 220),
                    stop:0.5 rgba(120, 120, 120, 240),
                    stop:1 rgba(90, 90, 90, 220));
                border: 2px solid #e0e0e0;
                text-shadow: 2px 2px 3px black;
            }
        """)
        fixed_left_layout.addWidget(self.label)

        # تصویر نمادین کارمند
        self.staff_image = QLabel()
        staff_pixmap = QPixmap("staff.png")
        if not staff_pixmap.isNull():
            self.staff_image.setPixmap(staff_pixmap.scaled(
                300, 300,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            ))
        self.staff_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        fixed_left_layout.addWidget(self.staff_image)

        # لایه فرم ورود
        form_layout = QVBoxLayout()
        form_layout.setSpacing(20)

        # فیلد نام کاربری
        self.username = QLineEdit()
        self.username.setFont(QFont('nazanintar', 16))
        self.username.setPlaceholderText("نام کاربری")
        self.username.setStyleSheet("""
            QLineEdit {
                background: white;
                border: 2px solid #3498db;
                border-radius: 5px;
                padding: 5px;
                min-width: 300px;
            }
        """)
        form_layout.addWidget(self.username)

        # فیلد رمز عبور
        self.password = QLineEdit()
        self.password.setFont(QFont('nazanintar', 16))
        self.password.setPlaceholderText("رمز عبور")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)  # نمایش نقطه به‌جای کاراکتر
        self.password.setStyleSheet(self.username.styleSheet())
        self.password.returnPressed.connect(self.check_login)  # زدن Enter باعث ورود شود
        form_layout.addWidget(self.password)

        # لایه دکمه‌ها
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(20)

        # دکمه بازگشت
        self.back_button = QPushButton("بازگشت")
        self.back_button.setFont(QFont('nazanintar', 20))
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border-radius: 5px;
                min-width: 120px;
                min-height: 50px;
            }
            QPushButton:hover {
                background-color: #e0392b;
            }
        """)
        self.back_button.clicked.connect(lambda: self.parent.init_main_menu())  # بازگشت به منوی اصلی
        buttons_layout.addWidget(self.back_button)

        # دکمه ورود
        self.login_button = QPushButton("ورود")
        self.login_button.setFont(QFont('nazanintar', 20))
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 5px;
                min-width: 120px;
                min-height: 50px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.login_button.clicked.connect(self.check_login)  # اتصال دکمه به متد ورود
        self.login_button.setDefault(True)  # پیش‌فرض برای فشردن Enter
        buttons_layout.addWidget(self.login_button)

        form_layout.addLayout(buttons_layout)

        # دکمه راهنما / بازیابی رمز عبور
        self.help_button = QPushButton("بازیابی رمز عبور")
        self.help_button.setFont(QFont('nazanintar', 20))
        self.help_button.setStyleSheet("""
            QPushButton {
                background-color: #4a709b;
                color: white;
                border-radius: 5px;
                min-width: 180px;
                min-height: 50px;
            }
            QPushButton:hover {
                background-color: #6f86a1;
            }
        """)
        self.help_button.clicked.connect(self.show_help)  # نمایش پیام راهنما
        form_layout.addWidget(self.help_button, alignment=Qt.AlignmentFlag.AlignCenter)

        fixed_left_layout.addLayout(form_layout)

        # --- مرکزچین کردن ویجت چپ در لایه خارجی ---
        left_side = QVBoxLayout()
        left_side.addStretch(1)
        left_side.addWidget(fixed_left_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        left_side.addStretch(1)

        outer_layout.addLayout(left_side, 1)  # نیمه چپ
        outer_layout.addStretch(1)           # نیمه راست (خالی)

    # بررسی اطلاعات ورود
    def check_login(self):
        db = DataBase("project_db.db")  # اتصال به پایگاه داده

        username = self.username.text()
        password = self.password.text()

        try:
            correct_password = db.staff_pass(username)  # دریافت رمز صحیح از پایگاه داده
            if correct_password and correct_password[0] == password:
                QMessageBox.information(self, "ورود", "خوش آمدید", QMessageBox.StandardButton.Ok)
                # ورود موفق، می‌توان به صفحه بعدی منتقل شد
            else:
                QMessageBox.warning(self, "خطا", "نام کاربری یا رمز عبور اشتباه است!", QMessageBox.StandardButton.Ok)
                self.password.setText("")  # پاک کردن رمز عبور اشتباه
        except Exception as e:
            QMessageBox.critical(self, "خطا", "مشکلی در سیستم به وجود آمده است!", QMessageBox.StandardButton.Ok)
            self.password.setText("")

    # متد راهنما
    def show_help(self):
        QMessageBox.information(self, "راهنما", "در صورت نیاز به راهنمایی، با مدیر تماس بگیرید.", QMessageBox.StandardButton.Ok)
