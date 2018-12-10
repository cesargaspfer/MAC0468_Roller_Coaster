import math
import numpy as np
from OpenGL import GL
from Source.Graphics.Actor import Actor

class Icosahedron(Actor):

    ## initialization
    def __init__(self, renderer,  **kwargs):
        """Initialize actor."""
        super(Icosahedron, self).__init__(renderer, **kwargs)

        self._level = kwargs.get("level", 0)
        self._radius = kwargs.get("radius", 1.0)
        self._vertices = None

        ## create actor
        self.initialize()


    def addVertex(self, v, vertices):
        """Add a vertex into the array"""
        vn = v / np.linalg.norm(v) * self._radius
        vertices += [[vn[0], vn[1], vn[2]]]
        return len(vertices)-1


    def getMiddlePoint(self, p1, p2, vertices, indexCache):
        """Returns index of point in the middle of p1 and p2"""

        ## first check if we have it already
        firstIsSmaller = p1 < p2;
        smallerIndex = p1 if p1 < p2 else p2
        greaterIndex = p2 if p1 < p2 else p1
        key = (smallerIndex << 32) + greaterIndex

        try:
            ret = indexCache[key]
            return ret
        except:
            pass

        ## not in cache, calculate it
        point1 = vertices[p1]
        point2 = vertices[p2]
        middle = ((point1[0] + point2[0]) / 2.0, (point1[1] + point2[1]) / 2.0, (point1[2] + point2[2]) / 2.0)

        ## add vertex makes sure point is on unit sphere
        index = self.addVertex(np.array(middle), vertices)

        ## store it, return index
        indexCache[key] = index

        return index

    def getTexCoords(self):
        tex = []
        for v in self._vertices:
            tex.append([
                0.5 + math.atan2(v[2], v[0])/(2*math.pi),
                0.5 - math.asin(v[1])/math.pi
            ])
        return np.array(tex, dtype=np.float32)


    def generateGeometry(self):
        """Generate vertices"""
        vertices = []
        indices = []
        middlePointIndexCache = dict()

        t = (1.0 + math.sqrt(5.0)) / 2.0

        self.addVertex(np.array((-1.0,  t,  0)), vertices)
        self.addVertex(np.array(( 1.0,  t,  0)), vertices)
        self.addVertex(np.array((-1.0, -t,  0)), vertices)
        self.addVertex(np.array(( 1.0, -t,  0)), vertices)

        self.addVertex(np.array(( 0, -1.0,  t)), vertices)
        self.addVertex(np.array(( 0,  1.0,  t)), vertices)
        self.addVertex(np.array(( 0, -1.0, -t)), vertices)
        self.addVertex(np.array(( 0,  1.0, -t)), vertices)

        self.addVertex(np.array(( t,  0, -1.0)), vertices)
        self.addVertex(np.array(( t,  0,  1.0)), vertices)
        self.addVertex(np.array((-t,  0, -1.0)), vertices)
        self.addVertex(np.array((-t,  0,  1.0)), vertices)

        ## 5 faces around point 0
        indices += [[0, 11, 5]]
        indices += [[0, 11, 5]]
        indices += [[0, 5, 1]]
        indices += [[0, 1, 7]]
        indices += [[0, 7, 10]]
        indices += [[0, 10, 11]]

        ## 5 adjacent faces
        indices += [[1, 5, 9]]
        indices += [[5, 11, 4]]
        indices += [[11, 10, 2]]
        indices += [[10, 7, 6]]
        indices += [[7, 1, 8]]

        ## 5 faces around point 3
        indices += [[3, 9, 4]]
        indices += [[3, 4, 2]]
        indices += [[3, 2, 6]]
        indices += [[3, 6, 8]]
        indices += [[3, 8, 9]]

        ## 5 adjacent faces
        indices += [[4, 9, 5]]
        indices += [[2, 4, 11]]
        indices += [[6, 2, 10]]
        indices += [[8, 6, 7]]
        indices += [[9, 8, 1]]

        ## subdivide triangles
        for i in range(self._level):

            new_indices = []

            for tri in indices:

                ## replace triangle by 4 triangles
                a = self.getMiddlePoint(tri[0], tri[1], vertices, middlePointIndexCache)
                b = self.getMiddlePoint(tri[1], tri[2], vertices, middlePointIndexCache)
                c = self.getMiddlePoint(tri[2], tri[0], vertices, middlePointIndexCache)

                new_indices += [[tri[0], a, c]]
                new_indices += [[tri[1], b, a]]
                new_indices += [[tri[2], c, b]]
                new_indices += [[a, b, c]]

            indices = new_indices

        self._vertices = np.array(vertices, dtype=np.float32)
        self._normals = np.array(vertices, dtype=np.float32)
        self._indices = np.array(indices, dtype=np.uint32)
        self._texcoords = self.getTexCoords()


    def initialize(self):
        """Creates icosahedron geometry"""
        if self._vertices is None:
            self.generateGeometry()

        self._isIcosahedron = False
        ## create object
        self.create(self._vertices,
            normals=self._normals,
            indices=self._indices,
            texcoords=self._texcoords)


    def render(self):
        """Render icosahedron"""
        GL.glDrawElements(self._render_mode, self.numberOfIndices, GL.GL_UNSIGNED_INT, None)
