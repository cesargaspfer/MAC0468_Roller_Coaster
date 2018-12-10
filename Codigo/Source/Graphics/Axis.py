import numpy as np

from OpenGL import GL
from Source.Graphics.Actor import Actor

class Axis(Actor):

    ## initialization
    def __init__(self, scene, **kwargs):
        """Initialize actor."""
        super(Axis, self).__init__(scene, type=Actor.RenderType.Overlay, **kwargs)

        self._length_row = kwargs.get("length_row", 1.0)
        self._length_col = kwargs.get("length_col", 1.0)

        ## register shaders
        self.setSolidShader(self.shaderCollection.attributeColorShader())
        self.setSolidFlatShader(self.shaderCollection.attributeColorShader())
        self.setNoLightSolidShader(self.shaderCollection.attributeColorShader())
        self.setWireframeShader(self.shaderCollection.attributeColorShader())
        self.setNoLightWireframeShader(self.shaderCollection.attributeColorShader())

        self._vertices = None

        ## create actor
        self.initialize()


    def generateGeometry(self):
        """Generate vertices"""
        self._vertices = np.array([
            -self._length_col/2.0, 0.0, 0.0,
            self._length_col/2.0, 0.0, 0.0,
            0.0, 0.0, -self._length_row/2.0,
            0.0, 0.0, self._length_row/2.0,
        ], dtype=np.float32)
    
        self._colors = np.array([
            1.0, 0.0, 0.0,
            1.0, 0.0, 0.0,
            0.0, 0.47, 0.78,
            0.0, 0.47, 0.78
        ], dtype=np.float32)


    def initialize(self):
        """Creates axis"""
        if self._vertices is None:
            self.generateGeometry()

        ## create object
        self.create(self._vertices, colors=self._colors)


    def render(self):
        """Render grid"""
        GL.glDrawArrays(GL.GL_LINES, 0, 4)



    