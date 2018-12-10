import math
import ctypes
import numpy as np
from Source.Graphics.Bezier import Bezier
from Source.Graphics.SegmentodeTrilho import SegmentodeTrilho
from Source.Graphics.Cylinder import Cylinder
from Source.Graphics.Material import Material

from PyQt5.QtCore import QObject
from PyQt5.QtGui import QMatrix4x4, QVector3D, QVector4D, QOpenGLShader, QOpenGLShaderProgram, QOpenGLBuffer, QOpenGLVertexArrayObject
from PyQt5.QtWidgets import QOpenGLWidget


from OpenGL import GL

class Construtor(QObject):
    ## initialization
    def __init__(self,  **kwargs):
        """Initialize actor."""
        super(Construtor, self).__init__()

        self._world = kwargs.get("world", None)
        self._segmentos = []
        self._suportes = []
        self._comprimento = kwargs.get("comprimento", 4)
        self._elevacao = kwargs.get("elevacao", 0.0)
        self._rotacao = kwargs.get("rotacao", 0.0)
        self._inclinacao = kwargs.get("inclinacao", 0.0)
        self._tipo = kwargs.get("tipo", 0)
        self._terreno = kwargs.get("terreno", 0)
        self._primeiro_ponto = [0.0, 0.0, 0.0]
        self._primeiro_tengente = [0.0, 0.0, 0.0]
        self._primeiro_inclinacao = 0.0

        self._ponto_inicial = [0.0, 0.0, 0.0]
        self._ponto_final = [0.0, 0.0, 0.0]
        self._tangente_inicial = [1.0, 0.0, 0.0]
        self._up_inicial = [0.0, 1.0, 0.0]
        self._cross_inicial = [0.0, 0.0, 1.0]
        self._tangente_final = [-1.0, 0.0, 0.0]
        self._up_final = [0.0, 1.0, 0.0]
        self._cross_final = [0.0, 0.0, 1.0]
        self._inclinacao_inicial = 0.0
        self._inclinacao_final = 0.0
        self._rotacaoGlobal = 0.0
        self._elevacaoGlobal = 0.0



        self._segmentoAtual = None
        self._bezierAtual = None


    def rotation_matrix(self, axis, theta):
        """
        Return the rotation matrix associated with counterclockwise rotation about
        the given axis by theta radians.
        """
        axis = np.asarray(axis)
        axis = axis / math.sqrt(np.dot(axis, axis))
        a = math.cos(theta / 2.0)
        b, c, d = -axis * math.sin(theta / 2.0)
        aa, bb, cc, dd = a * a, b * b, c * c, d * d
        bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
        return np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                         [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                         [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])

    def vec3sum(self, a, b):
        return [a[0]+b[0], a[1]+b[1],a[2]+b[2]]

    def escalarVec3(self, num, vec):
        vec2 = []
        for i in range(3):
            vec2.append(vec[i])
        for i in range(3):
            vec2[i] = vec2[i]*num
        return(vec2)

    def escalar(self, v1, v2):
        return(v1[0]*v2[0]+v1[1]*v2[1]+v1[2]*v2[2])

    def normalizar(self, v):
        norm = np.linalg.norm(v)
        if norm != 0.0:
            v = v/norm
        return(v)

    def escalarTangente(self, tan):
        return self.escalarVec3(self._raio*0.551915024494, tan)

    def calcularPontoFinaleTangente(self):
        sinTeta = math.sin(self._elevacaoGlobal + self._elevacao)
        cosTeta = math.cos(self._elevacaoGlobal + self._elevacao)
        sinFi = math.sin(self._rotacaoGlobal + self._rotacao)
        cosFi = math.cos(self._rotacaoGlobal + self._rotacao)


        if(self._elevacao != 0.0):
            self._tangente_final = np.dot(self.rotation_matrix(self._cross_inicial, self._elevacao), self._tangente_inicial)
            self._up_final = np.dot(self.rotation_matrix(self._cross_inicial, self._elevacao), self._up_inicial)
        else:
            self._tangente_final = self._tangente_inicial
            self._up_final = self._up_inicial

        if(self._rotacao != 0.0):
            self._tangente_final =  np.dot(self.rotation_matrix(self._up_inicial, self._rotacao), self._tangente_final)
            self._up_final = np.dot(self.rotation_matrix(self._up_inicial, self._rotacao), self._up_final)
            self._cross_final =  np.dot(self.rotation_matrix(self._up_inicial, self._rotacao), self._cross_inicial)
        else:
            self._cross_final = self._cross_inicial

        if(self._inclinacao != 0.0):
            self._up_final = np.dot(self.rotation_matrix(self._tangente_final, self._inclinacao), self._up_final)
            self._cross_final =  np.dot(self.rotation_matrix(self._tangente_final, self._inclinacao), self._cross_final)

        self._tangente_final = self.escalarVec3(-1.0, self._tangente_final)
        self._ponto_final = self.vec3sum(self.vec3sum(self._ponto_inicial,
                                                      self.escalarVec3((self._comprimento/2.0), self._tangente_inicial)),
                                         self.escalarVec3(-1.0*(self._comprimento/2.0), self._tangente_final))


    def atualizarPontos(self):
        self.calcularPontoFinaleTangente()
        self._inclinacao_final = self._inclinacao_inicial + self._inclinacao

        angulo = self.escalar(self._tangente_inicial, self.escalarVec3(-1.0, self._tangente_final))
        c = self.vec3sum(self._tangente_inicial, self.escalarVec3(-1.0, self._tangente_final))
        c_norm = np.linalg.norm(c)
        if angulo >= -1.0 and angulo <= 1.0:
            angulo = math.acos(angulo)
        else:
            if angulo > 1.0:
                angulo = 0.0
            else:
                angulo = math.pi
        L = c_norm
        if angulo != 0:
            L = (angulo*c_norm)/(2.0*math.sin(angulo/2.0))

        if L != 0:
            self._raio =  (self._comprimento/2.0)/L
        else:
            self._raio = self._comprimento/2.0
        self._ponto_final = self.vec3sum(self.vec3sum(self._ponto_inicial,
                                                      self.escalarVec3(self._raio,self._tangente_inicial)),
                                         self.escalarVec3(-self._raio, self._tangente_final))
        pontos = []
        pontos.append(self._ponto_inicial)

        pontos.append(self.vec3sum(self._ponto_inicial, self.escalarTangente(self._tangente_inicial)))
        pontos.append(self.vec3sum(self._ponto_final, self.escalarTangente(self._tangente_final)))

        pontos.append(self._ponto_final)

        # print(str(self._elevacao*180.0/math.pi) + " " + str(self._rotacao*180.0/math.pi) + " " + str(self._inclinacao*180.0/math.pi))
        return(pontos)

    def addSegmento(self):
        if(len(self._segmentos) != 0):
            self.addSuporte(0.0)
            self.addSuporte(0.25)
            self.addSuporte(0.5)
            self.addSuporte(0.75)
        self._rotacaoGlobal = self._rotacaoGlobal + self._rotacao
        self._elevacaoGlobal = self._elevacaoGlobal + self._elevacao
        #self._inclinacao_inicial += self._inclinacao_final

        self._ponto_inicial = self._ponto_final


        self._tangente_inicial = self.escalarVec3(-1.0, self._tangente_final)
        self._up_inicial = self._up_final
        self._cross_inicial = self._cross_final



        self._bezierAtual = Bezier()
        self._bezierAtual.create(self.atualizarPontos())


        cor = self.corTrilho()
        mat = Material(cbase=cor)
        self._segmentoAtual = SegmentodeTrilho(self._world, comprimento=self._comprimento,
                                               bezier=self._bezierAtual, tang=self._tangente_inicial, up=self._up_inicial, cross=self._cross_inicial,
                                               inclinacao=self._inclinacao, rotacao=self._rotacao, elevacao=self._elevacao, tipo=self._tipo, ptInicial=self._ponto_inicial,
                                               material=mat)
        self._segmentoAtual.should_be_rendered = True
        self._segmentos.append(self._segmentoAtual)

        self._world.addActor(self._segmentoAtual)


    def rmTrilho(self):
        if(len(self._segmentos) == 1):
            return
        anterior = self._segmentos[len(self._segmentos)-2]

        self._rotacaoGlobal -= anterior._rotacao
        self._elevacaoGlobal -= anterior._elevacao


        self._ponto_inicial = anterior._ponto_inicial
        self._tangente_inicial = anterior._tang
        self._up_inicial = anterior._up
        self._cross_inicial = anterior._cross

        self._world.removeActor(self._segmentoAtual)
        self._segmentos.pop()
        self.rmSuporte()
        self.rmSuporte()
        self.rmSuporte()
        self.rmSuporte()
        self._segmentoAtual = anterior
        self._segmentoAtual._elevacao = self._elevacao
        self._segmentoAtual._rotacao = self._rotacao
        self._segmentoAtual._inclinacao = self._inclinacao
        self._segmentoAtual._tipo = self._tipo
        self.mudouTamanho(self._comprimento)

    def addSuporte(self, t):
        tg = self._segmentoAtual._bezier.tangent(t)
        up = self._segmentoAtual.up(t*self._comprimento, tg)

        if(self.escalar(up, [0.0, 1.0, 0.0]) < 0.0):
            self._suportes.append(None)
        else:
            posCima = self._segmentoAtual._bezier.point(t)
            yBaixo = self._terreno.f(posCima[0], posCima[2])
            yCentro = (posCima[1] + yBaixo)*0.5
            altura = posCima[1] - yBaixo
            suporte = Cylinder(self._world, resolution=8, radius=0.05, height=altura)
            suporte._transform.translate(QVector3D(posCima[0], yCentro, posCima[2]))
            self._world.addActor(suporte)
            self._suportes.append(suporte)

    def rmSuporte(self):
        suporte = self._suportes.pop()
        if(suporte != None):
            self._world.removeActor(suporte)

    def mudouElevacao(self, rotacao):
        rotacao = float(rotacao) + 0.01
        self._elevacao = rotacao
        self._bezierAtual.create(self.atualizarPontos())
        self._segmentoAtual._bezier.create(self.atualizarPontos())
        self._segmentoAtual._elevacao = rotacao
        self._segmentoAtual.generateGeometry()
        self._segmentoAtual.updateBuffer(vertices=self._segmentoAtual._vertices, normals=self._segmentoAtual._normals)


    def mudouRotacao(self, rotacao):
        rotacao = float(rotacao) + 0.01
        self._rotacao = rotacao
        self._bezierAtual.create(self.atualizarPontos())
        self._segmentoAtual._bezier.create(self.atualizarPontos())
        self._segmentoAtual._rotacao = rotacao
        self._segmentoAtual.generateGeometry()
        self._segmentoAtual.updateBuffer(vertices=self._segmentoAtual._vertices, normals=self._segmentoAtual._normals)

    def mudouInclinacao(self, rotacao):
        rotacao = float(rotacao) + 0.01
        self._inclinacao = rotacao
        self._bezierAtual.create(self.atualizarPontos())
        self._segmentoAtual._bezier.create(self.atualizarPontos())
        self._segmentoAtual._inclinacao = rotacao
        self._segmentoAtual.generateGeometry()
        self._segmentoAtual.updateBuffer(vertices=self._segmentoAtual._vertices, normals=self._segmentoAtual._normals)

    def mudouTamanho(self, tamanho):
        self._comprimento = tamanho
        self._bezierAtual.create(self.atualizarPontos())
        self._segmentoAtual._bezier.create(self.atualizarPontos())
        self._segmentoAtual._comprimento = tamanho
        self._segmentoAtual.generateGeometry()
        self._segmentoAtual.updateBuffer(vertices=self._segmentoAtual._vertices, normals=self._segmentoAtual._normals, texcoords=self._segmentoAtual._texcoords, usage=QOpenGLBuffer.DynamicCopy)

    def mudouTipo(self, tipo):
        self._tipo = tipo
        self._segmentoAtual._tipo = tipo
        self._segmentoAtual._active_material._cbase = self.corTrilho()

    def terminar(self):
        self._tipo = 4
        self._rotacaoGlobal = self._rotacaoGlobal + self._rotacao
        self._elevacaoGlobal = self._elevacaoGlobal + self._elevacao
        self._inclinacao_final = self._inclinacao_inicial + self._inclinacao

        distancia = np.linalg.norm(self.vec3sum(self._ponto_final,self.escalarVec3(-1.0, self._primeiro_ponto)))
        if int(distancia) == distancia:
            distancia = int(distancia)
        else:
            distancia = int(distancia) + 1

        self._ponto_inicial = self._ponto_final
        self._tangente_inicial = self.escalarVec3(-1.0, self._tangente_final)
        self._up_inicial = self._up_final
        self._cross_inicial = self._cross_final

        elevacao_final = 0.0
        rotacao_final = 0.0
        inclinacao_final = 0.0
        # if self._elevacaoGlobal != 0.0:
        #     elevacao_final = -(self._elevacaoGlobal%math.pi)*(self._elevacaoGlobal/abs(self._elevacaoGlobal))
        # if self._rotacaoGlobal != 0.0:
        #     rotacao_final = -(self._rotacaoGlobal%math.pi)*(self._rotacaoGlobal/abs(self._rotacaoGlobal))
        # if self._inclinacao_final != 0.0:
        #     inclinacao_final = -(self._inclinacao_final%math.pi)*(self._inclinacao_final/abs(self._inclinacao_final))

        self._bezierAtual = Bezier()
        self._bezierAtual.create(self.terminarPontos(distancia))
        self.atualizarPontos()
        self._segmentoAtual = SegmentodeTrilho(self._world, comprimento=distancia,
                                               bezier=self._bezierAtual, tang=self._tangente_inicial, up=self._up_inicial, cross=self._cross_inicial,
                                               inclinacao=inclinacao_final, rotacao=rotacao_final, elevacao=elevacao_final, tipo=self._tipo)
        self._segmentoAtual.should_be_rendered = True
        self._segmentos.append(self._segmentoAtual)

        self._world.addActor(self._segmentoAtual)
        self._segmentoAtual = None

    def corTrilho(self):
        cor = None
        if(self._tipo == 0):
            cor = QVector3D(1.0, 0.5, 0.5)
        elif(self._tipo == 1):
            cor = QVector3D(1.0, 1.0, 1.0)
        elif(self._tipo == 2):
            cor = QVector3D(0.5, 0.5, 1.0)
        elif(self._tipo == 3):
            cor = QVector3D(0.5, 0.5, 0.1)
        else:
            cor = QVector3D(1.0, 0.1, 0.1)
        return cor

    def terminarPontos(self, distancia):
        tg = self.vec3sum(self._ponto_final,self.escalarVec3(-1.0, self._primeiro_ponto))
        tg = tg/np.linalg.norm(tg)
        pontos = []
        pontos.append(self._ponto_inicial)
        pontos.append(self.vec3sum(self._ponto_inicial, self.escalarVec3((-distancia*0.15), tg)))
        pontos.append(self.vec3sum(self._ponto_inicial, self.escalarVec3((-distancia*0.3), tg)))
        pontos.append([0.0, 0.0, 0.0])

        return(pontos)
