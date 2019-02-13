import math
import numpy as np
from OpenGL import GL
from Source.Graphics.Actor import Actor

class Support(Actor):

    ## initialization
    def __init__(self, renderer,  **kwargs):
        """Initialize actor."""
        super(Support, self).__init__(renderer, **kwargs)

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


    def generateGeometry(self):
        """Creates cone geometry"""

        ## circle coordinates in x-z plane
        h2 = self._height * 0.5
        angle = np.linspace(0.0, 2.0*math.pi, self._resolution, endpoint=False)
        angle = np.append(angle, [2.0*math.pi])

        ## circle in x-z plane
        x = -np.sin(angle) * self._radius
        y = np.zeros(self._resolution+1)
        z = -np.cos(angle) * self._radius

        ## normal vectors
        nx = -np.sin(angle)
        ny = np.zeros(self._resolution+1)
        nz = -np.cos(angle)

        ## top and bottom circles
        #top = np.vstack((x,y+h2,z)).reshape(3,-1).T.astype(np.float32)
        #bot = np.vstack((x,y-h2,z)).reshape(3,-1).T.astype(np.float32)

        ## top cap
        vertices, normals, texcoords = [[0.0, h2, 0.0]], [[0.0, 1.0, 0.0]], [[0.5, 0.5]]
        for i in list(range(self._resolution+1)):
            vertices.append([x[i], h2, z[i]])
            normals.append([0.0, 1.0, 0.0])
            texcoords.append([x[i]/(2*self._radius) + 0.5, z[i]/(2*self._radius) + 0.5]),
        vertices_top = np.array(vertices, dtype=np.float32)
        normals_top = np.array(normals, dtype=np.float32)
        texcoords_top = np.array(texcoords, dtype=np.float32)
        self._num_vertices_top = len(vertices_top)

        ## side
        vertices, normals, texcoords = [], [], []
        for i in list(range(self._resolution)):
            vertices.append([x[i], h2, z[i]])
            normals.append([nx[i], ny[i], nz[i]])
            texcoords.append([angle[i]/(2*math.pi), 1.0])

            vertices.append([x[i], -h2, z[i]])
            normals.append([nx[i], ny[i], nz[i]])
            texcoords.append([angle[i]/(2*math.pi), 0.0])

            vertices.append([x[i+1], h2, z[i+1]])
            normals.append([nx[i+1], ny[i+1], nz[i+1]])
            texcoords.append([angle[i+1]/(2*math.pi), 1.0])

            vertices.append([x[i], -h2, z[i]])
            normals.append([nx[i], ny[i], nz[i]])
            texcoords.append([angle[i]/(2*math.pi), 0.0])

            vertices.append([x[i+1], -h2, z[i+1]])
            normals.append([nx[i+1], ny[i+1], nz[i+1]])
            texcoords.append([angle[i+1]/(2*math.pi), 0.0])

            vertices.append([x[i+1], h2, z[i+1]])
            normals.append([nx[i+1], ny[i+1], nz[i+1]])
            texcoords.append([angle[i+1]/(2*math.pi), 1.0])

        vertices_side = np.array(vertices, dtype=np.float32)
        normals_side = np.array(normals, dtype=np.float32)
        texcoords_side = np.array(texcoords, dtype=np.float32)
        self._num_vertices_side = len(vertices_side)

        ##  bottom cap
        vertices, normals, texcoords = [[0.0, -h2, 0.0]], [[0.0, -1.0, 0.0]], [[0.5, 0.5]]
        for i in list(reversed(range(self._resolution+1))):
            vertices.append([x[i], -h2, z[i]])
            normals.append([0.0, -1.0, 0.0])
            texcoords.append([x[i]/(2*self._radius) + 0.5, z[i]/(2*self._radius) + 0.5])

        vertices_bot = np.array(vertices, dtype=np.float32)
        normals_bot = np.array(normals, dtype=np.float32)
        texcoords_bot = np.array(texcoords, dtype=np.float32)
        self._num_vertices_bot = len(vertices_bot)

        self._vertices = np.concatenate((vertices_top, vertices_side, vertices_bot))
        self._normals = np.concatenate((normals_top, normals_side, normals_bot))
        self._texcoords = np.concatenate((texcoords_top, texcoords_side, texcoords_bot))



    def initialize(self):
        """Creates cone geometry"""
        if self._vertices is None:
            self.generateGeometry()

        ## create object
        self.create(self._vertices, normals=self._normals, texcoords=self._texcoords)


    def render(self):
        """Render cube"""
        GL.glDrawArrays(GL.GL_TRIANGLE_FAN, 0, self._num_vertices_top)
        GL.glDrawArrays(GL.GL_TRIANGLES, self._num_vertices_top, self._num_vertices_side)
        GL.glDrawArrays(GL.GL_TRIANGLE_FAN, self._num_vertices_top + self._num_vertices_side, self._num_vertices_bot)
