#! python3
#! main.py -- Basic image editor

import os, sys, shutil

from PIL import Image
from PyQt6.QtGui import QIcon, QImage, QPixmap, QAction
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QMainWindow, QHBoxLayout, QGridLayout, QVBoxLayout,
    QFileDialog, QSlider, QMenu
)


class MainWindow(QMainWindow):
    def __init__(self):                                 # -- Initiates the application
        super().__init__()
        self.currentImage: str = ""
        self.tempEditedImage: str = ""
        self.tempUneditedImage: str = ""
        self.imageEdited: bool = False
        self.blackWhiteActive: bool = False
        self.currentMouseX: int = 0
        self.currentMouseY: int = 0

        self.setWindowTitle("Image Editor")
        self.setFixedSize(600, 800)
        self.initWidget()
        self.initLayout()
        self.filterWidgetLayout()
        self.initConfigWidgets()
        self.initConfigConnections()
        self.initStyleSheets()
        self.widgetToolTips()
        self.setCentralWidget(self.mainContainer)
        self.initFilterMenu()

        self.labelWidth: int = self.imageLabel.width()
        self.labelHeight: int = self.imageLabel.height()

    def initWidget(self) -> None:                       # -- Initiates main window widgets
        self.mainContainer: QWidget = QWidget()                             # - QWidgets
        self.colapsedMenu: QWidget = QWidget()
        self.expandedMenu: QWidget = QWidget()
        self.mainApplication: QWidget = QWidget()
        
        # Colapsed Menu Buttons
        self.colapedMenuBtn: QWidget = QPushButton()                        # - QPushButtons
        self.colapsedLoadImageBtn: QWidget = QPushButton()
        
        # Expanded menu Buttons
        self.expandedMenuBtn: QWidget = QPushButton("Colapse")
        self.expandedLoadImageBtn: QWidget = QPushButton("Load Image")
        
        #self.expandedBlackWhiteSlide: QWidget = QSlider(Qt.Orientation.Horizontal)                   # - QSliders

        self.imageLabel: QWidget = QLabel()                                 # - QLabels

    def initLayout(self) -> None:                       # -- Applies widgets to layout/sets main layout
        self.mainContainer.layout = QHBoxLayout()       # - Main Layouts
        self.colapsedMenu.layout = QGridLayout()
        self.expandedMenu.layout = QGridLayout()
        self.mainApplication.layout = QVBoxLayout()

        self.colapsedMenu.layout.addWidget(self.colapedMenuBtn, 0, 0, Qt.AlignmentFlag.AlignLeft)
        self.colapsedMenu.layout.addWidget(self.colapsedLoadImageBtn, 1, 0, Qt.AlignmentFlag.AlignLeft)   

        self.expandedMenu.layout.addWidget(self.expandedMenuBtn, 0, 0, Qt.AlignmentFlag.AlignLeft)
        self.expandedMenu.layout.addWidget(self.expandedLoadImageBtn, 1, 0, Qt.AlignmentFlag.AlignLeft) 

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
        self.colapsedFiltersBtn.setIcon(QIcon(os.path.join("icons", "filters-icon.png")))
        self.expandedMenuBtn.setIcon(QIcon(os.path.join("icons", "expanded-menu.png")))
        self.expandedLoadImageBtn.setIcon(QIcon(os.path.join("icons", "save-icon.png")))
        self.expandedBlackWhiteBtn.setIcon(QIcon(os.path.join("icons", "black-white-icon.png")))
        self.expandedFiltersBtn.setIcon(QIcon(os.path.join("icons", "filters-icon.png")))
        self.expandedSmoothBtn.setIcon(QIcon(os.path.join("icons", "smooth-filter.png")))
        self.expandedSharpenBtn.setIcon(QIcon(os.path.join("icons", "sharpen-icon.png")))
        self.expandedEmbossBtn.setIcon(QIcon(os.path.join("icons", "emboss-icon.png")))

        self.mainApplication.setMaximumHeight(self.height())                                        # - Max Width/Height
        self.colapsedMenu.setMaximumWidth(40)
        self.expandedMenu.setMaximumWidth(150)
        self.expandedMenu.setMinimumWidth(150)

    def initConfigConnections(self) -> None:            # -- Configures connections between buttons and functions
        self.colapedMenuBtn.clicked.connect(self.expandSideMenu)
        self.expandedMenuBtn.clicked.connect(self.colapseSideMenu)
        self.colapsedLoadImageBtn.clicked.connect(self.openImageDialog)
        self.expandedLoadImageBtn.clicked.connect(self.openImageDialog)
        self.expandedBlackWhiteBtn.clicked.connect(self.blackAndWhite)
        self.colapsedFiltersBtn.clicked.connect(lambda: self.openMenu('filter'))

    def initStyleSheets(self) -> None:                  # -- Applies css stylesheets/incode styles to applicaiton
        self.colapsedMenu.setStyleSheet("background-color: darkgrey;")
        self.expandedMenu.setStyleSheet("background-color: darkgrey;")
        self.mainApplication.setStyleSheet("background-color: black; color: white;")
        self.setStyleSheet("background-color: black;")

    def widgetToolTips(self) -> None:                   # -- Sets up widget hover tool tips
        self.colapedMenuBtn.setToolTip("Expand Menu")
        self.expandedMenuBtn.setToolTip("Colapse Menu")
        self.colapsedLoadImageBtn.setToolTip("Load Image")
        self.expandedLoadImageBtn.setToolTip("Load Image")  
        self.colapsedFiltersBtn.setToolTip("Filters")
        self.expandedBlackWhiteBtn.setToolTip("Black/White")
        self.expandedSmoothBtn.setToolTip("Smooth")
        self.expandedSharpenBtn.setToolTip("Sharpen")
        self.expandedEmbossBtn.setToolTip("Emboss")

    def filterWidgetLayout(self) -> None:               # -- Applies Layouts for the filterWidgets
        filtersLayout = QVBoxLayout()
        headerlayout = QHBoxLayout()
        rowOneLayout = QHBoxLayout()
        rowTwoLayout = QHBoxLayout()

        self.colapsedFiltersBtn: QWidget = QPushButton()
        self.expandedFiltersBtn: QWidget = QPushButton("        Filters")
        self.expandedBlackWhiteBtn: QWidget = QPushButton()
        self.expandedSmoothBtn: QWidget = QPushButton() 
        self.expandedSharpenBtn: QWidget = QPushButton()
        self.expandedEmbossBtn: QWidget = QPushButton()

        headerlayout.addWidget(self.expandedFiltersBtn)
        rowOneLayout.addWidget(self.expandedBlackWhiteBtn)
        rowOneLayout.addWidget(self.expandedSmoothBtn)
        rowOneLayout.addWidget(self.expandedSharpenBtn)
        rowOneLayout.addWidget(self.expandedEmbossBtn)

        

        filtersLayout.addLayout(headerlayout)
        filtersLayout.addLayout(rowOneLayout)

        self.colapsedMenu.layout.addWidget(self.colapsedFiltersBtn, 2, 0, Qt.AlignmentFlag.AlignLeft)
        self.expandedMenu.layout.addLayout(filtersLayout, 2, 0, Qt.AlignmentFlag.AlignLeft)

        self.expandedBlackWhiteBtn.setMaximumSize(25,25)
        self.expandedSmoothBtn.setMaximumSize(25,25)

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

            self.applyImage(self.tempImage)
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
            self.imageEdited = True
        
        self.applyImage(updatedImage)

    def applyImage(self, img) -> None:                  # -- Applies image to main label
        pixmap = QPixmap(img)
        scaled = pixmap.scaled(self.labelWidth, self.labelHeight, Qt.AspectRatioMode.KeepAspectRatio)
        self.imageLabel.setPixmap(scaled)
        
    def initFilterMenu(self) -> None:                   # -- Initiates colapsed filter context menu
        self.filterMenu: QWidget = QMenu()
        self.filterMenu.addAction("Black/White")
        self.filterMenu.addAction("two")
        self.filterMenu.addAction("three")
        self.filterMenu.hide()  

    def openMenu(self, type):                           # -- Opens Filter Context Menu
        if type == "filter":
            self.filterMenu.show()
            self.filterMenu.move(700, 691)  

    def mousePressEvent(self, event):
        x = event.position().x()
        y = event.position().y()
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow: QWidget = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())