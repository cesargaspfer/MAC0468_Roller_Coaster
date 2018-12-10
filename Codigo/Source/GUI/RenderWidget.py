import math
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from Source.Graphics.Renderer import Renderer
from Source.Graphics.Material import Material
from Source.Graphics.Textures import Textures
import os

class RenderWidget(QWidget):

    basepath = os.getcwd() + "/"

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
        self._shadingCombo.activated.connect(self.qualityChanged)
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

        '''
        label = QLabel("Object: ")
        label.setFont(self._font)
        self._renderLayout.addWidget(label)
        self._shadingCombo = QComboBox(self)
        self._shadingCombo.addItem("Toro")
        self._shadingCombo.addItem("Oceano")
        self._shadingCombo.addItem("Teapot")
        self._shadingCombo.addItem("Cubo")
        self._shadingCombo.addItem("Esfera")
        self._shadingCombo.addItem("Cone")
        self._shadingCombo.addItem("Cilindro")
        self._shadingCombo.setFont(self._font)
        self._shadingCombo.activated.connect(self._renderer.objectChanged)
        self._shadingCombo.setCurrentIndex(0)
        self._renderLayout.addWidget(self._shadingCombo)
        '''
        self._bottomLayout.addStretch(1)
        self._mainLayout.addLayout(self._bottomLayout)

        ## create second bottom layout
        self._renderOptionsLayout = QHBoxLayout()
        self._renderOptionsLayout.setContentsMargins(3, 0, 3, 0)
        self._renderOptionsLayout.setSpacing(3)
        '''
        label = QLabel("Specular: ")
        label.setFont(self._font)
        self._renderOptionsLayout.addWidget(label)
        label = QLabel("Use Texture")
        label.setFont(self._font)
        self._renderOptionsLayout.addWidget(label)
        self.specularCheckBox = QCheckBox()
        self.specularCheckBox.stateChanged.connect(self.specularcheckchange)
        self.specularCheckBox.setChecked(False)
        self._renderOptionsLayout.addWidget(self.specularCheckBox)
        self.specularTextures = QComboBox(self)
        self.specularTextures.addItem("< Select File >")
        self.specularTextures.setFont(self._font)
        self.specularTextures.activated.connect(self.specularTexturesChange)
        self.specularTextures.setCurrentIndex(0)
        self._renderOptionsLayout.addWidget(self.specularTextures)
        self.specularTextures.setVisible(False)
        self.specularBox = QDoubleSpinBox()
        self.specularBox.setRange(0,1)
        self.specularBox.setSingleStep(0.01)
        self.specularBox.setValue(Material.std_specular_color[0])
        self.specularBox.valueChanged.connect(self._renderer.specularChange)
        self._renderOptionsLayout.addWidget(self.specularBox)
        label = QLabel("Roughness: ")
        label.setFont(self._font)
        self._renderOptionsLayout.addWidget(label)
        label = QLabel("Use Texture")
        label.setFont(self._font)
        self._renderOptionsLayout.addWidget(label)
        self.roughCheckBox = QCheckBox()
        self.roughCheckBox.stateChanged.connect(self.roughcheckchange)
        self.roughCheckBox.setChecked(False)
        self._renderOptionsLayout.addWidget(self.roughCheckBox)
        self.roughnessTextures = QComboBox(self)
        self.roughnessTextures.addItem("< Select File >")
        self.roughnessTextures.setFont(self._font)
        self.roughnessTextures.activated.connect(self.roughnessTexturesChange)
        self.roughnessTextures.setCurrentIndex(0)
        self._renderOptionsLayout.addWidget(self.roughnessTextures)
        self.roughnessTextures.setVisible(False)
        self.roughnessBox = QDoubleSpinBox()
        self.roughnessBox.setRange(0,1)
        self.roughnessBox.setSingleStep(0.01)
        self.roughnessBox.setValue(Material.std_roughness)
        self.roughnessBox.valueChanged.connect(self._renderer.roughnessChange)
        self._renderOptionsLayout.addWidget(self.roughnessBox)
        label = QLabel("Metallic: ")
        label.setFont(self._font)
        self._renderOptionsLayout.addWidget(label)
        label = QLabel("Use Texture")
        label.setFont(self._font)
        self._renderOptionsLayout.addWidget(label)
        self.metalCheckBox = QCheckBox()
        self.metalCheckBox.stateChanged.connect(self.metalcheckchange)
        self.metalCheckBox.setChecked(False)
        self._renderOptionsLayout.addWidget(self.metalCheckBox)
        self.metalnessTextures = QComboBox(self)
        self.metalnessTextures.addItem("< Select File >")
        self.metalnessTextures.setFont(self._font)
        self.metalnessTextures.activated.connect(self.metalnessTexturesChange)
        self.metalnessTextures.setCurrentIndex(0)
        self._renderOptionsLayout.addWidget(self.metalnessTextures)
        self.metalnessTextures.setVisible(False)
        self.metallicBox = QDoubleSpinBox()
        self.metallicBox.setRange(0,1)
        self.metallicBox.setSingleStep(0.01)
        self.metallicBox.setValue(Material.std_metallic)
        self.metallicBox.valueChanged.connect(self._renderer.metallicChange)
        self._renderOptionsLayout.addWidget(self.metallicBox)

        label = QLabel("Base Color: ")
        label.setFont(self._font)
        self._renderOptionsLayout.addWidget(label)
        label = QLabel("Use Texture")
        label.setFont(self._font)
        self._renderOptionsLayout.addWidget(label)
        self.baseColorTexturecheckbox = QCheckBox()
        self.baseColorTexturecheckbox.stateChanged.connect(self.baseColorcheckchange)
        self.baseColorTexturecheckbox.setChecked(False)
        self._renderOptionsLayout.addWidget(self.baseColorTexturecheckbox)
        self.baseColorTextures = QComboBox(self)
        self.baseColorTextures.addItem("< Select File >")
        self.baseColorTextures.setFont(self._font)
        self.baseColorTextures.activated.connect(self.baseColorTexturesChange)
        self.baseColorTextures.setCurrentIndex(0)
        self._renderOptionsLayout.addWidget(self.baseColorTextures)
        self.baseColorTextures.setVisible(False)
        self.baseRBox = QDoubleSpinBox()
        self.baseRBox.setRange(0,1)
        self.baseRBox.setSingleStep(0.01)
        self.baseRBox.setValue(Material.std_cbase.x())
        self.baseRBox.setObjectName('R')
        self.baseRBox.valueChanged.connect(self._renderer.baseColorChange)
        self._renderOptionsLayout.addWidget(self.baseRBox)
        self.baseGBox = QDoubleSpinBox()
        self.baseGBox.setRange(0,1)
        self.baseGBox.setSingleStep(0.01)
        self.baseGBox.setValue(Material.std_cbase.y())
        self.baseGBox.setObjectName('G')
        self.baseGBox.valueChanged.connect(self._renderer.baseColorChange)
        self._renderOptionsLayout.addWidget(self.baseGBox)
        self.baseBBox = QDoubleSpinBox()
        self.baseBBox.setRange(0,1)
        self.baseBBox.setSingleStep(0.01)
        self.baseBBox.setValue(Material.std_cbase.z())
        self.baseBBox.setObjectName('B')
        self.baseBBox.valueChanged.connect(self._renderer.baseColorChange)
        self._renderOptionsLayout.addWidget(self.baseBBox)

        label = QLabel("Normal Map: ")
        label.setFont(self._font)
        self._renderOptionsLayout.addWidget(label)
        self.normalsTextures = QComboBox(self)
        self.normalsTextures.addItem("~ None ~")
        self.normalsTextures.addItem("< Select File >")
        self.normalsTextures.setFont(self._font)
        self.normalsTextures.activated.connect(self.normalsTexturesChange)
        self.normalsTextures.setCurrentIndex(0)
        self._renderOptionsLayout.addWidget(self.normalsTextures)
        '''
        self._renderOptionsLayout.addStretch(1)
        self._mainLayout.addLayout(self._renderOptionsLayout)

        self.createLightOptionsMenu(1)
        self.lightOptionsWidgets = self.createPointLightMenu()
        self._lightOptions.addStretch(1)

        self._rotacoesOptions = QHBoxLayout()
        self._rotacoesOptions.setContentsMargins(1, 0, 1, 0)
        self._rotacoesOptions.setSpacing(3)
        label = QLabel(" Comprimento: ")
        label.setFont(self._font)
        self._rotacoesOptions.addWidget(label)
        self.sl4 = QSlider(Qt.Horizontal)
        self.sl4.setMinimum(1)
        self.sl4.setMaximum(20)
        self.sl4.setValue(4)
        self.sl4.setTickPosition(QSlider.TicksBelow)
        self.sl4.setTickInterval(1)
        self.sl4.valueChanged.connect(self.mudouTamanho)
        self._rotacoesOptions.addWidget(self.sl4)

        label = QLabel(" Elevação:   ")
        label.setFont(self._font)
        self._rotacoesOptions.addWidget(label)
        self.sl = QSlider(Qt.Horizontal)
        self.sl.setMinimum(-90)
        self.sl.setMaximum(90)
        self.sl.setValue(0)
        self.sl.setTickPosition(QSlider.TicksBelow)
        self.sl.setTickInterval(15)
        self.sl.valueChanged.connect(self.mudouElevacao)
        self._rotacoesOptions.addWidget(self.sl)

        self._mainLayout.addLayout(self._rotacoesOptions)

        self._rotacoesOptions2 = QHBoxLayout()
        self._rotacoesOptions2.setContentsMargins(1, 0, 1, 0)
        self._rotacoesOptions2.setSpacing(3)

        label = QLabel(" Rotação:     ")
        label.setFont(self._font)
        self._rotacoesOptions2.addWidget(label)
        self.sl2 = QSlider(Qt.Horizontal)
        self.sl2.setMinimum(-90)
        self.sl2.setMaximum(90)
        self.sl2.setValue(0)
        self.sl2.setTickPosition(QSlider.TicksBelow)
        self.sl2.setTickInterval(15)
        self.sl2.valueChanged.connect(self.mudouRotacao)
        self._rotacoesOptions2.addWidget(self.sl2)


        label = QLabel(" Inclinação: ")
        label.setFont(self._font)
        self._rotacoesOptions2.addWidget(label)
        self.sl3 = QSlider(Qt.Horizontal)
        self.sl3.setMinimum(-90)
        self.sl3.setMaximum(90)
        self.sl3.setValue(0)
        self.sl3.setTickPosition(QSlider.TicksBelow)
        self.sl3.setTickInterval(15)
        self.sl3.valueChanged.connect(self.mudouInclinacao)
        self._rotacoesOptions2.addWidget(self.sl3)

        self._mainLayout.addLayout(self._rotacoesOptions2)


        self._trilhosOptions = QHBoxLayout()
        self._trilhosOptions.setContentsMargins(1, 0, 1, 0)
        self._trilhosOptions.setSpacing(3)

        label = QLabel(" Tipo: ")
        self._trilhosOptions.addWidget(label)
        self._tiposCombo = QComboBox(self)
        self._tiposCombo.addItem("Plataforma")
        self._tiposCombo.addItem("Normal")
        self._tiposCombo.addItem("Alavanca")
        self._tiposCombo.addItem("Freio")
        self._tiposCombo.addItem("Final")
        self._tiposCombo.activated.connect(self._renderer.mudouTipo)
        self._tiposCombo.setCurrentIndex(0)
        self._trilhosOptions.addWidget(self._tiposCombo)

        self.b1 = QPushButton("Adicionar")
        self.b1.setCheckable(True)
        self.b1.toggle()
        self.b1.clicked.connect(self.addTrilho)
        self._trilhosOptions.addWidget(self.b1)

        self.b2 = QPushButton("Remover")
        self.b2.setCheckable(True)
        self.b2.toggle()
        self.b2.clicked.connect(self.rmTrilho)
        self._trilhosOptions.addWidget(self.b2)

        self.b3 = QPushButton("Simular")
        self.b3.setCheckable(True)
        self.b3.toggle()
        self.b3.clicked.connect(self.simular)
        self._trilhosOptions.addWidget(self.b3)

        self.b4 = QPushButton("Parar")
        self.b4.setCheckable(True)
        self.b4.toggle()
        self.b4.clicked.connect(self.parar)
        self._trilhosOptions.addWidget(self.b4)

        self.b5 = QPushButton("Mudar Camera")
        self.b5.setCheckable(True)
        self.b5.toggle()
        self.b5.clicked.connect(self.mudarCamera)
        self._trilhosOptions.addWidget(self.b5)

        self._mainLayout.addLayout(self._trilhosOptions)
        '''
        self._spikeOptions = QHBoxLayout()
        self._spikeOptions.setContentsMargins(1, 0, 1, 0)
        self._spikeOptions.setSpacing(3)


        label = QLabel("Spike Shader: ")
        label.setFont(self._font)
        self._spikeOptions.addWidget(label)

        label = QLabel("Use Spike Shader")
        label.setFont(self._font)
        self._spikeOptions.addWidget(label)
        self.spikeCheckBox = QCheckBox()
        self.spikeCheckBox.stateChanged.connect(self.spikecheckchange)
        self.spikeCheckBox.stateChanged.connect(self._renderer.spikeChange)

        self.spikeBox_h = QDoubleSpinBox()
        self.spikeBox_h.setRange(0,10)
        self.spikeBox_h.setSingleStep(0.01)
        self.spikeBox_h.setValue(Material.std_spike_h)
        self.spikeBox_h.valueChanged.connect(self._renderer.spike_hChange)

        self.spikeBox_r = QDoubleSpinBox()
        self.spikeBox_r.setRange(0,10)
        self.spikeBox_r.setSingleStep(0.01)
        self.spikeBox_r.setValue(Material.std_spike_w)
        self.spikeBox_r.valueChanged.connect(self._renderer.spike_wChange)
        self.spikeCheckBox.setChecked(False)
        self._spikeOptions.addWidget(self.spikeCheckBox)
        label = QLabel("h:")
        label.setFont(self._font)
        self._spikeOptions.addWidget(label)
        self._spikeOptions.addWidget(self.spikeBox_h)
        label = QLabel("w:")
        label.setFont(self._font)
        self._spikeOptions.addWidget(label)
        self._spikeOptions.addWidget(self.spikeBox_r)
        self._spikeOptions.addStretch(1)

        self._mainLayout.addLayout(self._spikeOptions)
        '''


        self.setLayout(self._mainLayout)
        '''
        self.initalizeTextures()
        '''
    def mudouElevacao(self):
        rotacao = self.sl.value()
        self._renderer.mudouElevacao(rotacao)

    def mudouRotacao(self):
        rotacao = self.sl2.value()
        self._renderer.mudouRotacao(rotacao)

    def mudouInclinacao(self):
        rotacao = self.sl3.value()
        self._renderer.mudouInclinacao(rotacao)

    def mudouTamanho(self):
        rotacao = self.sl4.value()
        self._renderer.mudouTamanho(rotacao)

    def addTrilho(self):
        self._renderer.addTrilho()

    def rmTrilho(self):
        self._renderer.rmTrilho()


    def simular(self):
        self._renderer.simular()

    def parar(self):
        self._renderer.parar()

    def mudarCamera(self):
        self._renderer.mudarCamera()


    '''
    def initalizeTextures(self):
            base = RenderWidget.basepath + "/sample-textures/"
            bpath = base + "sample-basecolor.png"
            mpath = base + "sample-metalness.png"
            spath = base + "sample-specular.png"
            rpath = base + "sample-roughness.png"
            npath = base + "sample-normals.png"
            if os.path.isfile(bpath):
                self.baseColorTextures.insertItem(0, Textures.preloadTexture(bpath, "baseColor"))
                self.baseColorTextures.setCurrentIndex(0)
                self.baseRBox.setVisible(False)
                self.baseGBox.setVisible(False)
                self.baseBBox.setVisible(False)
                self.baseColorTextures.setVisible(True)
                self.baseColorTexturecheckbox.setChecked(True)
            if os.path.isfile(mpath):
                self.metalnessTextures.insertItem(0, Textures.preloadTexture(mpath, "metalness"))
                self.metalnessTextures.setCurrentIndex(0)
                self.metallicBox.setVisible(True)
                self.metalnessTextures.setVisible(False)
                self.metalCheckBox.setChecked(True)
            if os.path.isfile(spath):
                self.specularTextures.insertItem(0, Textures.preloadTexture(spath, "specular"))
                self.specularTextures.setCurrentIndex(0)
                self.specularBox.setVisible(True)
                self.specularTextures.setVisible(False)
                self.specularCheckBox.setChecked(True)
            if os.path.isfile(rpath):
                self.roughnessTextures.insertItem(0, Textures.preloadTexture(rpath, "roughness"))
                self.roughnessTextures.setCurrentIndex(0)
                self.roughnessBox.setVisible(True)
                self.roughnessTextures.setVisible(False)
                self.roughCheckBox.setChecked(True)
            if os.path.isfile(npath):
                self.normalsTextures.insertItem(0, Textures.preloadTexture(npath, "normals"))
                self.normalsTextures.setCurrentIndex(0)



    def loadNewTexture(self, group):
            opts = QFileDialog.Options()
            opts |= QFileDialog.DontUseNativeDialog
            fileName = QFileDialog.getOpenFileName(self, "Open " + group + " Image", RenderWidget.basepath, "Image Files (*.png)", options=opts)[0]
            if fileName == "":
                return False
            txt = Textures.addTexture(fileName, group)
            Textures.useTexture(group, txt)
            if group == "baseColor": self.baseColorTextures.insertItem(0, txt);   self.baseColorTextures.setCurrentIndex(0)
            elif group == "metalness": self.metalnessTextures.insertItem(0, txt);   self.metalnessTextures.setCurrentIndex(0)
            elif group == "specular": self.specularTextures.insertItem(0, txt);   self.specularTextures.setCurrentIndex(0)
            elif group == "roughness": self.roughnessTextures.insertItem(0, txt);   self.roughnessTextures.setCurrentIndex(0)
            elif group == "normals": self.normalsTextures.insertItem(0, txt);   self.normalsTextures.setCurrentIndex(0)
            else: return False
            return True

    def normalsTexturesChange(self, index):
        value = str(self.sender().currentText())
        if value == "< Select File >":
            self.loadNewTexture("normals")
        elif value == "~ None ~":
            Textures.stopUsingTexture("normals")
        else:
            Textures.useTexture("normals", value)

    def baseColorcheckchange(self, state):
        if state:
            self.baseRBox.setVisible(False)
            self.baseGBox.setVisible(False)
            self.baseBBox.setVisible(False)
            self.baseColorTextures.setVisible(True)
            if len(Textures.txtrs["baseColor"]) == 0:
                if not self.loadNewTexture("baseColor"):
                    self.sender().setChecked(False)
                    self.baseColorcheckchange(False)
            else:
                Textures.useTexture("baseColor", str(self.baseColorTextures.currentText()))
        else:
            self.baseRBox.setVisible(True)
            self.baseGBox.setVisible(True)
            self.baseBBox.setVisible(True)
            self.baseColorTextures.setVisible(False)
            Textures.stopUsingTexture("baseColor")

    def baseColorTexturesChange(self, index):
        value = str(self.sender().currentText())
        if value == "< Select File >":
            self.loadNewTexture("baseColor")
        else:
            Textures.useTexture("baseColor", value)

    def roughcheckchange(self, state):
        if state:
            self.roughnessBox.setVisible(False)
            self.roughnessTextures.setVisible(True)
            if len(Textures.txtrs["roughness"]) == 0:
                if not self.loadNewTexture("roughness"):
                    self.sender().setChecked(False)
                    self.roughcheckchange(False)
            else:
                Textures.useTexture("roughness", str(self.roughnessTextures.currentText()))
        else:
            self.roughnessBox.setVisible(True)
            self.roughnessTextures.setVisible(False)
            Textures.stopUsingTexture("roughness")

    def roughnessTexturesChange(self, index):
        value = str(self.sender().currentText())
        if value == "< Select File >":
            self.loadNewTexture("roughness")
        else:
            Textures.useTexture("roughness", value)

    def metalcheckchange(self, state):
        if state:
            self.metallicBox.setVisible(False)
            self.metalnessTextures.setVisible(True)
            if len(Textures.txtrs["metalness"]) == 0:
                if not self.loadNewTexture("metalness"):
                    self.sender().setChecked(False)
                    self.metalcheckchange(False)
            else:
                Textures.useTexture("metalness", str(self.metalnessTextures.currentText()))
        else:
            self.metallicBox.setVisible(True)
            self.metalnessTextures.setVisible(False)
            Textures.stopUsingTexture("metalness")

    def metalnessTexturesChange(self, index):
        value = str(self.sender().currentText())
        if value == "< Select File >":
            self.loadNewTexture("metalness")
        else:
            Textures.useTexture("metalness", value)

    def specularcheckchange(self, state):
        if state:
            self.specularBox.setVisible(False)
            self.specularTextures.setVisible(True)
            if len(Textures.txtrs["specular"]) == 0:
                if not self.loadNewTexture("specular"):
                    self.sender().setChecked(False)
                    self.baseColorcheckchange(False)
            else:
                Textures.useTexture("specular", str(self.specularTextures.currentText()))
        else:
            self.specularBox.setVisible(True)
            self.specularTextures.setVisible(False)
            Textures.stopUsingTexture("specular")
    '''
    def spikecheckchange(self, state):
        '''
        if state:
            self.spikeBox_h.setVisible(True)
            self.spikeBox_r.setVisible(True)
        else:
            self.spikeBox_h.setVisible(False)
            self.spikeBox_r.setVisible(False)
        '''

    def specularTexturesChange(self, index):
        value = str(self.sender().currentText())
        if value == "< Select File >":
            self.loadNewTexture("specular")
        else:
            Textures.useTexture("specular", value)

    def qualityChanged(self, index):
        if index == 0:
            self.normalsTextures.setCurrentIndex(self.normalsTextures.findText("~ None ~"))
            self.normalsTextures.setEnabled(False)
            Textures.stopUsingTexture("normals")
        else:
            self.normalsTextures.setEnabled(True)
        self._renderer.shadingChanged(index)

    def lightChanged(self, index):
        self._renderer.lightChanged(index)
        self.roughnessBox.setValue(self._renderer.cur_obj._active_material._roughness)
        self.specularBox.setValue(self._renderer.cur_obj._active_material._specularColor[0])
        self.metallicBox.setValue(self._renderer.cur_obj._active_material._metallic)
        self.baseRBox.setValue(self._renderer.cur_obj._active_material._cbase.x())
        self.baseGBox.setValue(self._renderer.cur_obj._active_material._cbase.y())
        self.baseBBox.setValue(self._renderer.cur_obj._active_material._cbase.z())

        for w in self.lightOptionsWidgets:
            self._lightOptions.removeWidget(w)
            w.deleteLater()

        spacing = self._lightOptions.itemAt(self._lightOptions.count() - 1)
        self._lightOptions.removeItem(spacing)

        if index == 0:
            self.lightOptionsWidgets = self.createHemisfericalLightMenu()
            self._renderer._world.light._headlight = True
        elif index == 1: self.lightOptionsWidgets = self.createPointLightMenu()
        elif index == 2: self.lightOptionsWidgets = self.createDirectionalLightMenu()
        self._lightOptions.addStretch(1)

    def createLightOptionsMenu(self, index):
        self._lightOptions = QHBoxLayout()
        self._lightOptions.setContentsMargins(3, 0, 3, 0)
        self._lightOptions.setSpacing(3)

        label = QLabel("Light: ")
        label.setFont(self._font)
        self._lightOptions.addWidget(label)
        self._lightCombo = QComboBox(self)
        self._lightCombo.addItem("Hemisferical")
        self._lightCombo.addItem("Point")
        self._lightCombo.addItem("Directional")
        self._lightCombo.setFont(self._font)
        self._lightCombo.activated.connect(self.lightChanged)
        self._lightCombo.setCurrentIndex(index)
        self._lightOptions.addWidget(self._lightCombo)
        self._mainLayout.addLayout(self._lightOptions)

    def createDirectionalLightMenu(self):
        ws = []
        label = QLabel("Headlight: ")
        label.setFont(self._font)
        self._lightOptions.addWidget(label)
        ws.append(label)
        self.headLightBox = QCheckBox()
        self.headLightBox.stateChanged.connect(self._renderer.headLightChanged)
        self.headLightBox.setChecked(self._renderer._world.light._headlight)
        self._lightOptions.addWidget(self.headLightBox)
        ws.append(self.headLightBox)
        label = QLabel("Light Color: ")
        label.setFont(self._font)
        self._lightOptions.addWidget(label)
        ws.append(label)
        box = QDoubleSpinBox()
        box.setRange(0,1)
        box.setSingleStep(0.01)
        box.setValue(self._renderer._world._light._color.x())
        box.setObjectName('R')
        box.valueChanged.connect(self._renderer.lightColorChange)
        self._lightOptions.addWidget(box)
        ws.append(box)
        box = QDoubleSpinBox()
        box.setRange(0,1)
        box.setSingleStep(0.01)
        box.setValue(self._renderer._world._light._color.y())
        box.setObjectName('G')
        box.valueChanged.connect(self._renderer.lightColorChange)
        self._lightOptions.addWidget(box)
        ws.append(box)
        box = QDoubleSpinBox()
        box.setRange(0,1)
        box.setSingleStep(0.01)
        box.setValue(self._renderer._world._light._color.z())
        box.setObjectName('B')
        box.valueChanged.connect(self._renderer.lightColorChange)
        self._lightOptions.addWidget(box)
        ws.append(box)

        label = QLabel("Light Direction: ")
        label.setFont(self._font)
        self._lightOptions.addWidget(label)
        ws.append(label)
        box = QDoubleSpinBox()
        box.setRange(-200, 200)
        box.setSingleStep(0.2)
        box.setValue(self._renderer._world._light._position.x())
        box.setObjectName('X')
        box.valueChanged.connect(self._renderer.lightPosChange)
        self._lightOptions.addWidget(box)
        ws.append(box)
        box = QDoubleSpinBox()
        box.setRange(-200, 200)
        box.setSingleStep(0.2)
        box.setValue(self._renderer._world._light._position.y())
        box.setObjectName('Y')
        box.valueChanged.connect(self._renderer.lightPosChange)
        self._lightOptions.addWidget(box)
        ws.append(box)
        box = QDoubleSpinBox()
        box.setRange(-200, 200)
        box.setSingleStep(0.2)
        box.setValue(self._renderer._world._light._position.z())
        box.setObjectName('Z')
        box.valueChanged.connect(self._renderer.lightPosChange)
        self._lightOptions.addWidget(box)
        ws.append(box)
        return ws

    def createPointLightMenu(self):
        ws = []
        label = QLabel("Headlight: ")
        label.setFont(self._font)
        self._lightOptions.addWidget(label)
        ws.append(label)
        self.headLightBox = QCheckBox()
        self.headLightBox.stateChanged.connect(self._renderer.headLightChanged)
        self.headLightBox.setChecked(self._renderer._world.light._headlight)
        self._lightOptions.addWidget(self.headLightBox)
        ws.append(self.headLightBox)
        label = QLabel("Light Color: ")
        label.setFont(self._font)
        self._lightOptions.addWidget(label)
        ws.append(label)
        box = QDoubleSpinBox()
        box.setRange(0,1)
        box.setSingleStep(0.01)
        box.setValue(self._renderer._world._light._color.x())
        box.setObjectName('R')
        box.valueChanged.connect(self._renderer.lightColorChange)
        self._lightOptions.addWidget(box)
        ws.append(box)
        box = QDoubleSpinBox()
        box.setRange(0,1)
        box.setSingleStep(0.01)
        box.setValue(self._renderer._world._light._color.y())
        box.setObjectName('G')
        box.valueChanged.connect(self._renderer.lightColorChange)
        self._lightOptions.addWidget(box)
        ws.append(box)
        box = QDoubleSpinBox()
        box.setRange(0,1)
        box.setSingleStep(0.01)
        box.setValue(self._renderer._world._light._color.z())
        box.setObjectName('B')
        box.valueChanged.connect(self._renderer.lightColorChange)
        self._lightOptions.addWidget(box)
        ws.append(box)

        label = QLabel("Light Position: ")
        label.setFont(self._font)
        self._lightOptions.addWidget(label)
        ws.append(label)
        box = QDoubleSpinBox()
        box.setRange(-200, 200)
        box.setSingleStep(0.2)
        box.setValue(self._renderer._world._light._position.x())
        box.setObjectName('X')
        box.valueChanged.connect(self._renderer.lightPosChange)
        self._lightOptions.addWidget(box)
        ws.append(box)
        box = QDoubleSpinBox()
        box.setRange(-200, 200)
        box.setSingleStep(0.2)
        box.setValue(self._renderer._world._light._position.y())
        box.setObjectName('Y')
        box.valueChanged.connect(self._renderer.lightPosChange)
        self._lightOptions.addWidget(box)
        ws.append(box)
        box = QDoubleSpinBox()
        box.setRange(-200, 200)
        box.setSingleStep(0.2)
        box.setValue(self._renderer._world._light._position.z())
        box.setObjectName('Z')
        box.valueChanged.connect(self._renderer.lightPosChange)
        self._lightOptions.addWidget(box)
        ws.append(box)

        label = QLabel("lradius: ")
        label.setFont(self._font)
        ws.append(label)
        self._lightOptions.addWidget(label)
        box = QDoubleSpinBox()
        box.setRange(0,200)
        box.setSingleStep(0.5)
        box.setValue(self._renderer._world._light._lradious)
        box.valueChanged.connect(self._renderer.lradiusChange)
        self._lightOptions.addWidget(box)
        ws.append(box)
        label = QLabel("aconst: ")
        label.setFont(self._font)
        ws.append(label)
        self._lightOptions.addWidget(label)
        box = QDoubleSpinBox()
        box.setRange(0,1)
        box.setSingleStep(0.01)
        box.setValue(self._renderer._world._light._aconst)
        box.valueChanged.connect(self._renderer.aconstChange)
        self._lightOptions.addWidget(box)
        ws.append(box)
        label = QLabel("alinear: ")
        label.setFont(self._font)
        ws.append(label)
        self._lightOptions.addWidget(label)
        box = QDoubleSpinBox()
        box.setRange(0,1)
        box.setSingleStep(0.01)
        box.setValue(self._renderer._world._light._alinear)
        box.valueChanged.connect(self._renderer.alinearChange)
        self._lightOptions.addWidget(box)
        ws.append(box)
        label = QLabel("aquad: ")
        label.setFont(self._font)
        ws.append(label)
        self._lightOptions.addWidget(label)
        box = QDoubleSpinBox()
        box.setRange(0,1)
        box.setSingleStep(0.01)
        box.setValue(self._renderer._world._light._aquad)
        box.valueChanged.connect(self._renderer.aquadChange)
        self._lightOptions.addWidget(box)
        ws.append(box)
        return ws

    def createHemisfericalLightMenu(self):
        ws = []
        label = QLabel("Sky Color: ")
        label.setFont(self._font)
        ws.append(label)
        self._lightOptions.addWidget(label)
        box = QDoubleSpinBox()
        box.setRange(0,1)
        box.setSingleStep(0.01)
        box.setValue(self._renderer._world._light._csky.x())
        box.setObjectName('R')
        box.valueChanged.connect(self._renderer.skyColorChange)
        self._lightOptions.addWidget(box)
        ws.append(box)
        box = QDoubleSpinBox()
        box.setRange(0,1)
        box.setSingleStep(0.01)
        box.setValue(self._renderer._world._light._csky.y())
        box.setObjectName('G')
        box.valueChanged.connect(self._renderer.skyColorChange)
        self._lightOptions.addWidget(box)
        ws.append(box)
        box = QDoubleSpinBox()
        box.setRange(0,1)
        box.setSingleStep(0.01)
        box.setValue(self._renderer._world._light._csky.z())
        box.setObjectName('B')
        box.valueChanged.connect(self._renderer.skyColorChange)
        self._lightOptions.addWidget(box)
        ws.append(box)
        label = QLabel("Ground Color: ")
        label.setFont(self._font)
        ws.append(label)
        self._lightOptions.addWidget(label)
        box = QDoubleSpinBox()
        box.setRange(0,1)
        box.setSingleStep(0.01)
        box.setValue(self._renderer._world._light._cground.x())
        box.setObjectName('R')
        box.valueChanged.connect(self._renderer.groundColorChange)
        self._lightOptions.addWidget(box)
        ws.append(box)
        box = QDoubleSpinBox()
        box.setRange(0,1)
        box.setSingleStep(0.01)
        box.setValue(self._renderer._world._light._cground.y())
        box.setObjectName('G')
        box.valueChanged.connect(self._renderer.groundColorChange)
        self._lightOptions.addWidget(box)
        ws.append(box)
        box = QDoubleSpinBox()
        box.setRange(0,1)
        box.setSingleStep(0.01)
        box.setValue(self._renderer._world._light._cground.z())
        box.setObjectName('B')
        box.valueChanged.connect(self._renderer.groundColorChange)
        self._lightOptions.addWidget(box)
        ws.append(box)
        return ws


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
