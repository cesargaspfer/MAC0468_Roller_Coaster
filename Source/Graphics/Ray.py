import math
import numpy as np

from PyQt5.QtCore import QObject
from PyQt5.QtGui import QVector3D, QVector4D, QMatrix4x4, QQuaternion

##  Base ray class
class Ray(QObject):

    def __init__(self, parent=None, origin=QVector3D(0, 0, 0), direction=QVector3D(0.0, 0.0, -1.0)):
        """Initialize ray object."""
        super(Ray, self).__init__(parent)

        ## register bounds
        self._origin = origin
        self._direction = direction

    def origin(self):
        """Returns the origin of the ray"""
        return self._origin

    def setOrigin(self, origin):
        """Sets new origin"""
        self._origin = origin

    def direction(self):
        """Returns the direction of the ray"""
        return self._direction

    def setDirection(self, direction):
        """Sets the ray direction"""
        self._direction = direction

     
