'''
This code contains makes Algebra calculations

Funnctions:
    normalize(vec)
        Normalizes the vector
        Returns np.array

    angle_between(v1, v2)
        Calculates the angle in radians between two vectors
        Returns float

    rotation_matrix(axis, theta)
        Return the rotation matrix associated with counterclockwise rotation about
        the given axis by theta radians.
        Returns np.array Matrix

    opbt_matrix(basis_from, basis_to)
        Calculates the matrix of a orthonornal positive basis transformation
        Returns np.array

    transform_points(matrix, points)
        transform the points of the array of points given the matrix of basis transformation
        Returns np.array

    three_rot_matrix(initial_basis, angles)
        Calculates the basis transformation matrix of three rotations from the angles
        angles is np.array([elevation, rotation, inclination])
        Returns np.array

'''
import math
import numpy as np

''' ---------------------- Public ---------------------- '''

def normalize(vec):
    norm = np.linalg.norm(vec)
    if(norm == 0):
        return(np.array(vec))
    else:
        return(vec / norm)

def angle_between(v1, v2):
    theta = np.dot(v1, v2)
    if(theta > 1.0):
        return(0.0)
    elif(theta < -1.0):
        return(math.pi)
    else:
        return(math.acos(theta))

def rotation_matrix(axis, theta):
    """
    Return the rotation matrix associated with counterclockwise rotation about
    the given axis by theta radians.
    """
    axis = np.asarray(axis)
    axis_dot = np.dot(axis, axis)
    if(theta == math.pi and axis_dot == 0.0):
        return np.array([[1.0, 0.0, 0.0], [0.0, -1.0,0.0], [0.0,0.0,-1.0]])
    if(theta == 0.0 or axis_dot == 0.0):
        return np.array([[1.0, 0.0, 0.0], [0.0, 1.0,0.0], [0.0,0.0,1.0]])

    axis = axis / math.sqrt(np.dot(axis, axis))
    a = math.cos(theta / 2.0)
    b, c, d = -axis * math.sin(theta / 2.0)
    aa, bb, cc, dd = a * a, b * b, c * c, d * d
    bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
    return np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                     [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                     [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])

def opbt_matrix(basis_from, basis_to):
    f_x = np.array(basis_from[0])
    f_y = np.array(basis_from[1])

    t_x = np.array(basis_to[0])
    t_y = np.array(basis_to[1])

    # First Rotation
    ang = angle_between(f_y, t_y)
    cross = normalize(np.cross(f_y, t_y))
    matrix_1 = rotation_matrix(cross, ang)
    if(ang != 0.0):
        f_x = np.dot(matrix_1, f_x)
        f_y = np.dot(matrix_1, f_y)

    # Second Rotation
    ang = angle_between(f_x, t_x)
    cross = normalize(np.cross(f_x, t_x))
    if(np.linalg.norm(cross) == 0.0):
        matrix_2 = rotation_matrix(-t_y, ang)
    else:
        matrix_2 = rotation_matrix(cross, ang)

    matrix = np.dot(matrix_2, matrix_1)
    return(matrix)

def transform_points(matrix, points):
    new_points = []
    for i in range(len(points)):
        new_points.append(np.dot(matrix, points[i]))
    new_points = np.array(new_points)
    return(new_points)

def three_rot_matrix(initial_basis, angles):
    # Reading arguments
    ele = angles[0]
    rot = angles[1]
    inc = angles[2]

    x = initial_basis[0]
    y = initial_basis[1]
    z = initial_basis[2]

    # Calculate the three rotations,
    # the first two are global and the last is local
    matrix_1 = rotation_matrix(z, ele)
    x = transform_points(matrix_1, [x])[0]

    matrix_2 = rotation_matrix(y, rot)
    x = transform_points(matrix_2, [x])[0]

    matrix_3 = rotation_matrix(x, inc)

    # The final matrix
    matrix = np.dot(matrix_3, np.dot(matrix_2, matrix_1))
    return(matrix)

''' ---------------------- Private ---------------------- '''
