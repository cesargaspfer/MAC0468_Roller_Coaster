import sys
import platform
import argparse
import math

from OpenGL import GL
from PyQt5 import Qt, QtCore

# A deletar
from .RCMath.Curves.Bezier import Bezier
from .RCMath.Algebra import *
from .Tools.Extruder import *
from .Structure.RailModels.Cylindrical import Cylindrical
from .Structure.Rail import Rail
from .Structure.Rail_Model import Rail_Model
from .Structure.Constructor import Constructor
import numpy as np


from .Structure.Rail_Extruder import Rail_Extruder



def test():

    # Bezier Test
    print("/-----------------------------------------------------------------------/")
    print()
    print("Testing Bezier")
    print()
    bezier = Bezier()
    bezier.create([[0.0, 0.0, 0.0], [0.0, 1.0, 0.0], [1.0, 1.0, 0.0], [1.0, 0.0, 0.0]])
    print("Bezier created with points:")
    print("   [[0.0, 0.0, 0.0], [0.0, 1.0, 0.0], [1.0, 1.0, 0.0], [1.0, 0.0, 0.0]]")
    print("point t = 0.0:   " + str(bezier.point(0.0)))
    print("point t = 0.5:   " + str(bezier.point(0.5)))
    print("point t = 1.0:   " + str(bezier.point(1.0)))
    print("tangent t = 0.0: " + str(bezier.tangent(0.0)))
    print("tangent t = 0.5: " + str(bezier.tangent(0.5)))
    print("tangent t = 1.0: " + str(bezier.tangent(1.0)))
    bezier.Update([[0.0, 0.0, 0.0], [0.0, 0.0, 1.0], [0.0, 1.0, 1.0], [0.0, 1.0, 0.0]])
    print("Bezier changed to:")
    print("   [[0.0, 0.0, 0.0], [0.0, 0.0, 1.0], [0.0, 1.0, 1.0], [0.0, 1.0, 0.0]]")
    print("point t = 0.0:   " + str(bezier.point(0.0)))
    print("point t = 0.5:   " + str(bezier.point(0.5)))
    print("point t = 1.0:   " + str(bezier.point(1.0)))
    print("tangent t = 0.0: " + str(bezier.tangent(0.0)))
    print("tangent t = 0.5: " + str(bezier.tangent(0.5)))
    print("tangent t = 1.0: " + str(bezier.tangent(1.0)))
    print()
    print("End of the Bezier test")
    print()
    print("/-----------------------------------------------------------------------/")
    print()
    print("Testing Algebra")
    print()
    print("norm of [1.0, 1.0]: " + str(normalize([1.0, 1.0])))
    print("norm of [0.0, 0.0]: " + str(normalize([0.0, 0.0])))
    print("rotation_matrix already tested")
    print("ortho_transform_matrix and transform_points testing:")
    elementary_basis = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
    other_basis = np.array([[0.0, 0.0, 1.0], [0.0, 1.0, 0.0], [-1.0, 0.0, 0.0]])
    matrix = opbt_matrix(elementary_basis, other_basis)
    print(transform_points(matrix, elementary_basis))
    print()
    print("End of the Algebra test")
    print()
    print("/-----------------------------------------------------------------------/")
    print()
    print("Testing Extruder")
    print()
    bezier.Update([[0.0, 0.0, 0.0], [0.551915024494, 0.0, 0.0], [1.0, 1.0-0.551915024494, 0.0], [1.0, 1.0, 0.0]])
    print(extrude_along(elementary_basis, elementary_basis, elementary_basis, bezier, [math.pi/2.0, 0.0, 0.0], 2)[0][2])
    print()
    print("End of the Extruder test")
    print()
    print("/-----------------------------------------------------------------------/")
    print()
    print("Testing Cylindrical")
    print()
    cil = Cylindrical()
    (points, normals) = cil.get_points(0)
    print("points:")
    print(points)
    print("Extruded:")
    (points, normals) = extrude_along(points, normals, elementary_basis, bezier, [math.pi/2.0, 0.0, 0.0], 8)
    print(points[2])
    (points, normals, textures, colors) = cil.construct(0, points, normals)
    print()
    print("End of the Cylindrical test")
    print()
    print("/-----------------------------------------------------------------------/")
    print()
    print("Testing Rail")
    print()
    '''
    rm = Rail_Model()
    rail = Rail(self._world, rm, rot_prop=[math.pi/2.0, 0.0, 0.0], spc_prop=[[0,0,0], elementary_basis, bezier, 4.0], rail_type=[0, 0, 8])
    self._world.addActor(rail)
    '''
    print()
    print("End of the Rail test")
    print()
    print("/-----------------------------------------------------------------------/")
    print()
    print("Testing Constructor")
    print()
    spc_prop = [np.array([0.0, 0.0, 1.0]), elementary_basis]
    const = Constructor(self._world, spc_prop)
    print()
    print("End of the Constructor test")
    print()
    print("/-----------------------------------------------------------------------/")
