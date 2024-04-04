import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6.QtCore import Qt, QPoint

class MouseTrackingApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Mouse Tracking Example")
        self.setGeometry(100, 100, 400, 400)

        self.mouse_coordinates_label = QLabel(self)
        self.mouse_coordinates_label.setGeometry(10, 10, 150, 30)
        self.mouse_coordinates_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Track mouse movements in the main window
        self.setMouseTracking(True)

    def mousePressEvent(self, event):
        x = event.position().x()
        y = event.position().y()
        print(x, y)
        self.mouse_coordinates_label.setText(f"Mouse Coordinates: ({x}, {y})")


def main():
    app = QApplication(sys.argv)
    window = MouseTrackingApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()