from PyQt5.QtCore import QObject
from PyQt5.QtGui import QVector3D, QVector4D

##  Base class for light properties.
class Light(QObject):

    ## initialization
    def __init__(self, **kwargs):
        """Initialize actor."""
        super(Light, self).__init__()

        self._headlight = kwargs.get("headlight", True)
        self._position = kwargs.get("position", QVector4D(2.0, 2.0, 2.0, 1.0))
        self._ambientColor = kwargs.get("ambient", QVector3D(0.5, 0.5, 0.5))
        self._diffuseColor = kwargs.get("diffuse", QVector3D(1.0, 1.0, 1.0))
        self._specularColor = kwargs.get("specular", QVector3D(1.0, 1.0, 1.0))
        self._attenuation = kwargs.get("attenuation", QVector3D(1.0, 0.02, 0.002))
        self._directional = kwargs.get("directional", False)
        self._color  = kwargs.get("color", QVector3D(0.5, 0.5, 0.5))
        self._lradious = float(kwargs.get("lradious", 0.0))
        self._aconst   = float(kwargs.get("aconst", 0.06))
        self._alinear  = float(kwargs.get("alinear", 0.01))
        self._aquad    = float(kwargs.get("aquad", 0.0))
        self._hemispheric = kwargs.get("hemispheric", False)
        self._csky = kwargs.get("csky", QVector3D(0.0, 0.0, 1.0))
        self._cground = kwargs.get("cground", QVector3D(0.0, 1.0, 0.0))

    @property
    def csky(self):
        return self._csky

    @property
    def cground(self):
        return self._cground

    @property
    def lradious(self):
        return self._lradious

    @property
    def aconst(self):
        return self._aconst

    @property
    def alinear(self):
        return self._alinear

    @property
    def aquad(self):
        return self._aquad

    @property
    def color(self):
        return self._color

    @property
    def hemispheric(self):
        return self._hemispheric

    @property
    def headlight(self):
        """Returns true if a headlight"""
        return self._headlight


    def setHeadLight(self, headlight):
        """Sets headlight on/off"""
        self._headlight = headlight

    @property
    def directional(self):
        """Returns true if this is a directional light"""
        return self._directional


    def setDirectional(self, directional):
        """Sets whether this is directoinal light"""
        self._directional = directional


    @property
    def position(self):
        """The position of this light in space"""
        return QVector4D(self._position[0], self._position[1], self._position[2], 1.0 - float(self._directional))


    @property
    def ambientColor(self):
        """The ambient color of this light"""
        return self._ambientColor


    @property
    def diffuseColor(self):
        """The diffusive color of this light"""
        return self._diffuseColor


    @property
    def specularColor(self):
        """The specular color of this light"""
        return self._specularColor


    @property
    def attenuation(self):
        """The quadratic, linear, and constant attenuation light factors"""
        return self._attenuation
