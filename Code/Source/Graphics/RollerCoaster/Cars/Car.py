'''
This code is the Car class, contains the car properties and fills the OpenGL Buffer

Funnctions:
    Car(self, renderer, car_model, typ_prop = None)
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

    update_model(self, model, type)
        Updates the rail
        Arguments:
            rot_prop = [elevation, rotation, inclination]
            spc_prop = [initial_pos, basis, curve, length]
            typ_prop = [model, type, resolution, rail, rail_model]
        Returns nothing
'''
import numpy as np
from OpenGL import GL
from Source.Graphics.Actor import Actor
from PyQt5.QtGui import QMatrix4x4, QVector3D, QVector4D, QOpenGLShader, QOpenGLShaderProgram, QOpenGLBuffer, QOpenGLVertexArrayObject


class Car(Actor):

    ''' ---------------------- Public ---------------------- '''

    def __init__(self, renderer, car_model, **kwargs):
        """Initialize actor"""
        super(Car, self).__init__(renderer, **kwargs)

        """ --------- Model Properties --------- """

        typ_prop = kwargs.get("typ_prop", [0, 0])

        self._model   = typ_prop[0]
        self._type    = typ_prop[1]


        self._car       = None
        self._car_model = car_model

        """ --------- Model Properties (Private) --------- """

        self._vertices_to_render = 0
        self._created = False

        self.update_model(self._model, self._type)


    @classmethod
    def isSelectable(self):
        """Returns true if actor is selectable"""
        return True

    def update_model(self, model, type):

        # Updating data
        self._model = model
        self._type  = type

        # Getting the model
        self._car = self._car_model.get_rail(self._model)
        (points, normals, textures, colors) = self._car.get_points(self._type)

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

    def render(self):
        """Render Rail"""
        GL.glDrawArrays(self._render_mode, 0, self._vertices_to_render)
