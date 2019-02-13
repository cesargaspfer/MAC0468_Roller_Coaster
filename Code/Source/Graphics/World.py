import numpy as np

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from OpenGL import GL
from Source.Graphics.Scene import Scene
from Source.Graphics.Camera import Camera
from Source.Graphics.Light import Light
from Source.Graphics.Material import Material
from Source.Graphics.Background import Background
from Source.Graphics.Floor import Floor
from Source.Graphics.Grid import Grid
from Source.Graphics.Axis import Axis

##  World scene class
class World(Scene):

    def __init__(self, viewer, **kwargs):
        """Initialize scene object"""

        self._home_position = kwargs.get("home_position", QVector3D(0.0, 0.0, 1.0))

		## define a camera
        self._camera = Camera(name="main", position=self._home_position, lens=Camera.Lens.Perspective)
        self._camera.pointAt(QVector3D(0.0, 0.0, 0.0))

 		## create light source
        light = Light(
        	position=QVector4D(2.0, 2.0, 0.5, 0.0), 
            ambient=QVector3D(0.5, 0.5, 0.5),
            diffuse=QVector3D(1.0, 1.0, 1.0), 
            specular=QVector3D(1.0, 1.0, 1.0), headlight=True)
        
        ## create camera for gnomon scene
        camera = Camera(name="main", position=QVector3D(0.0, 0.0, 4.0), lens=Camera.Lens.Perspective)
        camera.pointAt(QVector3D(0.0, 0.0, 0.0))

        self._background = {
            'top_left': QColor(107, 128, 140),
            'top_center': QColor(107, 128, 140),
            'top_right': QColor(107, 128, 140),
            'mid_left': QColor(149, 164, 164),
            'mid_center': QColor(149, 164, 164),
            'mid_right': QColor(149, 164, 164),
            'bot_left': QColor(191, 199, 199),
            'bot_center': QColor(191, 199, 199),
            'bot_right': QColor(191, 199, 199)
        }

        self._gridProperties = {
            'color': QColor(128, 128, 128), 
            'length_rows': 10.0, 
            'length_cols': 10.0,
            'rows': 24,
            'cols': 24
        }

        self._gridActor = None
        self._axisActor = None
        self._backgroundActor = None

        super(World, self).__init__(viewer, light=light, camera=camera, **kwargs)


    def initialize(self):
        """initialize scene"""
        if self._backgroundActor is not None:
            self.removeSystemActor(self._backgroundActor)
        
        self._backgroundActor = Background(self, name="background", palette=self._background)
        self.addSystemActor(self._backgroundActor)
        self.createGridLines()

        ## recreate actors if any
        for each in self.actors():
            each.initialize()

        
    def background(self):
        """Returns background properties"""
        return self._background


    def setBackground(self, background):
        """Sets background properties"""
        self._background = background


    def updateBackground(self):
        if self._backgroundActor is not None:
            self._backgroundActor.setPalette(self._background)


    def gridProperties(self):
        """Returns grid properties"""
        return self._gridProperties


    def setGridProperties(self, properties):
        """Sets grid properties"""
        self._gridProperties = properties


    def createGridLines(self, properties=None):
        """Create grid"""
        gridVisible = axisVisible = True
        if self._gridActor is not None:
            gridVisible = self._gridActor.isVisible()
            self.removeSystemActor(self._gridActor)
        if self._axisActor is not None:
            axisVisible = self._axisActor.isVisible()
            self.removeSystemActor(self._axisActor)

        self._gridActor = Grid(self, name="floor", 
            length_rows = self._gridProperties['length_rows'], 
            length_cols = self._gridProperties['length_cols'],
            rows = self._gridProperties['rows'],
            cols = self._gridProperties['cols'],
            material = Material(diffuse=QVector3D(self._gridProperties['color'].redF(), self._gridProperties['color'].greenF(), self._gridProperties['color'].blueF())))  
        self._gridActor.setVisible(gridVisible)
        self.addSystemActor(self._gridActor)

        self._axisActor = Axis(self, name="axis", length_row=self._gridProperties['length_rows'], length_col=self._gridProperties['length_cols'])
        self._axisActor.setVisible(axisVisible)
        self.addSystemActor(self._axisActor)


    def enableGridLines(self, state):
        """Turn on or off gridlines"""
        if self._gridActor is not None:
            self._gridActor.setVisible(state)


    def enableAxes(self, state):
        """Turn on or off axes"""
        if self._axisActor is not None:
            self._axisActor.setVisible(state)


    def setCameraLens(self, lens):
        """Switch camera lens"""
        self.camera.setLens(lens, adjust=True)


    def storeCamera(self):
        """Store current camera parameters"""
        self.camera.store()


    def recallCamera(self):
        """Recall camera parameters"""
        self.camera.recall(self.viewer.width() / float(self.viewer.height() if self.viewer.height() > 0.0 else 1.0))


    def resetCamera(self):
        """Reset camera parameters"""
        self.camera.setPosition(self._home_position)
        self.camera.pointAt(QVector3D(0.0, 0.0, 0.0))
        self.camera.setAspectRatio(self.viewer.width() / float(self.viewer.height() if self.viewer.height() > 0.0 else 1.0))
        self.camera.setLens(Camera.Lens.Perspective)

