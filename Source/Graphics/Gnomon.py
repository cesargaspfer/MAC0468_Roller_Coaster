import numpy as np

from PyQt5.QtGui import QVector3D, QVector4D, QMatrix4x4, QQuaternion

from OpenGL import GL
from Source.Graphics.Scene import Scene
from Source.Graphics.Light import Light
from Source.Graphics.Camera import Camera
from Source.Graphics.OrientationMarker import OrientationMarker

##  Gnomon scene class
class Gnomon(Scene):

    def __init__(self, viewer, **kwargs):
        """Initialize scene object"""
        self._maxsize = kwargs.get("maxsize", 70)

 		## create headlight
        light = Light(
            ambient=QVector3D(0.5, 0.5, 0.5),
            diffuse=QVector3D(1.0, 1.0, 1.0),
            specular=QVector3D(1.0, 1.0, 1.0), headlight=True)

        ## create camera for gnomon scene
        camera = Camera(name="gnomon", position=QVector3D(0.0, 0.0, 4.0), lens=Camera.Lens.Perspective)
        camera.pointAt(QVector3D(0.0, 0.0, 0.0))
        camera.scaleHeight(0.6)

        self._marker = None

        super(Gnomon, self).__init__(viewer, light=light, camera=camera, **kwargs)


    def initialize(self):
        ## create orientation marker
        if self._marker is not None:
            self.removeActor(self._marker)
        self._marker = OrientationMarker(self)
        self.addActor(self._marker)


    def setCameraLens(self, lens):
        """Switch camera lens"""
        self.camera.setLens(lens, adjust=True)


    def setViewportRegion(self):
    	## select gnomon viewport region
    	width = self._viewer.devicePixelRatio() * self._viewer.width()
    	height = self._viewer.devicePixelRatio() * self._viewer.height()
    	max_width = self._maxsize * self._viewer.devicePixelRatio()
    	max_height = self._maxsize * self._viewer.devicePixelRatio()

    	GL.glViewport(int(width - max_width), 0, int(max_width), int(max_height))
