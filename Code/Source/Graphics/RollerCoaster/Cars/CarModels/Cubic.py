'''
This code contains the class of the object that have
the model of the cubic cars

Funnctions:
    Cubic()
        Instantiates the object described above

    get_points(self, type)
        Get the points of the cubic car according to the car type
        Types:
            0 - First
            1 - Middle
            2 - Last
        returns the points, normals, texcoords and colors respectively
        Returns (np.array, np.array, np.array, np.array)

'''
import numpy as np
from PyQt5.QtGui import QVector3D

from OpenGL import GL
from Source.Graphics.Actor import Actor

class Cubic():

    ## initialization
    def __init__(self,  **kwargs):
        """Initialize actor."""
        super(Cubic, self).__init__()

    def get_points(self, type):
        # First
        if(type == 0):
            return(self.generate_points())
        # Middle
        if(type == 1):
            return(self.generate_points())
        # Last
        if(type == 2):
            return(self.generate_points())

    def generate_points(self):
        """Generate geometry"""
        vertices = np.array([
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

        for i in range(int(len(vertices)/3)):
            # X
            vertices[3*i+0] *= 0.5
            # Y
            vertices[3*i+1] *= 0.3
            vertices[3*i+1] += 0.3
            # Z
            vertices[3*i+2] *= 0.3



        normals = np.array([
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

        texcoords = np.array([
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

        colors = []
        for i in range(int(len(vertices))):
            colors.append(0.2)
            colors.append(0.2)
            colors.append(0.8)
        colors = np.array(colors, dtype=np.float32)

        return((vertices, normals, texcoords, colors))
