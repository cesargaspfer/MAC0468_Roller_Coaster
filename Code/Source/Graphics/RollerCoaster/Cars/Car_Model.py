'''
This code contains class of the object that contains all car types

Funnctions:
    Car_Model()
        Instantiates the object described above

    get_car(self, type)
        Get the object associated with the car model required
        Returns object

'''
from .CarModels.Cubic import Cubic

class Car_Model():

    def __init__(self, **kwargs):
        """Initialize actor."""
        super(Car_Model, self).__init__()

        self._models = [Cubic()]

    def get_rail(self, type):
        return(self._models[type])
