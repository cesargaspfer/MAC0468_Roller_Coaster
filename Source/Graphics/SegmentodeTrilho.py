import math
import numpy as np
from OpenGL import GL
from Source.Graphics.Actor import Actor
from Source.Graphics.Bezier import Bezier
from PyQt5.QtGui import QMatrix4x4, QVector3D, QVector4D, QOpenGLShader, QOpenGLShaderProgram, QOpenGLBuffer, QOpenGLVertexArrayObject

class SegmentodeTrilho(Actor):
    ## initialization
    def __init__(self, renderer,  **kwargs):
        """Initialize actor."""
        super(SegmentodeTrilho, self).__init__(renderer, **kwargs)

        self._comprimento = kwargs.get("comprimento", 4)

        self._elevacao = kwargs.get("elevacao", 0.0)
        self._bezier = kwargs.get("bezier", None)
        self._tang = kwargs.get("tang", None)
        self._up = kwargs.get("up", None)
        self._cross = kwargs.get("cross", None)

        self._inclinacao = kwargs.get("inclinacao", 0.0)
        self._rotacao = kwargs.get("rotacao", 0.0)
        self._elevacao = kwargs.get("elevacao", 0.0)

        self._tipo = kwargs.get("tipo", 0)

        self._ponto_inicial = kwargs.get("ptInicial", 0)

        self._vertices = None
        self._normals = None
        self._texcoords = None
        self._colors = None

        ## create actor
        self.initialize()

    def rotation_matrix(self, axis, theta):

        """
        Return the rotation matrix associated with counterclockwise rotation about
        the given axis by theta radians.
        """
        axis = np.asarray(axis)
        if(np.dot(axis, axis) == 0.0):
            return np.array([[1.0, 0.0, 0.0], [0.0,-1.0,0.0],[0.0,0.0,1.0]])
        axis = axis / math.sqrt(np.dot(axis, axis))
        a = math.cos(theta / 2.0)
        b, c, d = -axis * math.sin(theta / 2.0)
        aa, bb, cc, dd = a * a, b * b, c * c, d * d
        bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
        return np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                         [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                         [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])

    def escalar(self, v1, v2):
        return(v1[0]*v2[0]+v1[1]*v2[1]+v1[2]*v2[2])

    def vec3sum(self, a, b):
        return [a[0]+b[0], a[1]+b[1],a[2]+b[2]]

    def vec3minus(self, a):
        return [a[0],a[1],a[2]]

    def vec3escalar(self, num, vec):
        vec2 = []
        for i in range(3):
            vec2.append(vec[i])
        for i in range(3):
            vec2[i] = vec2[i]*num
        return(vec2)

    def posicao(self, pos):
        if(pos >= self._comprimento):
            return(-1)
        if(pos < 0):
            return(-2)
        t = pos/float(self._comprimento)
        return(self._bezier.point(t))

    def tangent(self, pos):
        t = pos/float(self._comprimento)
        tang = self._bezier.tangent(t)
        if np.linalg.norm(tang) != 0.0:
            tang = tang/np.linalg.norm(tang)
        return(tang)

    def up(self, pos, tangente):
        t = pos/float(self._comprimento)
        ele = t*self._elevacao
        rot = t*self._rotacao
        inc = t*self._inclinacao
        tangente = self._bezier.tangent(t)
        up = [self._up[0], self._up[1], self._up[2]]

        if ele != 0:
            matriz_rotacao = self.rotation_matrix(self._cross, ele)
            up = np.dot(matriz_rotacao, up)

        if rot != 0:
            matriz_rotacao = self.rotation_matrix(self._up, rot)
            up = np.dot(matriz_rotacao, up)

        if inc != 0:
            matriz_rotacao = self.rotation_matrix(tangente, inc)
            up = np.dot(matriz_rotacao, up)

        if np.linalg.norm(up) != 0.0:
            up = up/np.linalg.norm(up)


        return(up)


    def transforme(self, pos, transf, tangente, up):
        t = pos/float(self._comprimento)
        ele = t*self._elevacao
        rot = t*self._rotacao
        inc = t*self._inclinacao


        orientacao_tang = [0.0, 0.0, 1.0]
        orientacao_up = [0.0, 1.0, 0.0]



        up = self.vec3sum(up, self.vec3escalar(-self.escalar(up, tangente), tangente))
        if np.linalg.norm(up) != 0.0:
            up = up/np.linalg.norm(up)
        cross = np.cross(tangente, up)
        tmp = self.escalar(orientacao_up, up)
        ang1 = 0.0
        if(tmp >= -1.0 and tmp <= 1.0):
            ang1 = math.acos(tmp)
        if(tmp < -1.0):
            ang1 = math.pi
        cross1 = np.cross(orientacao_up, up)
        if np.linalg.norm(cross1) != 0.0:
            cross1 = cross1/np.linalg.norm(cross1)
        matriz1 = None
        if(ang1 != 0.0):
            matriz1 = self.rotation_matrix(cross1, ang1)
            orientacao_tang = np.dot(matriz1, orientacao_tang)
            orientacao_up = np.dot(matriz1, orientacao_up)
            if np.linalg.norm(orientacao_up) != 0.0:
                orientacao_up = orientacao_up/np.linalg.norm(orientacao_up)
            if np.linalg.norm(orientacao_tang) != 0.0:
                orientacao_tang = orientacao_tang/np.linalg.norm(orientacao_tang)
        if(ang1 != 0):
            transf.rotate(ang1*(180.0/math.pi), QVector3D(cross1[0], cross1[1], cross1[2]))

        tmp = self.escalar(orientacao_tang, tangente)
        ang2 = 0.0
        if(tmp >= -1.0 and tmp <= 1.0):
            ang2 = math.acos(tmp)
        if(tmp < -1.0):
            ang2 = math.pi
        cross2 = np.cross(orientacao_tang, tangente)
        if np.linalg.norm(cross2) != 0.0:
            cross2 = cross2/np.linalg.norm(cross2)

        if(ang2 != 0):
            if self.escalar(cross2, up) > 0.0:
                transf.rotate(ang2*(180.0/math.pi), QVector3D(0.0, 1.0, 0.0))
            else:
                transf.rotate(ang2*(180.0/math.pi), QVector3D(0.0, -1.0, 0.0))
        matriz2 = None
        if(ang2 != 0.0):
            matriz2 = self.rotation_matrix(cross2, ang2)
            orientacao_tang = np.dot(matriz2, orientacao_tang)
            orientacao_up = np.dot(matriz2, orientacao_up)
            if np.linalg.norm(orientacao_up) != 0.0:
                orientacao_up = orientacao_up/np.linalg.norm(orientacao_up)
            if np.linalg.norm(orientacao_tang) != 0.0:
                orientacao_tang = orientacao_tang/np.linalg.norm(orientacao_tang)
        # print(up)
        # print(cross2)
        # print("----------------------------------------------------")
        # if(self.escalar(orientacao_tang, tangente) > -1.0 and self.escalar(orientacao_tang, tangente) < 1.0):
        #     print((180.0/math.pi)*math.acos(self.escalar(orientacao_tang, tangente)))
        # elif(self.escalar(orientacao_tang, tangente) == 1.0):
        #     print(0.0)
        # else:
        #     print(180.0)
        # if(self.escalar(cross2, up) > -1.0 and self.escalar(cross2, up) < 1.0):
        #     print((180.0/math.pi)*math.acos(self.escalar(cross2, up)))
        # elif(self.escalar(cross2, up) == 1.0):
        #     print(0.0)
        # else:
        #     print(180.0)
        # if(self.escalar(orientacao_tang, up) < 1.0):
        #     print((180.0/math.pi)*math.acos(self.escalar(orientacao_tang, up)))
        # else:
        #     print(0.0)
        # if(self.escalar(tangente, up) < 1.0):
        #     print((180.0/math.pi)*math.acos(self.escalar(tangente, up)))
        # else:
        #     print(0.0)
        # if(self.escalar(orientacao_up, up) < 1.0):
        #     print((180.0/math.pi)*math.acos(self.escalar(orientacao_up, up)))
        # else:
        #     print(0.0)

        # cross = np.cross(tangente, up)
        # transf.lookAt(QVector3D(0.0, 0.0, 0.0),  QVector3D(tangente[0], -tangente[1], tangente[2]), QVector3D(up[0], up[1], up[2]))
        #transf.lookAt(QVector3D(0.0, 0.0, 0.0), QVector3D(up[0], up[1], up[2]), QVector3D(0.0, 1.0, 0.0))
        #transf.rotate(-90.0, QVector3D(up[0], up[1], up[2]))
        #transf.scale(1.0, 1.0, 1.0)
        '''
        if self._ang1 != 0:
            transf.rotate(self._ang1*(180.0/math.pi), self._cross1[0], self._cross1[1], self._cross1[2])

        if self._ang2 != 0:
            transf.rotate(self._ang2*(180.0/math.pi), -self._cross2[0], -self._cross2[1], -self._cross2[2])
        '''
        '''
        if ele != 0:
            transf.rotate(ele*(180/math.pi), self._cross[0], self._cross[1], self._cross[2])
        if rot != 0:
            transf.rotate(rot*(180/math.pi), self._up[0], self._up[1], self._up[2])
        if inc != 0:
            transf.rotate(inc*(180/math.pi), tangente[0], tangente[1], tangente[2])
        '''
        return(transf)

    def generateGeometry(self):
        """Generate vertices"""
        vertices = []
        normals = []
        texcoords = []
        colors = []

        # Pre-processamento da orientacao
        orientacao_tang = [0.0, 0.0, 1.0]
        orientacao_up = [0.0, 1.0, 0.0]
        orientacao_cross = [1.0, 0.0, 0.0]

        tmp = self.escalar(orientacao_up, self._up)
        self._ang1 = 0.0
        if(tmp >= -1.0 and tmp <= 1.0):
            self._ang1 = math.acos(tmp)
        elif(tmp < -1.0):
            self._ang1 = math.pi
        self._cross1 = np.cross(orientacao_up, self._up)
        self._matriz1 = None
        if np.linalg.norm(self._cross1) != 0.0:
            self._cross1 = self._cross1/np.linalg.norm(self._cross1)
        if(self._ang1 != 0.0):
            self._matriz1 = self.rotation_matrix(self._cross1, self._ang1)
            orientacao_tang = np.dot(self._matriz1, orientacao_tang)
            orientacao_up = np.dot(self._matriz1, orientacao_up)

        tmp = self.escalar(orientacao_tang, self._tang)
        self._cross2 = np.cross(self._tang, orientacao_tang)
        if np.linalg.norm(self._cross2) != 0.0:
            self._cross2 = self._cross2/np.linalg.norm(self._cross2)
        if(self._cross2[0] == 0.0 and self._cross2[1] == 0.0 and self._cross2[2] == 0.0):
            self._cross2 = self._up
        self._ang2 = 0.0
        if(tmp >= -1.0 and tmp <= 1.0):
            self._ang2 = math.acos(tmp)
        elif(tmp < -1.0):
            print(orientacao_tang)
            print(self._tang)
            print(self._up)
            print(self._cross2)
            self._ang2 = math.pi
        self._matriz2 = None
        if(self._ang2 != 0.0):
            # Qualquer coisa estava _cross2 em vez de up
            self._matriz2 = self.rotation_matrix(-self._cross2, self._ang2)
            orientacao_tang = np.dot(self._matriz2, orientacao_tang)
        orientacao_tang = orientacao_tang/np.linalg.norm(orientacao_tang)


        # Pre-processamento da rotacao
        pontos_bezier = []
        tangentes_bezier = []
        crosses_bezier = []
        for i in range(int((self._comprimento*2)+1)):
            t = float(i)/(float(self._comprimento)*2.0)
            tangente = self._bezier.tangent(t)

            pontos_bezier.append(self._bezier.point(t))
            tangentes_bezier.append(tangente)

        # Pre-processamento dos pontos orientados para a tangente
        cilindroPrincipal = []
        cilindroPrincipal_Normal = []
        resolucao = 16.0
        for j in range(0, int(resolucao)+1):
            ponto = [math.cos((j/(resolucao))*2.0*math.pi), math.sin((j/(resolucao))*2.0*math.pi), 0.0]

            if(self._ang1 != 0.0):
                ponto = np.dot(self._matriz1, ponto)
            if(self._ang2 != 0.0):
                ponto = np.dot(self._matriz2, ponto)

            cilindroPrincipal.append(ponto)
            cilindroPrincipal_Normal.append(ponto/np.linalg.norm(ponto))

        # Pre-processamento dos deslocamentos
        deslocamento_original1 = [0.15, 0.15, 0.0]
        deslocamento_original2 = [-0.15, 0.15, 0.0]
        if(self._ang1 != 0.0):
            deslocamento_original1 = np.dot(self._matriz1, deslocamento_original1)
            deslocamento_original2 = np.dot(self._matriz1, deslocamento_original2)
        if(self._ang2 != 0.0):
            deslocamento_original1 = np.dot(self._matriz2, deslocamento_original1)
            deslocamento_original2 = np.dot(self._matriz2, deslocamento_original2)

        teste = True
        for i in range(int(self._comprimento)*2):

            t1 = float(i)/(float(self._comprimento)*2.0)
            t2 = float(i+1.0)/(float(self._comprimento)*2.0)

            ponto1 = pontos_bezier[i]
            tangente1 = tangentes_bezier[i]
            ele1 = t1*self._elevacao
            rot1 = t1*self._rotacao
            inc1 = t1*self._inclinacao

            ponto2 = pontos_bezier[i+1]
            tangente2 = tangentes_bezier[i+1]
            ele2 = t2*self._elevacao
            rot2 = t2*self._rotacao
            inc2 = t2*self._inclinacao



            for j in range(0, int(resolucao)):

                p1 = cilindroPrincipal[j]
                p2 = cilindroPrincipal[j+1]

                v1_1 = np.array(p1)
                v1_2 = np.array(p2)
                v2_1 = np.array(p1)
                v2_2 = np.array(p2)

                n1_1 = cilindroPrincipal_Normal[j]
                n2_1 = cilindroPrincipal_Normal[j]
                n1_2 = cilindroPrincipal_Normal[j+1]
                n2_2 = cilindroPrincipal_Normal[j+1]

                deslocamento1_1 = deslocamento_original1
                deslocamento1_2 = deslocamento_original2
                deslocamento2_1 = deslocamento_original1
                deslocamento2_2 = deslocamento_original2

                up1 = self._up
                if ele1 != 0:
                    matriz_rotacao = self.rotation_matrix(self._cross, ele1)
                    v1_1 = np.dot(matriz_rotacao, v1_1)
                    v1_2 = np.dot(matriz_rotacao, v1_2)
                    n1_1 = np.dot(matriz_rotacao, n1_1)
                    n1_2 = np.dot(matriz_rotacao, n1_2)
                    up1 =  np.dot(matriz_rotacao, up1)
                    deslocamento1_1 = np.dot(matriz_rotacao, deslocamento1_1)
                    deslocamento1_2 = np.dot(matriz_rotacao, deslocamento1_2)

                if rot1 != 0:
                    matriz_rotacao = self.rotation_matrix(self._up, rot1)
                    v1_1 = np.dot(matriz_rotacao, v1_1)
                    v1_2 = np.dot(matriz_rotacao, v1_2)
                    n1_1 = np.dot(matriz_rotacao, n1_1)
                    n1_2 = np.dot(matriz_rotacao, n1_2)
                    up1 =  np.dot(matriz_rotacao, up1)
                    deslocamento1_1 = np.dot(matriz_rotacao, deslocamento1_1)
                    deslocamento1_2 = np.dot(matriz_rotacao, deslocamento1_2)

                if inc1 != 0:
                    matriz_rotacao = self.rotation_matrix(tangente1, inc1)
                    v1_1 = np.dot(matriz_rotacao, v1_1)
                    v1_2 = np.dot(matriz_rotacao, v1_2)
                    n1_1 = np.dot(matriz_rotacao, n1_1)
                    n1_2 = np.dot(matriz_rotacao, n1_2)
                    up1 =  np.dot(matriz_rotacao, up1)
                    deslocamento1_1 = np.dot(matriz_rotacao, deslocamento1_1)
                    deslocamento1_2 = np.dot(matriz_rotacao, deslocamento1_2)


                up2 = self._up
                if ele2 != 0:
                    matriz_rotacao = self.rotation_matrix(self._cross, ele2)
                    v2_1 = np.dot(matriz_rotacao, v2_1)
                    v2_2 = np.dot(matriz_rotacao, v2_2)
                    n2_1 = np.dot(matriz_rotacao, n2_1)
                    n2_2 = np.dot(matriz_rotacao, n2_2)
                    up2 =  np.dot(matriz_rotacao, up2)
                    deslocamento2_1 = np.dot(matriz_rotacao, deslocamento2_1)
                    deslocamento2_2 = np.dot(matriz_rotacao, deslocamento2_2)

                if rot2 != 0:
                    matriz_rotacao = self.rotation_matrix(self._up, rot2)
                    v2_1 = np.dot(matriz_rotacao, v2_1)
                    v2_2 = np.dot(matriz_rotacao, v2_2)
                    n2_1 = np.dot(matriz_rotacao, n2_1)
                    n2_2 = np.dot(matriz_rotacao, n2_2)
                    deslocamento2_1 = np.dot(matriz_rotacao, deslocamento2_1)
                    deslocamento2_2 = np.dot(matriz_rotacao, deslocamento2_2)

                if inc2 != 0:
                    matriz_rotacao = self.rotation_matrix(tangente2, inc2)
                    v2_1 = np.dot(matriz_rotacao, v2_1)
                    v2_2 = np.dot(matriz_rotacao, v2_2)
                    n2_1 = np.dot(matriz_rotacao, n2_1)
                    n2_2 = np.dot(matriz_rotacao, n2_2)
                    deslocamento2_1 = np.dot(matriz_rotacao, deslocamento2_1)
                    deslocamento2_2 = np.dot(matriz_rotacao, deslocamento2_2)


                n1_1 = n1_1/np.linalg.norm(n1_1)
                n1_2 = n1_1/np.linalg.norm(n1_2)
                n2_1 = n1_1/np.linalg.norm(n2_1)
                n2_2 = n1_1/np.linalg.norm(n2_2)


                vertices.append(self.vec3sum(self.vec3escalar(0.1, v1_1), ponto1))
                vertices.append(self.vec3sum(self.vec3escalar(0.1, v1_2), ponto1))
                vertices.append(self.vec3sum(self.vec3escalar(0.1, v2_1), ponto2))

                vertices.append(self.vec3sum(self.vec3escalar(0.1, v1_2), ponto1))
                vertices.append(self.vec3sum(self.vec3escalar(0.1, v2_2), ponto2))
                vertices.append(self.vec3sum(self.vec3escalar(0.1, v2_1), ponto2))

                normals.append(n1_1)
                normals.append(n1_2)
                normals.append(n2_1)

                normals.append(n1_2)
                normals.append(n2_2)
                normals.append(n2_1)

                texcoords.append(0.0)
                texcoords.append(0.0)
                texcoords.append(0.0)
                texcoords.append(1.0)
                texcoords.append(1.0)
                texcoords.append(0.0)
                texcoords.append(0.0)
                texcoords.append(1.0)
                texcoords.append(1.0)
                texcoords.append(1.0)
                texcoords.append(1.0)
                texcoords.append(0.0)


                vertices.append(self.vec3sum(v1_1*0.05 + deslocamento1_1, ponto1))
                vertices.append(self.vec3sum(v1_2*0.05 + deslocamento1_1, ponto1))
                vertices.append(self.vec3sum(v2_1*0.05 + deslocamento2_1, ponto2))

                vertices.append(self.vec3sum(v1_2*0.05 + deslocamento1_1, ponto1))
                vertices.append(self.vec3sum(v2_2*0.05 + deslocamento2_1, ponto2))
                vertices.append(self.vec3sum(v2_1*0.05 + deslocamento2_1, ponto2))

                normals.append(n1_1)
                normals.append(n1_2)
                normals.append(n2_1)

                normals.append(n1_2)
                normals.append(n2_2)
                normals.append(n2_1)

                texcoords.append(0.0)
                texcoords.append(0.0)
                texcoords.append(0.0)
                texcoords.append(1.0)
                texcoords.append(1.0)
                texcoords.append(0.0)
                texcoords.append(0.0)
                texcoords.append(1.0)
                texcoords.append(1.0)
                texcoords.append(1.0)
                texcoords.append(1.0)
                texcoords.append(0.0)


                vertices.append(self.vec3sum(self.vec3sum(v1_1*0.05, ponto1),deslocamento1_2))
                vertices.append(self.vec3sum(self.vec3sum(v1_2*0.05, ponto1),deslocamento1_2))
                vertices.append(self.vec3sum(self.vec3sum(v2_1*0.05, ponto2),deslocamento2_2))

                vertices.append(self.vec3sum(self.vec3sum(v1_2*0.05, ponto1),deslocamento1_2))
                vertices.append(self.vec3sum(self.vec3sum(v2_2*0.05, ponto2),deslocamento2_2))
                vertices.append(self.vec3sum(self.vec3sum(v2_1*0.05, ponto2),deslocamento2_2))

                normals.append(n1_1)
                normals.append(n1_2)
                normals.append(n2_1)

                normals.append(n1_2)
                normals.append(n2_2)
                normals.append(n2_1)

                texcoords.append(0.0)
                texcoords.append(0.0)
                texcoords.append(0.0)
                texcoords.append(1.0)
                texcoords.append(1.0)
                texcoords.append(0.0)
                texcoords.append(0.0)
                texcoords.append(1.0)
                texcoords.append(1.0)
                texcoords.append(1.0)
                texcoords.append(1.0)
                texcoords.append(0.0)


            '''
            for k in range(0, 18*3):
                colors.append(0.0)
            if(teste):
                for k in range(0, 18*2*3):
                    colors.append(0.5)
                teste = False
            else:
                for k in range(0, 18*2*3):
                    colors.append(1.0)
            for k in range(0, (18*(int(resolucao)-3))*3):
                colors.append(0.0)
            '''

        '''
        for i in range(int(len(vertices)/3)):
            print(str(vertices[i*3]) + " " + str(vertices[i*3 + 1]) + " " + str(vertices[i*3 + 2]))
        '''
        self._vertices = np.array(vertices, dtype=np.float32)
        self._normals = np.array(normals, dtype=np.float32)
        self._texcoords = np.array(texcoords, dtype=np.float32)



    def initialize(self):
        """Creates icosahedron geometry"""
        if self._vertices is None and not(self._bezier is None):
            self.generateGeometry()

        ## create object
        self.create(self._vertices,
            normals=self._normals,
            texcoords=self._texcoords)

    def render(self):
        """Render icosahedron"""
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, len(self._vertices))
        #GL.glDrawElements(self._render_mode, self.numberOfIndices, GL.GL_UNSIGNED_INT, None)
