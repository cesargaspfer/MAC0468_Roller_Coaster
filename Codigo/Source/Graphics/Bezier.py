import math
import ctypes
import numpy as np

from PyQt5.QtCore import QObject
from PyQt5.QtGui import QMatrix4x4, QVector3D, QVector4D, QOpenGLShader, QOpenGLShaderProgram, QOpenGLBuffer, QOpenGLVertexArrayObject
from PyQt5.QtWidgets import QOpenGLWidget

from OpenGL import GL

class Bezier(QObject):
    ## initialization
    def __init__(self,  **kwargs):
        """Initialize actor."""
        super(Bezier, self).__init__()

        self._points = []

    def create(self, points):
        pontos = []
        for i in range(0, 4):
            pontos.append(points[i])
        self._points = pontos

    def point(self, t):
        t = float(t)
        return [self.pointComp(t, 0), self.pointComp(t, 1), self.pointComp(t, 2)]

    def Atualizar(self, pontos):
        self._points = pontos

    def pointComp(self, t, i):
        return self._points[3][i]*t**3 + 3.0*self._points[2][i]*t**2*(1.0-t) + 3.0*self._points[1][i]*t*(1.0-t)**2 + self._points[0][i]*(1.0-t)**3

    def tangent(self, t):
        t = float(t)
        tangente = [self.tangentComp(t, 0), self.tangentComp(t, 1), self.tangentComp(t, 2)]
        if(np.linalg.norm(tangente) != 0.0):
            return (tangente/np.linalg.norm(tangente))
        else:
            return(tangente)

    def tangentComp(self, t, i):
        return 3.0*(1.0-t)**2*(self._points[1][i]-self._points[0][i]) + 6.0*(self._points[2][i]-self._points[1][i])*t*(1.0-t) + 3.0*(self._points[3][i]-self._points[2][i])*t**2
    def change(self, i, point):
        self._points[i] = point
