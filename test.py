import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QButtonGroup, QPushButton, QVBoxLayout, QWidget, QGroupBox
from PyQt6.QtCore import Qt, QPoint

class MouseTrackingApp(QWidget):
    def __init__(self):
        super().__init__()

        group = QGroupBox()
        x = QPushButton()
        y = QPushButton()
        z = QPushButton()
        a = QLabel("BUttons")

        group.addAction(x)
        group.addAction(y)
        group.addAction(z)

        self.layout = QVBoxLayout()
        self.layout.addWidget(a)
        self.layout.addWidget()
        self.setLayout(self.layout)
        


def main():
    app = QApplication(sys.argv)
    window = MouseTrackingApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()