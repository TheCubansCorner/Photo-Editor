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
        self.initConfigWidgets()
        self.initConfigConnections()
        self.initStyleSheets()
        self.widgetToolTips()
        self.initFilterMenu()
        self.setCentralWidget(self.mainContainer)

        self.labelWidth: int = self.imageLabel.width()
        self.labelHeight: int = self.imageLabel.height()

    def initWidget(self) -> None:                       # -- Initiates main window widgets
        self.mainContainer: QWidget = QWidget()                                                       # - QWidgets
        self.colapsedMenu: QWidget = QWidget()
        self.expandedMenu: QWidget = QWidget()
        self.mainApplication: QWidget = QWidget()
        
        # Colapsed Menu Buttons
        self.colapsedMenuBtn: QWidget = QPushButton()                                                 # - QPushButtons Colapseed
        self.colapsedLoadImageBtn: QWidget = QPushButton()
        self.colapsedBrightnessBtn: QWidget = QPushButton()
        self.colapsedContrastBtn: QWidget = QPushButton()
        self.colapsedFiltersBtn: QWidget = QPushButton()  
        self.colapsedRotationBtn: QWidget = QPushButton()
        self.colapsedSaveBtn: QWidget = QPushButton()
        
        # Expanded menu Buttons
        self.expandedMenuBtn: QWidget = QPushButton("Colapse")                                        # - QPushButton Expanded
        self.expandedLoadImageBtn: QWidget = QPushButton("Load Image")
        self.expandedFiltersBtn: QWidget = QPushButton("        Filters")
        self.expandedBlackWhiteBtn: QWidget = QPushButton()
        self.expandedSmoothBtn: QWidget = QPushButton() 
        self.expandedSharpenBtn: QWidget = QPushButton()
        self.expandedEmbossBtn: QWidget = QPushButton()
        self.expandedRotateRightBtn: QWidget = QPushButton()
        self.expandedRotateLeftBtn: QWidget = QPushButton()
        self.expandedSaveBtn: QWidget = QPushButton("Save Image")
        self.expandedEdgeBtn: QWidget = QPushButton()
        self.expandedBlurBtn: QWidget = QPushButton()
        self.expandedDetailBtn: QWidget = QPushButton()
        self.expandedContourBtn: QWidget = QPushButton()
        
        self.expandedBrightnessSlide: QWidget = QSlider(Qt.Orientation.Horizontal)                   # - QSliders
        self.expandedContrastSlide: QWidget = QSlider(Qt.Orientation.Horizontal)

        self.imageLabel: QWidget = QLabel()                                                           # - QLabels
        self.expandedBrightnessLabel: QWidget = QLabel("Brightness")
        self.expandedContrastLabel: QWidget = QLabel("Contrast")

    def initLayout(self) -> None:                       # -- Applies widgets to layout/sets main layout
        self.mainContainer.layout = QHBoxLayout()       # - Main Layouts
        self.colapsedMenu.layout = QGridLayout()
        self.expandedMenu.layout = QGridLayout()
        self.mainApplication.layout = QVBoxLayout()

        filtersLayout = QVBoxLayout()                   # - Filter Layouts
        headerlayout = QHBoxLayout()
        rowOneLayout = QHBoxLayout()
        rowTwoLayout = QHBoxLayout()

        brightnessLayout = QHBoxLayout()
        contrastLayout = QHBoxLayout()
        rotationLayout = QHBoxLayout()

        headerlayout.addWidget(self.expandedFiltersBtn)                                                         # - FIlter Menu
        rowOneLayout.addWidget(self.expandedBlackWhiteBtn)
        rowOneLayout.addWidget(self.expandedSmoothBtn)
        rowOneLayout.addWidget(self.expandedSharpenBtn)
        rowOneLayout.addWidget(self.expandedEmbossBtn)
        rowTwoLayout.addWidget(self.expandedEdgeBtn)
        rowTwoLayout.addWidget(self.expandedBlurBtn)
        rowTwoLayout.addWidget(self.expandedDetailBtn)
        rowTwoLayout.addWidget(self.expandedContourBtn)
        filtersLayout.addLayout(headerlayout)
        filtersLayout.addLayout(rowOneLayout)
        filtersLayout.addLayout(rowTwoLayout)

        brightnessLayout.addWidget(self.expandedBrightnessLabel)                                                # - Brightness Menu
        brightnessLayout.addWidget(self.expandedBrightnessSlide)

        contrastLayout.addWidget(self.expandedContrastLabel)                                                    # - Contrast Menu
        contrastLayout.addWidget(self.expandedContrastSlide)

        rotationLayout.addWidget(self.expandedRotateLeftBtn)                                                    # - Rotation Menu
        rotationLayout.addWidget(self.expandedRotateRightBtn)

        self.colapsedMenu.layout.addWidget(self.colapsedMenuBtn, 0, 0, Qt.AlignmentFlag.AlignLeft)              # - Colapsed Tool Menu
        self.colapsedMenu.layout.addWidget(self.colapsedLoadImageBtn, 1, 0, Qt.AlignmentFlag.AlignLeft)
        self.colapsedMenu.layout.addWidget(self.colapsedSaveBtn, 2, 0, Qt.AlignmentFlag.AlignLeft)
        self.colapsedMenu.layout.addWidget(self.colapsedFiltersBtn, 3, 0, Qt.AlignmentFlag.AlignLeft)  
        self.colapsedMenu.layout.addWidget(self.colapsedBrightnessBtn, 4, 0, Qt.AlignmentFlag.AlignLeft)
        self.colapsedMenu.layout.addWidget(self.colapsedContrastBtn, 5, 0, Qt.AlignmentFlag.AlignLeading)
        self.colapsedMenu.layout.addWidget(self.colapsedRotationBtn, 6, 0, Qt.AlignmentFlag.AlignLeft)

        self.expandedMenu.layout.addWidget(self.expandedMenuBtn, 0, 0, Qt.AlignmentFlag.AlignLeft)              # - Expanded Tool Menu
        self.expandedMenu.layout.addWidget(self.expandedLoadImageBtn, 1, 0, Qt.AlignmentFlag.AlignLeft) 
        self.expandedMenu.layout.addWidget(self.expandedSaveBtn, 2, 0, Qt.AlignmentFlag.AlignLeft)
        self.expandedMenu.layout.addLayout(filtersLayout, 3, 0, Qt.AlignmentFlag.AlignLeft)
        self.expandedMenu.layout.addLayout(brightnessLayout, 4, 0, Qt.AlignmentFlag.AlignLeft)
        self.expandedMenu.layout.addLayout(contrastLayout, 5, 0, Qt.AlignmentFlag.AlignLeft)
        self.expandedMenu.layout.addLayout(rotationLayout, 6, 0, Qt.AlignmentFlag.AlignLeft)

        self.mainApplication.layout.addWidget(self.imageLabel, Qt.AlignmentFlag.AlignCenter)                    # - Main Layout

        self.colapsedMenu.setLayout(self.colapsedMenu.layout)
        self.expandedMenu.setLayout(self.expandedMenu.layout)
        self.mainApplication.setLayout(self.mainApplication.layout)

        self.mainContainer.layout.addWidget(self.colapsedMenu)
        self.mainContainer.layout.addWidget(self.expandedMenu)
        self.mainContainer.layout.addWidget(self.mainApplication)
        
        self.mainContainer.setLayout(self.mainContainer.layout) 

    def initConfigWidgets(self) -> None:                # -- Configured widgets (size, width, etc)
        self.expandedMenu.hide()

        self.imageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)                                   # - Alignments

        pixmap = QPixmap(os.path.join("icons", "blank.jpg"))                                         # - Setting Initial Pixmap
        self.imageLabel.setPixmap(pixmap)

        self.colapsedMenuBtn.setIcon(QIcon(os.path.join("icons", "colapsed-menu.png")))              # - Setting Icons
        self.colapsedLoadImageBtn.setIcon(QIcon(os.path.join("icons", "open-img-icon.png")))
        self.colapsedFiltersBtn.setIcon(QIcon(os.path.join("icons", "filters-icon.png")))     
        self.colapsedBrightnessBtn.setIcon(QIcon(os.path.join("icons", "brightness-icon.png")))
        self.colapsedContrastBtn.setIcon(QIcon(os.path.join("icons", "contrast-icon.png")))
        self.colapsedRotationBtn.setIcon(QIcon(os.path.join("icons", "rotate-right.png")))
        self.colapsedSaveBtn.setIcon(QIcon(os.path.join("icons", "save-icon.png")))
        
        self.expandedMenuBtn.setIcon(QIcon(os.path.join("icons", "expanded-menu.png")))
        self.expandedLoadImageBtn.setIcon(QIcon(os.path.join("icons", "open-img-icon.png")))
        self.expandedBlackWhiteBtn.setIcon(QIcon(os.path.join("icons", "black-white-icon.png")))
        self.expandedFiltersBtn.setIcon(QIcon(os.path.join("icons", "filters-icon.png")))
        self.expandedSmoothBtn.setIcon(QIcon(os.path.join("icons", "smooth-filter.png")))
        self.expandedSharpenBtn.setIcon(QIcon(os.path.join("icons", "sharpen-icon.png")))
        self.expandedEmbossBtn.setIcon(QIcon(os.path.join("icons", "emboss-icon.png")))
        self.expandedSaveBtn.setIcon(QIcon(os.path.join("icons", "save-icon.png")))
        self.expandedRotateRightBtn.setIcon(QIcon(os.path.join("icons", "rotate-right.png")))
        self.expandedRotateLeftBtn.setIcon(QIcon(os.path.join("icons", "rotate-left.png")))
        self.expandedEdgeBtn.setIcon(QIcon(os.path.join("icons", "edge-icon.png")))
        self.expandedBlurBtn.setIcon(QIcon(os.path.join("icons", "blur-icon.png")))
        self.expandedDetailBtn.setIcon(QIcon(os.path.join("icons", "detail-icon.png")))
        self.expandedContourBtn.setIcon(QIcon(os.path.join("icons", "contour-icon.png")))


        self.mainContainer.layout.setContentsMargins(0, 0, 0, 0)                                    # - Content Margins
        self.colapsedMenuBtn.setContentsMargins(0,0,0,0)
        self.colapsedFiltersBtn.setContentsMargins(0,0,0,0)
        self.colapsedBrightnessBtn.setContentsMargins(0,0,0,0)
        self.colapsedMenu.setContentsMargins(0, 0, 0, 0)

        self.mainApplication.setMaximumHeight(self.height())                                        # - Max Size
        self.colapsedMenu.setMaximumWidth(40)
        self.expandedMenu.setMaximumWidth(150)
        self.expandedMenu.setMinimumWidth(150)
        self.expandedBlackWhiteBtn.setMaximumSize(25,25)                                        
        self.expandedSmoothBtn.setMaximumSize(25,25)
        self.expandedBlurBtn.setMaximumSize(25,25)
        self.expandedDetailBtn.setMaximumSize(25,25)
        self.expandedEdgeBtn.setMaximumSize(25,25)

    def initConfigConnections(self) -> None:            # -- Configures connections between buttons and functions
        self.colapsedMenuBtn.clicked.connect(self.expandSideMenu)
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
        self.colapsedMenuBtn.setToolTip("Expand Menu")
        self.colapsedBrightnessBtn.setToolTip("Brightness")
        self.colapsedContrastBtn.setToolTip("Contrast")
        self.colapsedLoadImageBtn.setToolTip("Load Image")
        self.colapsedFiltersBtn.setToolTip("Filters")
        self.colapsedRotationBtn.setToolTip("Rotation")
        self.colapsedSaveBtn.setToolTip("Save Image")

        self.expandedMenuBtn.setToolTip("Colapse Menu")
        self.expandedLoadImageBtn.setToolTip("Load Image") 
        self.expandedBlackWhiteBtn.setToolTip("Black/White")
        self.expandedSmoothBtn.setToolTip("Smooth")
        self.expandedSharpenBtn.setToolTip("Sharpen")
        self.expandedEmbossBtn.setToolTip("Emboss")    
        self.expandedRotateLeftBtn.setToolTip("Rotate Left")
        self.expandedRotateRightBtn.setToolTip("Rotate Right") 
        self.expandedSaveBtn.setToolTip("Save Image")
        self.expandedFiltersBtn.setToolTip("Filters")
        self.expandedBrightnessLabel.setToolTip("Brightness")
        self.expandedContrastLabel.setToolTip("Contrast")
        self.expandedEdgeBtn.setToolTip("Edge Enhance")
        self.expandedBlurBtn.setToolTip("Blur")
        self.expandedDetailBtn.setToolTip("Detail Image")
        self.expandedContourBtn.setToolTip("Contour")

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
            xy = self.colapsedFiltersBtn.mapToGlobal(self.colapsedFiltersBtn.pos())
            self.filterMenu.move(xy)

    def mousePressEvent(self, event):
        x = event.position().x()
        y = event.position().y()
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow: QWidget = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())