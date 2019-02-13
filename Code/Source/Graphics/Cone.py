import math
import numpy as np
from OpenGL import GL
from Source.Graphics.Actor import Actor

class Cone(Actor):

    ## initialization
    def __init__(self, renderer,  **kwargs):
        """Initialize actor."""
        super(Cone, self).__init__(renderer, **kwargs)

        self._radius = kwargs.get("radius", 1.0)
        self._height = kwargs.get("height", 2.0)
        self._resolution = kwargs.get("resolution", 5)

        self._vertices = None

        ## create actor
        self.initialize()
        

    @property
    def radius(self):
        """Returns the bottom radius of this cone"""
        return self._radius


    @property
    def height(self):
        """Returns the height of this cone"""
        return self._height


    @property
    def resolution(self):
        """Returns the resolution of this cone"""
        return self._resolution


    def generateGeometry(self):
        """Generate geometry"""
        
        ## circle coordinates in x-z plane
        h2 = self._height * 0.5
        angle = np.linspace(0.0, 2.0*math.pi, self._resolution, endpoint=False)
        angle = np.append(angle, [0.0])

        ## scaling factors for vertex normals
        cosn = (self._height / np.sqrt( self._height * self._height + self._radius * self._radius ))
        sinn = (self._radius / np.sqrt( self._height * self._height + self._radius * self._radius ))

        x = np.cos(angle) * self._radius
        y = np.zeros(self._resolution+1)
        z = np.sin(angle) * self._radius

        ## normals
        nx = np.cos(angle) * cosn
        ny = sinn * np.ones(self._resolution+1)
        nz = np.sin(angle) * cosn
        
        #t = 1.0
        #delta = 1.0 / self._resolution
        vertices, normals = [], []
        #texcoords = []
        for i in list(range(self._resolution)):

            vertices.append([0.0, h2, 0.0])
            normals.append([(nx[i]+nx[i+1])*0.5, (ny[i]+ny[i+1])*0.5, (nz[i]+nz[i+1])*0.5])
            #texcoords.append([t-delta*0.5, 1])

            vertices.append([x[i], -h2, z[i]])
            normals.append([nx[i], ny[i], nz[i]])
            #texcoords.append([t, 0.0])

            vertices.append([x[i+1], -h2, z[i+1]])
            normals.append([nx[i+1], ny[i+1], nz[i+1]])
            #texcoords.append([t-delta, 0.0])

            #t -= delta

        vertices_side = np.array(vertices, dtype=np.float32)
        normals_side = np.array(normals, dtype=np.float32)
        #textcoords_side = np.array(normals, dtype=np.float32)
        self._num_vertices_side = len(vertices_side)

        ##  bottom cap
        vertices, normals = [[0.0, -h2, 0.0]], [[0.0, -1.0, 0.0]]
        for i in list(reversed(range(self._resolution+1))):
            vertices.append([x[i], -h2, z[i]])
            normals.append([0.0, -1.0, 0.0])
        vertices_bot = np.array(vertices, dtype=np.float32)
        normals_bot = np.array(normals, dtype=np.float32)
        self._num_vertices_bot = len(vertices_bot)

        self._vertices = np.concatenate((vertices_side, vertices_bot))
        self._normals = np.concatenate((normals_side, normals_bot))


    def initialize(self):
        """Creates cone geometry"""
        if self._vertices is None:
            self.generateGeometry()

        ## create object
        self.create(self._vertices, normals=self._normals)


    def render(self):
        """Render cube"""
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, self._num_vertices_side)
        GL.glDrawArrays(GL.GL_TRIANGLE_FAN, self._num_vertices_side, self._num_vertices_bot)

    