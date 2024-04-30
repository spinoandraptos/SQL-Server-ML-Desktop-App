'''
Front-end GUI components and their communication with the backend and ML model
'''
# import ml
from PyQt5.QtCore import (
    Qt
)
from PyQt5.QtGui import (
    QPalette,
    QIcon,
    QColor,
    QPixmap
)
from PyQt5.QtWidgets import (
    QApplication, 
    QMainWindow,
    QDesktopWidget,
    QStatusBar,
    QPushButton, 
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QLabel,
    QAction,
    QWidget,
    QFileDialog,
    QLineEdit
)

'''
The widget 
'''
class MlWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('../media/logo.png'))
        self.setWindowTitle('Trane Custom ML Processor')
        self.resize(QDesktopWidget().availableGeometry(self).size() * 0.6);
        
        self.createNavMenu()
        self.createStatusBar()
        self.createCentralWidget()

    def createNavMenu(self):
        menu = self.menuBar()
        mlSettings = menu.addMenu('ML Model Settings')
        sqlSettings = menu.addMenu('SQL Server Settings')
        networkSettings = menu.addMenu('Network Settings')
        genSettings = menu.addMenu('General Settings')
        helpSettings = menu.addMenu('Help')
   
    def createStatusBar(self):
        #Initialise status bar
        self.statusBar = QStatusBar()

        #Create save button for saving changes to any configurations
        self.saveButton = QPushButton('Save')
        self.saveButton.setStyleSheet('padding: 5px;')
        self.saveButton.setToolTip('Save latest configuration')
        self.saveButton.clicked.connect(self.saveChanges)  

        #Create close button for closing the window
        self.closeButton = QPushButton('Close')
        self.closeButton.setToolTip('Close the application')
        self.closeButton.clicked.connect(self.exitApp) 

        #Add copyright message for application
        self.copyright = QLabel('© Man Juncheng, 2024')
        self.copyright.setStyleSheet('margin-left: 10px;')
        #Attach status bar widgets and configure aesthetics
        self.statusBar.addPermanentWidget(self.copyright,86)
        self.statusBar.addPermanentWidget(self.saveButton,7)
        self.statusBar.addPermanentWidget(self.closeButton,7)
        self.statusBar.setStyleSheet('margin-top: 5px;'
                                'margin-bottom: 10px;'
                                'margin-left:5px;'
                                'padding: 5px;') 
        
        #Configure status bar with the above design
        self.setStatusBar(self.statusBar)

    #Action for closing window
    def saveChanges(self):
        self.close()

    #Action for closing window
    def exitApp(self):
        self.close()

    def createCentralWidget(self):
        #Box for choosing the MLflow model to load into the application
        self.modelLoadingBox = QGroupBox("MLflow Model Selection")
        self.modelLoadingBox.setMaximumWidth(QDesktopWidget().availableGeometry(self).size().width()* 0.3)
        self.modelLoadingBox.setMinimumWidth(QDesktopWidget().availableGeometry(self).size().width()* 0.15)
        self.modelLoadingBox.setMinimumHeight(QDesktopWidget().availableGeometry(self).size().height()* 0.18)
        self.modelLoadingBox.setMaximumHeight(QDesktopWidget().availableGeometry(self).size().height()* 0.3)
        self.loadingBoxLayout = QVBoxLayout(self.modelLoadingBox)
        
        #Create section for choosing MLflow model from local directory
        self.modelPathWidget = QWidget(self)
        self.modelPathLayout = QHBoxLayout(self.modelPathWidget)
        #Label for widget
        self.modelPathLabel = QLabel('Model Path')
        #Text display of selected model path
        self.modelPathDisplay = QLineEdit(self)
        self.modelPathDisplay.setText('Enter model directory')
        self.modelPathDisplay.textChanged.connect(self.enterModelPath)
        #Click button for browsing for the right directory
        self.browseButton = QPushButton('Browse')
        self.browseButton.clicked.connect(self.getModelPath)
        #Aligning the widgets 
        self.modelPathLayout.addWidget(self.modelPathLabel)
        self.modelPathLayout.addWidget(self.modelPathDisplay)
        self.modelPathLayout.addWidget(self.browseButton)
        
        #Create section for displaying selected model 
        self.chosenModelWidegt = QWidget(self)
        self.chosenModelLayout = QHBoxLayout(self.chosenModelWidegt)
        self.chosenModelLayout.setAlignment(Qt.AlignTop)
        #Label for widget
        self.modelPathLabel = QLabel('Selected Model')
        #Widget for details of the model
        self.modelDetailsWidget = QWidget(self)
        self.modelDetailsLayout = QVBoxLayout(self.modelDetailsWidget)
        self.modelDetailsLayout.setAlignment(Qt.AlignTop)
        #Placement of MLflow logo
        self.modelTypeLogo = QLabel()
        self.modelTypeLogo.setPixmap(QPixmap('../media/MLflow-logo.png').scaled(150,55))
        self.modelName = QLabel('No model loaded')
        #Align model details widget
        self.modelDetailsLayout.addWidget(self.modelTypeLogo)
        self.modelDetailsLayout.addWidget(self.modelName)
        #Align overarching chosen model widget
        self.chosenModelLayout.addWidget(self.modelPathLabel)
        self.chosenModelLayout.addWidget(self.modelDetailsWidget)

        #Align widgets for entire ML loading box
        self.loadingBoxLayout.addWidget(self.modelPathWidget, 20)
        self.loadingBoxLayout.addWidget(self.chosenModelWidegt, 80)

        #Box for choosing the MLflow model to load into the application
        self.dataConfigBox = QGroupBox("Data Sink and Source Selection")
        self.configBoxLayout = QVBoxLayout(self.dataConfigBox)
        self.dataConfigBox.setMinimumHeight(QDesktopWidget().availableGeometry(self).size().height()* 0.18)
        self.dataConfigBox.setMaximumHeight(QDesktopWidget().availableGeometry(self).size().height()* 0.3)
       
        #Box for choosing the MLflow model to load into the application
        self.modelOutputBox = QGroupBox("Model Data Output")
        self.outputBoxLayout = QVBoxLayout(self.modelOutputBox)

        #Each inner widget has a horizontal layout, top row has 2 columns
        self.topRowWidget = QWidget(self)
        self.topRowWidgetLayout = QHBoxLayout(self.topRowWidget)
        self.topRowWidgetLayout.addWidget(self.modelLoadingBox)
        self.topRowWidgetLayout.addWidget(self.dataConfigBox)
        self.topRowWidgetLayout.setSpacing(20)
        self.topRowWidgetLayout.setAlignment(Qt.AlignTop)
        self.topRowWidget.setStyleSheet('margin-top: 10px;')

        self.bottomRowWidget = QWidget(self)
        self.bottomRowWidgetLayout = QHBoxLayout(self.bottomRowWidget)
        self.bottomRowWidgetLayout.addWidget(self.modelOutputBox)
        self.bottomRowWidgetLayout.setAlignment(Qt.AlignTop)

        #Central widget is a template widget with vertical layout (2 rows)
        self.mainWidget = QWidget(self)
        self.mainWidgetLayout = QVBoxLayout(self.mainWidget)
        self.mainWidgetLayout.addWidget(self.topRowWidget)
        self.mainWidgetLayout.addWidget(self.bottomRowWidget)
        self.mainWidgetLayout.setAlignment(Qt.AlignTop)

        #Apply the widget design to window central widget
        self.setCentralWidget(self.mainWidget)

    def enterModelPath(self):
        self.modelPath = self.modelPathDisplay.text()
    
    def getModelPath(self):
        modelSelector = QFileDialog()
        modelSelector.setFileMode(QFileDialog.AnyFile)
        modelPath = modelSelector.getExistingDirectory(self, 'Select Folder')
        self.modelPathDisplay.setText(modelPath)
        self.modelPathDisplay.setCursorPosition(0)
        self.modelPath = modelPath

    def loadModelInfo(self):
        filePointer = open(f'{self.modelPath}/MLmodel', "r")
        modelInfo = filePointer.read()
        
        self.modelName = 'HAHAHA'

