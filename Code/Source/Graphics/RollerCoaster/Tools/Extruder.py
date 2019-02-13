'''
This code makes extrudes

Funnctions:
    extrude_along(points, normals, initial_basis, curve, angles, resolution)
        Calculates the extruded points and normals of "points" and normals respectively,
        along the curves and according to the angles. The resolution is the number of
        divisions that the extrude will have.
        Returns (points, normals)

'''
import numpy as np
from ..RCMath.Algebra import *

''' ---------------------- Public ---------------------- '''

def extrude_along(points, normals, initial_basis, curve, angles, resolution):

    # transform points to initial_basis
    elementary_basis = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
    initial_transf_matrix = opbt_matrix(elementary_basis, initial_basis)
    new_points = transform_points(initial_transf_matrix, points)
    new_normals = transform_points(initial_transf_matrix, normals)

    extruded_points = []
    extruded_offsets = []
    extruded_normals = []

    # Extrusion
    for i in range(0, resolution + 1):
        t = float(i) / float(resolution)

        # Calculete the rotation matrix
        angles = np.array(angles)
        rot_matrix = three_rot_matrix(initial_basis, t * angles)

        # Transform
        extruded_points.append(transform_points(rot_matrix, new_points))
        extruded_normals.append(transform_points(rot_matrix, new_normals))

        # Offset the points according to the curve
        offset = curve.point(t)
        for j in range(len(extruded_points[i])):
            extruded_points[i][j] += offset

    return((extruded_points, extruded_normals))

''' ---------------------- Private ---------------------- '''
