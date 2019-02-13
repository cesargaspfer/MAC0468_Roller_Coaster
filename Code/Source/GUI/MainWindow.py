import platform

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from Source.GUI.RenderWidget import RenderWidget

class MainWindow(QMainWindow):

    ## initialization
    def __init__(self, **kwargs):
        super(MainWindow, self).__init__()

        self._format = kwargs.get("format", None)

        self.initialize()

        self._timer = QTimer(self)
        self._timer.timeout.connect(self.handleTimer)
        self._timer.start(1000)

        self.setWindowTitle("Viewer")
        self.setUnifiedTitleAndToolBarOnMac(True)



    def createFileActions(self):
        """Create file menu actions"""
        self._fileNewAction = QAction("&New", self, shortcut=QKeySequence.New,
            statusTip="Create a new protocol", triggered=self.new)

        self._fileOpenAction = QAction("&Open...", self, shortcut=QKeySequence.Open,
            statusTip="Open an existing synaptic protocol file", triggered=self.open)

        self._fileSaveAction = QAction("&Save", self, shortcut=QKeySequence.Save,
            statusTip="Saves synaptic protocol", triggered=self.save)

        self._fileSaveAsAction = QAction("&Save As...", self, shortcut=QKeySequence.SaveAs,
            statusTip="Saves synaptic protocol under a different name", triggered=self.saveAs)

        self._fileExitAction = QAction("E&xit", self, shortcut="Ctrl+Q",
            statusTip="Exit the application", triggered=self.close)


    ## create menus
    def createMenus(self):

        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self._fileNewAction)
        self.fileMenu.addAction(self._fileOpenAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self._fileSaveAction)
        self.fileMenu.addAction(self._fileSaveAsAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self._fileExitAction)


    ## initialize user interface
    def initialize(self):               

        ## create menus
        self.createFileActions()
        self.createMenus()

        fontSize10 = QFont()
        fontSize10.setPointSize(10)

        self.statusBar().setFont(fontSize10)
        self.statusBar().showMessage("Ready")

        self.statistics = QLabel(" ")
        self.statistics.setFont(fontSize10)
        self.statusBar().addPermanentWidget(self.statistics)

        ## create scene 
        self._renderWidget = RenderWidget(self, font=fontSize10)

        ## set the renderer as main widget
        self.setCentralWidget(self._renderWidget)
       

    def new(self):
        """New file"""
        pass


    def open(self):
        """Open file"""
        pass


    def save(self):
        """Save file"""
        pass


    def saveAs(self):
        """Save file as"""
        pass


    def stopTimer(self):
        """Stop second-long timer"""
        self._timer.stop()


    def restartTimer(self):
        """Restart second-long timer"""
        self._timer.start()


    def handleTimer(self):
        times = self._renderWidget.renderTimeEstimates()
        self.statistics.setText("Render time: " + str(round(times[0],2)) + "ms, GPU time: " + str(round(times[1],2)) + "ms")


    def clearStatistics(self):
        self.statistics.setText(" ")


    def closeEvent(self, closeEvent):
        """Intercept close event and perform clean-up"""

        ## then propagae event
        super(MainWindow, self).closeEvent(closeEvent)






