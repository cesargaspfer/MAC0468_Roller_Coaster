from PyQt5.QtGui import QMatrix4x4, QVector3D, QVector4D

from OpenGL import GL
from Source.Graphics.Actor import Actor
from Source.Graphics.Group import Group
from Source.Graphics.Material import Material
from Source.Graphics.Cone import Cone
from Source.Graphics.Cylinder import Cylinder
from Source.Graphics.Icosahedron import Icosahedron

##  The orientation marker
class OrientationMarker(Group):

    ## initialization
    def __init__(self, scene, **kwargs):
        """Initialize actor."""
        super(OrientationMarker, self).__init__(scene, **kwargs)

        self._resolution = kwargs.get("resolution", 12)
        self._colorx = kwargs.get("xcolor", QVector3D(1.0, 0.0, 0.0))
        self._colory = kwargs.get("ycolor", QVector3D(0.0, 1.0, 0.0))
        self._colorz = kwargs.get("zcolor", QVector3D(0.0, 0.47, 0.78))

        ## create sphere
        matrix = QMatrix4x4()
        matrix.scale(0.4, 0.4, 0.4)
        self.addPart(Icosahedron(self.scene, name="sphere",
            level=2, colors=False, material=Material(cbase=QVector3D(0.4, 0.4, 0.4),
            ambient=QVector3D(0.25, 0.25, 0.25),
            diffuse=QVector3D(0.4, 0.4, 0.4),
            specular=QVector3D(.2, .2, .2),
            shininess=128.8), transform=matrix))

        ## x axis cone
        matrix = QMatrix4x4()
        matrix.rotate(-90.0, QVector3D(0.0, 0.0, 1.0))
        matrix.scale(0.19, 0.2, 0.19)
        matrix.translate(0.0, 2.8, 0.0)
        self.addPart(Cone(self.scene, name="xaxis",
            resolution=self._resolution, material=Material(diffuse=self._colorx,
            cbase=self._colorx, specular=QVector3D(0.5, 0.5, 0.5),
            shininess=76.8), transform=matrix))

        ## y axis cone
        matrix = QMatrix4x4()
        matrix.scale(0.19, 0.2, 0.19)
        matrix.translate(0.0, 2.7, 0.0) ##6.0
        self.addPart(Cone(self.scene, name="yaxis",
            resolution=self._resolution, material=Material(diffuse=self._colory,
            cbase=self._colory, specular=QVector3D(0.5, 0.5, 0.5),
            shininess=76.8), transform=matrix))

        ## z axis cone
        matrix = QMatrix4x4()
        matrix.rotate(90.0, QVector3D(1.0, 0.0, 0.0))
        matrix.scale(0.19, 0.2, 0.19)
        matrix.translate(0.0, 2.7, 0.0)
        self.addPart(Cone(self.scene, name="zaxis",
            resolution=self._resolution, material=Material(diffuse=self._colorz, cbase=self._colorz, specular=QVector3D(0.5, 0.5, 0.5),
            shininess=76.8), transform=matrix))
