import math
import numpy as np

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from OpenGL import GL
from Source.Graphics.Trackball import Trackball
from Source.Graphics.Light import Light
from Source.Graphics.Camera import Camera
from Source.Graphics.Material import Material
from Source.Graphics.Scene import Scene
from Source.Graphics.Actor import Actor
from Source.Graphics.Group import Group
from Source.Graphics.Gnomon import Gnomon
from Source.Graphics.World import World

from Source.Graphics.Cube import Cube
from Source.Graphics.Cylinder import Cylinder
from Source.Graphics.Cone import Cone
from Source.Graphics.Teapot import Teapot
from Source.Graphics.Torus import Torus
from Source.Graphics.Ocean import Ocean
from Source.Graphics.Icosahedron import Icosahedron
from Source.Graphics.Textures import Textures
from Source.Graphics.Bezier import Bezier
from Source.Graphics.SegmentodeTrilho import SegmentodeTrilho
from Source.Graphics.Construtor import Construtor
from Source.Graphics.Carro import Carro
from Source.Graphics.Simulador import Simulador
'''
from Source.Graphics.Portal import Portal
from Source.Graphics.PortalSystem import PortalSystem
'''

class Renderer(QOpenGLWidget):

    ## initialization
    def __init__(self, parent=None, **kwargs):
        """Initialize OpenGL version profile."""
        super(Renderer, self).__init__(parent)

        self._Teste = False

        self._parent = parent

        ## deal with options
        self._lighting = kwargs.get("lighting", True)
        self._antialiasing = kwargs.get("antialiasing", False)
        self._statistics = kwargs.get("statistics", True)

        ## define home orientation
        self._home_rotation = QQuaternion.fromAxisAndAngle(QVector3D(1.0, 0.0, 0.0), 25.0) * QQuaternion.fromAxisAndAngle(QVector3D(0.0, 1.0, 0.0), -50.0)

        ## define scene trackball
        self._trackball = Trackball(velocity=0.05, axis=QVector3D(0.0, 1.0, 0.0), mode=Trackball.TrackballMode.Planar, rotation=self._home_rotation, paused=True)

        ## create main scene
        self._world = World(self, home_position=QVector3D(0, 0.0, 3.5))

        ## do not animate
        self._animating = True

        ## not yet initialized
        self._initialized = False

        self._simulando = False
        self._primeiraPessoa = False

        self.setAutoFillBackground(False)


    def printOpenGLInformation(self, format, verbosity=0):
        print("\n*** OpenGL context information ***")
        print("Vendor: {}".format(GL.glGetString(GL.GL_VENDOR).decode('UTF-8')))
        print("Renderer: {}".format(GL.glGetString(GL.GL_RENDERER).decode('UTF-8')))
        print("OpenGL version: {}".format(GL.glGetString(GL.GL_VERSION).decode('UTF-8')))
        print("Shader version: {}".format(GL.glGetString(GL.GL_SHADING_LANGUAGE_VERSION).decode('UTF-8')))
        print("Maximum samples: {}".format(GL.glGetInteger(GL.GL_MAX_SAMPLES)))
        print("\n*** QSurfaceFormat from context ***")
        print("Depth buffer size: {}".format(format.depthBufferSize()))
        print("Stencil buffer size: {}".format(format.stencilBufferSize()))
        print("Samples: {}".format(format.samples()))
        print("Red buffer size: {}".format(format.redBufferSize()))
        print("Green buffer size: {}".format(format.greenBufferSize()))
        print("Blue buffer size: {}".format(format.blueBufferSize()))
        print("Alpha buffer size: {}".format(format.alphaBufferSize()))
            #print("\nAvailable extensions:")
            #for k in range(0, GL.glGetIntegerv(GL.GL_NUM_EXTENSIONS)-1):
            #    print("{},".format(GL.glGetStringi(GL.GL_EXTENSIONS, k).decode('UTF-8')))
            #print("{}".format(GL.glGetStringi(GL.GL_EXTENSIONS, k+1).decode('UTF-8')))


    def initializeGL(self):
        """Apply OpenGL version profile and initialize OpenGL functions."""
        if not self._initialized:
            self.printOpenGLInformation(self.context().format())

            ## create gnomon
            self._gnomon = Gnomon(self)

            ## update cameras
            self._world.camera.setRotation(self._trackball.rotation().inverted())
            self._gnomon.camera.setRotation(self._trackball.rotation().inverted())


            GL.glEnable(GL.GL_DEPTH_TEST)
            GL.glEnable(GL.GL_DEPTH_CLAMP)
            #GL.glEnable(GL.GL_CULL_FACE)
            GL.glEnable(GL.GL_MULTISAMPLE)
            GL.glEnable(GL.GL_FRAMEBUFFER_SRGB)

            ## attempt at line antialising
            if self._antialiasing:

                GL.glEnable(GL.GL_POLYGON_SMOOTH)
                GL.glEnable(GL.GL_BLEND)

                GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
                GL.glHint(GL.GL_LINE_SMOOTH_HINT, GL.GL_NICEST)
                GL.glHint(GL.GL_POLYGON_SMOOTH_HINT, GL.GL_NICEST)

                GL.glPointSize(5)
                GL.glLineWidth(1)

            ## clear color
            GL.glClearColor(0.75, 0.76, 0.76, 0.0)

            ## initialize scene
            self._world.initialize()

            ## initialize gnomon
            self._gnomon.initialize()

            ## timer for immediate update
            self._timer = QTimer(self)
            self._timer.setTimerType(Qt.PreciseTimer)
            self._timer.timeout.connect(self.updateScene)
            self._timer.start()

            ## timer for measuring elapsed time
            self._elapsed_timer = QElapsedTimer()
            self._elapsed_timer.restart()
            self._frameElapsed = 0
            self._gpuElapsed = 0

            self._initialized = True

            ###
            ### Add an object to the scene
            ###
            '''
            PortalsTransf = [QMatrix4x4(), QMatrix4x4()]
            PortalsTransf[0].translate(0.0, 0.0, 2.0)
            PortalsTransf[0].rotate(180.0, 0.0, 1.0, 0.0)
            PortalsTransf[1].translate(0.0, 0.0, -2.0)
            Portals = [Portal(self._world, transform=PortalsTransf[0]), Portal(self._world, transform=PortalsTransf[1])]
            self._world.addActor(Portals[0])
            self._world.addActor(Portals[1])
            self.portalsystem = PortalSystem(self._world)
            self.portalsystem.addPortal(Portals[0])
            self.portalsystem.addPortal(Portals[1])


            transf = QMatrix4x4()
            transf.translate(0.0, 0.0, 0.0)
            transf.rotate(90.0, 0.0, 1.0, 0.0)
            '''
            mat = Material(cbase=QVector3D(0.1, 0.9, 0.1), shininess=0.0, roughness=1.0, metallic=0.0)
            self.terreno = Ocean(self._world, material=mat)
            self.terreno.should_be_rendered = True
            self._world.addActor(self.terreno)


            transf = QMatrix4x4()
            cubicBezier = Bezier()
            cubicBezier.create([[0.0,0.0,0.0], [0.5519,0.0,0.0], [1.0,0.5519,0.0], [1.0,1.0,0.0]])

            self.construtor = Construtor(world=self._world, comprimento=4, bezier=cubicBezier, terreno=self.terreno)

            self.objects = [
                Cube(self._world, transform=transf),
                Torus(self._world, R=1.0, r=0.5, latitude=5, longitude=5, transform=transf),
                Ocean(self._world, ocean=True),
                Teapot(self._world),

                Icosahedron(self._world, level=4),
                Cone(self._world, resolution=50),
                Cylinder(self._world, resolution=50)
            ]
            self.construtor._tipo = 0
            self.construtor.addSegmento()

            if self._Teste:
                self.construtor._tipo = 1
                self.construtor._elevacao = -math.pi/4.0
                self.construtor._rotacao = math.pi/2.0

                self.construtor.addSegmento()
                self.construtor.addSegmento()
                self.construtor.addSegmento()

                self.construtor._elevacao = -math.pi/6.0
                self.construtor._rotacao = math.pi/3.0
                self.construtor.addSegmento()

                self.construtor._elevacao = math.pi/3.0
                self.construtor._rotacao = 0.0
                self.construtor.addSegmento()

                self.construtor._elevacao = -math.pi/3.0
                self.construtor._rotacao = 0.0
                self.construtor.addSegmento()

                self.construtor._elevacao = -math.pi/3.0
                self.construtor._rotacao = math.pi/2.0
                self.construtor.addSegmento()

                self.construtor._comprimento = 15
                self.construtor._elevacao = 5.0*(math.pi/180.0)
                self.construtor._rotacao = math.pi/2.0
                self.construtor._inclinacao = -45.0*(math.pi/180.0)
                self.construtor.addSegmento()

                self.construtor._comprimento = 3
                self.construtor._elevacao = 60.0*(math.pi/180.0)
                self.construtor._rotacao = 10.0*(math.pi/180.0)
                self.construtor._inclinacao = 0.0
                self.construtor.addSegmento()
                self.construtor.addSegmento()
                self.construtor.addSegmento()
                self.construtor.addSegmento()
                self.construtor.addSegmento()
                self.construtor._elevacao = 55.0*(math.pi/180.0)
                self.construtor._rotacao = 10.0*(math.pi/180.0)
                self.construtor.addSegmento()

                self.construtor._tipo = 2
                self.construtor._comprimento = 6
                self.construtor._elevacao = 0.0*(math.pi/180.0)
                self.construtor._rotacao = 0.0*(math.pi/180.0)

                self.construtor.addSegmento()
                self.construtor._elevacao = 90.0*(math.pi/180.0)
                self.construtor.addSegmento()

                self.construtor._comprimento = 4
                self.construtor._elevacao = 0.0*(math.pi/180.0)
                self.construtor.addSegmento()


                self.construtor._elevacao = -90.0*(math.pi/180.0)
                self.construtor.addSegmento()

                self.construtor._elevacao = -5.0*(math.pi/180.0)
                self.construtor._rotacao = 90.0*(math.pi/180.0)
                self.construtor.addSegmento()

                self.construtor._comprimento = 8
                self.construtor._elevacao = 0.0*(math.pi/180.0)
                self.construtor._rotacao = 90.0*(math.pi/180.0)
                self.construtor.addSegmento()

                self.construtor.terminar()



            self.carro = Carro(self._world, transform=transf)
            self._world.addActor(self.carro)
            self.carro2 = Carro(self._world, transform=transf)
            self._world.addActor(self.carro2)

            self.simulador = Simulador(contrutor=self.construtor)
            self.simulador.addCarro(self.carro)
            self.simulador.addCarro(self.carro2)
            self.simulador.parar()

            for each in self.objects:
                each.should_be_rendered = False

                self._world.addActor(each)

            '''
            self.portalsystem.addToSystem(self.objects[0])
            self.portalsystem.detectColisions()
            '''
            self.cur_obj = self.objects[0]
            self.cur_obj.should_be_rendered = False

            self._timer_simulacao = QElapsedTimer()
            self._timer_simulacao.restart()
            ###


        else:
            ## initialize scene
            self._world.initialize()

            ## initialize gnomon
            self._gnomon.initialize()

        ## initialize OpenGL timer
        self._query = GL.glGenQueries(1)
        Textures.loadTextures()




    def mudouElevacao(self, rotacao):
        self.construtor.mudouElevacao((int(rotacao)/180.0)*math.pi)


    def mudouRotacao(self, rotacao):
        self.construtor.mudouRotacao(-(int(rotacao)/180.0)*math.pi)


    def mudouInclinacao(self, rotacao):
        self.construtor.mudouInclinacao((int(rotacao)/180.0)*math.pi)

    def mudouTamanho(self, tamanho):
        self.makeCurrent()
        self.construtor.mudouTamanho(tamanho)
        self.doneCurrent()

    def mudouTipo(self, index):
        self.construtor.mudouTipo(index)
        self.update()

    def addTrilho(self):
        self.makeCurrent()
        self.construtor.addSegmento()
        self.doneCurrent()

    def rmTrilho(self):
        if(self._simulando == False):
            self.makeCurrent()
            self.construtor.rmTrilho()
            self.doneCurrent()
            

    def mudarCamera(self):
        if self._primeiraPessoa:
            self._trackball._rotation = self._trRot
            self._world.camera._position = self._cmPos
            self._world.camera._primeiraPessoa = False
            self._trackball._primeiraPessoa = False
            self._primeiraPessoa = False
        else:
            self._trRot = self._trackball._rotation
            self._cmPos = self._world.camera._position
            self._world.camera._primeiraPessoa = True
            self._trackball._primeiraPessoa = True
            self._primeiraPessoa = True


    def simular(self):
        self.simulador.Iniciar()
        self._simulando = True

    def parar(self):
        self.simulador.parar()
        self._simulando = False

    def clear(self):
        """Clear scene"""
        self._world.clear()
        self.update()


    def renderTimeEstimates(self):
        return [self._frameElapsed, self._gpuElapsed]


    @property
    def lighting(self):
        return self._lighting


    def setDrawStyle(self, style):
        self._draw_style = style


    def activeSceneCamera(self):
        """Returns main scene camera"""
        return self._world.camera


    def setAnimating(self, value):
        """Sets continuous update"""
        self._animating = value


    def isAnimating(self):
        """Returns whether continous update is active"""
        return self._animating

    def escalar(self, v1, v2):
        return(v1[0]*v2[0]+v1[1]*v2[1]+v1[2]*v2[2])

    def updateScene(self):
        '''
        """Schedule an update to the scene"""
        self.objects[0]._transform.translate(-0.01,0.0,0.0)
        if self.objects[0]._transform[2,3] >= 2.0:
            self.objects[0]._transform.translate(4.0,0.0,0.0)
        self.portalsystem.detectColisions()
        '''
        tempo = self._timer_simulacao.elapsed()
        self._timer_simulacao.restart()
        if self._simulando:
            self.simulador.step(tempo)
        if self._primeiraPessoa:

            pos = self.simulador._carros[1].position()
            up = QVector3D(self.simulador._up[1][0], self.simulador._up[1][1], self.simulador._up[1][2])*0.35
            tg = QVector3D(self.simulador._tangente[1][0], self.simulador._tangente[1][1], self.simulador._tangente[1][2])*0.28


            rot = QQuaternion()
            m4 = self.simulador._carros[1]._transform
            m4.rotate(180.0,0.0,1.0,0.0)
            m3 = QMatrix3x3()
            for i in range(3):
                for j in range(3):
                    m3[i, j] = m4[j, i]
            rot = QQuaternion.fromRotationMatrix(m3)

            self._world.camera.setPosition(pos + up + tg)
            self._trackball._rotation = rot
            self._world.camera.setRotation(QVector3D(0.0, math.pi, 0.0))
            # self._world.camera.setRotation()
            # self._trackball._axis = self.simulador._carros[0].position()
            # self._world.camera.setPosition(self.simulador._carros[0].position())
            # self._world.camera.pointAt(QVector3D(0.0, 6.0, 10.0))
            # self._trackball.reset(QQuaternion.fromAxisAndAngle(QVector3D(0.0, 1.0, 0.0), -90.0))
            # self._world.camera.cameraMatrix()
        if self.isAnimating():
            self.update()


    def renderScene(self):
        """Draw main scene"""

        ## set scene rotation
        self._world.camera.setRotation(self._trackball.rotation().inverted())
        self._gnomon.camera.setRotation(self._trackball.rotation().inverted())

        self._world.render()

        ## render gnomon
        self._gnomon.render()


    def paintGL(self):
        """Draw scene"""

        ## record render time statistics
        if self._statistics:

            ## begin GPU time query
            GL.glBeginQuery(GL.GL_TIME_ELAPSED, self._query)

            ## render scene
            self.renderScene()

            ## finish GPU time query
            GL.glEndQuery(GL.GL_TIME_ELAPSED)

            ## record render time statistics, need to stall the CPU a bit
            ready = False
            while not ready:
                ready = GL.glGetQueryObjectiv(self._query, GL.GL_QUERY_RESULT_AVAILABLE)
            self._gpuElapsed = GL.glGetQueryObjectuiv(self._query, GL.GL_QUERY_RESULT ) / 1000000.0

            ## delete query object
            #GL.glDeleteQueries( self._query )

        else:

            ## render scene
            self.renderScene()

        self._frameElapsed = self._elapsed_timer.restart()


    def resizeGL(self, width, height):
        """ Called by the Qt libraries whenever the window is resized"""
        self._world.camera.setAspectRatio(width / float(height if height > 0.0 else 1.0))


    def pan(self, point, state='start'):
        """Move camera according to mouse move"""
        if state == 'start':
            self._lastPanningPos = point
        elif state == 'move':
            delta = QLineF(self._lastPanningPos, point)
            self._lastPanningPos = point
            direction = QVector3D(-delta.dx(), -delta.dy(), 0.0).normalized()
            newpos = self._world.camera.position + delta.length()*2.0 * direction
            self._world.camera.setPosition(newpos)


    def mousePressEvent(self, event):
        """ Called by the Qt libraries whenever the window receives a mouse click."""
        super(Renderer, self).mousePressEvent(event)

        if event.isAccepted():
            return

        if event.buttons() & Qt.LeftButton:
            self._trackball.press(self._pixelPosToViewPos(event.localPos()), QQuaternion())
            self._trackball.start()
            event.accept()
            if not self.isAnimating():
                self.update()

        elif event.buttons() & Qt.RightButton:
            self.pan(self._pixelPosToViewPos(event.localPos()), state='start')
            self.update()


    def mouseMoveEvent(self, event):
        """Called by the Qt libraries whenever the window receives a mouse move/drag event."""
        super(Renderer, self).mouseMoveEvent(event)

        if event.isAccepted():
            return

        if event.buttons() & Qt.LeftButton:
            self._trackball.move(self._pixelPosToViewPos(event.localPos()), QQuaternion())
            event.accept()
            if not self.isAnimating():
                self.update()

        elif event.buttons() & Qt.RightButton:
            self.pan(self._pixelPosToViewPos(event.localPos()), state='move')
            self.update()


    def mouseReleaseEvent(self, event):
        """ Called by the Qt libraries whenever the window receives a mouse release."""
        super(Renderer, self).mouseReleaseEvent(event)

        if event.isAccepted():
            return

        if event.button() == Qt.LeftButton:
            self._trackball.release(self._pixelPosToViewPos(event.localPos()), QQuaternion())
            event.accept()
            if not self.isAnimating():
                self._trackball.stop()
                self.update()


    def wheelEvent(self, event):
        """Process mouse wheel movements"""
        super(Renderer, self).wheelEvent(event)
        self.zoom(-event.angleDelta().y() / 950.0)
        event.accept()
        ## scene is dirty, please update
        self.update()


    def zoom(self, diffvalue):
        """Zooms in/out the active camera"""
        multiplicator = math.exp(diffvalue)

        ## get a hold of the current active camera
        camera = self._world.camera

        if camera.lens == Camera.Lens.Orthographic:
            # Since there's no perspective, "zooming" in the original sense
            # of the word won't have any visible effect. So we just increase
            # or decrease the field-of-view values of the camera instead, to
            # "shrink" the projection size of the model / scene.
            camera.scaleHeight(multiplicator)

        else:

            old_focal_dist = camera.focalDistance
            new_focal_dist = old_focal_dist * multiplicator

            direction = camera.orientation * QVector3D(0.0, 0.0, -1.0)
            newpos = camera.position + (new_focal_dist - old_focal_dist) * -direction

            camera.setPosition(newpos)
            camera.setFocalDistance(new_focal_dist)


    def viewFront(self):
        """Make camera face the front side of the scene"""
        self._trackball.reset(QQuaternion())
        self.update()


    def viewBack(self):
        """Make camera face the back side of the scene"""
        self._trackball.reset(QQuaternion.fromAxisAndAngle(QVector3D(0.0, 1.0, 0.0), 180.0))
        self.update()


    def viewLeft(self):
        """Make camera face the left side of the scene"""
        self._trackball.reset(QQuaternion.fromAxisAndAngle(QVector3D(0.0, 1.0, 0.0), -90.0))
        self.update()


    def viewRight(self):
        """Make camera face the right side of the scene"""
        self._trackball.reset(QQuaternion.fromAxisAndAngle(QVector3D(0.0, 1.0, 0.0), 90.0))
        self.update()


    def viewTop(self):
        """Make camera face the top side of the scene"""
        self._trackball.reset(QQuaternion.fromAxisAndAngle(QVector3D(1.0, 0.0, 0.0), 90.0))
        self.update()


    def viewBottom(self):
        """Make camera face the bottom side of the scene"""
        self._trackball.reset(QQuaternion.fromAxisAndAngle(QVector3D(1.0, 0.0, 0.0), -90.0))
        self.update()


    def createGridLines(self):
        """Set gridlines"""
        self.makeCurrent()
        self._world.createGridLines()
        self.doneCurrent()


    def cameraLensChanged(self, lens):
        """Switch world's. camera lens"""
        self._world.setCameraLens(lens)
        self._gnomon.setCameraLens(lens)
        self.update()


    def storeCamera(self):
        """Store world's camera parameters"""
        self._world.storeCamera()


    def recallCamera(self):
        """Recall camera parameters"""
        self._world.recallCamera()
        self._trackball.reset(self._world.camera.rotation.inverted())
        self.update()


    def resetCamera(self):
        """Reset world's camera parameters"""
        self._world.resetCamera()
        self._trackball.reset(self._home_rotation)
        self.update()


    def drawStyleChanged(self, index):
        self._world.setDrawStyle(Scene.DrawStyle.Styles[index])
        self.update()


    def lightingChanged(self, state):
        self._world.setLighting(state)
        self.update()



    def shadingChanged(self, index):
        self._world.setShading(Scene.Shading.Types[index])
        self.update()

    def objectChanged(self, index):
        self.cur_obj.should_be_rendered = False
        self.cur_obj = self.objects[index]
        self.cur_obj.should_be_rendered = True
        # self.update()

    def roughnessChange(self, value):
        for obj in self.objects:
            obj._active_material._roughness = value

    def specularChange(self, value):
        for obj in self.objects:
            obj._active_material._specularColor = QVector3D(value,value,value)

    def metallicChange(self, value):
        for obj in self.objects:
            obj._active_material._metallic = value

    def spikeChange(self, value):
        for obj in self.objects:
            obj._material._spike = value
            obj._wireframe._spike = value

    def spike_wChange(self, value):
        for obj in self.objects:
            obj._material._spike_w = value
            obj._wireframe._spike_w = value

    def spike_hChange(self, value):
        for obj in self.objects:
            obj._material._spike_h = value
            obj._wireframe._spike_h = value

    def spike_wChange(self, value):
        for obj in self.objects:
            obj._active_material._spike_w = value

    def baseColorChange(self, value):
        component = self.sender().objectName()
        if component == 'R':
            for obj in self.objects:
                old = obj._active_material._cbase
                obj._active_material._cbase = QVector3D(value, old.y(), old.z())
        elif component == 'G':
            for obj in self.objects:
                old = obj._active_material._cbase
                obj._active_material._cbase = QVector3D(old.x(), value, old.z())
        elif component == 'B':
            for obj in self.objects:
                old = obj._active_material._cbase
                obj._active_material._cbase = QVector3D(old.x(), old.y(), value)

    def lightChanged(self, index):
        if index == 0:
            self._world._light._directional = False
            self._world._light._hemispheric = True
        elif index == 1:
            self._world._light._directional = False
            self._world._light._hemispheric = False
        else:
            self._world._light._directional = True
            self._world._light._hemispheric = False

    def skyColorChange(self, value):
        component = self.sender().objectName()
        if component == 'R':
            old = self._world._light._csky
            self._world._light._csky = QVector3D(value, old.y(), old.z())
        elif component == 'G':
            old = self._world._light._csky
            self._world._light._csky = QVector3D(old.x(), value, old.z())
        elif component == 'B':
            old = self._world._light._csky
            self._world._light._csky = QVector3D(old.x(), old.y(), value)

    def groundColorChange(self, value):
        component = self.sender().objectName()
        if component == 'R':
            old = self._world._light._cground
            self._world._light._cground = QVector3D(value, old.y(), old.z())
        elif component == 'G':
            old = self._world._light._cground
            self._world._light._cground = QVector3D(old.x(), value, old.z())
        elif component == 'B':
            old = self._world._light._cground
            self._world._light._cground = QVector3D(old.x(), old.y(), value)

    def lightColorChange(self, value):
        component = self.sender().objectName()
        if component == 'R':
            old = self._world._light._color
            self._world._light._color = QVector3D(value, old.y(), old.z())
        elif component == 'G':
            old = self._world._light._color
            self._world._light._color = QVector3D(old.x(), value, old.z())
        elif component == 'B':
            old = self._world._light._color
            self._world._light._color = QVector3D(old.x(), old.y(), value)

    def lightPosChange(self, value):
        component = self.sender().objectName()
        if component == 'X':
            old = self._world._light._position
            self._world._light._position = QVector3D(value, old.y(), old.z())
        elif component == 'Y':
            old = self._world._light._position
            self._world._light._position = QVector3D(old.x(), value, old.z())
        elif component == 'Z':
            old = self._world._light._position
            self._world._light._position = QVector3D(old.x(), old.y(), value)

    def lradiusChange(self, value):
        self._world._light._lradious = value

    def aconstChange(self, value):
        self._world._light._aconst = value

    def alinearChange(self, value):
        self._world._light._alinear = value

    def aquadChange(self, value):
        self._world._light._aquad = value




    def headLightChanged(self, state):
        self._world.light.setHeadLight(state)
        self.update()


    def directionalLightChanged(self, state):
        self._world.light.setDirectional(state)
        self.update()


    def enableProfiling(self, enable):
        self._statistics = enable


    def enableAnimation(self, enable):
        self.setAnimating(enable)
        if not enable:
            self._trackball.stop()


    def _pixelPosToViewPos(self, point):
        return QPointF(2.0 * float(point.x()) / self.width() - 1.0, 1.0 - 2.0 * float(point.y()) / self.height())
