import math

from PyQt5.QtCore import QObject
from PyQt5.QtGui import QVector3D, QVector4D, QMatrix4x4, QQuaternion

##  Base camera class
class Camera(QObject):

    class Lens:
        Perspective = 0
        Orthographic = 1


    def __init__(self, **kwargs):
        """Initialize camera object."""
        super(Camera, self).__init__()

        self._name = kwargs.get("name", "main")

        self._lens = kwargs.get("lens", Camera.Lens.Perspective)
        self._position = kwargs.get("position", QVector3D(0.0, 0.0, 4.0))
        self._fovy = kwargs.get("fovy", 45.0)
        self._height = kwargs.get("height", 2.0)
        self._near_distance = kwargs.get("near", 0.1)
        self._far_distance = kwargs.get("far", 100.0)

        self._projection_matrix = QMatrix4x4()
        self._view_matrix = QMatrix4x4()
        self._orientation = QMatrix4x4()
        self._rotation = kwargs.get("rotation", QQuaternion())

        self._focal_distance = 5.0
        self._aspect_ratio = 1.0

        self._stored = None

        self._first_person = False


    def copyFrom(self, camera):
        """Copy parameters from other camera"""
        self._name = camera.name
        self._lens = camera.lens
        self._position = camera.position
        self._fovy = camera.heightAngle
        self._height = camera.height
        self._near_distance = camera.nearDistance
        self._far_distance = camera.farDistance

        self._projection_matrix = QMatrix4x4(camera.projectionMatrix.data())
        self._view_matrix = QMatrix4x4(camera.viewMatrix.data())
        self._orientation = QMatrix4x4(camera.orientation.data())
        self._rotation = QQuaternion(camera.rotation.toVector4D())

        self._focal_distance = camera.focalDistance
        self._aspect_ratio = camera.aspectRatio


    def store(self):
        """Save current camera settings"""
        if not self._stored:
            self._stored = Camera()
        self._stored.copyFrom(self)


    def recall(self, aspect=1.0):
        """Recall stored camera settings"""
        if self._stored:
            self.copyFrom(self._stored)
            self._aspect_ratio = aspect


    @property
    def name(self):
        """Returns the name of this camera"""
        return self._name


    @property
    def lens(self):
        """Returns lens type of this camera"""
        return self._lens


    def setLens(self, lens, adjust=False):
        """Sets lens for this camera"""
        if lens != self._lens:

            if adjust:

                if self.lens == Camera.Lens.Perspective:
                    ## switch to orthographic and adjust
                    self._height = 2.0 * self._focal_distance * math.tan(math.radians(self._fovy / 2.0))
                else:
                    ## switch to perspective and adjust
                    direction = self._orientation * QVector3D(0.0, 0.0, -1.0)
                    focal_point = self._position + self._focal_distance * direction
                    self._focal_distance = (self._height / 2.0) / math.tan(math.radians(self._fovy / 2.0))
                    self._position = focal_point - self._focal_distance * direction

            self._lens = lens


    @property
    def position(self):
        """Returns position of this camera in space"""
        return self._position


    def setPosition(self, position):
        """Sets the position of the camera"""
        self._position = position


    @property
    def aspectRatio(self):
        """Returns the aspect ratio of this camera"""
        return self._aspect_ratio


    def setAspectRatio(self, aspect):
        """Sets the aspect ratio of the camera"""
        self._aspect_ratio = aspect


    @property
    def focalDistance(self):
        """Returns the focal distance of this camera"""
        return self._focal_distance


    def setFocalDistance(self, focal_distance):
        """Sets the focal distance of the camera"""
        self._focal_distance = focal_distance


    @property
    def height(self):
        """Returns height of this camera"""
        return self._height


    def setHeight(self, height):
        """Sets the height of the camera"""
        self._height = height


    def scaleHeight(self, scaleFactor):
        """Scales the height of the camera"""
        if self._lens == Camera.Lens.Orthographic:
            self._height *= scaleFactor
        else:
            self._fovy *= scaleFactor


    @property
    def heightAngle(self):
        """Returns height angle of this camera"""
        return self._fovy


    def setHeightAngle(self, fov):
        """Sets the height angle of the camera"""
        self._fovy = fovy


    @property
    def nearDistance(self):
        """Returns distance to the near clipping plane from camera"""
        return self._near_distance


    def setNearDistance(self, near):
        """Sets the distance to the near clipping plane from the camera"""
        self._near_distance = near


    @property
    def farDistance(self):
        """Returns distance to the far clipping plane from camera"""
        return self._far_distance


    def setFarDistance(self, far):
        """Sets the distance to the far clipping plane from the camera"""
        self._far_distance = far


    @property
    def rotation(self):
        """Returns the rotation of this camera"""
        return self._rotation


    def setRotation(self, rotation):
        """Sets the rotation of the camera"""
        self._rotation = rotation


    @property
    def orientation(self):
        """Returns the orientation matrix"""
        return self._orientation


    def setOrientation(self, orientation):
        """Sets the orientation matrix of the camera"""
        self._orientation = orientation


    def pointAt(self, target, up=QVector3D(0.0, 1.0, 0.0)):
        """Sets the view matrix for this camera"""
        self._focal_distance = (target - self._position).length()
        direction = (target - self._position).normalized()
        self.lookAt(direction, up.normalized())


    def lookAt(self, direction, up):
        """Calculate new camera orientation based on camera direction and up vectors"""
        z = -direction
        x = QVector3D.crossProduct(up, z)
        y = QVector3D.crossProduct(z, x)
        self._orientation = QMatrix4x4(
            x[0], x[1], x[2], 0.0,
            y[0], y[1], y[2], 0.0,
            z[0], z[1], z[2], 0.0,
            0.0, 0.0, 0.0, 1.0)


    def cameraMatrixOriginal(self):
        """Calculate camera matrix"""
        camera_matrix = QMatrix4x4()
        if(self._first_person == True):
            camera_matrix.translate(self._position)
            camera_matrix *= self._orientation
        else:
            camera_matrix *= self._orientation
            camera_matrix.translate(self._position)
        return camera_matrix


    def cameraMatrix(self):
        """Calculate camera matrix"""
        camera_matrix = QMatrix4x4()
        camera_matrix *= self._orientation
        if(self._first_person == True):
            camera_matrix.translate(self._position)
            camera_matrix.rotate(self._rotation)
        else:
            camera_matrix.rotate(self._rotation)
            camera_matrix.translate(self._position)
        return camera_matrix


    @property
    def viewMatrix(self):
        """Returns view matrix for this camera"""
        return self.cameraMatrix().inverted()[0]


    @property
    def projectionMatrix(self):
        """Returns the projection matrix for this camera"""
        self._projection_matrix.setToIdentity()
        if self._lens == Camera.Lens.Orthographic:
            xradius = 0.5 * self._height * self._aspect_ratio
            yradius = 0.5 * self._height
            self._projection_matrix.ortho(-xradius, xradius, -yradius, yradius, self._near_distance, self._far_distance)
        else:
            self._projection_matrix.perspective(self._fovy, self._aspect_ratio, self._near_distance, self._far_distance)
        return self._projection_matrix
