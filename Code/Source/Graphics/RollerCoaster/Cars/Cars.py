'''

'''
import numpy as np
from .Car_Model import Car_Model
from .Car import Car

class Cars():

    ''' ---------------------- Public ---------------------- '''

    def __init__(self, renderer, **kwargs):
        super(Cars, self).__init__()

        """ --------- Car Properties --------- """

        self._renderer = renderer
        self._cars     = []

        """ --------- Model Properties --------- """

        model_prop = kwargs.get("model_prop", [0, 0])
        self._model = model_prop[0]
        self._type  = model_prop[1]

        self._car_model = Car_Model()

    def add_car(self):
        car = Car(self._renderer, self._car_model, typ_prop=[self._model, self._type])
        self._cars.append(car)
        self._renderer.addActor(car)
        car.should_be_rendered = False

    def update_model(self, model, type):
        for i in range(0, len(self._cars)):
            self._cars[i].update_model(model, type)

    def first_car(self):
        return(self._cars[0])

    def get_cars(self):
        return(self._cars)

    ''' ---------------------- Private ---------------------- '''
