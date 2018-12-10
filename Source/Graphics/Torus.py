import math
import numpy as np
from OpenGL import GL
from Source.Graphics.Actor import Actor

class Torus(Actor):
    ## initialization
    def __init__(self, renderer,  **kwargs):
        """Initialize actor."""
        super(Torus, self).__init__(renderer, **kwargs)

        self._R = kwargs.get("R", 1.0)
        self._r = kwargs.get("r", 0.5)
        self._latitude = float(kwargs.get("latitude", 10))
        self._longitude = float(kwargs.get("longitude", 20))
        self._vertices = None
        ## create actor
        self.initialize()


    def addVertex(self, v, vertices):
        """Add a vertex into the array"""
        vn = v / np.linalg.norm(v) * self._radius
        vertices += [[vn[0], vn[1], vn[2]]]
        return len(vertices)-1


    def getTexCoords(self):
        tex = []
        for v in self._vertices:
            tex.append([
                0.5 + math.atan2(v[2], v[0])/(2*math.pi),
                0.5 - math.asin(v[1])/math.pi
            ])
        return np.array(tex, dtype=np.float32)



    def x(self, ang1, ang2):
        return((self._R + self._r*math.cos(ang1))*math.cos(ang2))

    def y(self, ang1, ang2):
        return((self._R + self._r*math.cos(ang1))*math.sin(ang2))

    def z(self, ang1, ang2):
        return(self._r*math.sin(ang1))

    def der1_x(self, ang1, ang2):
        return(-self._r*math.sin(ang1)*math.cos(ang2))

    def der1_y(self, ang1, ang2):
        return(-self._r*math.sin(ang1)*math.sin(ang2))

    def der1_z(self, ang1, ang2):
        return(self._r*math.cos(ang1))

    def der2_x(self, ang1, ang2):
        return(-(self._R + self._r*math.cos(ang1))*math.sin(ang2))

    def der2_y(self, ang1, ang2):
        return((self._R + self._r*math.cos(ang1))*math.cos(ang2))

    def der2_z(self, ang1, ang2):
        return(0)


    def genVert(self, vertices, normals, ang1, ang2):
        vertices.append([self.x(ang1, ang2), self.y(ang1, ang2), self.z(ang1, ang2)])
        norma = np.cross([self.der1_x(ang1, ang2), self.der1_y(ang1, ang2), self.der1_z(ang1, ang2)],
                                [self.der2_x(ang1, ang2), self.der2_y(ang1, ang2), self.der2_z(ang1, ang2)])
        norma /= -np.linalg.norm(norma)
        normals.append(norma)

    def generateGeometry(self):
        """Generate vertices"""
        vertices = []
        normals = []
        texcoords = []
        colors = []


        for i in range(int(self._latitude)):
            for j in range(int(self._longitude)):
                ang1_1 = (i/self._latitude)*2*math.pi
                ang1_2 = ((i+1.0)/self._latitude)*2*math.pi
                ang2_1 = (j/self._longitude)*2*math.pi
                ang2_2 = ((j+1.0)/self._longitude)*2*math.pi

                self.genVert(vertices, normals,ang1_1, ang2_1)
                self.genVert(vertices, normals,ang1_1, ang2_2)
                self.genVert(vertices, normals,ang1_2, ang2_2)

                self.genVert(vertices, normals,ang1_1, ang2_1)
                self.genVert(vertices, normals,ang1_2, ang2_2)
                self.genVert(vertices, normals,ang1_2, ang2_1)



                texcoords.append(i/self._latitude)
                texcoords.append(j/self._longitude)

                texcoords.append(i/self._latitude)
                texcoords.append(((j+1.0))/self._longitude)

                texcoords.append(((i+1.0))/self._latitude)
                texcoords.append(((j+1.0))/self._longitude)

                texcoords.append(i/self._latitude)
                texcoords.append(j/self._longitude)

                texcoords.append(((i+1.0))/self._latitude)
                texcoords.append(((j+1.0))/self._longitude)

                texcoords.append(((i+1.0))/self._latitude)
                texcoords.append(j/self._longitude)

                for k in range(0, 18):
                    colors.append(1.0)


        self._vertices = np.array(vertices, dtype=np.float32)
        self._normals = np.array(normals, dtype=np.float32)
        self._texcoords = np.array(texcoords, dtype=np.float32)
        self._colors = np.array(colors, dtype=np.float32)


    def initialize(self):
        """Creates icosahedron geometry"""
        if self._vertices is None:
            self.generateGeometry()

        ## create object
        self.create(self._vertices,
            normals=self._normals,
            texcoords=self._texcoords,
            colors=self._colors)

    def render(self):
        """Render icosahedron"""
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, len(self._vertices))
        #GL.glDrawElements(self._render_mode, self.numberOfIndices, GL.GL_UNSIGNED_INT, None)
