import math

from PyQt5.QtCore import QObject
from PyQt5.QtGui import QVector3D, QVector4D, QMatrix4x4, QQuaternion
from collections import OrderedDict

from OpenGL import GL
from Source.Graphics.Ray import Ray
from Source.Graphics.Light import Light
from Source.Graphics.Camera import Camera
from Source.Graphics.Actor import Actor
from Source.Graphics.Group import Group
from Source.Graphics.Floor import Floor
from Source.Graphics.Background import Background

##  Base scene class
class Scene(QObject):

    class DrawStyle:
        Point = GL.GL_POINT
        Wireframe = GL.GL_LINE
        Solid = GL.GL_FILL
        SolidWithEdges = GL.GL_FILL + 1
        Styles = [Point, Wireframe, Solid, SolidWithEdges]


    class Shading:
        Flat = GL.GL_FLAT
        Smooth = GL.GL_SMOOTH
        Types = [Flat, Smooth]


    def __init__(self, viewer, **kwargs):
        """Initialize camera object."""
        super(Scene, self).__init__()

        self._viewer = viewer
        self._name = kwargs.get("name", "main")
        self._draw_style = Scene.DrawStyle.Solid
        self._background_actor = kwargs.get("background", None)
        self._actors = OrderedDict()
        self._systemActors = OrderedDict()
        self._selectedActor = None
        self._highlightedActor = None
        self._camera = kwargs.get("camera", None)
        self._light = kwargs.get("light", None)
        self._lighting = kwargs.get("lighting", True)
        self._shading = kwargs.get("shading", Scene.Shading.Smooth)


    @property
    def name(self):
        """Returns the name of this camera"""
        return self._name


    def setViewer(self, viewer):
        self._viewer = viewer


    @property
    def viewer(self):
        """Returns the viewer rendering this scene"""
        return self._viewer


    def clear(self):
        """Clear actors from scene"""
        self._actors.clear()


    def actor(self, index):
        """Returns an specified actor"""
        return self._actors[index]


    def systemActor(self, index):
        """Returns an specified systemactor"""
        return self._systemActors[index]


    def findActorByName(self, name):
        """Returns an actor by name if it exists"""
        if name in self._actors.keys():
            return self._actors[name]
        return None


    def actors(self):
        """Returns list of actors"""
        return list(self._actors.values())


    def systemActors(self):
        """Returns list of system actors"""
        return list(self._systemActors.values())


    def addActor(self, actor, select=False):
        """Add actor to the list"""
        self._actors[actor.name] = actor
        if select:
            self.selectActor(actor)


    def addSystemActor(self, actor):
        """Add actor to the system list"""
        self._systemActors[actor.name] = actor


    def removeActor(self, actor):
        """Removes a specific actor from scene"""
        if actor.name is not None:
            actor = self._actors.pop(actor.name)
            if actor == self.selectedActor():
                if len(self._actors) > 0:
                    selectable_actors = [key for (key, actor) in self._actors.items() if actor.isSelectable()]
                    if len(selectable_actors) > 0:
                        lastActor = next(reversed(selectable_actors))
                        self.selectActor(self._actors[lastActor])
                    else:
                        self.selectActor(None)
                else:
                    self.selectActor(None)
            del actor


    def removeSystemActor(self, actor):
        """Removes a specific system actor from scene"""
        if actor.name is not None:
            del self._systemActors[actor.name]


    def highlightedActor(self):
        """Returns highlighted actor"""
        return self._highlightedActor


    def highlightActor(self, actor):
        """Highlight actor"""
        if self._highlightedActor is not None:
            self._highlightedActor.setHighlighted(False)
        self._highlightedActor = actor
        if actor is not None:
            self._highlightedActor.setHighlighted(True)


    def selectedActor(self):
        """Returns list of selected Actors"""
        return self._selectedActor


    def selectActor(self, actor):
        """Select actor"""
        if self._selectedActor is not None:
            self._selectedActor.setSelected(False)
        self._selectedActor = actor
        if actor is not None:
            self._selectedActor.setSelected(True)


    def setDrawStyle(self, style):
        """Sets the drawing style"""
        self._draw_style = style


    def setCamera(self, camera):
        """Sets the active camera for this viewer"""
        self._camera = camera


    @property
    def camera(self):
        return self._camera


    def setLight(self, light):
        """Sets the active light source for this viewer"""
        self._light = light


    @property
    def light(self):
        return self._light


    @property
    def lighting(self):
        return self._lighting


    def setLighting(self, state):
        """Sets light calculations on or off"""
        self._lighting = state


    @property
    def shading(self):
        return self._shading


    def setShading(self, type):
        """Sets shading type"""
        self._shading = type


    def initialize(self):
        pass


    def project(self, point, depth=0.0):
        """Returns intersection if any"""
        ray = self.ray(point)
        tMin = -math.inf
        tMax = math.inf
        obb_xform = QMatrix4x4()
        obb_center = QVector3D(0.0, 0.0, depth)
        point = obb_center - ray.origin()
        plane_size = [100.0, 100.0, 1E-6]
        for i in range(3):
            axis = QVector3D(obb_xform[0,i], obb_xform[1,i], obb_xform[2,i]).normalized()
            half_length = plane_size[i]
            e = QVector3D.dotProduct(axis, point)
            f = QVector3D.dotProduct(axis, ray.direction())
            if abs(f) > 10E-6:
                t1 = (e + half_length) / f
                t2 = (e - half_length) / f
                if t1 > t2:
                    w=t1; t1=t2; t2=w
                if t1 > tMin:
                    tMin = t1
                if t2 < tMax:
                    tMax = t2
                if tMin > tMax:
                    return QVector3D(0, 0, 0)
                if tMax < 0:
                    return QVector3D(0, 0, 0)
            elif -e-half_length > 0.0 or -e+half_length < 0.0:
                return  QVector3D(0, 0, 0)
        if tMin > 0:
            return ray.origin() + tMin * ray.direction()
        return ray.origin() + tMax * ray.direction()


    def ray(self, point):
        ray_start = QVector4D(point); ray_start.setZ(-1.0); ray_start.setW(1.0)
        ray_end = QVector4D(point); ray_end.setZ(0.0); ray_end.setW(1.0)
        inverseProjectionMatrix = self._camera.projectionMatrix.inverted()[0]
        inverseViewMatrix = self._camera.viewMatrix.inverted()[0]
        ray_start_camera = inverseProjectionMatrix * ray_start; ray_start_camera /= ray_start_camera.w()
        ray_end_camera = inverseProjectionMatrix * ray_end; ray_end_camera /= ray_end_camera.w()
        ray_start_world = inverseViewMatrix * ray_start_camera; ray_start_world /= ray_start_world.w()
        ray_end_world = inverseViewMatrix * ray_end_camera; ray_end_world /= ray_end_world.w()
        ray = ray_end_world - ray_start_world
        ray_direction = QVector3D(ray[0], ray[1], ray[2]).normalized()
        return Ray(self,
            origin=QVector3D(ray_start_world[0], ray_start_world[1], ray_start_world[2]),
            direction=QVector3D(ray_direction[0], ray_direction[1], ray_direction[2]))


    def pick(self, point):
        """Finds closest intersection if it exists"""
        result = (None, None)
        distance = math.inf

        ## compute ray
        ray = self.ray(point)

        ## inspect all actors
        for each in self.actors():

            ## inspect actor
            if each.isPickable():
                #print("inspecting actor: ", each.name)
                hit = each.intersect(ray)
                if hit[0] and hit[1] < distance:
                    result = (each, None); distance = hit[1]

                ## inspect group
                if isinstance(each, Group):
                    #print("inspecting group: ", each.name)
                    for part in each.parts[1:]:
                        if part.isPickable():
                            #print("   inspecting part: ", part)
                            hit = part.intersect(ray)
                            if hit[0] and hit[1] <= distance:
                                result = (each, part); distance = hit[1]

        return result


    def renderPart(self, part, draw_style, passNumber):
        """Render a single actor"""

        if part.isVisible():
            ## set up rendering for this actor
            part.beginRendering(draw_style, self.lighting, self.shading, passNumber)

            ## draw actor
            part.render()

            ## finish rendering
            part.endRendering()


    def renderBackground(self, actor):
        """Render scene background"""
        self.renderPart(actor, Scene.DrawStyle.Solid, 0)


    def renderGridFloor(self, actor):
        """Render scene grid floor"""
        self.renderPart(actor, Scene.DrawStyle.Solid, 0)


    def renderFirstPass(self, actor):
        """Render first pass of the scene"""

        if actor.isVisible():
            GL.glEnable(GL.GL_POLYGON_OFFSET_FILL)

            if self._draw_style == Scene.DrawStyle.SolidWithEdges:
                GL.glPolygonOffset(1, 4)

            draw_style = Scene.DrawStyle.Solid if self._draw_style == Scene.DrawStyle.SolidWithEdges else self._draw_style

            if isinstance(actor, Group):

                ## if this is group, render its parts individually
                for each in actor.parts:
                    self.renderPart(each, draw_style, 0)

            else:

                ## render this actor with current draw style
                self.renderPart(actor, draw_style, 0)


    def renderSecondPass(self, actor):
        """Render second pass of the scene"""

        if actor.isVisible():
            GL.glDisable(GL.GL_POLYGON_OFFSET_FILL)

            if self._draw_style == Scene.DrawStyle.SolidWithEdges:

                GL.glPolygonOffset(0, 0)

                if isinstance(actor, Group):

                    ## if this is group, render its parts individually
                    for each in actor.parts:
                        self.renderPart(each, Scene.DrawStyle.Wireframe, 1)

                else:

                    ## render this actor with current draw style
                    self.renderPart(actor, Scene.DrawStyle.Wireframe, 1)


    def setViewportRegion(self):
        """Define viewport region to render the scene to"""
        pass


    def render(self):

        ## set viewport region
        self.setViewportRegion()

        ## clear buffers
        GL.glClear(GL.GL_DEPTH_BUFFER_BIT)

        for each in self.systemActors() + self.actors():

            if isinstance(each, Background):

                ## render background
                self.renderBackground(each)

            elif isinstance(each, Floor):

                ## render grid floor
                self.renderGridFloor(each)

            else:
                if not hasattr(each, 'should_be_rendered') or each.should_be_rendered:
                    ## render first pass of the scene
                    self.renderFirstPass(each)

                    ## render second pass of the scene
                    self.renderSecondPass(each)
