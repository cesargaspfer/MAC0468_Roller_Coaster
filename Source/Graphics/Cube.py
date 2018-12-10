import numpy as np
from PyQt5.QtGui import QVector3D

from OpenGL import GL
from Source.Graphics.Actor import Actor

class Cube(Actor):

    ## initialization
    def __init__(self, scene,  **kwargs):
        """Initialize actor."""
        super(Cube, self).__init__(scene, mode=Actor.RenderMode.Triangles, **kwargs)

        self._vertices = None

        ## create actor
        self.initialize()


    @classmethod
    def isSelectable(self):
        """Returns true if actor is selectable"""
        return True


    def generateGeometry(self):
        """Generate geometry"""
        self._vertices = np.array([
            -0.5, -0.5, -0.5,
            0.5, -0.5, -0.5,
            0.5,  0.5, -0.5,
            0.5,  0.5, -0.5,
            -0.5,  0.5, -0.5,
            -0.5, -0.5, -0.5,

            -0.5, -0.5,  0.5,
            0.5, -0.5,  0.5,
            0.5,  0.5,  0.5,
            0.5,  0.5,  0.5,
            -0.5,  0.5,  0.5,
            -0.5, -0.5,  0.5,

            -0.5,  0.5,  0.5,
            -0.5,  0.5, -0.5,
            -0.5, -0.5, -0.5,
            -0.5, -0.5, -0.5,
            -0.5, -0.5,  0.5,
            -0.5,  0.5,  0.5,

            0.5,  0.5,  0.5,
            0.5,  0.5, -0.5,
            0.5, -0.5, -0.5,
            0.5, -0.5, -0.5,
            0.5, -0.5,  0.5,
            0.5,  0.5,  0.5,

            -0.5, -0.5, -0.5,
            0.5, -0.5, -0.5,
            0.5, -0.5,  0.5,
            0.5, -0.5,  0.5,
            -0.5, -0.5,  0.5,
            -0.5, -0.5, -0.5,

            -0.5,  0.5, -0.5,
            0.5,  0.5, -0.5,
            0.5,  0.5,  0.5,
            0.5,  0.5,  0.5,
            -0.5,  0.5,  0.5,
            -0.5,  0.5, -0.5], dtype=np.float32)

        self._normals = np.array([
            0.0,  0.0, -1.0,
            0.0,  0.0, -1.0,
            0.0,  0.0, -1.0,
            0.0,  0.0, -1.0,
            0.0,  0.0, -1.0,
            0.0,  0.0, -1.0,

            0.0,  0.0,  1.0,
            0.0,  0.0,  1.0,
            0.0,  0.0,  1.0,
            0.0,  0.0,  1.0,
            0.0,  0.0,  1.0,
            0.0,  0.0,  1.0,

            -1.0,  0.0,  0.0,
            -1.0,  0.0,  0.0,
            -1.0,  0.0,  0.0,
            -1.0,  0.0,  0.0,
            -1.0,  0.0,  0.0,
            -1.0,  0.0,  0.0,

            1.0,  0.0,  0.0,
            1.0,  0.0,  0.0,
            1.0,  0.0,  0.0,
            1.0,  0.0,  0.0,
            1.0,  0.0,  0.0,
            1.0,  0.0,  0.0,

            0.0, -1.0,  0.0,
            0.0, -1.0,  0.0,
            0.0, -1.0,  0.0,
            0.0, -1.0,  0.0,
            0.0, -1.0,  0.0,
            0.0, -1.0,  0.0,

            0.0,  1.0,  0.0,
            0.0,  1.0,  0.0,
            0.0,  1.0,  0.0,
            0.0,  1.0,  0.0,
            0.0,  1.0,  0.0,
            0.0,  1.0,  0.0], dtype=np.float32)

        self._texcoords = np.array([
            0.0, 0.0,
            1.0, 0.0,
            1.0,  1.0,
            1.0,  1.0,
            0.0,  1.0,
            0.0, 0.0,

            0.0, 0.0,
            1.0, 0.0,
            1.0,  1.0,
            1.0,  1.0,
            0.0,  1.0,
            0.0, 0.0,

            0.0, 0.0,
            1.0, 0.0,
            1.0,  1.0,
            1.0,  1.0,
            0.0,  1.0,
            0.0, 0.0,

            0.0, 0.0,
            1.0, 0.0,
            1.0,  1.0,
            1.0,  1.0,
            0.0,  1.0,
            0.0, 0.0,

            0.0, 0.0,
            1.0, 0.0,
            1.0,  1.0,
            1.0,  1.0,
            0.0,  1.0,
            0.0, 0.0,

            0.0, 0.0,
            1.0, 0.0,
            1.0,  1.0,
            1.0,  1.0,
            0.0,  1.0,
            0.0, 0.0, ], dtype=np.float32)


    def initialize(self):
        """Creates cube's geometry"""
        if self._vertices is None:
            self.generateGeometry()

        ## create object
        self.create(self._vertices, normals=self._normals, texcoords=self._texcoords)


    def render(self):
        """Render cube"""
        GL.glDrawArrays(self._render_mode, 0, int(len(self._vertices)/3))
