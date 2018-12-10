import math
import numpy as np
from OpenGL import GL
import random
from Source.Graphics.Actor import Actor

class Ocean(Actor):
    ## initialization
    def __init__(self, renderer,  **kwargs):
        """Initialize actor."""
        super(Ocean, self).__init__(renderer, **kwargs)

        self._x = kwargs.get("x", 50.0)
        self._z = kwargs.get("z", 50.0)
        self._latitude = float(kwargs.get("latitude", 20))
        self._longitude = float(kwargs.get("longitude", 20))
        self._vertices = None

        ## create actor
        self.initialize()

    def f(self, x, y):
        return(0.25*(math.cos((x+y)*0.5)+math.cos((x-y)*0.5) - 3.0))

    def dx(self, x, y):
        return(-0.25*math.sin(x*0.5)*math.cos(y*0.5))

    def dz(self, x, y):
        return(-0.25*math.cos(x*0.5)*math.sin(y*0.5))

    def genVert(self, vertices, normals, texcoords, i, j):
        x = (i/self._latitude)*self._x-(self._x/2.0)
        z = (j/self._longitude)*self._z-(self._z/2.0)
        vertices.append([x, self.f(x, z), z])
        normals.append([self.dx(x, z),-1.0,self.dz(x, z)]/-np.linalg.norm([self.dx(x, z),1.0,self.dz(x, z)]))
        texcoords.append([i/self._latitude, j/self._longitude])




    def generateGeometry(self):

        """Generate vertices"""
        vertices = []
        normals = []
        texcoords = []

        for i in range(int(self._latitude)):
            for j in range(int(self._longitude)):
                x_1 = i
                x_2 = i + 1
                z_1 = j
                z_2 = j + 1

                self.genVert(vertices, normals, texcoords, x_1, z_1)
                self.genVert(vertices, normals, texcoords, x_1, z_2)
                self.genVert(vertices, normals, texcoords, x_2, z_2)

                self.genVert(vertices, normals, texcoords, x_1, z_1)
                self.genVert(vertices, normals, texcoords, x_2, z_2)
                self.genVert(vertices, normals, texcoords, x_2, z_1)

        self._vertices = np.array(vertices, dtype=np.float32)
        self._normals = np.array(normals, dtype=np.float32)
        self._texcoords = np.array(texcoords, dtype=np.float32)


    def initialize(self):
        """Creates icosahedron geometry"""
        if self._vertices is None:
            self.generateGeometry()

        ## create object
        self.create(self._vertices,
            normals=self._normals,
            texcoords=self._texcoords)


        '''
        waves = []
        for i in range(0, 10):
            waves.append(random.random())
            waves.append(random.random() * math.pi)
            waves.append(random.random() * math.pi)
            vel = random.random() * 2
            ang = random.random() * math.pi
            waves.append(vel*math.cos(ang))
            waves.append(vel*math.sin(ang))

        self._waves = np.array(waves, dtype=np.float32)
        '''

    def render(self):
        """Render icosahedron"""
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, len(self._vertices))
        #GL.glDrawElements(self._render_mode, self.numberOfIndices, GL.GL_UNSIGNED_INT, None)
