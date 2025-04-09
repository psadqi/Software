from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QMessageBox, QVBoxLayout, QHBoxLayout, QDialog
)
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt
from data_base import DataBase
from passlib.hash import argon2

class ManagerLogin(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        # Outer layout
        outer_layout = QHBoxLayout(self)

        # === Left fixed container ===
        fixed_left_widget = QWidget()
        fixed_left_widget.setFixedSize(400, 600)
        fixed_left_layout = QVBoxLayout(fixed_left_widget)
        fixed_left_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Title label
        self.label = QLabel("ورود مدیر")
        self.label.setFont(QFont('nazanintar', 28))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 28px;
                font-weight: bold;
                border-radius: 5px;
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

        # Staff image
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

        # Form layout
        form_layout = QVBoxLayout()
        form_layout.setSpacing(20)

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

        self.password = QLineEdit()
        self.password.setFont(QFont('nazanintar', 16))
        self.password.setPlaceholderText("رمز عبور")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.setStyleSheet(self.username.styleSheet())
        # Connect returnPressed signal to check_login
        self.password.returnPressed.connect(self.check_login)
        form_layout.addWidget(self.password)

        # Buttons layout
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(20)

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
        # Set as default button to respond to Enter key
        self.login_button.setDefault(True)
        buttons_layout.addWidget(self.login_button)

        form_layout.addLayout(buttons_layout)

        # Help button
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

        # Wrap fixed_left_widget with spacing
        left_side = QVBoxLayout()
        left_side.addStretch(1)
        left_side.addWidget(fixed_left_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        left_side.addStretch(1)

        outer_layout.addLayout(left_side, 1)
        outer_layout.addStretch(1)

    def check_login(self):
        db = DataBase("project_db.db")
        username = self.username.text()
        password = self.password.text()

        try:
            stored_hash = db.manager_pass(username)
            if stored_hash and argon2.verify(password, stored_hash[0]):
                QMessageBox.information(
                    self, "ورود", "مدیر خوش آمدید", QMessageBox.StandardButton.Ok)
                # Proceed to next screen
            else:
                QMessageBox.warning(
                    self, "خطا", "نام کاربری یا رمز عبور اشتباه است",
                    QMessageBox.StandardButton.Ok)
                self.username.setText("")
                self.password.setText("")
        except Exception as e:
            QMessageBox.critical(
                self, "خطا", f"مشکل در سیستم به وجود آمده: {str(e)}",
                QMessageBox.StandardButton.Ok)
            self.username.setText("")
            self.password.setText("")

    def show_help(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("بازیابی رمز عبور")
        dialog.setFixedSize(400, 300)
        dialog.setStyleSheet("background-color: #7da9b8;")

        # Main layout
        main_layout = QVBoxLayout()

        # First stage widgets
        first_stage_widget = QWidget()
        first_layout = QVBoxLayout()

        label = QLabel("لطفاً اطلاعات مورد نیاز را وارد کنید:")
        label.setFont(QFont('nazanintar', 20))
        label.setWordWrap(True)
        first_layout.addWidget(label)

        self.username_edit = QLineEdit()
        self.answer_edit = QLineEdit()
        self.username_edit.setPlaceholderText("نام کاربری")
        self.username_edit.setStyleSheet("""
            QLineEdit {
                background-color: #e1e8f0;
                border-radius: 3px;
            }
        """)
        self.username_edit.setFont(QFont('nazanintar', 16))

        self.answer_edit.setPlaceholderText("جواب سوال امنیتی")
        self.answer_edit.setStyleSheet("""
            QLineEdit {
                background-color: #e1e8f0;
                border-radius: 3px;
            }
        """)
        self.answer_edit.setFont(QFont('nazanintar', 16))
        first_layout.addWidget(self.username_edit)
        first_layout.addWidget(self.answer_edit)

        self.verify_button = QPushButton("تایید")
        self.verify_button.setFont(QFont('nazanintar', 16))
        self.verify_button.setStyleSheet("""
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
        first_layout.addWidget(self.verify_button)
        first_stage_widget.setLayout(first_layout)
        main_layout.addWidget(first_stage_widget)

        # Second stage widgets (initially hidden)
        self.second_stage_widget = QWidget()
        second_layout = QVBoxLayout()
        self.new_pass_label = QLabel("رمز عبور جدید را وارد کنید:")
        self.new_pass_label.setFont(QFont('nazanintar', 16))
        second_layout.addWidget(self.new_pass_label)

        self.new_pass_edit = QLineEdit()
        self.new_pass_edit.setPlaceholderText("رمز عبور جدید")
        self.new_pass_edit.setFont(QFont('nazanintar', 16))
        self.new_pass_edit.setStyleSheet("""
            QLineEdit {
                background-color: #e1e8f0;
                border-radius: 3px;
            }
        """)
        self.new_pass_edit.setEchoMode(QLineEdit.EchoMode.Password)
        # Connect returnPressed to submit_new_password
        self.new_pass_edit.returnPressed.connect(self.submit_new_password)
        second_layout.addWidget(self.new_pass_edit)

        self.confirm_pass_edit = QLineEdit()
        self.confirm_pass_edit.setPlaceholderText("تکرار رمز عبور")
        self.confirm_pass_edit.setFont(QFont('nazanintar', 16))
        self.confirm_pass_edit.setStyleSheet("""
            QLineEdit {
                background-color: #e1e8f0;
                border-radius: 3px;
            }
        """)
        self.confirm_pass_edit.setEchoMode(QLineEdit.EchoMode.Password)
        # Connect returnPressed to submit_new_password
        self.confirm_pass_edit.returnPressed.connect(self.submit_new_password)
        second_layout.addWidget(self.confirm_pass_edit)

        self.submit_button = QPushButton("تغییر رمز")
        self.submit_button.setFont(QFont('nazanintar', 16))
        self.submit_button.setStyleSheet("""
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
        second_layout.addWidget(self.submit_button)
        self.second_stage_widget.setLayout(second_layout)
        main_layout.addWidget(self.second_stage_widget)
        self.second_stage_widget.hide()

        dialog.setLayout(main_layout)

        def verify_answer():
            db = DataBase("project_db.db")
            passRecovery = db.manager_recovery(self.username_edit.text())

            if passRecovery and passRecovery[0] == self.answer_edit.text():
                first_stage_widget.hide()
                self.second_stage_widget.show()
                dialog.setFixedSize(400, 250)
            else:
                QMessageBox.warning(
                    self, "خطا", "اطلاعات وارد شده صحیح نیست",
                    QMessageBox.StandardButton.Ok)
                self.username_edit.setText("")
                self.answer_edit.setText("")

        def submit_new_password():
            new_pass = self.new_pass_edit.text()
            confirm_pass = self.confirm_pass_edit.text()

            if not new_pass:
                QMessageBox.warning(
                    self, "خطا", "لطفاً رمز عبور جدید را وارد کنید",
                    QMessageBox.StandardButton.Ok)
                return

            if new_pass != confirm_pass:
                QMessageBox.warning(
                    self, "خطا", "رمزهای عبور مطابقت ندارند",
                    QMessageBox.StandardButton.Ok)
                return

            try:
                db = DataBase("project_db.db")
                db.update_pass(self.username_edit.text(), new_pass)
                QMessageBox.information(
                    self, "موفق", "رمز عبور با موفقیت تغییر یافت",
                    QMessageBox.StandardButton.Ok)
                dialog.accept()
            except Exception as e:
                QMessageBox.critical(
                    self, "خطا", f"خطا در تغییر رمز عبور: {str(e)}",
                    QMessageBox.StandardButton.Ok)

        # Also connect Enter key in answer_edit to verify_answer
        self.answer_edit.returnPressed.connect(verify_answer)
        self.verify_button.clicked.connect(verify_answer)
        self.submit_button.clicked.connect(submit_new_password)
        dialog.exec()