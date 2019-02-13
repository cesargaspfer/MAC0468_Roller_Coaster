from PyQt5.QtCore import QObject
from PyQt5.QtGui import QVector3D


##  Base class for material properties.
class Material(QObject):

    std_roughness =  0.2
    std_metallic = 0.0
    std_specular_color = QVector3D(1.0, 1.0, 1.0)
    std_cbase = QVector3D(1.0, 1.0, 1.0)
    std_spike = False
    std_spike_h = 0.3
    std_spike_w = 0.1
    ## initialization
    def __init__(self, **kwargs):
        """Initialize material."""
        super(Material, self).__init__()

        self._emissionColor = kwargs.get("emission", QVector3D(0.0, 0.0, 0.0))
        self._ambientColor = kwargs.get("ambient", QVector3D(0.2, 0.2, 0.2))
        self._diffuseColor = kwargs.get("diffuse", QVector3D(0.8, 0.8, 0.8))
        self._specularColor = kwargs.get("specular", Material.std_specular_color)
        self._shininess = float(kwargs.get("shininess", 12.0))
        self._roughness = float(kwargs.get("roughness", Material.std_roughness))
        self._metallic  = float(kwargs.get("metallic", Material.std_metallic))
        self._cbase     = kwargs.get("cbase", Material.std_cbase)
        self._spike = kwargs.get("spike", Material.std_spike)
        self._spike_h = float(kwargs.get("spike_h", Material.std_spike_h))
        self._spike_w = float(kwargs.get("spike_w", Material.std_spike_w))

    @property
    def roughness(self):
        return self._roughness

    @property
    def metallic(self):
        return self._metallic

    @property
    def cbase(self):
        return self._cbase

    @property
    def emissionColor(self):
        """The emission color of this material"""
        return self._emissionColor


    @emissionColor.setter
    def emissionColor(self, value):
        self._emissionColor = value


    @property
    def ambientColor(self):
        """The ambient color of this material"""
        return self._ambientColor


    @ambientColor.setter
    def ambientColor(self, value):
        self._ambientColor = value


    @property
    def diffuseColor(self):
        """The diffusive color of this material"""
        return self._diffuseColor


    @diffuseColor.setter
    def diffuseColor(self, value):
        self._diffuseColor = value


    @property
    def specularColor(self):
        """The specular color of this material"""
        return self._specularColor


    @specularColor.setter
    def specularColor(self, value):
        self._specularColor = value


    @property
    def shininess(self):
        """The shininess factor of this material"""
        return self._shininess


    @shininess.setter
    def shininess(self, value):
        self._shininess = float(value)


    @property
    def spike(self):
        """The shininess factor of this material"""
        return self._spike


    @spike.setter
    def spike(self, value):
        self._spike = float(value)


    @property
    def spike_h(self):
        """The shininess factor of this material"""
        return self._spike_h


    @spike_h.setter
    def spike_h(self, value):
        self._spike_h = float(value)

    @property
    def spike_w(self):
        """The shininess factor of this material"""
        return self._spike_w


    @spike_w.setter
    def spike_w(self, value):
        self._spike_w = float(value)



    @classmethod
    def brass(cls):
        """Return brass material"""
        return Material(
            ambient=QVector3D(0.329412, 0.223529, 0.027451),
            diffuse=QVector3D(0.780392, 0.568627, 0.113725),
            specular=QVector3D(0.992157, 0.941176, 0.807843),
            shininess=27.89743616)


    @classmethod
    def bronze(cls):
        """Return bronze material"""
        return Material(
            ambient=QVector3D(0.2125, 0.1275, 0.054),
            diffuse=QVector3D(0.714, 0.4284, 0.18144),
            specular=QVector3D(0.393548, 0.271906, 0.166721),
            shininess=25.6)


    @classmethod
    def polishedBronze(cls):
        """Return polished bronze material"""
        return Material(
            ambient=QVector3D(0.25, 0.148, 0.06475),
            diffuse=QVector3D(0.4, 0.2368, 0.1036),
            specular=QVector3D(0.774597, 0.458561, 0.200621),
            shininess=76.8)


    @classmethod
    def chrome(cls):
        """Return chrome material"""
        return Material(
            ambient=QVector3D(0.25, 0.25, 0.25),
            diffuse=QVector3D(0.4, 0.4, 0.4),
            specular=QVector3D(0.774597, 0.774597, 0.774597),
            shininess=76.8)


    @classmethod
    def copper(cls):
        """Return copper material"""
        return Material(
            ambient=QVector3D(0.19125, 0.0735, 0.0225),
            diffuse=QVector3D(0.7038, 0.27048, 0.0828),
            specular=QVector3D(0.256777, 0.137622, 0.086014),
            shininess=12.8)


    @classmethod
    def polishedCopper(cls):
        """Return polished copper material"""
        return Material(
            ambient=QVector3D(0.2295, 0.08825, 0.0275),
            diffuse=QVector3D(0.5508, 0.2118, 0.066),
            specular=QVector3D(0.580594, 0.223257, 0.0695701),
            shininess=51.2)


    @classmethod
    def plasticCyan(cls):
        """Return cyan plastic material"""
        return Material(
            ambient=QVector3D(0.0, 0.0, 0.0),
            diffuse=QVector3D(0.1, 0.35, 0.1),
            specular=QVector3D(0.45, 0.55, 0.45),
            shininess=32.0)


    @classmethod
    def emerald(cls):
        """Return emerald material"""
        return Material(
            ambient=QVector3D(0.0215, 0.1745, 0.0215),
            diffuse=QVector3D(0.07568, 0.61424, 0.07568),
            specular=QVector3D(0.633, 0.727811, 0.633),
            shininess=76.8)


    @classmethod
    def gold(cls):
        """Return gold material"""
        return Material(
            ambient=QVector3D(0.24725, 0.1995, 0.0745),
            diffuse=QVector3D(0.75164, 0.60648, 0.22648),
            specular=QVector3D(0.628281, 0.555802, 0.366065),
            shininess=51.2)


    @classmethod
    def polishedGold(cls):
        """Return polished gold material"""
        return Material(
            ambient=QVector3D(0.24725, 0.2245, 0.0645),
            diffuse=QVector3D(0.34615, 0.3143, 0.0903),
            specular=QVector3D(0.797357, 0.723991, 0.208006),
            shininess=83.2)


    @classmethod
    def jade(cls):
        """Return jade material"""
        return Material(
            ambient=QVector3D(0.135, 0.2225, 0.1575),
            diffuse=QVector3D(0.54, 0.89, 0.63),
            specular=QVector3D(0.316228, 0.316228, 0.316228),
            shininess=12.8)


    @classmethod
    def obsidian(cls):
        """Return obsidian material"""
        return Material(
            ambient=QVector3D(0.05375, 0.05, 0.06625),
            diffuse=QVector3D(0.18275, 0.17, 0.22525),
            specular=QVector3D(0.332741, 0.328634, 0.346435),
            shininess=38.4)


    @classmethod
    def pearl(cls):
        """Return pearl material"""
        return Material(
            ambient=QVector3D(0.25, 0.20725, 0.20725),
            diffuse=QVector3D(1, 0.829, 0.829),
            specular=QVector3D(0.296648, 0.296648, 0.296648),
            shininess=11.264)


    @classmethod
    def plasticRed(cls):
        """Return red plastic material"""
        return Material(
            ambient=QVector3D(0.0, 0.0, 0.0),
            diffuse=QVector3D(0.5, 0.0, 0.0),
            specular=QVector3D(0.7, 0.6, 0.6),
            shininess=32)


    @classmethod
    def ruby(cls):
        """Return ruby material"""
        return Material(
            ambient=QVector3D(0.1745, 0.01175, 0.01175),
            diffuse=QVector3D(0.61424, 0.04136, 0.04136),
            specular=QVector3D(0.727811, 0.626959, 0.626959),
            shininess=76.8)


    @classmethod
    def silver(cls):
        """Return silver material"""
        return Material(
            ambient=QVector3D(0.19225, 0.19225, 0.19225),
            diffuse=QVector3D(0.50754, 0.50754, 0.50754),
            specular=QVector3D(0.508273, 0.508273, 0.508273),
            shininess=51.2)


    @classmethod
    def polishedSilver(cls):
        """Return polished silver material"""
        return Material(
            ambient=QVector3D(0.23125, 0.23125, 0.23125),
            diffuse=QVector3D(0.2775, 0.2775, 0.2775),
            specular=QVector3D(0.773911, 0.773911, 0.773911),
            shininess=89.6)


    @classmethod
    def tin(cls):
        """Return tin material"""
        return Material(
            ambient=QVector3D(0.105882, 0.058824, 0.113725),
            diffuse=QVector3D(0.427451, 0.470588, 0.541176),
            specular=QVector3D(0.333333, 0.333333, 0.521569),
            shininess=9.84615)


    @classmethod
    def turquoise(cls):
        """Return turquoise material"""
        return Material(
            ambient=QVector3D(0.1, 0.18725, 0.1745),
            diffuse=QVector3D(0.396, 0.74151, 0.69102),
            specular=QVector3D(0.297254, 0.30829, 0.306678),
            shininess=12.8)


    @classmethod
    def rubberCyan(cls):
        """Return cyan rubber material"""
        return Material(
            ambient=QVector3D(0.0, 0.05, 0.05),
            diffuse=QVector3D(0.4, 0.5, 0.5),
            specular=QVector3D(0.04, 0.7, 0.7),
            shininess=10.0)


    @classmethod
    def rubberWhite(cls):
        """Return white rubber material"""
        return Material(
            ambient=QVector3D(0.05, 0.05,0.05),
            diffuse=QVector3D(0.5, 0.5, 0.5),
            specular=QVector3D(0.7, 0.7, 0.7),
            shininess=10.0)


    @classmethod
    def rubberBlack(cls):
        """Return black rubber material"""
        return Material(
            ambient=QVector3D(0.02, 0.02, 0.02),
            diffuse=QVector3D(0.01, 0.01, 0.0),
            specular=QVector3D(0.4, 0.4, 0.4),
            shininess=10.0)


    @classmethod
    def sun(cls):
        """Return sun material"""
        return Material(
            emission=QVector3D(1.0, 1.0, 1.0),
            ambient=QVector3D(1.0, 1.0, 1.0),
            diffuse=QVector3D(1.0, 1.0, 1.0),
            specular=QVector3D(1.0, 1.0, 1.0),
            shininess=10.0)
