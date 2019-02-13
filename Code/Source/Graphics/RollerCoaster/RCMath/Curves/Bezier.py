'''
This code contains the class of 3D Cubic Bezier objects

Funnctions:
    Bezier()
        Instantiates a 3D Cubic Bezier object

    create(self, points)
        Creates a 3D Cubic Bezier with the "points" in the following format:
        [p_1, p_2, p_3, p_4], where p_i is [float, float, float]
        Returns nothing

    Update(self, pontos)
        Updates the points of the 3D Cubic Bezier with the "points" in the following format:
        [p_1, p_2, p_3, p_4], where p_i is [float, float, float]
        Returns nothing

    point(self, t)
        Calculates the point of the 3D Cubic Bezier in t, where "t" is a float
        Returns float

    tangent(self, t)
        Calculates the tangent (normalized) of the 3D Cubic Bezier in t, where "t" is a float
        Returns np.array([float, float, float])
'''
import numpy as np

class Bezier():

    ''' ---------------------- Public ---------------------- '''

    def __init__(self, **kwargs):
        """Initialize actor."""
        super(Bezier, self).__init__()

        self._points = np.array([])

    def create(self, points):
        self._points = np.array(points)

    def Update(self, pontos):
        self._points = np.array(pontos)

    def point(self, t):
        t = float(t)
        return np.array([self.pointComp(t, 0), self.pointComp(t, 1), self.pointComp(t, 2)])

    def tangent(self, t):
        t = float(t)
        tangente = np.array([self.tangentComp(t, 0), self.tangentComp(t, 1), self.tangentComp(t, 2)])
        if(np.linalg.norm(tangente) != 0.0):
            return (tangente/np.linalg.norm(tangente))
        else:
            return(tangente)

    ''' ---------------------- Private ---------------------- '''

    def pointComp(self, t, i):
        return self._points[3][i]*t**3 + 3.0*self._points[2][i]*t**2*(1.0-t) + 3.0*self._points[1][i]*t*(1.0-t)**2 + self._points[0][i]*(1.0-t)**3

    def tangentComp(self, t, i):
        return 3.0*(1.0-t)**2*(self._points[1][i]-self._points[0][i]) + 6.0*(self._points[2][i]-self._points[1][i])*t*(1.0-t) + 3.0*(self._points[3][i]-self._points[2][i])*t**2
