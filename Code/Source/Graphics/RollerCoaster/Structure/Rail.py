'''
This code is the Rail class, contains the rail properties and fills the OpenGL Buffer

Funnctions:
    Rail(self, renderer, rail_model, rot_prop = None, spc_prop = None, typ_prop = None)
        Instantiates a Rail object
        Arguments:
            renderer is the render of the scene
            rail_model is the object that contains the rail models
            rot_prop = [elevation, rotation, inclination]
            spc_prop = [initial_pos, basis, curve, length]
            typ_prop = [model, type, resolution]
        Returns nothing

    isSelectable(self)
        Returns true if actor is selectable
        Returns bool

    update(self, rot_prop = None, spc_prop = None, typ_prop = None)
        Updates the rail
        Arguments:
            rot_prop = [elevation, rotation, inclination]
            spc_prop = [initial_pos, basis, curve, length]
            typ_prop = [model, type, resolution, rail, rail_model]
        Returns nothing

    get_basis_in(self, pos)
        Get the basis of the rail in the local position passed in the argument
        Returns np.array
'''
import numpy as np
from OpenGL import GL
from Source.Graphics.Actor import Actor
from PyQt5.QtGui import QMatrix4x4, QVector3D, QVector4D, QOpenGLShader, QOpenGLShaderProgram, QOpenGLBuffer, QOpenGLVertexArrayObject
from Source.Graphics.Material import Material

from ..Tools.Extruder import *
from ..RCMath.Algebra import three_rot_matrix, transform_points

class Rail(Actor):

    ''' ---------------------- Public ---------------------- '''

    def __init__(self, renderer, rail_model, **kwargs):
        """Initialize actor"""
        super(Rail, self).__init__(renderer, **kwargs)

        """ --------- Rotations Properties --------- """

        rot_prop = kwargs.get("rot_prop", [0.0, 0.0, 0.0])

        self._elevation   = rot_prop[0]
        self._rotation    = rot_prop[1]
        self._inclination = rot_prop[2]

        """ --------- Space Properties --------- """

        spc_prop = kwargs.get("spc_prop", [None, None, None, 4.0])

        self._initial_pos = spc_prop[0]
        self._basis       = spc_prop[1]
        self._curve       = spc_prop[2]
        self._length      = spc_prop[3]

        """ --------- Rail Properties --------- """

        typ_prop = kwargs.get("typ_prop", [0, 0, int(self._length)*2])

        self._model      = typ_prop[0]
        self._type       = typ_prop[1]
        self._resolution = typ_prop[2]

        self._rail       = None
        self._rail_model = rail_model

        """ --------- Model Properties (Private) --------- """

        self._vertices_to_render = 0
        self._created = False

        self.update_rail()


    @classmethod
    def isSelectable(self):
        """Returns true if actor is selectable"""
        return True


    def update_rail(self, rot_prop = None, spc_prop = None, typ_prop = None):

        if(rot_prop != None):
            self._elevation   = rot_prop[0]
            self._rotation    = rot_prop[1]
            self._inclination = rot_prop[2]

        if(spc_prop != None):
            self._initial_pos = spc_prop[0]
            self._basis       = spc_prop[1]
            self._curve       = spc_prop[2]
            self._length      = spc_prop[3]

        if(typ_prop != None):
            self._model      = typ_prop[0]
            self._type       = typ_prop[1]
            self._resolution = typ_prop[2]

        # Getting the surface to extrude
        self._rail = self._rail_model.get_rail(self._model)
        (points, normals) = self._rail.get_points(self._type)

        # Extruding
        rot_prop = [self._elevation, self._rotation, self._inclination]
        (points, normals) = extrude_along(points, normals, self._basis,
                                          self._curve, rot_prop, self._resolution)

        # Constructing (triangulating) the points
        (points, normals, textures, colors) = self._rail.construct(self._type, points, normals)

        # Passing data to buffer
        self._vertices_to_render = len(points)
        if(self._created):
            self.updateBuffer(vertices=points,
                              normals=normals,
                              texcoords=textures,
                              colors=colors,
                              usage=QOpenGLBuffer.DynamicCopy)
        else:
            self.create(points,
                        normals=normals,
                        texcoords=textures,
                        colors=colors)
            self._created = True
        self.update(material=Material(cbase=self._rail.get_color(self._type)))

    def position_in_rail(self, pos):
        if(pos >= self._length):
            return(-1)
        if(pos < 0):
            return(-2)
        t = pos/float(self._length)
        return(self._curve.point(t))

    def get_rot_basis_in(self, pos):
        t = pos/float(self._length)
        ele = t*self._elevation
        rot = t*self._rotation
        inc = t*self._inclination
        angles = np.array([ele, rot, inc])
        elementary_basis = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])

        rot_matrix = three_rot_matrix(self._basis, angles)
        final_matrix = transform_points(self._basis, rot_matrix)
        return(final_matrix)

    def get_basis_in(self, pos):
        t = pos/float(self._length)
        ele = t*self._elevation
        rot = t*self._rotation
        inc = t*self._inclination
        angles = np.array([ele, rot, inc])
        elementary_basis = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])

        rot_matrix = three_rot_matrix(self._basis, angles)
        final_matrix = transform_points(rot_matrix, self._basis)
        return(final_matrix)

    def tangent(self, pos):
        t = pos/float(self._length)
        return(self._curve.tangent(t))
        
    def render(self):
        """Render Rail"""
        GL.glDrawArrays(self._render_mode, 0, self._vertices_to_render)


    ''' ---------------------- Private ---------------------- '''
