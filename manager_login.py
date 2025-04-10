from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QMessageBox, QVBoxLayout, QHBoxLayout, QDialog, QToolButton
)
from PyQt6.QtGui import QFont, QPixmap, QIcon
from PyQt6.QtCore import Qt, QSize
from data_base import DataBase


# کلاس ورود مدیر
class ManagerLogin(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()

    # تنظیمات رابط کاربری
    def setup_ui(self):
        self.setStyleSheet("background-color: white;border-radius: 20px;")
        outer_layout = QHBoxLayout(self)

        # ویجت سمت چپ ثابت برای نمایش محتوا
        fixed_left_widget = QWidget()
        fixed_left_widget.setFixedSize(400, 600)
        fixed_left_widget.setStyleSheet("background-color: white;")
        fixed_left_layout = QVBoxLayout(fixed_left_widget)
        fixed_left_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # برچسب برای نمایش عنوان "ورود مدیر"
        self.label = QLabel("ورود مدیر")
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

        # تصویر مربوط به مدیر
        self.staff_image = QLabel()
        staff_pixmap = QPixmap("manager.png")
        if not staff_pixmap.isNull():
            self.staff_image.setPixmap(staff_pixmap.scaled(
                300, 300,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            ))
        self.staff_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        fixed_left_layout.addWidget(self.staff_image)

        # طراحی فرم برای ورودی‌ها
        form_layout = QVBoxLayout()
        form_layout.setSpacing(20)

        # فیلد ورودی نام کاربری
        self.username = QLineEdit()
        self.username.setFont(QFont('nazanintar', 16))
        self.username.setPlaceholderText("\u200Eنام کاربری")
        self.username.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
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

        # فیلد ورودی رمز عبور با آیکون چشم
        self.password = QLineEdit()
        self.password.setFont(QFont('nazanintar', 16))
        self.password.setPlaceholderText("\u200Eرمز عبور")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.password.setStyleSheet("""
            QLineEdit {
                background: white;
                border: 2px solid #3498db;
                border-radius: 5px;
                padding: 5px;
                min-width: 300px;
                padding-right: 40px;  /* ایجاد فضا برای آیکون چشم */
            }
        """)
        self.password.returnPressed.connect(self.check_login)

        # دکمه چشم برای نمایش یا مخفی کردن رمز عبور
        self.eye_button = QToolButton(self.password)
        self.eye_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.eye_button.setStyleSheet("""
            QToolButton {
                border: none;
                background: transparent;
                padding: 0px;
                margin: 0px;
            }
        """)
        # تنظیم آیکون بزرگ برای چشم
        eye_icon = QIcon("eye.png")
        eye_off_icon = QIcon("eye-off.png")
        self.eye_button.setIconSize(QSize(30, 30))
        self.eye_button.setIcon(eye_icon)
        self.eye_button.clicked.connect(self.toggle_password_visibility)

        # موقعیت‌یابی دکمه چشم داخل فیلد رمز عبور
        self.eye_button.move(self.password.width() - 35, 5)
        self.eye_button.resize(30, 30)

        # بروزرسانی موقعیت دکمه چشم هنگام تغییر اندازه فیلد رمز عبور
        self.password.resizeEvent = lambda event: self.eye_button.move(
            self.password.width() - 35, 5
        )

        form_layout.addWidget(self.password)

        # طراحی دکمه‌ها
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(20)

        # دکمه برگشت
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
        self.back_button.clicked.connect(lambda: self.parent.init_main_menu())
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
        self.login_button.clicked.connect(self.check_login)
        self.login_button.setDefault(True)
        buttons_layout.addWidget(self.login_button)

        form_layout.addLayout(buttons_layout)

        # دکمه بازیابی رمز عبور
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
        self.help_button.clicked.connect(self.show_help)
        form_layout.addWidget(self.help_button, alignment=Qt.AlignmentFlag.AlignCenter)

        fixed_left_layout.addLayout(form_layout)

        left_side = QVBoxLayout()
        left_side.addStretch(1)
        left_side.addWidget(fixed_left_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        left_side.addStretch(1)

        outer_layout.addLayout(left_side, 1)
        outer_layout.addStretch(1)

    # تابع برای تغییر وضعیت نمایش رمز عبور
    def toggle_password_visibility(self):
        if self.password.echoMode() == QLineEdit.EchoMode.Password:
            self.password.setEchoMode(QLineEdit.EchoMode.Normal)
            self.eye_button.setIcon(QIcon("eye-off.png"))
        else:
            self.password.setEchoMode(QLineEdit.EchoMode.Password)
            self.eye_button.setIcon(QIcon("eye.png"))
        # حفظ اندازه آیکون
        self.eye_button.setIconSize(QSize(30, 30))

    # تابع برای بررسی ورود
    def check_login(self):
        db = DataBase("project_db.db")
        username = self.username.text()
        password = self.password.text()

        try:
            stored_hash = db.manager_pass(username)
            if stored_hash and db._verify_password(stored_hash[0], password):
                QMessageBox.information(
                    self, "ورود", "ورود موفقیت آمیز بود",
                    QMessageBox.StandardButton.Ok)
            else:
                QMessageBox.warning(
                    self, "خطا", "نام کاربری یا رمز عبور اشتباه است",
                    QMessageBox.StandardButton.Ok)
                self.password.setText("")
        except Exception as e:
            QMessageBox.critical(
                self, "خطا", f"خطا در سیستم: {str(e)}",
                QMessageBox.StandardButton.Ok)
            self.password.setText("")

    # تابع برای نمایش دیالوگ بازیابی رمز عبور
    def show_help(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("بازیابی رمز عبور")
        dialog.setFixedSize(400, 300)
        dialog.setStyleSheet("background-color: white;")

        main_layout = QVBoxLayout()

        first_stage_widget = QWidget()
        first_layout = QVBoxLayout()

        label = QLabel("لطفاً اطلاعات امنیتی را وارد کنید:")
        label.setFont(QFont('nazanintar', 20))
        label.setWordWrap(True)
        first_layout.addWidget(label)

        username_edit = QLineEdit()
        answer_edit = QLineEdit()
        username_edit.setPlaceholderText("نام کاربری")
        username_edit.setStyleSheet("""
            QLineEdit {
                background-color: #e1e8f0;
                border-radius: 3px;
            }
        """)
        username_edit.setFont(QFont('nazanintar', 16))

        answer_edit.setPlaceholderText("پاسخ سوال امنیتی")
        answer_edit.setStyleSheet("""
            QLineEdit {
                background-color: #e1e8f0;
                border-radius: 3px;
            }
        """)
        answer_edit.setFont(QFont('nazanintar', 16))
        first_layout.addWidget(username_edit)
        first_layout.addWidget(answer_edit)

        verify_button = QPushButton("تایید")
        verify_button.setFont(QFont('nazanintar', 16))
        verify_button.setStyleSheet("""
            QPushButton {
                background-color: #4a709b;
                border-radius: 5px;
                color: white;
                min-width: 300px;
                min-height: 40px;
            }
            QPushButton:hover {
                background-color: #6f86a1;
            }
        """)
        first_layout.addWidget(verify_button)
        first_stage_widget.setLayout(first_layout)
        main_layout.addWidget(first_stage_widget)

        second_stage_widget = QWidget()
        second_layout = QVBoxLayout()
        new_pass_label = QLabel("رمز عبور جدید را وارد کنید:")
        new_pass_label.setFont(QFont('nazanintar', 16))
        second_layout.addWidget(new_pass_label)

        new_pass_edit = QLineEdit()
        new_pass_edit.setPlaceholderText("رمز عبور جدید")
        new_pass_edit.setFont(QFont('nazanintar', 16))
        new_pass_edit.setStyleSheet("""
            QLineEdit {
                background-color: #e1e8f0;
                border-radius: 3px;
            }
        """)
        new_pass_edit.setEchoMode(QLineEdit.EchoMode.Password)
        second_layout.addWidget(new_pass_edit)

        confirm_pass_edit = QLineEdit()
        confirm_pass_edit.setPlaceholderText("تکرار رمز عبور")
        confirm_pass_edit.setFont(QFont('nazanintar', 16))
        confirm_pass_edit.setStyleSheet("""
            QLineEdit {
                background-color: #e1e8f0;
                border-radius: 3px;
            }
        """)
        confirm_pass_edit.setEchoMode(QLineEdit.EchoMode.Password)
        second_layout.addWidget(confirm_pass_edit)

        submit_button = QPushButton("تغییر رمز")
        submit_button.setFont(QFont('nazanintar', 16))
        submit_button.setStyleSheet("""
            QPushButton {
                background-color: #4a709b;
                color: white;
                border-radius: 5px;
                min-width: 180px;
                min-height: 40px;
            }
            QPushButton:hover {
                background-color: #6f86a1;
            }
        """)
        second_layout.addWidget(submit_button)
        second_stage_widget.setLayout(second_layout)
        main_layout.addWidget(second_stage_widget)
        second_stage_widget.hide()

        dialog.setLayout(main_layout)

        def verify_answer():
            db = DataBase("project_db.db")
            passRecovery = db.manager_recovery(username_edit.text())

            if passRecovery and passRecovery[0] == answer_edit.text():
                first_stage_widget.hide()
                second_stage_widget.show()
                dialog.setFixedSize(400, 250)
            else:
                QMessageBox.warning(
                    dialog, "خطا", "اطلاعات وارد شده صحیح نیست",
                    QMessageBox.StandardButton.Ok)
                username_edit.setText("")
                answer_edit.setText("")

        def submit_new_password():
            new_pass = new_pass_edit.text()
            confirm_pass = confirm_pass_edit.text()

            if not new_pass:
                QMessageBox.warning(
                    dialog, "خطا", "لطفاً رمز عبور جدید را وارد کنید",
                    QMessageBox.StandardButton.Ok)
                return

            if new_pass != confirm_pass:
                QMessageBox.warning(
                    dialog, "خطا", "رمزهای عبور مطابقت ندارند",
                    QMessageBox.StandardButton.Ok)
                return

            try:
                db = DataBase("project_db.db")
                db.update_pass(username_edit.text(), new_pass)
                QMessageBox.information(
                    dialog, "موفق", "رمز عبور با موفقیت تغییر یافت",
                    QMessageBox.StandardButton.Ok)
                dialog.accept()
            except Exception as e:
                QMessageBox.critical(
                    dialog, "خطا", f"خطا در تغییر رمز عبور: {str(e)}",
                    QMessageBox.StandardButton.Ok)

        answer_edit.returnPressed.connect(verify_answer)
        verify_button.clicked.connect(verify_answer)
        new_pass_edit.returnPressed.connect(submit_new_password)
        confirm_pass_edit.returnPressed.connect(submit_new_password)
        submit_button.clicked.connect(submit_new_password)

        dialog.exec()
