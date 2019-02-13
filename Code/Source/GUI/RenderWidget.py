from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from Source.Graphics.Renderer import Renderer

class RenderWidget(QWidget):

    def __init__(self, parent=None, **kwargs):
        super(RenderWidget, self).__init__(parent)

        self._font = kwargs.get("font", QFont())
        self.setFont(self._font)

        ## create render window
        self._parent = parent
        self._renderer = Renderer(self, antialiasing=True, **kwargs)

        self._mainLayout = QVBoxLayout()
        self._mainLayout.setContentsMargins(0, 0, 0, 0)
        self._mainLayout.setSpacing(3)

        ## create viewer
        self._mainLayout.addWidget(self._renderer)

        ## create bottom layout
        self._bottomLayout = QHBoxLayout()
        self._bottomLayout.setContentsMargins(3, 0, 3, 0)
        self._bottomLayout.setSpacing(3)

        ## create view sublayout
        self._viewLayout = QHBoxLayout()
        self._viewLayout.setContentsMargins(0, 0, 0, 0)
        self._viewLayout.setSpacing(3)

        ## register view functions
        self._viewFunc = [
            self._renderer.viewLeft,
            self._renderer.viewRight,
            self._renderer.viewTop,
            self._renderer.viewBottom,
            self._renderer.viewFront,
            self._renderer.viewBack]

        label = QLabel("Axis: ")
        label.setFont(self._font)
        self._viewLayout.addWidget(label)
        self._viewCombo = QComboBox(self)
        self._viewCombo.addItem("+x")
        self._viewCombo.addItem("-x")
        self._viewCombo.addItem("+y")
        self._viewCombo.addItem("-y")
        self._viewCombo.addItem("+z")
        self._viewCombo.addItem("-z")
        self._viewCombo.setFont(self._font)
        self._viewCombo.activated.connect(self.viewDirectionChanged)
        self._viewLayout.addWidget(self._viewCombo)

        self._bottomLayout.addLayout(self._viewLayout)

        ## create camera sublayout
        self._cameraLayout = QHBoxLayout()
        self._cameraLayout.setContentsMargins(0, 0, 5, 0)
        self._cameraLayout.setSpacing(3)

        label = QLabel(" Camera: ")
        label.setFont(self._font)
        self._cameraLayout.addWidget(label)
        self._cameraLensCombo = QComboBox(self)
        self._cameraLensCombo.addItem("Perspective")
        self._cameraLensCombo.addItem("Ortographic")
        self._cameraLensCombo.setFont(self._font)
        self._cameraLensCombo.activated.connect(self._renderer.cameraLensChanged)
        self._cameraLayout.addWidget(self._cameraLensCombo)

        self._cameraCombo = QComboBox(self)
        self._cameraCombo.addItem("Store")
        self._cameraCombo.addItem("Recall")
        self._cameraCombo.addItem("Reset")
        self._cameraCombo.setFont(self._font)
        self._cameraCombo.activated.connect(self.cameraOperationChanged)
        self._cameraLayout.addWidget(self._cameraCombo)

        self._bottomLayout.addLayout(self._cameraLayout)

        self._renderLayout = QHBoxLayout()
        self._renderLayout.setContentsMargins(0, 0, 5, 0)
        self._renderLayout.setSpacing(3)
        label = QLabel(" Style: ")
        label.setFont(self._font)
        self._renderLayout.addWidget(label)
        self._drawStyleCombo = QComboBox(self)
        self._drawStyleCombo.addItem("Points")
        self._drawStyleCombo.addItem("Wireframe")
        self._drawStyleCombo.addItem("Solid")
        self._drawStyleCombo.addItem("Solid with edges")
        self._drawStyleCombo.setFont(self._font)
        self._drawStyleCombo.activated.connect(self._renderer.drawStyleChanged)
        self._drawStyleCombo.setCurrentIndex(2)
        self._renderLayout.addWidget(self._drawStyleCombo)

        label = QLabel(" Quality: ")
        label.setFont(self._font)
        self._renderLayout.addWidget(label)
        self._shadingCombo = QComboBox(self)
        self._shadingCombo.addItem("Low")
        self._shadingCombo.addItem("High")
        self._shadingCombo.setFont(self._font)
        self._shadingCombo.activated.connect(self._renderer.shadingChanged)
        self._shadingCombo.setCurrentIndex(1)
        self._renderLayout.addWidget(self._shadingCombo)

        self._bottomLayout.addLayout(self._renderLayout)

        menu = QMenu()
        menu.setFont(self._font)
        lightingAction = QAction("Lighting", self)
        lightingAction.setCheckable(True)
        lightingAction.setChecked(True)
        lightingAction.triggered.connect(self._renderer.lightingChanged)
        menu.addAction(lightingAction)

        profilingAction = QAction("Profiling", self)
        profilingAction.setCheckable(True)
        profilingAction.setChecked(True)
        profilingAction.triggered.connect(self.profilingChanged)
        menu.addAction(profilingAction)

        menu.addSeparator()
        animateAction = QAction("Animate", self)
        animateAction.setCheckable(True)
        animateAction.setChecked(False)
        animateAction.triggered.connect(self.animateChanged)
        menu.addAction(animateAction)

        self._options = QPushButton()
        self._options.setText("Options")
        self._options.setFont(self._font)
        self._options.setMenu(menu)
        self._renderLayout.addWidget(self._options)

        self._bottomLayout.addStretch(1)

        self._mainLayout.addLayout(self._bottomLayout)

        self._rotacoesOptions = QHBoxLayout()
        self._rotacoesOptions.setContentsMargins(1, 0, 1, 0)
        self._rotacoesOptions.setSpacing(3)
        label = QLabel(" Length:    ")
        label.setFont(self._font)
        self._rotacoesOptions.addWidget(label)
        self.sl4 = QSlider(Qt.Horizontal)
        self.sl4.setMinimum(1)
        self.sl4.setMaximum(20)
        self.sl4.setValue(4)
        self.sl4.setTickPosition(QSlider.TicksBelow)
        self.sl4.setTickInterval(1)
        self.sl4.valueChanged.connect(self.length_changed)
        self._rotacoesOptions.addWidget(self.sl4)

        label = QLabel(" Elevation:  ")
        label.setFont(self._font)
        self._rotacoesOptions.addWidget(label)
        self.sl = QSlider(Qt.Horizontal)
        self.sl.setMinimum(-90)
        self.sl.setMaximum(90)
        self.sl.setValue(0)
        self.sl.setTickPosition(QSlider.TicksBelow)
        self.sl.setTickInterval(15)
        self.sl.valueChanged.connect(self.elevation_changed)
        self._rotacoesOptions.addWidget(self.sl)

        self._mainLayout.addLayout(self._rotacoesOptions)

        self._rotacoesOptions2 = QHBoxLayout()
        self._rotacoesOptions2.setContentsMargins(1, 0, 1, 0)
        self._rotacoesOptions2.setSpacing(3)

        label = QLabel(" Rotation:  ")
        label.setFont(self._font)
        self._rotacoesOptions2.addWidget(label)
        self.sl2 = QSlider(Qt.Horizontal)
        self.sl2.setMinimum(-90)
        self.sl2.setMaximum(90)
        self.sl2.setValue(0)
        self.sl2.setTickPosition(QSlider.TicksBelow)
        self.sl2.setTickInterval(15)
        self.sl2.valueChanged.connect(self.rotation_changed)
        self._rotacoesOptions2.addWidget(self.sl2)


        label = QLabel(" Inclination: ")
        label.setFont(self._font)
        self._rotacoesOptions2.addWidget(label)
        self.sl3 = QSlider(Qt.Horizontal)
        self.sl3.setMinimum(-90)
        self.sl3.setMaximum(90)
        self.sl3.setValue(0)
        self.sl3.setTickPosition(QSlider.TicksBelow)
        self.sl3.setTickInterval(15)
        self.sl3.valueChanged.connect(self.inclination_changed)
        self._rotacoesOptions2.addWidget(self.sl3)

        self._mainLayout.addLayout(self._rotacoesOptions2)


        self._trilhosOptions = QHBoxLayout()
        self._trilhosOptions.setContentsMargins(1, 0, 1, 0)
        self._trilhosOptions.setSpacing(3)

        label = QLabel(" Type: ")
        self._trilhosOptions.addWidget(label)
        self._tiposCombo = QComboBox(self)
        self._tiposCombo.addItem("Platform")
        self._tiposCombo.addItem("Normal")
        self._tiposCombo.addItem("Lever")
        self._tiposCombo.addItem("Brakes")
        self._tiposCombo.addItem("Final")
        self._tiposCombo.activated.connect(self.type_changed)
        self._tiposCombo.setCurrentIndex(0)
        self._trilhosOptions.addWidget(self._tiposCombo)

        self.b1 = QPushButton("Construct")
        self.b1.setCheckable(True)
        self.b1.toggle()
        self.b1.clicked.connect(self.construct)
        self._trilhosOptions.addWidget(self.b1)

        self.b2 = QPushButton("Remove")
        self.b2.setCheckable(True)
        self.b2.toggle()
        self.b2.clicked.connect(self.remove)
        self._trilhosOptions.addWidget(self.b2)

        self.b3 = QPushButton("Simulate")
        self.b3.setCheckable(True)
        self.b3.toggle()
        self.b3.clicked.connect(self.simulate)
        self._trilhosOptions.addWidget(self.b3)

        self.b4 = QPushButton("Stop")
        self.b4.setCheckable(True)
        self.b4.toggle()
        self.b4.clicked.connect(self.stop)
        self._trilhosOptions.addWidget(self.b4)

        self.b5 = QPushButton("Change Camera")
        self.b5.setCheckable(True)
        self.b5.toggle()
        self.b5.clicked.connect(self.camera_changed)
        self._trilhosOptions.addWidget(self.b5)

        self._mainLayout.addLayout(self._trilhosOptions)

        self.setLayout(self._mainLayout)


    def clear(self):
        """Clear viewer"""
        self._renderer.clear()


    def updateViewer(self):
        """Refresh viewer"""
        self._renderer.update()


    def viewDirectionChanged(self, index):
        """Called upon a change in view direction"""
        self._viewFunc[index]()


    def cameraOperationChanged(self, index):
        """Called upon a chnage in camera operation"""
        if index == 0:
            self.storeViewerCamera()
        elif index == 1:
            self.recallViewerCamera()
        else:
            self.resetViewerCamera()


    def storeViewerCamera(self):
        """Ask the the viewer to store active camera parameters"""
        self._renderer.storeCamera()


    def recallViewerCamera(self):
        """Ask the viewer to recall previously stored camera parameters"""
        self._renderer.recallCamera()
        self._cameraLensCombo.setCurrentIndex(self._renderer.activeSceneCamera().lens)


    def resetViewerCamera(self):
        """Ask viewer to reset the active camera parameters"""
        self._renderer.resetCamera()
        self._cameraLensCombo.setCurrentIndex(self._renderer.activeSceneCamera().lens)


    def profilingChanged(self, state):
        """Turn on or off rendering profiling"""
        if state:
            self._renderer.enableProfiling(True)
            self._parent.restartTimer()
        else:
            self._renderer.enableProfiling(False)
            self._parent.stopTimer()
            self._parent.clearStatistics()


    def animateChanged(self, state):
        """Turn on or off animation"""
        self._renderer.enableAnimation(state)


    def renderTimeEstimates(self):
        """Ask viewer for current render time estimates"""
        return self._renderer.renderTimeEstimates()


    def sizeHint(self):
        return QSize(1280, 800)


    def elevation_changed(self):
        ele = self.sl.value()
        self._renderer.elevation_changed(ele)
    def rotation_changed(self):
        rot = self.sl2.value()
        self._renderer.rotation_changed(-rot)
    def inclination_changed(self):
        inc = self.sl3.value()
        self._renderer.inclination_changed(inc)
    def length_changed(self):
        len = self.sl4.value()
        self._renderer.length_changed(len)
    def type_changed(self, type):
        self._renderer.type_changed(type)
    def construct(self):
        self._renderer.construct()
    def remove(self):
        self._renderer.remove()
    def simulate(self):
        self._renderer.simulate()
    def stop(self):
        self._renderer.stop()
    def camera_changed(self):
        self._renderer.camera_changed()
