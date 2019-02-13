'''

'''

from .Structure.Constructor import Constructor
from .Cars.Cars import Cars
from .Simulator.Simulator import Simulator
from .RCMath.Algebra import *
import numpy as np
import math

class Roller_Coaster():

    ''' ---------------------- Public ---------------------- '''

    def __init__(self, renderer, ground, spc_prop, **kwargs):
        super(Roller_Coaster, self).__init__()

        self._world = renderer

        elementary_basis = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
        matrix = three_rot_matrix(elementary_basis, [math.pi/4.0, math.pi/4.0, math.pi/4.0])
        base = transform_points(matrix, elementary_basis)

        self._constructor = Constructor(self._world, ground, spc_prop)
        self._cars = Cars(self._world)

        # Cars preset
        self._cars.add_car()
        self._cars.add_car()

        self._simulator = Simulator(self._constructor, self._cars)
        self._simulating = False


    ''' ---------------------- Constructor ---------------------- '''

    def add_rail(self):
        self._constructor.add_rail()

    def remove_rail(self):
        if(not self._simulating):
            self._constructor.remove_rail()

    def update_rail(self, elevation=None, rotation=None, inclination=None,
                          length=None, model=None, type=None, resolution=None):
        self._constructor.update(elevation, rotation,
                          inclination, length, model,
                          type, resolution)

    ''' ---------------------- Cars ---------------------- '''

    def update_cars(self, model=None, type=None):
        self._cars.update_model(model, type)

    ''' ---------------------- Simulator ---------------------- '''

    def simulation_start(self):
        self._simulating = True
        self._simulator.start()

    def simulation_step(self):
        self._simulator.step()

    def simulation_stop(self):
        self._simulating = False
        self._simulator.stop()

    def update_camera(self, camera, trackball):
        if(self._simulating):
            self._simulator.update_camera(camera, trackball)

    def first_person(self, fp):
        self._simulator.update_fp(fp)
