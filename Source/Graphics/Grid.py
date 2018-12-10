import numpy as np

from PyQt5.QtGui import QVector3D, QMatrix4x4, QOpenGLShader, QOpenGLShaderProgram, QOpenGLBuffer, QOpenGLVertexArrayObject

from OpenGL import GL
from Source.Graphics.Actor import Actor
from Source.Graphics.Material import Material

class Grid(Actor):

    ## initialization
    def __init__(self, scene, **kwargs):
        """Initialize actor."""
        super(Grid, self).__init__(scene, mode=Actor.RenderMode.LineStrip, **kwargs)

        self._lengthRows = kwargs.get("length_rows", 10.0)
        self._lengthCols = kwargs.get("length_cols", 10.0)
        self._rows = kwargs.get("rows", 10)
        self._cols = kwargs.get("cols", 10)
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


    def generateGeometry(self):
        """Generate vertices"""
        starty = -self._lengthRows / 2.0
        endy = self._lengthRows / 2.0

        startx = -self._lengthCols / 2.0
        endx = self._lengthCols / 2.0
        
        self._resx = resx = self._cols + 1
        self._resy = resy = self._rows + 1

        ## create grid coordinates
        xsteps = np.linspace(startx, endx, self._resx)
        ysteps = np.linspace(starty, endy, self._resy)
        
        x, y, z = np.meshgrid(xsteps, 0.0, ysteps)
        
        vertical = np.vstack((x, y, z)).reshape(3, -1).T.astype(np.float32)
        horizontal = np.vstack((x, y, z)).T.astype(np.float32)

        ## create vertices array from grid coordinates
        self._vertices = np.concatenate((vertical.flatten(), horizontal.flatten()))

        ## create supporting arrays for rendering
        ystart = list(range(0, resx*resy, resy))
        xstart = list(range(ystart[-1]+resy, ystart[-1]+resy+resx*resy, resx))
        ylen = [resy] * resx
        xlen = [resx] * resy

        self._start = np.array(ystart + xstart, dtype=np.dtype(np.uint32))
        self._lengths = np.array(ylen + xlen, dtype=np.dtype(np.uint32))


    def initialize(self):
        """Creates floor grid geometry"""
        if self._vertices is None:
            self.generateGeometry()

        ## create object
        self.create(self._vertices)


    def render(self):
        """Render grid"""
        GL.glMultiDrawArrays(self._render_mode, self._start, self._lengths, self._resx+self._resy)



    