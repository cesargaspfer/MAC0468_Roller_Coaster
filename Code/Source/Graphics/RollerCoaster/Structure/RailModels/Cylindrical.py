'''
This code contains the class of the object that have
the surface to extrude a Cylindrical Roller Coaster

Funnctions:
    Cylindrical()
        Instantiates the object described above

    get_points(self, type)
        Get the points to extrude according to the rail type
        Types:
            0 - Platform
            1 - Normal
            2 - Lever
            3 - Brakes
            4 - Final
        returns the points, normals, texcoords and colors respectively
        Returns (np.array, np.array, np.array, np.array)

    construct(self, type, points, normals)
        Returns the points, normals and colors to render according to the rail type
        Returns (np.array, np.array, np.array)


'''
import math
import numpy as np
from ...RCMath.Algebra import *
from PyQt5.QtGui import QVector3D

class Cylindrical():

    ''' ---------------------- Public ---------------------- '''

    def __init__(self,  **kwargs):
        """Initialize actor."""
        super(Cylindrical, self).__init__()

    def get_points(self, type):
        # Platform
        if(type == 0):
            return(self.generate_points())
        # Normal
        elif(type == 1):
            return(self.generate_points())
        # Lever
        elif(type == 2):
            return(self.generate_points())
        # Brakes
        elif(type == 3):
            return(self.generate_points())
        # Final
        elif(type == 4):
            return(self.generate_points())
        # Not Defined
        else:
            return(self.generate_points())


    def construct(self, type, points, points_normals):
        vertices = []
        normals = []
        texcoords = []
        colors = None

        for i in range(len(points)-1):
            for j in range(int(len(points[i])/3)-1):
                # Main
                self.triangulate(points, points_normals, i, j, vertices, normals, texcoords)
                # Side
                self.triangulate(points, points_normals, i, j+int(len(points[i])/3), vertices, normals, texcoords)
                self.triangulate(points, points_normals, i, j+2*int(len(points[i])/3), vertices, normals, texcoords)

        vertices = np.array(vertices, dtype=np.float32)
        normals = np.array(normals, dtype=np.float32)
        texcoords = np.array(texcoords, dtype=np.float32)
        colors = np.array(colors, dtype=np.float32)

        return((vertices, normals, texcoords, colors))


    ''' ---------------------- Private ---------------------- '''

    def generate_points(self):
        points = []
        norms = []
        resolution = 5
        R = 0.1
        ratio = 0.25

        for i in range(0, int(resolution)+1):
            point = np.array([0.0, math.cos((i/(resolution))*2.0*math.pi), math.sin((i/(resolution))*2.0*math.pi)])
            points.append(R * point)
            norms.append(point)


        offset = np.array([0.0, 0.15, 0.15])
        for i in range(0, int(resolution)+1):
            points.append(ratio * points[i] + offset)
            norms.append(norms[i])

        offset = np.array([0.0, 0.15, -0.15])
        for i in range(0, int(resolution)+1):
            points.append(ratio * points[i] + offset)
            norms.append(norms[i])


        points = np.array(points)
        norms = np.array(norms)

        return((points, norms))


    def triangulate(self, pnts, norms, i, j, vertices, normals, texcoords):
        '''
        1_1
        1_2
        2_1

        1_2
        2_2
        2_1
        '''

        vertices.append(pnts[i  ][j  ])
        vertices.append(pnts[i  ][j+1])
        vertices.append(pnts[i+1][j  ])

        vertices.append(pnts[i  ][j+1])
        vertices.append(pnts[i+1][j+1])
        vertices.append(pnts[i+1][j  ])

        normals.append(norms[i  ][j  ])
        normals.append(norms[i  ][j+1])
        normals.append(norms[i+1][j  ])

        normals.append(norms[i  ][j+1])
        normals.append(norms[i+1][j+1])
        normals.append(norms[i+1][j  ])

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


    def get_color(self, type):
        color = None
        if(type == 0):
            color = QVector3D(1.0, 0.5, 0.5)
        elif(type == 1):
            color = QVector3D(1.0, 1.0, 1.0)
        elif(type == 2):
            color = QVector3D(0.5, 0.5, 1.0)
        elif(type == 3):
            color = QVector3D(0.5, 0.5, 0.1)
        else:
            color = QVector3D(1.0, 0.1, 0.1)
        return color
