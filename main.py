#! python3, PyQt6, Pillow
#! main.py - Image Editing program

"""
TODO: Adjust widget placement
"""

import sys, os

from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (QPushButton, QLabel, QApplication, QWidget, QSlider, QVBoxLayout, QHBoxLayout)
from PIL import Image, ImageEnhance, ImageQt,  ImageFilter

class Alter(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.emptyPixmap: QPixmap = QPixmap(os.path.join("icons", "blank.jpg"))

        self.initUI()
        self.initIcons()
        self.initConfigWidgets()
        self.initToolTips()
        self.initConfigConnections()
        self.initStyleSheets()
        self.initLayout()

    def initUI(self) -> None:               # -- Initiates Widgets
        self.mainPicLabel: QWidget = QLabel()                                   # - Main Image Label

        self.editImgBtn: QPushButton = QPushButton()                            # - Home Options
        self.saveImgBtn: QPushButton = QPushButton()
        self.addImgBtn: QPushButton = QPushButton()

        self.rotateRightBtn: QPushButton = QPushButton()                        # - Edit Options
        self.rotateLeftBtn: QPushButton = QPushButton()
        self.backBtn: QPushButton = QPushButton()
        self.brightnessBtn: QPushButton = QPushButton()
        self.cropBtn: QPushButton = QPushButton()
        self.mainFilterBtn: QPushButton = QPushButton()

        self.brightnessBackBtn: QPushButton = QPushButton()                     # - Brightness Options
        self.brightnessSlider: QSlider = QSlider(Qt.Orientation.Horizontal)

        self.blackWhiteBtn: QPushButton = QPushButton()                         # - Main Filter Options
        self.contrastBtn: QPushButton = QPushButton()
        self.filtersBtn: QPushButton = QPushButton()
        self.filterBackBtn: QPushButton = QPushButton()

        self.backToFilterBtn: QPushButton = QPushButton()                       # - Secondary Filter Options
        self.smoothBtn: QPushButton = QPushButton()
        self.embossBtn: QPushButton = QPushButton()
        self.blurBtn: QPushButton = QPushButton()
        self.sharpenBtn: QPushButton = QPushButton()
        self.contourBtn: QPushButton = QPushButton()
        self.detailBtn: QPushButton = QPushButton()

        self.contrastBackBtn: QPushButton = QPushButton()                       # - Contrast Options
        self.contrastSlider: QSlider = QSlider(Qt.Orientation.Horizontal)

        self.homeWidgetList: list = [self.editImgBtn, self.saveImgBtn, self.addImgBtn]
        self.brightnessWidgetList: list = [self.brightnessBackBtn, self.brightnessSlider]
        self.contrastWidgetsList: list = [self.contrastBackBtn, self.contrastSlider]
        self.filterWidgetsList: list = [self.filterBackBtn, self.blackWhiteBtn, self.contrastBtn, self.mainFilterBtn]
        self.moreFiltersWidgetList: list = [
                                            self.backToFilterBtn, self.smoothBtn, self.embossBtn,
                                            self.blurBtn, self.sharpenBtn, self.contourBtn, self.detailBtn
                                            ]
        self.editOptionsWidgetList: list = [
                                            self.rotateLeftBtn, self.rotateRightBtn, self.backBtn,
                                            self.brightnessBtn, self.cropBtn, self.filtersBtn
                                            ]

    def initConfigWidgets(self) -> None:            # -- Configures widgets (size, etc)
        self.setFixedSize(500, 800)
        self.mainPicLabel.setPixmap(self.emptyPixmap)

        self.addImgBtn.setIconSize(QSize(50,50))
        self.embossBtn.setIconSize(QSize(25, 25))

        self.brightnessSlider.setMaximum(10)
        self.contrastSlider.setMaximum(10)

        self.brightnessSlider.setMinimum(0)
        self.contrastSlider.setMinimum(0)

        self.brightnessSlider.setValue(2)
        self.contrastSlider.setValue(2)

        self.brightnessSlider.setTickPosition(QSlider.TickPosition.TicksBothSides)
        self.contrastSlider.setTickPosition(QSlider.TickPosition.TicksBothSides)
        
    def initIcons(self) -> None:                    # -- Applies Icons to Widgets
        self.editImgBtn.setIcon(QIcon(os.path.join('icons', 'edit-icon.png')))
        self.saveImgBtn.setIcon(QIcon(os.path.join('icons', 'save-icon.png')))
        self.addImgBtn.setIcon(QIcon(os.path.join('icons', 'open-img-icon.png')))
        self.rotateLeftBtn.setIcon(QIcon(os.path.join('icons', 'rotate-left.png')))
        self.rotateRightBtn.setIcon(QIcon(os.path.join('icons', 'rotate-right.png')))
        self.backBtn.setIcon(QIcon(os.path.join('icons', 'back-icon.png')))
        self.brightnessBtn.setIcon(QIcon(os.path.join('icons', 'brightness-icon.png')))
        self.cropBtn.setIcon(QIcon(os.path.join('icons', 'crop-icon.png')))
        self.mainFilterBtn.setIcon(QIcon(os.path.join('icons', 'filters-icon.png')))
        self.brightnessBackBtn.setIcon(QIcon(os.path.join('icons', 'back-icon.png')))
        self.blackWhiteBtn.setIcon(QIcon(os.path.join('icons', 'black-white-icon.png')))
        self.contrastBtn.setIcon(QIcon(os.path.join('icons', 'contrast-icon.png')))
        self.filterBackBtn.setIcon(QIcon(os.path.join('icons', 'back-icon.png')))
        self.filtersBtn.setIcon(QIcon(os.path.join('icons', 'filter-icon.png')))
        self.backToFilterBtn.setIcon(QIcon(os.path.join('icons', 'back-icon.png')))
        self.smoothBtn.setIcon(QIcon(os.path.join('icons', 'smooth-filter.png')))
        self.embossBtn.setIcon(QIcon(os.path.join('icons', 'emboss-icon.png')))
        self.blurBtn.setIcon(QIcon(os.path.join('icons', 'blur-icon.png')))
        self.sharpenBtn.setIcon(QIcon(os.path.join('icons', 'sharpen-icon.png')))
        self.contourBtn.setIcon(QIcon(os.path.join('icons', 'contour-icon.png')))
        self.detailBtn.setIcon(QIcon(os.path.join('icons', 'detail-icon.png')))
        self.contrastBackBtn.setIcon(QIcon(os.path.join('icons', 'back-icon.png')))

    def initToolTips(self) -> None:                 # -- initiates tooltips for Widgets
        self.mainPicLabel.setToolTip("Main Image")
        self.editImgBtn.setToolTip("Edit Options")
        self.saveImgBtn.setToolTip("Save Image")
        self.addImgBtn.setToolTip("Add a photo editor")
        self.rotateRightBtn.setToolTip("Rotate Right")
        self.rotateLeftBtn.setToolTip("Rotate Left")
        self.backBtn.setToolTip("Back to Home")
        self.brightnessBtn.setToolTip("Brightness")
        self.cropBtn.setToolTip("Crop")
        self.mainFilterBtn.setToolTip("Filter Options")
        self.brightnessBackBtn.setToolTip("Return to Edit")
        self.brightnessSlider.setToolTip("Brightness")
        self.filterBackBtn.setToolTip("Back to Edit")
        self.blackWhiteBtn.setToolTip("Black/White")
        self.contrastBtn.setToolTip("Contrast")
        self.filtersBtn.setToolTip("More Filters")
        self.backToFilterBtn.setToolTip("Back to Main Filters")
        self.smoothBtn.setToolTip("Smooth")
        self.embossBtn.setToolTip("Emboss")
        self.blurBtn.setToolTip("Blur")
        self.sharpenBtn.setToolTip("Sharpen")
        self.contourBtn.setToolTip("Contour")
        self.detailBtn.setToolTip("Detail")
        self.contrastSlider.setToolTip("Contrast")
        self.contrastBackBtn.setToolTip("Back to Filters")

    def initConfigConnections(self) -> None:        # -- Connects Widgets to functions
        self.editImgBtn.clicked.connect(self.openEditOptions)
        self.backBtn.clicked.connect(self.backToHome)
        self.filtersBtn.clicked.connect(self.openMainFilterOptions)
        self.filterBackBtn.clicked.connect(self.backToEdit)

    def initLayout(self) -> None:                   # -- Applies Widgets to layouts
        self.hideEditOptions()
        self.hideBrightnessOptions()
        self.hideMainFilterOptions()
        self.hideSecondaryFilterOptions()
        self.hideContrastOptions()

        self.mainLayout: QVBoxLayout = QVBoxLayout()
        self.rowTwoLayout: QHBoxLayout = QHBoxLayout()
        self.rowThreeLayout: QHBoxLayout = QHBoxLayout()

        self.rowTwoLayout.addWidget(self.mainPicLabel, Qt.AlignmentFlag.AlignCenter)        # - Home Page
        self.rowThreeLayout.addWidget(self.editImgBtn)
        self.rowThreeLayout.addWidget(self.addImgBtn)
        self.rowThreeLayout.addWidget(self.saveImgBtn)

        self.rowThreeLayout.addWidget(self.backBtn)                                         # - Edit Page
        self.rowThreeLayout.addWidget(self.rotateLeftBtn)
        self.rowThreeLayout.addWidget(self.brightnessBtn)
        self.rowThreeLayout.addWidget(self.cropBtn)
        self.rowThreeLayout.addWidget(self.mainFilterBtn)
        self.rowThreeLayout.addWidget(self.rotateRightBtn)

        self.rowThreeLayout.addWidget(self.filterBackBtn)                                   # - Main Filter Page
        self.rowThreeLayout.addWidget(self.contrastBtn)
        self.rowThreeLayout.addWidget(self.blackWhiteBtn)
        self.rowThreeLayout.addWidget(self.filtersBtn)

        self.rowThreeLayout.addWidget(self.backToFilterBtn)                                 # - Secondary Filter Page
        self.rowThreeLayout.addWidget(self.smoothBtn)
        self.rowThreeLayout.addWidget(self.embossBtn)
        self.rowThreeLayout.addWidget(self.blurBtn)
        self.rowThreeLayout.addWidget(self.sharpenBtn)
        self.rowThreeLayout.addWidget(self.contourBtn)
        self.rowThreeLayout.addWidget(self.detailBtn)

        self.rowThreeLayout.addWidget(self.brightnessBackBtn)                               # - Brightness Page
        self.rowThreeLayout.addWidget(self.brightnessSlider)

        self.rowThreeLayout.addWidget(self.contrastBackBtn)                                 # - Contrast page
        self.rowThreeLayout.addWidget(self.contrastSlider)

        self.mainLayout.addLayout(self.rowTwoLayout)
        self.mainLayout.addLayout(self.rowThreeLayout)
        self.setLayout(self.mainLayout)    

    def initStyleSheets(self) -> None:              # -- Initiates the application
        self.setStyleSheet("""
            QWidget {
                    background : black;
                    padding-top : 20px;
                    }

            QPushButton {
                        color : white;
                        background-color: rgba(0, 0, 0, 0)
                        }

            QLabel {
                    color : white;
                    border : 1px solid grey;
                    padding-left : 13px;
                    padding-right : 13px;
                    padding-top : 13px;
                    padding-bottom : 13px;
                    }
            """)
        
    def hideHomeOptions(self) -> None:              # -- Hides Home Widgets
        for widg in self.homeWidgetList:
            widg.hide()

    def showHomeOptions(self) -> None:              # -- Show Home Widgets
        for widg in self.homeWidgetList:
            widg.show()

    def hideEditOptions(self) -> None:              # -- Hides edit widgets
        for widg in self.editOptionsWidgetList:
            widg.hide()

    def showEditOptions(self) -> None:              # -- Shows edit widgets
        for widg in self.editOptionsWidgetList:
            widg.show()

    def hideBrightnessOptions(self) -> None:        # -- Hides Brightness Widgets
        for widg in self.brightnessWidgetList:
            widg.hide()

    def showBrightnessOptions(self) -> None:        # -- Shows Brightness WIdgets
        for widg in self.brightnessWidgetList:
            widg.show()

    def hideMainFilterOptions(self) -> None:        # -- Hides main filter Widgets
        for widg in self.filterWidgetsList:
            widg.hide()

    def showMainFilterOptions(self) -> None:        # -- Shows main filter Widgets
        for widg in self.filterWidgetsList:
            widg.show()

    def hideSecondaryFilterOptions(self) -> None:   # -- Hides Secondary Filter Widgets
        for widg in self.moreFiltersWidgetList:
            widg.hide()

    def showSecondaryFilterOptions(self) -> None:   # -- Shows secondary filter widgets
        for widg in self.moreFiltersWidgetList:
            widg.show()

    def hideContrastOptions(self) -> None:          # -- Hides Contrast Widgets
        for widg in self.contrastWidgetsList:
            widg.hide()

    def showContrastOptions(self) -> None:          # -- Shows Contrast Widgets
        for widg in self.contrastWidgetsList:
            widg.show()

    def backToHome(self) -> None:                   # -- Returns to main options           
        self.hideEditOptions()
        self.showHomeOptions()

    def backToEdit(self) -> None:
        self.hideMainFilterOptions()
        self.showEditOptions()

    def openEditOptions(self) -> None:              # -- Opens edit options
        self.hideHomeOptions()
        self.showEditOptions()

    def openMainFilterOptions(self) -> None:        # -- Opens Main Filter Options
        self.hideEditOptions()
        self.showMainFilterOptions()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    alter: QWidget = Alter()
    alter.show()
    sys.exit(app.exec())
