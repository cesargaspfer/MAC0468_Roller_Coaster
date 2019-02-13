'''
This code calculates the imaginary sphere to define
the curve and position of the rail

Funnctions:
    imaginary_sphere(space_prop, rail_prop)
        Calculates the imaginary sphere and returns (curve, final_basis, final_point)
            space_prop = [position, basis]
            rail_prop  = [elevation, rotation, inclination, length]
        Returns (object, np.array, np.array)

'''
import math
import numpy as np
from .Curves.Bezier import Bezier
from .Algebra import *

''' ---------------------- Public ---------------------- '''

def imaginary_sphere(space_prop, rail_prop):

    # Reads the arguments
    position =  np.array(space_prop[0])
    basis     = space_prop[1]

    elevation =   rail_prop[0]
    rotation =    rail_prop[1]
    inclination = rail_prop[2]
    length =      rail_prop[3]

    # Calculates the rotation matrix to the final segment basis
    rot_matrix = three_rot_matrix(basis, rail_prop)

    # Calculates the radius of the imaginary sphere
    vec_1 = basis[0]
    vec_2 = np.dot(rot_matrix, basis[0])

    radius = length
    angle = angle_between(vec_1, vec_2)
    if(angle < -0.01 or angle > 0.01):
        distance = np.linalg.norm(vec_1 + vec_2)
        radius /= 2*(distance*(angle/(2*math.sin(0.5*angle))))
    else:
        radius /= 4.0

    # Calculates the final basis
    final_basis = transform_points(rot_matrix, basis)

    # Calculates the Bezier points and curve
    bezier_points = np.array([None, None, None, None])

    bezier_points[0] = position
    bezier_points[1] = position + approximate(radius, vec_1)

    bezier_points[3] = position + radius * vec_1 + radius * vec_2
    bezier_points[2] = bezier_points[3] - approximate(radius, vec_2)

    curve = Bezier()
    curve.Update(bezier_points)

    final_point = bezier_points[3]

    return((curve, final_basis, final_point))


''' ---------------------- Private ---------------------- '''

def approximate(radius, vec):
    return(0.551915024494*radius*vec)
