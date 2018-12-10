import numpy as np

from PyQt5.QtGui import QVector3D, QMatrix4x4, QOpenGLShader, QOpenGLShaderProgram, QOpenGLBuffer, QOpenGLVertexArrayObject

from OpenGL import GL
from Source.Graphics.Actor import Actor
from Source.Graphics.Material import Material

class Floor(Actor):

    ## initialization
    def __init__(self, scene, **kwargs):
        """Initialize actor."""
        super(Floor, self).__init__(scene, mode=Actor.RenderMode.LineStrip, **kwargs)

        self._length = kwargs.get("length", 4)
        self._resolution = kwargs.get("resolution", 25)
        self._material = kwargs.get("material", Material(diffuse=QVector3D(0.5, 0.5, 0.5)))

        ## register shaders
        self.setSolidShader(self.shaderCollection.uniformMaterialShader())
        self.setSolidFlatShader(self.shaderCollection.uniformMaterialShader())
        self.setNoLightSolidShader(self.shaderCollection.uniformMaterialShader())
        self.setWireframeShader(self.shaderCollection.uniformMaterialShader())
        self.setNoLightWireframeShader(self.shaderCollection.uniformMaterialShader())

        self._vertices = None

        ## create actor
        self.initialize()


    @property
    def resolution(self):
        """Returns the resolution of this floor grid"""
        return self._resolution


    def generateGeometry(self):
        """Creates floor grid geometry"""
        resx, resy = self._resolution, self._resolution

        ## create grid coordinates
        xsteps = np.linspace(-self._length, self._length, resx)
        ysteps = np.linspace(-self._length, self._length, resy)
        x, y, z = np.meshgrid(xsteps, 0.0, ysteps)
        vertical = np.vstack((x, y, z)).reshape(3, -1).T.astype(np.float32)
        horizontal = np.vstack((z, y, x)).reshape(3, -1).T.astype(np.float32)

        ## create vertices array from grid coordinates
        self._vertices = np.concatenate((vertical, horizontal)).flatten()

        ## create supporting arrays for rendering
        ystart = list(range(0, resx*resy, resy))
        xstart = list(range(ystart[-1]+resy, ystart[-1]+resy+resx*resy, resx))
        ylen = [resy] * resx
        xlen = [resx] * resy

        self._start = ystart + xstart
        self._lengths = ylen + xlen


    def initialize(self):
        """Creates cone geometry"""
        if self._vertices is None:
            self.generateGeometry()

        ## create object
        self.create(self._vertices)


    def render(self):
        """Render grid"""
        GL.glMultiDrawArrays(self._render_mode, self._start, self._lengths, self._resolution+self._resolution)



    