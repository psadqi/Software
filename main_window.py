from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QLineEdit, QLabel
from PyQt6.QtGui import QPixmap, QPainter, QFont, QIcon
from manager_login import ManagerLogin
from staff_login import StaffLogin


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("گیم نت")
        self.setWindowIcon(QIcon("logo.png"))


        # Fixed window size (matches image size)
        self.setFixedSize(1100, 700)

        # Load the background image
        self.background = QPixmap("main.jpg")  # Ensure "main.jpg" is in the same folder

        # Central widget
        # self.central_widget = QWidget(self)
        # self.setCentralWidget(self.central_widget)

        self.init_main_menu()

    def paintEvent(self, event):
        """Handles painting the background image."""
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.background)  # Draw the image at the exact window size

    def init_main_menu(self):
        """Creates the main menu interface with Manager and Staff buttons."""
        self.clear_layout()

        # Recreate the Manager Button
        self.manager_button = QPushButton("مالک", self)
        self.manager_button.setGeometry((self.width() // 2) - 150, 600, 300, 50)
        self.manager_button.setFont(QFont('nazanintar', 20))
        self.manager_button.setStyleSheet("""
            QPushButton {
                background-color: rgb(75, 200, 255);
                border-radius: 14px;
                color: white;
            }
            QPushButton:hover {
                background-color: rgb(65, 180, 240);
            }
        """)
        self.manager_button.clicked.connect(self.show_manager_login)
        self.manager_button.show()  # Make sure it's visible

        # Recreate the Staff Button
        self.staff_button = QPushButton("کارکن", self)
        self.staff_button.setGeometry((self.width() // 2) - 150, 530, 300, 50)
        self.staff_button.setFont(QFont("nazanintar", 20))
        self.staff_button.setStyleSheet("""
            QPushButton {
                background-color: rgb(75, 200, 255);
                border-radius: 14px;
                color: white;
            }
            QPushButton:hover {
                background-color: rgb(65, 180, 240);
            }
        """)
        self.staff_button.clicked.connect(self.show_staff_login)
        self.staff_button.show()  # Make sure it's visible


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
        self.layout().addWidget(ManagerLogin(self))

    def show_staff_login(self):
        self.clear_layout()
        self.layout().addWidget(StaffLogin(self))

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
