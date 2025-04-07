from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QLineEdit, QLabel, QVBoxLayout
from PyQt6.QtGui import QFont, QIcon, QPixmap, QPainter, QPalette, QBrush
from PyQt6.QtCore import Qt
from manager_login import ManagerLogin
from staff_login import StaffLogin


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("گیم نت")
        self.setWindowIcon(QIcon("logo.png"))
        self.setGeometry(300, 300, 600, 600)
        self.showMaximized()

        # Set background image
        self.set_background("1.jpg")
        self.init_main_menu()

    def set_background(self, image_path):
        """Sets a background image that scales with the window"""
        palette = self.palette()
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            print(f"Error: Could not load background image from {image_path}")
            return

        palette.setBrush(QPalette.ColorRole.Window, QBrush(pixmap.scaled(
            self.size(),
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )))
        self.setPalette(palette)

    def resizeEvent(self, event):
        """Handle window resize events to update the background"""
        self.set_background("1.jpg")
        super().resizeEvent(event)

    def init_main_menu(self):
        """Creates the main menu interface with Manager and Staff buttons."""
        self.clear_layout()

        # Create a central widget with transparent background
        central_widget = QWidget(self)
        central_widget.setStyleSheet("background: transparent;")
        self.setCentralWidget(central_widget)

        # Manager Button
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

        # Staff Button
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

        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        # Top half (empty)
        layout.addStretch(2)

        # Spacer for centering in bottom half
        layout.addStretch(1)

        # Buttons
        layout.addWidget(self.staff_button, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.manager_button, 0, Qt.AlignmentFlag.AlignCenter)

        # Bottom spacer
        layout.addStretch(1)

    def clear_layout(self):
        """Removes all widgets before switching screens."""
        for widget in self.findChildren(QPushButton):
            widget.deleteLater()
        for widget in self.findChildren(QLineEdit):
            widget.deleteLater()
        for widget in self.findChildren(QLabel):
            widget.deleteLater()

    def show_manager_login(self):
        self.clear_layout()
        self.manager_login = ManagerLogin(self)
        self.setCentralWidget(self.manager_login)
        self.set_background("1.jpg")

    def show_staff_login(self):
        self.clear_layout()
        self.staff_login = StaffLogin(self)
        self.setCentralWidget(self.staff_login)
        self.set_background("1.jpg")


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()