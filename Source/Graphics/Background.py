import numpy as np

from OpenGL import GL
from PyQt5.QtGui import QColor
from Source.Graphics.Actor import Actor

class Background(Actor):

    ## initialization
    def __init__(self, scene, **kwargs):
        """Initialize actor."""
        super(Background, self).__init__(scene, type=Actor.RenderType.Overlay)

        defaultPalette = {
            'top_left': QColor(107, 128, 140),
            'top_center': QColor(107, 128, 140),
            'top_right': QColor(107, 128, 140),
            'mid_left': QColor(149, 164, 164),
            'mid_center': QColor(149, 164, 164),
            'mid_right': QColor(149, 164, 164),
            'bot_left': QColor(191, 199, 199),
            'bot_center': QColor(191, 199, 199),
            'bot_right': QColor(191, 199, 199)
        }

        self._name = kwargs.get("name", None)
        self._palette = kwargs.get("palette", defaultPalette)  
        self._vertices = None     

        ## register shaders
        self.setSolidShader(self.shaderCollection.backgroundShader())
        self.setSolidFlatShader(self.shaderCollection.backgroundShader())
        self.setNoLightSolidShader(self.shaderCollection.backgroundShader())
        self.setWireframeShader(self.shaderCollection.backgroundShader())
        self.setNoLightWireframeShader(self.shaderCollection.backgroundShader())
        
        ## create actor
        self.initialize()


    def generateGeometry(self):
        """Creates background plane geometry and colors"""
        self._vertices = np.array([
            -1, -1, 1,
            0, -1, 1,
            0, 0, 1,

            0, 0, 1,
            -1, 0, 1,
            -1, -1, 1,

            -1, 0, 1,
            0, 0, 1,
            0, 1, 1,

            0, 1, 1,
            -1, 1, 1,
            -1, 0, 1,

            0, -1, 1,
            1, -1, 1,
            1, 0, 1,

            1, 0, 1,
            0, 0, 0,
            0, -1, 1,

            0, 0, 1,
            1, 0, 1,
            1, 1, 1,

            1, 1, 1,
            0, 1, 1,
            0, 0, 0
        ], dtype=np.float32)
        
        self._colors = np.array([
            self._palette['bot_left'].getRgbF()[:3],
            self._palette['bot_center'].getRgbF()[:3],
            self._palette['mid_center'].getRgbF()[:3],

            self._palette['mid_center'].getRgbF()[:3],
            self._palette['mid_left'].getRgbF()[:3],
            self._palette['bot_left'].getRgbF()[:3],  

            self._palette['mid_left'].getRgbF()[:3], 
            self._palette['mid_center'].getRgbF()[:3],
            self._palette['top_center'].getRgbF()[:3], 
                                                 
            self._palette['top_center'].getRgbF()[:3], 
            self._palette['top_left'].getRgbF()[:3],
            self._palette['mid_left'].getRgbF()[:3], 

            self._palette['bot_center'].getRgbF()[:3],
            self._palette['bot_right'].getRgbF()[:3],
            self._palette['mid_right'].getRgbF()[:3], 
            
            self._palette['mid_right'].getRgbF()[:3], 
            self._palette['mid_center'].getRgbF()[:3],
            self._palette['bot_center'].getRgbF()[:3],

            self._palette['mid_center'].getRgbF()[:3],
            self._palette['mid_right'].getRgbF()[:3], 
            self._palette['top_right'].getRgbF()[:3],

            self._palette['top_right'].getRgbF()[:3],
            self._palette['top_center'].getRgbF()[:3], 
            self._palette['mid_center'].getRgbF()[:3]
                                                                                                                                              
        ], dtype=np.float32)


    def initialize(self):
        """Creates cone geometry"""
        if self._vertices is None:
            self.generateGeometry()

        ## create object
        self.create(self._vertices, colors=self._colors)


    def setPalette(self, palette):
        colors = np.array([
            palette['bot_left'].getRgbF()[:3],
            palette['bot_center'].getRgbF()[:3],
            palette['mid_center'].getRgbF()[:3],

            palette['mid_center'].getRgbF()[:3],
            palette['mid_left'].getRgbF()[:3],
            palette['bot_left'].getRgbF()[:3],  

            palette['mid_left'].getRgbF()[:3], 
            palette['mid_center'].getRgbF()[:3],
            palette['top_center'].getRgbF()[:3], 
                                                 
            palette['top_center'].getRgbF()[:3], 
            palette['top_left'].getRgbF()[:3],
            palette['mid_left'].getRgbF()[:3], 

            palette['bot_center'].getRgbF()[:3],
            palette['bot_right'].getRgbF()[:3],
            palette['mid_right'].getRgbF()[:3], 
            
            palette['mid_right'].getRgbF()[:3], 
            palette['mid_center'].getRgbF()[:3],
            palette['bot_center'].getRgbF()[:3],

            palette['mid_center'].getRgbF()[:3],
            palette['mid_right'].getRgbF()[:3], 
            palette['top_right'].getRgbF()[:3],

            palette['top_right'].getRgbF()[:3],
            palette['top_center'].getRgbF()[:3], 
            palette['mid_center'].getRgbF()[:3]
        ], dtype=np.float32)
        self.updateBuffer(colors=colors)


    def render(self):
        """Render background"""
        GL.glDrawArrays(self._render_mode, 0, self.numberOfVertices)



    