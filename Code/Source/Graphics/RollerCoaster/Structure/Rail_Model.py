'''
This code contains class of the object that contains all rail types

Funnctions:
    Rail_Model()
        Instantiates the object described above

    get_rail(self, type)
        Get the object associated with the rail model required
        Returns object

'''
from .RailModels.Cylindrical import Cylindrical

class Rail_Model():

    def __init__(self, **kwargs):
        """Initialize actor."""
        super(Rail_Model, self).__init__()

        self._models = [Cylindrical()]

    def get_rail(self, type):
        return(self._models[type])
