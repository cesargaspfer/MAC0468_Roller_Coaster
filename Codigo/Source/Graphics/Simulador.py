import math
import ctypes
import numpy as np
from Source.Graphics.Bezier import Bezier
from Source.Graphics.SegmentodeTrilho import SegmentodeTrilho

from PyQt5.QtCore import QObject
from PyQt5.QtGui import QMatrix4x4, QVector3D, QVector4D, QOpenGLShader, QOpenGLShaderProgram, QOpenGLBuffer, QOpenGLVertexArrayObject
from PyQt5.QtWidgets import QOpenGLWidget


from OpenGL import GL

class Simulador(QObject):
    ## initialization
    def __init__(self,  **kwargs):
        """Initialize actor."""
        super(Simulador, self).__init__()
        #self._world = kwargs.get("world", None)
        self._contrutor = kwargs.get("contrutor", None)
        self._carros = []


        self._posicao_escalar = []
        self._posicao_escalar_global = []
        self._velocidade = []
        self._forca = []
        self._tangente = []
        self._up = []
        self._posicao_vetorial = []
        self._segmento_atual = []

        self._segmentos = self._contrutor._segmentos
        self._t = 0.0

    def addCarro(self, carro):
        self._carros.append(carro)

        self._posicao_escalar.append(0.0)
        self._posicao_escalar_global.append(0.0)
        self._velocidade.append(0.0)
        self._forca.append(0.0)
        self._tangente.append(np.array([0.0, 0.0, 0.0]))
        self._up.append(np.array([0.0, 0.0, 0.0]))
        self._posicao_vetorial.append(np.array([0.0, 0.0, 0.0]))
        self._segmento_atual.append(0)

    def Iniciar(self):
        self._segmentos = self._contrutor._segmentos
        self._t = 0.0
        n = len(self._carros)
        m = len(self._segmentos)
        for i in range(n):
            transf = QMatrix4x4()
            j = 0
            id = n-i-1
            '''------------------------------------------------------------------'''
            pos_escalar = 0.6+1.1*id
            p = self._segmentos[j].posicao(pos_escalar)
            offset = 0.0
            while(p == -1):
                offset = self._segmentos[j]._comprimento
                j += 1
                j = j%m
                pos_escalar -= offset
                p = self._segmentos[j].posicao(pos_escalar)

            self._segmento_atual[id] = j
            self._posicao_escalar[id] = pos_escalar
            self._posicao_escalar_global[id] = pos_escalar
            self._velocidade[id] = 0.0
            self._forca[id] = 0.0
            self._posicao_vetorial[id] = p
            self._tangente[id] = self._segmentos[j].tangent(pos_escalar)
            self._up[id] = self._segmentos[j].up(pos_escalar, self._tangente[id])

            #transf.scale(0.5, 0.3, 0.3)
            transf.translate(float(p[0]), float(p[1]), float(p[2]))
            self._carros[id].should_be_rendered = True
            self._carros[id]._transform = transf

    def parar(self):
        for i in range(len(self._carros)):
            self._carros[i].should_be_rendered = False

    def step(self, dt):
        dt = dt/1000
        n = len(self._carros)
        m = len(self._segmentos)

        # Loop que calcula as velocidades, posicoes e forcas dos _carros
        sum = 0.0
        final = False
        for i in range(n):
            self.eulerStep(i, dt)
            sum += self._velocidade[i]
            if(self._segmentos[self._segmento_atual[i]]._tipo == 4):
                final = True
        if final == True:
            if(sum < 0.0):
                sum = 0.0
            else:
                sum /= float(n)
        else:
            sum /= float(n)
        for i in range(n):
             self._velocidade[i] = sum





        # Loop que calcula o segmento que o carro esta e sua posicao escalar local
        for i in range(n):
            id = n-i-1
            j = self._segmento_atual[id]
            pos_escalar = self._posicao_escalar[id] + self._velocidade[id]*dt
            p = self._segmentos[j].posicao(pos_escalar)
            offset = 0.0
            while(p == -2):
                j -= 1
                j = j%m
                pos_escalar = self._segmentos[j]._comprimento+pos_escalar
                p = self._segmentos[j].posicao(pos_escalar)
            while(p == -1):
                offset = self._segmentos[j]._comprimento
                j += 1
                j = j%m
                pos_escalar -= offset
                p = self._segmentos[j].posicao(pos_escalar)


            # Atualiza as componentes
            self._segmento_atual[id] = j
            self._posicao_escalar[id] = pos_escalar
            self._posicao_escalar_global[id] += self._velocidade[id]*dt
            self._posicao_vetorial[id] = p
            self._tangente[id] = self._segmentos[j].tangent(pos_escalar)
            self._up[id] = self._segmentos[j].up(pos_escalar, self._tangente[id])

            # Atualiza a posicao
            transf = QMatrix4x4()
            transf.translate(float(p[0]), float(p[1]), float(p[2]))
            transf = self._segmentos[j].transforme(pos_escalar, transf, self._tangente[id], self._up[id])

            # if(id == 0):
            #     print(sum)
            self._carros[id]._transform = transf
            #
        return

    def eulerStep(self, id, dt):
        car_tg = self._tangente[id]
        car_up = self._up[id]
        car_vel = self._velocidade[id]
        car_mass = 1.0
        car_forca = 0.0

        seg_tipo = self._segmentos[self._segmento_atual[id]]._tipo
        vel_max = 5.0
        vel_min = 4.0
        aceleracao = 5.0
        if(seg_tipo == 3):
            aceleracao = -5.0

        # Plataforma
        if(seg_tipo == 0):
            if(self._velocidade[id] < vel_min):
                seg_tipo = 2
                aceleracao = 10.0
            else:
                seg_tipo = 3
                aceleracao = -10.0

        # Normal
        if(seg_tipo == 1):
            gravidade = np.array([0.0, -1.0, 0.0])
            car_forca += np.dot(gravidade, car_tg)*9.8
            self._velocidade[id] += car_forca*dt - self._velocidade[id]*0.08*dt

        # Alavanca
        if(seg_tipo == 2):
            if(self._velocidade[id] < vel_min):
                self._velocidade[id] += aceleracao*dt
                if(self._velocidade[id] > vel_min):
                    self._velocidade[id] = vel_min
            else:
                gravidade = np.array([0.0, -1.0, 0.0])
                car_forca += np.dot(gravidade, car_tg)*9.8
                self._velocidade[id] += car_forca*dt - self._velocidade[id]*0.08*dt
                if(self._velocidade[id] < vel_min):
                    self._velocidade[id] = vel_min

        # Freios
        if(seg_tipo == 3):
            if(self._velocidade[id] > vel_max):
                self._velocidade[id] += aceleracao*dt
                if(self._velocidade[id] < vel_max):
                    self._velocidade[id] = vel_max
            else:
                gravidade = np.array([0.0, -1.0, 0.0])
                car_forca += np.dot(gravidade, car_tg)*9.8
                self._velocidade[id] += car_forca*dt - self._velocidade[id]*0.08*dt

        # Final
        if(seg_tipo == 4):
            if(self._velocidade[id] > 0.01):
                self._velocidade[id] -= 20.0*0.9*dt
            else:
                self._velocidade[id] = 0.0
