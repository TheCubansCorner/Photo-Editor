#! python3, PyQt6, Pillow
#! main.py - Image Editing program

"""
TODO: Adjust widget placement
TODO: Fix more filters button placement as shows at beginning of layout instead of the end
"""

import sys, os

from PIL import Image, ImageEnhance, ImageQt,  ImageFilter
from PyQt6.QtGui import QIcon, QPixmap, QImage
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (
                            QPushButton, QLabel, QApplication, QWidget,
                            QSlider, QVBoxLayout, QHBoxLayout, QFileDialog
                            )


class Alter(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.activeImg: Image = None
        self.editedImg: Image = None
        self.activeImageFile: str = os.path.join("icons", "blank.jpg")
        self.qImage: QImage = None
        self.pixmap: QPixmap = None
        self.currentRotation: int = 0
        self.currentContrast: int = 0
        self.currentBrightness: int = 0
        self.blackWhiteOn: bool = False
        self.embossOn: bool = False
        self.smoothOn: bool = False
        self.blurOn: bool = False
        self.sharpenON: bool = False
        self.contourOn: bool = False
        self.detailOn: bool = False

        self.initUI()
        self.initLayout()
        self.initIcons()
        self.initConfigWidgets()
        self.initToolTips()
        self.initConfigConnections()
        self.initStyleSheets()    

    def initUI(self) -> None:               # -- Initiates Widgets
        self.mainPicLabel: QLabel = QLabel()                                   # - Main Image Label

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
        self.showMaximized()
        self.setFixedSize(self.width(), self.height())

        self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mainPicLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.mainPicLabel.setPixmap(QPixmap(self.activeImageFile))

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
        self.mainFilterBtn.clicked.connect(self.openSecondaryFilterOptions)
        self.backToFilterBtn.clicked.connect(self.backToMainFilters)
        self.brightnessBtn.clicked.connect(self.openBrightnessOptions)
        self.brightnessBackBtn.clicked.connect(self.brightBackToEdit)
        self.contrastBtn.clicked.connect(self.openContrastOptions)
        self.contrastBackBtn.clicked.connect(self.contrastBackToEdit)
        self.addImgBtn.clicked.connect(self.openMainImage)
        self.rotateRightBtn.clicked.connect(lambda: self.rotateImage("right"))
        self.rotateLeftBtn.clicked.connect(self.rotateImage)
        self.blackWhiteBtn.clicked.connect(self.blackWhiteMode)
        self.embossBtn.clicked.connect(self.embossMode)
        self.smoothBtn.clicked.connect(self.smoothMode)
        self.blurBtn.clicked.connect(self.blurMode)
        self.sharpenBtn.clicked.connect(self.sharpenMode)
        self.contourBtn.clicked.connect(self.contourMode)
        self.detailBtn.clicked.connect(self.detailMode)
        self.brightnessSlider.valueChanged.connect(self.brightnessMode)
        self.contrastSlider.valueChanged.connect(self.contrastMode)


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

        self.mainLayout.addLayout(self.rowTwoLayout, Qt.AlignmentFlag.AlignCenter)
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

    def backToEdit(self) -> None:                   # -- Returns to Edit Options
        self.hideMainFilterOptions()
        self.showEditOptions()

    def backToMainFilters(self) -> None:            # -- Returns to main filter Options
        self.hideSecondaryFilterOptions()
        self.showMainFilterOptions()

    def brightBackToEdit(self) -> None:             # -- Returns to edit options from Brightness Slider
        self.hideBrightnessOptions()
        self.showEditOptions()

    def contrastBackToEdit(self) -> None:           # -- Returns to edit options from Contrast Slider
        self.hideContrastOptions()
        self.showMainFilterOptions()

    def openEditOptions(self) -> None:              # -- Opens edit options
        self.hideHomeOptions()
        self.showEditOptions()

    def openMainFilterOptions(self) -> None:        # -- Opens Main Filter Options
        self.hideEditOptions()
        self.showMainFilterOptions()

    def openSecondaryFilterOptions(self) -> None:   # -- Opens Secondary FIlter options
        self.hideMainFilterOptions()
        self.showSecondaryFilterOptions()
    
    def openBrightnessOptions(self) -> None:        # -- Opens Brightness slider option
        self.hideEditOptions()
        self.showBrightnessOptions()

    def openContrastOptions(self) -> None:          # -- Opens Contrast slider option
        self.hideMainFilterOptions()
        self.showContrastOptions()

    def openMainImage(self) -> None:                # -- Opens main image to edit
        try:
            imageToAdd = QFileDialog.getOpenFileName(self, "Open File")[0]
        except Exception as e:
            errorMessage: str = e
            imageToAdd: bool = False

        if imageToAdd:
            self.activeImgFile = imageToAdd
            self.activeImg: Image = Image.open(self.activeImgFile)
            self.qImage: QImage = self.activeImg.toqimage()
            self.pixmap = QPixmap.fromImage(self.qImage)
            self.applyImage()
        else:
            self.error: QWidget = QWidget()
            self.errorLabel: QLabel = QLabel("Somthing went wrong")
            okBtn: QPushButton = QPushButton("OK")
            self.error.layout = QVBoxLayout()
            
            okBtn.clicked.connect(self.error.close)
            self.error.layout.addWidget(self.errorLabel)
            self.error.layout.addWidget(okBtn)
            self.error.setLayout(self.error.layout)
            self.error.show()

        self.editedImg = self.activeImg

    def saveMainImage(self) -> None:                # -- Saves edited image
        pass

    def rotateImage(self, direction = None) -> None:             # -- Rotates the current image 90 degrees
        try:
            if self.currentRotation == -360 or self.currentRotation == 360:
                    self.currentRotation = 0
                    
            if direction == "right":
                self.currentRotation += -90
            else:
                self.currentRotation += 90
            
            self.currentImageSettings()
                
        except Exception as e:
            print(e)

    def blackWhiteMode(self) -> None:               # -- Changes image to black and white
        if self.blackWhiteOn:
            self.blackWhiteOn = False
        else:
            self.blackWhiteOn = True
        
        self.currentImageSettings()

    def embossMode(self) -> None:                   # -- Applies Emboss Filter to Image in main Qlabel
        if self.embossOn:
            self.embossOn = False
        else:
            self.embossOn = True

        self.currentImageSettings()

    def smoothMode(self) -> None:                   # -- Applies Smooth FIlter to main Qlabel
        if self.smoothOn:
            self.smoothOn = False
        else:
            self.smoothOn = True

        self.currentImageSettings()
        
    def blurMode(self) -> None:                     # -- Applies Blur filter to main Image Qlabel
        if self.blurOn:
            self.blurOn = False
        else:
            self.blurOn = True
        
        self.currentImageSettings()

    def sharpenMode(self) -> None:                  # -- Applies sharpen filter to main image in QLabel
        if self.sharpenON:
            self.sharpenON = False
        else:
            self.sharpenON = True

        self.currentImageSettings()

    def contourMode(self) -> None:                  # -- Applies Contour Filter to the main image in QLabel
        if self.contourOn:
            self.contourOn = False
        else:
            self.contourOn = True

        self.currentImageSettings()

    def detailMode(self) -> None:                   # -- Apply Detail filter to main Image in Qlabel
        if self.detailOn:
            self.detailOn = False
        else:
            self.detailOn = True

        self.currentImageSettings()

    def brightnessMode(self) -> None:               # -- Increases/decreases brightness on main Image in QLabel
        enhancer = ImageEnhance.Brightness(self.editedImg)
        self.currentBrightness = self.brightnessSlider.value() / 8
        imgOutput = enhancer.enhance(self.currentBrightness)
        self.qImage = imgOutput.toqimage()
        self.pixmap = QPixmap.fromImage(self.qImage)
        self.applyImage()

    def contrastMode(self) -> None:                 # -- Increase/Decrease Contrast on main Image in QLabel
        enhancer = ImageEnhance.Contrast(self.editedImg)
        self.currentContrast = self.contrastSlider.value() - 0.5
        imgOutput = enhancer.enhance(self.currentContrast)
        self.qImage = imgOutput.toqimage()
        self.pixmap = QPixmap.fromImage(self.qImage)
        self.applyImage()

    def applyImage(self) -> None:                   # -- Apply Image to main QLabel
        scaled: QPixmap = self.pixmap.scaled(500, 800, Qt.AspectRatioMode.KeepAspectRatioByExpanding)
        self.mainPicLabel.setPixmap(scaled)

    def currentImageSettings(self) -> None:         # -- Applies active image settings to main Image in QLabel
        self.editedImg: Image = self.activeImg

        if self.blackWhiteOn:
            self.editedImg = self.editedImg.convert('L')

        if self.sharpenON:
            self.editedImg = self.editedImg.filter(ImageFilter.SHARPEN)

        if self.embossOn:
            self.editedImg = self.editedImg.filter(ImageFilter.EMBOSS)

        if self.smoothOn:
            self.editedImg = self.editedImg.filter(ImageFilter.SMOOTH_MORE)

        if self.blurOn:
            self.editedImg = self.editedImg.filter(ImageFilter.BLUR)

        if self.contourOn:
            self.editedImg = self.editedImg.filter(ImageFilter.CONTOUR)

        if self.detailOn:
            self.editedImg = self.editedImg.filter(ImageFilter.DETAIL)

        self.editedImg = self.editedImg.rotate(self.currentRotation)
        self.qImage = self.editedImg.toqimage()
        self.pixmap = QPixmap.fromImage(self.qImage)

        self.applyImage()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    alter: QWidget = Alter()
    alter.show()
    sys.exit(app.exec())
