import math
import ctypes
import numpy as np

from PyQt5.QtCore import QObject
from PyQt5.QtGui import QMatrix4x4, QVector3D, QVector4D, QOpenGLShader, QOpenGLShaderProgram, QOpenGLBuffer, QOpenGLVertexArrayObject
from PyQt5.QtWidgets import QOpenGLWidget

from OpenGL import GL

class PortalSystem(QObject):
    ## initialization
    def __init__(self, renderer,  **kwargs):
        """Initialize actor."""
        super(PortalSystem, self).__init__(renderer, **kwargs)

        self._portals = []
        self._actors = []
        self.controle = 0


    def addToSystem(self, actor):
        actor._portalInteration = True;
        #self._portal1 = self._portals[0]._vertices; #vertices
        #self._portal2 = self._portals[1]._vertices; #vertices
        self._actors.append(actor)

    def addStatic(self, actor):
        actor._portalInteration = True;
        #self._portal1 = self._portals[0]._vertices; #vertices
        #self._portal2 = self._portals[1]._vertices; #vertices

    def addPortal(self, portal):
        portal._portalInteration = False;
        self._portals.append(portal)

    def makeGraph(self, vertices):
        return

    def detectColisions(self):
        crosses = []
        verticesTrasf = []
        for i in range(len(self._portals)):
            j = 0
            crossesAux = []
            verticesTrasfAux = []
            length = int(len(self._portals[i]._vertices))
            while j < length:
                verticesTrasfAux.append(self.times(self._portals[i]._transform, self._portals[i]._vertices[j]))
                verticesTrasfAux.append(self.times(self._portals[i]._transform, self._portals[i]._vertices[j+1]))
                verticesTrasfAux.append(self.times(self._portals[i]._transform, self._portals[i]._vertices[j+2]))

                v1 = verticesTrasfAux[j] - verticesTrasfAux[j+1]
                v2 = verticesTrasfAux[j+1] - verticesTrasfAux[j+2]
                cross = np.cross(v1, v2)
                crossesAux.append(cross)
                j += 3

            crosses.append(crossesAux)
            verticesTrasf.append(verticesTrasfAux)
        for i in range(len(self._actors)):
            for j in range(len(self._actors[i]._colors)):
                self._actors[i]._colors[j] = 0.0
            j = 0
            length = int(len(self._actors[i]._vertices))
            t = []
            while j < length:
                v = []
                v.append(self.times(self._actors[i]._transform, self._actors[i]._vertices[j]))
                v.append(self.times(self._actors[i]._transform, self._actors[i]._vertices[j+1]))
                v.append(self.times(self._actors[i]._transform, self._actors[i]._vertices[j+2]))
                indice = 0
                for n in range(len(self._portals)):
                    for m in range(int(len(self._portals[n]._vertices)/3.0)):
                        for k in range(0,3):
                            tupla = self.intersection(verticesTrasf[n], m*3, crosses[n][m], v[k], v[(k+1)%3])
                            if tupla[0] != 0:
                                t.append([tupla[0], j+k, n, tupla[1]])
                        indice += 1
                j+=3
            if(len(t)>0):
                self.divideGeometry(self._actors[i], t)
                self._actors[i]._portalInteration = True
            else:
                self._actors[i]._portalInteration = False
            self._actors[i].updateBuffer(colors=self._actors[i]._colors)

    def intersection(self, portal_vertices, indice, cross, v1, v2):
        crossNorm = cross/np.linalg.norm(cross)
        if float(self.escalar((v1-v2), crossNorm)) == 0:
            return [0,0]
        t = float(self.escalar(v1-portal_vertices[indice+1], crossNorm))/float(self.escalar((v1-v2), crossNorm))
        if t <= 0 or t >= 1:
            return [0]
        areaTotal = np.linalg.norm(cross)
        if areaTotal == 0:
            return [0]
        p = (v1-v2)*t + v2
        if self.PointInTriangle(p, portal_vertices[indice],portal_vertices[indice+1],portal_vertices[indice+2]) == False:
            return [0]
        if self.escalar((v1-portal_vertices[indice+1]), crossNorm) < 0:
            return [t, 1]
        else:
            return [t, 0]


    def SameSide(self, p1,p2, a,b):
        cp1 = np.cross(b-a, p1-a)
        cp2 = np.cross(b-a, p2-a)
        if self.escalar(cp1, cp2) >= 0:
            return True
        else:
            return False

    def PointInTriangle(self, p, a,b,c):
        if self.SameSide(p,a, b,c) and self.SameSide(p,b, a,c) and self.SameSide(p,c, a,b):
            return True
        else:
            return False

    def escalar(self, v1, v2):
        return(v1[0]*v2[0]+v1[1]*v2[1]+v1[2]*v2[2])

    def area(self, v1, v2, v3):
        a = v1-v3
        b = v2-v3
        area = np.cross(a, b)
        area = np.linalg.norm(area)
        return area

    def times(self, matrix, vec):
        vectemp = []
        for i in range(0, 3):
            vectemp.append(vec[0]*matrix[i,0]+vec[1]*matrix[i,1]+vec[2]*matrix[i,2]+matrix[i,3])
        vectemp = np.array(vectemp, dtype=np.float32)
        return vectemp


    def divideGeometry(self, actor, t):
        for i in range(len(actor._vertices)):
            z = self.times(actor._transform, actor._vertices[i])[2]
            if(z > 2.0 and t[0][2] == 0) or (z < -2.0 and t[0][2] == 1):
                actor._colors[i*3] = float(t[0][2])
                actor._colors[i*3+1] = 1.0
                actor._colors[i*3+2] = 0.5
            else:
                actor._colors[i*3] = float(t[0][2])
                actor._colors[i*3+1] = 0.0
                actor._colors[i*3+2] = 0.5
        for i in range(len(t)):
            actor._colors[t[i][1]*3] = float(t[i][2])   # id do portal
            actor._colors[t[i][1]*3+1] = float(t[i][0]) # interpolacao
            actor._colors[t[i][1]*3+2] = float(t[i][3]) # Caso esteja depois do portal 1, caso contrario 0
        return
