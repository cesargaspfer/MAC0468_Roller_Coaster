'''
This code is the Constructor class, contains the functions to construct the roller coaster

Funnctions:
    Constructor(renderer, spc_prop, model_prop = [0.0, 0.0, 0.0, 4.0],
                model_prop = [0, 0, length*2])
        Instantiates the Constructor object
            rail_prop  = [elevation, rotation, inclination, length]
            model_prop = [model, type, resolution]
            spc_prop   = [initial position, initial basis]
        Returns nothing

    add_rail(self)
        Constructs a new rail
        Returns nothing

    update(self, elevation=None, rotation=None, inclination=None,
           length=None, model=None, type=None, resolution=None)
        Makes an elementary update of the argument passed
        Returns nothing

    get_rails(self)
        Returns the array of rays
        Returns array

'''
import numpy as np
from PyQt5.QtGui import QVector3D

from .Rail_Model import Rail_Model
from .Rail import Rail
from ..RCMath.Imaginary_Sphere import *
from .Support import Support

class Constructor():

    ''' ---------------------- Public ---------------------- '''

    def __init__(self, renderer, ground, spc_prop, **kwargs):
        super(Constructor, self).__init__()

        """ --------- Rail Properties --------- """

        rail_prop = kwargs.get("rail_prop", [0.0, 0.0, 0.0, 4.0])

        self._elevation   = rail_prop[0]
        self._rotation    = rail_prop[1]
        self._inclination = rail_prop[2]
        self._length      = rail_prop[3]

        """ --------- Model Properties --------- """

        model_prop = kwargs.get("model_prop", [0, 0, int(self._length)*2])

        self._model      = model_prop[0]
        self._type       = model_prop[1]
        self._resolution = model_prop[2]

        self._rail_model = Rail_Model()

        """ --------- Space Properties --------- """

        self._initial_pos   = spc_prop[0]
        self._initial_basis = spc_prop[1]

        """ --------- Construtor Properties --------- """

        self._renderer       = renderer
        self._rails          = []
        self._supports       = []
        self._rail           = None
        self._position       = self._initial_pos
        self._basis          = self._initial_basis
        self._final_position = self._initial_pos
        self._final_basis    = self._initial_basis
        self._ground         = ground

        # Create first rail segment
        self.add_rail()

    def add_rail(self):
        self._position = self._final_position
        self._basis    = self._final_basis

        space_prop = [self._position, self._basis]
        rail_prop  = [self._elevation, self._rotation, self._inclination, self._length]
        (curve, final_basis, final_position) = imaginary_sphere(space_prop, rail_prop)

        self._final_position = final_position
        self._final_basis    = final_basis

        rot_prop = [self._elevation, self._rotation, self._inclination]
        spc_prop = [self._position, self._basis, curve, self._length]
        typ_prop = [self._model, self._type, self._resolution]

        self._rail = Rail(self._renderer, self._rail_model,
                          rot_prop = rot_prop,
                          spc_prop = spc_prop,
                          typ_prop = typ_prop)
        self._rails.append(self._rail)
        self._renderer.addActor(self._rail)

        self.add_support()

    def remove_rail(self):
        if(len(self._rails) <= 1):
            return

        old_rail = self._rails.pop()
        self._rail = self._rails[-1]

        self._position = self._rail._initial_pos
        self._basis    = self._rail._basis

        self._final_position = old_rail._initial_pos
        self._final_basis    = old_rail._basis

        self._renderer.removeActor(old_rail)

        support = self._supports.pop()
        if(support != None):
            self._renderer.removeActor(support)

        self.update()

    def update(self, elevation=None, rotation=None, inclination=None,
               length=None, model=None, type=None, resolution=None):

        if(elevation != None):
            self._elevation = elevation
        if(rotation != None):
            self._rotation = rotation
        if(inclination != None):
            self._inclination = inclination
        if(length != None):
            self._length = length
        if(model != None):
            self._model = model
        if(type != None):
            self._type = type
        if(resolution != None):
            self._resolution = resolution

        space_prop = [self._position, self._basis]
        rail_prop  = [self._elevation, self._rotation, self._inclination, self._length]

        (curve, final_basis, final_position) = imaginary_sphere(space_prop, rail_prop)

        self._final_position  = final_position
        self._final_basis     = final_basis

        rot_prop = [self._elevation, self._rotation, self._inclination]
        spc_prop = [self._position, self._basis, curve, self._length]
        typ_prop = [self._model, self._type, self._resolution]

        self._rail.update_rail(rot_prop = rot_prop, spc_prop = spc_prop, typ_prop = typ_prop)

    def get_rails(self):
        return(self._rails)

    ''' ---------------------- Private ---------------------- '''

    def add_support(self):
        tg = self._basis[0]
        up = self._basis[1]

        if(np.dot(up, [0.0, 1.0, 0.0]) < 0.0):
            self._supports.append(None)
        else:
            upper_pos = self._position
            lower_y = self._ground.height(upper_pos[0], upper_pos[2]) - 0.2
            center_y = (upper_pos[1] + lower_y)*0.5
            height = upper_pos[1] - lower_y
            support = Support(self._renderer, resolution=4, radius=0.05, height=height)
            support._transform.translate(QVector3D(upper_pos[0], center_y, upper_pos[2]))
            self._renderer.addActor(support)
            self._supports.append(support)
