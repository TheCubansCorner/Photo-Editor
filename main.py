#! python3
#! main.py -- Basic image editor

import os, sys, shutil

from PIL import Image
from PyQt6.QtGui import QIcon, QImage, QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QMainWindow, QHBoxLayout, QGridLayout, QVBoxLayout,
    QFileDialog, QSlider
)


class MainWindow(QMainWindow):
    def __init__(self):                                 # -- Initiates the application
        super().__init__()
        self.currentImage: str = ""
        self.tempImage: str = ""
        self.blackWhiteActive = False

        self.setWindowTitle("Image Editor")
        self.setFixedSize(600, 800)

        self.initWidget()
        self.initLayout()
        self.initConfigWidgets()
        self.initConfigConnections()
        self.initStyleSheets()
        self.widgetToolTips()

        self.setCentralWidget(self.mainContainer)

    def initWidget(self) -> None:                       # -- Initiates main window widgets
        self.mainContainer: QWidget = QWidget()                             # - QWidgets
        self.colapsedMenu: QWidget = QWidget()
        self.expandedMenu: QWidget = QWidget()
        self.mainApplication: QWidget = QWidget()
        
        # Colapsed Menu Buttons
        self.colapedMenuBtn: QWidget = QPushButton()                        # - QPushButtons
        self.colapsedLoadImageBtn: QWidget = QPushButton()
        self.colapsedBlackWhiteBtn: QWidget = QPushButton()

        # Expanded menu Buttons
        self.expandedMenuBtn: QWidget = QPushButton("Colapse")
        self.expandedLoadImageBtn: QWidget = QPushButton("Load Image")
        self.expandedBlackWhiteBtn: QWidget = QPushButton("Black/White")

        #self.expandedBlackWhiteSlide: QWidget = QSlider(Qt.Orientation.Horizontal)                   # - QSliders

        self.imageLabel: QWidget = QLabel()                                 # - QLabels

    def initLayout(self) -> None:                       # -- Applies widgets to layout/sets main layout
        self.mainContainer.layout = QHBoxLayout()       # - Main Layouts
        self.colapsedMenu.layout = QGridLayout()
        self.expandedMenu.layout = QGridLayout()
        self.mainApplication.layout = QVBoxLayout()

        self.colapsedMenu.layout.addWidget(self.colapedMenuBtn, 0, 0, Qt.AlignmentFlag.AlignLeft)
        self.colapsedMenu.layout.addWidget(self.colapsedLoadImageBtn, 1, 0, Qt.AlignmentFlag.AlignLeft)
        self.colapsedMenu.layout.addWidget(self.colapsedBlackWhiteBtn, 2, 0, Qt.AlignmentFlag.AlignLeft)

        self.expandedMenu.layout.addWidget(self.expandedMenuBtn, 0, 0, Qt.AlignmentFlag.AlignLeft)
        self.expandedMenu.layout.addWidget(self.expandedLoadImageBtn, 1, 0, Qt.AlignmentFlag.AlignLeft)
        self.expandedMenu.layout.addWidget(self.expandedBlackWhiteBtn, 2, 0, Qt.AlignmentFlag.AlignLeft)

        self.mainApplication.layout.addWidget(self.imageLabel, Qt.AlignmentFlag.AlignCenter)

        self.colapsedMenu.setLayout(self.colapsedMenu.layout)
        self.expandedMenu.setLayout(self.expandedMenu.layout)
        self.mainApplication.setLayout(self.mainApplication.layout)

        self.mainContainer.layout.addWidget(self.colapsedMenu)
        self.mainContainer.layout.addWidget(self.expandedMenu)
        self.mainContainer.layout.addWidget(self.mainApplication)
        
        self.mainContainer.setLayout(self.mainContainer.layout) 

    def initConfigWidgets(self) -> None:                # -- Configured widgets (size, width, etc)
        self.expandedMenu.hide()
        self.mainContainer.layout.setContentsMargins(0, 0, 0, 0)

        self.imageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)                                  # - Alignments

        pixmap = QPixmap(os.path.join("icons", "blank.jpg"))                                        # - Setting Pixmaps
        self.imageLabel.setPixmap(pixmap)

        self.colapedMenuBtn.setIcon(QIcon(os.path.join("icons", "colapsed-menu.png")))              # - Setting Icons
        self.colapsedLoadImageBtn.setIcon(QIcon(os.path.join("icons", "save-icon.png")))
        self.colapsedBlackWhiteBtn.setIcon(QIcon(os.path.join("icons", "black-white-icon.png")))

        self.expandedMenuBtn.setIcon(QIcon(os.path.join("icons", "expanded-menu.png")))
        self.expandedLoadImageBtn.setIcon(QIcon(os.path.join("icons", "save-icon.png")))
        self.expandedBlackWhiteBtn.setIcon(QIcon(os.path.join("icons", "black-white-icon.png")))

        self.mainApplication.setMaximumHeight(self.height())                                        # - Max Width/Height
        self.colapsedMenu.setMaximumWidth(40)
        self.expandedMenu.setMaximumWidth(150)
        self.expandedMenu.setMinimumWidth(150)

    def initConfigConnections(self) -> None:            # -- Configures connections between buttons and functions
        self.colapedMenuBtn.clicked.connect(self.expandSideMenu)
        self.expandedMenuBtn.clicked.connect(self.colapseSideMenu)
        self.colapsedLoadImageBtn.clicked.connect(self.openImageDialog)
        self.expandedLoadImageBtn.clicked.connect(self.openImageDialog)
        self.colapsedBlackWhiteBtn.clicked.connect(self.blackAndWhite)
        self.expandedBlackWhiteBtn.clicked.connect(self.blackAndWhite)

    def initStyleSheets(self) -> None:                  # -- Applies css stylesheets/incode styles to applicaiton
        self.colapsedMenu.setStyleSheet("background-color: darkgrey;")
        self.expandedMenu.setStyleSheet("background-color: darkgrey;")
        self.mainApplication.setStyleSheet("background-color: black; color: white;")

    def widgetToolTips(self) -> None:                   # -- Sets up widget hover tool tips
        self.colapedMenuBtn.setToolTip("Expand Menu")
        self.expandedMenuBtn.setToolTip("Colapse Menu")
        self.colapsedLoadImageBtn.setToolTip("Load Image")
        self.expandedLoadImageBtn.setToolTip("Load Image")  

    def expandSideMenu(self) -> None:                   # -- Expands the side menu
        self.colapsedMenu.hide()
        self.expandedMenu.show()

    def colapseSideMenu(self) -> None:                  # -- Colapses Side menu
        self.expandedMenu.hide()
        self.colapsedMenu.show()

    def openImageDialog(self) -> None:                  # -- Opens file dialogue to load images
        try:
            image_to_add: QWidget = QFileDialog.getOpenFileName(self, 'Open File', 'c:\\')[0]
            tempFile: str = os.path.split(image_to_add)[-1]
            self.suffix: str = tempFile.split(".")[-1]
        except Exception as e:
            image_to_add: bool = False

        if image_to_add:
            self.currentImage: str = image_to_add
            self.tempImage: str = os.path.join("temp_images", f"edited.{self.suffix}")

            shutil.copy(self.currentImage, "temp_images")

            try:
                os.rename(os.path.join("temp_images", tempFile), os.path.join("temp_images", f"edited.{self.suffix}"))
            except Exception as e:   
                os.replace(os.path.join("temp_images", tempFile), os.path.join("temp_images", f"edited.{self.suffix}"))

            pixmap: QPixmap = QPixmap(self.tempImage)
            self.imageLabel.setPixmap(pixmap)
        else:
            return

    def blackAndWhite(self) -> None:                    # -- Changes current image to black and white
        if self.blackWhiteActive:
            self.blackWhiteActive = False
            updatedImage = self.currentImage
        else:
            self.blackWhiteActive = True
            updatedImage = Image.open(self.tempImage).convert("L")  
            updatedImage.save(self.tempImage)
            updatedImage = updatedImage.toqpixmap()
        
        self.applyImage(updatedImage)

    def applyImage(self, updatedImage) -> None:                       # -- Applies image to main label
        pixmap = QPixmap(updatedImage)
        self.imageLabel.setPixmap(pixmap)
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow: QWidget = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())