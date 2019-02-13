import math
import numpy as np

from PyQt5.QtCore import QObject, QTime, QLineF, QPointF
from PyQt5.QtGui import QVector3D, QQuaternion

## The Trackball object
class Trackball(QObject):

    ## Define trackball modes
    class TrackballMode:
        Planar = 0
        Spherical = 1


    ## initialization
    def __init__(self, **kwargs):
        """Initialize trackball"""
        super(Trackball, self).__init__()

        self._rotation = kwargs.get("rotation", QQuaternion())
        self._angularVelocity = kwargs.get("velocity", 0.0)
        self._axis = kwargs.get("axis", QVector3D(0.0, 1.0, 0.0))
        self._mode = kwargs.get("mode", self.TrackballMode.Spherical)

        self._lastPos = QPointF()
        self._lastTime = QTime.currentTime()
        self._paused = kwargs.get("paused", False)
        self._pressed = False

        self._first_person = False


    @property
    def mode(self):
        """Returns trackball mode"""
        return self._mode


    def reset(self, quat=QQuaternion()):
        """Reset trackball"""
        self._rotation = quat
        self._angularVelocity = 0.0
        self._lastPos = QPointF()
        self._lastTime = QTime.currentTime()
        self._pressed = False
        self._paused = False


    def press(self, point, quat=None):
        """Press trackball"""
        self._rotation = self.rotation()
        self._pressed = True
        self._lastTime = QTime.currentTime()
        self._lastPos = point
        self._angularVelocity = 0.0


    def move(self, point, quat):
        """Move trackball"""
        if not self._pressed:
            return

        currentTime = QTime.currentTime()
        msecs = self._lastTime.msecsTo(currentTime)
        if msecs <= 20:
            return

        if self._mode == self.TrackballMode.Planar:

            delta = QLineF(self._lastPos, point)
            self._angularVelocity = 180.0 * delta.length() / (math.pi * msecs)
            self._axis = QVector3D(-delta.dy(), delta.dx(), 0.0).normalized()
            self._axis = quat.rotatedVector(self._axis)
            self._rotation = QQuaternion.fromAxisAndAngle(self._axis, 180.0 / math.pi * delta.length()) * self._rotation

        elif self._mode == self.TrackballMode.Spherical:

            lastPos3D = QVector3D(self._lastPos.x(), self._lastPos.y(), 0.0)
            sqrZ = 1.0 - QVector3D.dotProduct(lastPos3D, lastPos3D)
            if sqrZ > 0:
                lastPos3D.setZ(math.sqrt(sqrZ))
            else:
                lastPos3D.normalize()

            currentPos3D = QVector3D(point.x(), point.y(), 0.0)
            sqrZ = 1.0 - QVector3D.dotProduct(currentPos3D, currentPos3D)
            if sqrZ > 0:
                currentPos3D.setZ(math.sqrt(sqrZ))
            else:
                currentPos3D.normalize()

            self._axis = QVector3D.crossProduct(lastPos3D, currentPos3D)
            angle = 180.0 / math.pi * math.asin(math.sqrt(QVector3D.dotProduct(self._axis, self._axis)))

            self._angularVelocity = angle / msecs
            self._axis.normalize()
            self._axis = quat.rotatedVector(self._axis)
            self._rotation = QQuaternion.fromAxisAndAngle(self._axis, angle) * self._rotation

        self._lastPos = point
        self._lastTime = currentTime


    def release(self, point, quat):
        """Release trackball"""
        self.move(point, quat)
        self._pressed = False


    def start(self):
        """Start trackball"""
        self._lastTime = QTime.currentTime()
        self._paused = False


    def stop(self):
        """Stop trackball"""
        self._rotation = self.rotation()
        self._paused = True


    def rotation(self):
        """Returns rotation quarternion"""
        if self._paused or self._pressed:
            return self._rotation

        currentTime = QTime.currentTime()
        if(self._first_person):
            return self._rotation

        angle = self._angularVelocity * self._lastTime.msecsTo(currentTime)
        return QQuaternion.fromAxisAndAngle(self._axis, angle) * self._rotation