def setDarkTheme(app):
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.WindowText, Qt.white)
    dark_palette.setColor(QPalette.Base, QColor(35, 35, 35))
    dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipBase, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.ToolTipText, Qt.white)
    dark_palette.setColor(QPalette.Text, Qt.white)
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ButtonText, Qt.white)
    dark_palette.setColor(QPalette.BrightText, Qt.red)
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, QColor(35, 35, 35))
    dark_palette.setColor(QPalette.Active, QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.Disabled, QPalette.ButtonText, Qt.darkGray)
    dark_palette.setColor(QPalette.Disabled, QPalette.WindowText, Qt.darkGray)
    dark_palette.setColor(QPalette.Disabled, QPalette.Text, Qt.darkGray)
    dark_palette.setColor(QPalette.Disabled, QPalette.Light, QColor(53, 53, 53))
    app.setPalette(dark_palette)

def setLghtTheme(app):
    light_palette = QPalette()
    light_palette.setColor(QPalette.Window, QColor(255, 254, 250))
    light_palette.setColor(QPalette.WindowText, Qt.black)
    light_palette.setColor(QPalette.Base, Qt.white)
    light_palette.setColor(QPalette.AlternateBase, QColor(255, 254, 250))
    light_palette.setColor(QPalette.ToolTipBase, QColor(255, 244, 219))
    light_palette.setColor(QPalette.ToolTipText, QColor(23, 9, 4))
    light_palette.setColor(QPalette.Text, Qt.black)
    light_palette.setColor(QPalette.Button, QColor(255, 249, 235))
    light_palette.setColor(QPalette.ButtonText, Qt.black)
    light_palette.setColor(QPalette.BrightText, Qt.red)
    light_palette.setColor(QPalette.Link, QColor(255, 244, 219))
    light_palette.setColor(QPalette.Highlight, QColor(255, 244, 219))
    light_palette.setColor(QPalette.HighlightedText, QColor(23, 9, 4))
    light_palette.setColor(QPalette.Active, QPalette.Button, QColor(255, 249, 235))
    light_palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(23, 9, 4))
    light_palette.setColor(QPalette.Disabled, QPalette.WindowText, QColor(23, 9, 4))
    light_palette.setColor(QPalette.Disabled, QPalette.Text, QColor(23, 9, 4))
    light_palette.setColor(QPalette.Disabled, QPalette.Light, QColor(23, 9, 4))
    app.setPalette(light_palette)

app = QApplication([])
app.setStyle('fusion')
setLghtTheme(app)
entryWindow = MlWindow()