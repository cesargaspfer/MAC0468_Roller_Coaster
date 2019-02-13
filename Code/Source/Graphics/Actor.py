import math
import ctypes
import numpy as np

from PyQt5.QtCore import QObject
from PyQt5.QtGui import QMatrix4x4, QVector3D, QVector4D, QOpenGLShader, QOpenGLShaderProgram, QOpenGLBuffer, QOpenGLVertexArrayObject
from PyQt5.QtWidgets import QOpenGLWidget

from OpenGL import GL
from Source.Graphics.Shaders import Shaders
from Source.Graphics.Material import Material


##  Abstract base class for different actor implementations.
class Actor(QObject):

    class RenderType:
        NoType = 0      ## No special state changes are done.
        Solid = 1       ## Depth testing and depth writing are enabled.
        Transparent = 2 ## Depth testing is enabled, depth writing is disabled.
        Overlay = 3     ## Depth testing is disabled.
        Types = [NoType, Solid, Transparent, Overlay]


    ##  The mode to render objects in. These correspond to OpenGL render modes.
    class RenderMode:
        Points = GL.GL_POINTS
        Lines = GL.GL_LINES
        LineLoop = GL.GL_LINE_LOOP
        LineStrip = GL.GL_LINE_STRIP
        Triangles = GL.GL_TRIANGLES
        TriangleStrip = GL.GL_TRIANGLE_STRIP
        TriangleFan =  GL.GL_TRIANGLE_FAN
        Modes = [Points, Lines, LineLoop, LineStrip, Triangles, TriangleStrip, TriangleFan]


    ## initialization
    def __init__(self, scene, **kwargs):
        """Initialize actor."""
        super(Actor, self).__init__()


        self._isIcosahedron = False
        self._scene = scene
        self._transform = kwargs.get("transform", QMatrix4x4())
        self._render_mode = kwargs.get("mode", Actor.RenderMode.Triangles)
        self._render_type = kwargs.get("type", Actor.RenderType.Solid)
        self._material = kwargs.get("material", Material())
        self._wireframe = kwargs.get("wireframe", Material(diffuse=QVector3D(0.25, 0.25, 0.25)))
        self._viewport = kwargs.get("viewport", (0.0, 0.0, 1.0, 1.0))

        self._name = kwargs.get("name", "Actor"+str(id(self)))
        self._shader_collection = Shaders()

        self._solid_shader = self._shader_collection.uniformMaterialBRDFShader()


        self._solid_flat_shader = self._shader_collection.uniformMaterialBRDFShader()
        self._shader_name = "BRDF"
        self._nolight_solid_shader = self._shader_collection.uniformMaterialBRDFShader()
        self._wireframe_shader = self._shader_collection.uniformMaterialShader()
        self._nolight_wireframe_shader = self._shader_collection.uniformMaterialShader()
        self._active_shader = self._solid_shader
        self._active_material = self._material

        self._vao = QOpenGLVertexArrayObject()
        self._vbo = QOpenGLBuffer(QOpenGLBuffer.VertexBuffer)
        self._ibo = QOpenGLBuffer(QOpenGLBuffer.IndexBuffer)
        self._num_vertices = 0
        self._num_indices = 0

        self._hasNormals = False
        self._hasColors = False
        self._hasTextureCoords = False
        self._hasIndices = False

        self._waves = []

        self._portalInteration = False;
        self._portal1 = []; #vertices
        self._portal2 = []; #vertices

        #self._bbox = None
        self._visible = True
        self._enabled = False
        self._pickable = True
        self._selectable = False
        self._selected = False
        self._highlighted = False
        self._errorMaterial = Material.ruby()
        self._errorHighlight = False
        self._warningMaterial = Material.gold()
        self._warningHighlight = False

        self._pickFactor = 1.0


    def update(self, **kwargs):
        """Update this node"""
        self._transform = kwargs.get("transform", QMatrix4x4())
        self._render_mode = kwargs.get("mode", Actor.RenderMode.Triangles)
        self._render_type = kwargs.get("type", Actor.RenderType.Solid)
        self._material = kwargs.get("material", Material())
        self._wireframe = kwargs.get("wireframe", Material(diffuse=QVector3D(0.25, 0.25, 0.25)))


    def scene(self):
        return self._scene


    @property
    def name(self):
        """Returns the name of this actor"""
        return self._name


    def setName(self, name):
        """Sets this actor's name"""
        self._name = name


    @property
    def material(self):
        """Returns the material of this node"""
        return self._material


    def setTransform(self, xform):
        self._transform = xform


    def transform(self):
        return self._transform


    def position(self):
        xform = self.transform()
        return QVector3D(xform[0,3], xform[1,3], xform[2,3])


    def setPosition(self, pos):
        #print("pos==",pos)
        self._transform = QMatrix4x4()
        self._transform.translate(pos.x(), pos.y(), pos.z())

    def isPickable(self):
        """Sets whether or not this actor is pickable"""
        return self._pickable


    def setPickable(self, value):
        """Sets whether this actor is pickable"""
        self._pickable = value


    def isVisible(self):
        """Sets the visibility of this actor"""
        return self._visible


    def setVisible(self, value):
        """Sets the visibility of this actor"""
        self._visible = value


    def isEnabled(self):
        """Returns whether this actor is enabled or not"""
        return self._enabled


    def setEnabled(self, value):
        """Sets whether this actor is enabled or not"""
        self._enabled = value


    def setSelectable(self, value):
        """Sets whther or not this actor is selectable"""
        self._selectable = value


    def isSelectable(self):
        """Returns true if actor is selectable"""
        return self._selectable


    def setSelected(self, value):
        """Sets selection to value"""
        self._selected = value


    def isSelected(self):
        """Returns true if it is selected"""
        return self._selected


    def setHighlighted(self, value):
        """Sets the highlight value"""
        self._highlighted = value


    def isHighlighted(self):
        """Returns true if it is highlighted"""
        return self._highlighted


    def setErrorMaterial(self, material):
        """Sets the error material"""
        self._errorMaterial = material


    def setErrorHighlight(self, value):
        """Sets the error highlight"""
        self._errorHighlight = value


    def setWarningMaterial(self, material):
        """Sets the error material"""
        self._warningMaterial = material


    def setWarningHighlight(self, value):
        """Sets the warning highlight"""
        self._warningHighlight = value


    @property
    def shaderCollection(self):
        """Returns the shader collection"""
        return self._shader_collection


    @property
    def renderType(self):
        """Returns the rendering type of this actor"""
        return self._render_type


    @property
    def renderMode(self):
        """Returns the rendering mode of this actor"""
        return self._render_mode


    @property
    def solidShader(self):
        """Returns the default solid shader of this actor"""
        return self._solid_shader


    def setSolidShader(self, shader):
        """Sets the solid shader of this actor"""
        self._solid_shader = shader


    @property
    def solidFlatShader(self):
        """Returns the default solid flat shader of this actor"""
        return self._solid_flat_shader


    def setSolidFlatShader(self, shader):
        """Sets the solid flat shader of this actor"""
        self._solid_flat_shader = shader


    @property
    def noLightSolidShader(self):
        """Returns the default no light solid shader of this actor"""
        return self._nolight_solid_shader


    def setNoLightSolidShader(self, shader):
        """Sets the solid shader of this actor"""
        self._nolight_solid_shader = shader


    @property
    def wireframeShader(self):
        """Returns the default wireframe shader of this actor"""
        return self._wireframe_shader


    def setWireframeShader(self, shader):
        """Sets the default wireframe shader of this actor"""
        self._wireframe_shader = shader


    @property
    def noLightWireframeShader(self):
        """Returns the default no light wireframe shader of this actor"""
        return self._nolight_wireframe_shader


    def setNoLightWireframeShader(self, shader):
        """Sets the no light wireframe shader of this actor"""
        self._nolight_wireframe_shader = shader


    @property
    def numberOfVertices(self):
        """Returns the number of vertices of this actor"""
        return self._num_vertices


    @property
    def numberOfIndices(self):
        """Returns the number of indices of this actor"""
        return self._num_indices


    def mapBuffer(self, offset, count, access):
        """Map the given buffer into a numpy array"""
        vbo_ptr = self._vbo.mapRange( offset, count, access )
        vp_array = ctypes.cast(ctypes.c_void_p(int(vbo_ptr)), ctypes.POINTER(ctypes.c_byte * self._vbo.size())).contents
        # Note: we could have returned the raw ctypes.c_byte array instead... see pyglet github for map/unmap classes
        array = np.frombuffer( vp_array, 'B' )
        return array


    def unmapBuffer(self):
        """Update the GPU with new buffer contents"""
        self._vbo.unmap()


    def updateBuffer(self, vertices=None, normals=None, colors=None, texcoords=None, usage=QOpenGLBuffer.StaticDraw):
        """Update buffers"""
        ## list of shaders
        shaders = [self._solid_shader, self._wireframe_shader, self._nolight_solid_shader, self._nolight_wireframe_shader]

        ## bind vao
        self._vao.bind()

        ## define total sizes
        vertices = vertices.tostring()
        total_vertices = len(vertices)
        total_normals = 0
        total_colors = 0
        total_texcoords = 0
        self._num_vertices = total_vertices // (np.dtype(np.float32).itemsize * 3)

        if normals is not None:
            self._hasNormals = True
            normals = normals.tostring()
            total_normals = len(normals)

        if colors is not None:
            self._hasColors = True
            colors = colors.tostring()
            total_colors = len(colors)

        if texcoords is not None:
            self._hasTextureCoords = True
            texcoords = texcoords.tostring()
            total_texcoords = len(texcoords)

        ## create vertex buffer object
        self._vbo.setUsagePattern(usage)
        self._vbo.bind()

        ## populate vertex buffer object with data
        offset = 0
        self._vbo.allocate(total_vertices + total_normals + total_colors + total_texcoords)
        self._vbo.write(offset, vertices, total_vertices)
        for each in shaders:
            each.setAttributeBuffer('position', GL.GL_FLOAT, offset, 3, 3 * np.dtype(np.float32).itemsize)
        offset += total_vertices
        self._offsetNormals = offset

        if self._hasNormals:
            self._vbo.write(offset, normals, total_normals)
            for each in shaders:
                each.setAttributeBuffer('normal', GL.GL_FLOAT, offset, 3, 3 * np.dtype(np.float32).itemsize)
            offset += total_normals
        if self._hasColors:
            self._offsetColors = offset
            self._vbo.write(offset, colors, total_colors)
            for each in shaders:
                each.setAttributeBuffer('color', GL.GL_FLOAT, offset, 3, 3 * np.dtype(np.float32).itemsize)
            offset += total_colors
        if self._hasTextureCoords:
            self._offsetTexCoords = offset
            self._vbo.write(offset, texcoords, total_texcoords)
            for each in shaders:
                each.setAttributeBuffer('texcoord', GL.GL_FLOAT, offset, 2, 2 * np.dtype(np.float32).itemsize)
            offset += total_texcoords

        ## release buffer
        self._vbo.release(QOpenGLBuffer.VertexBuffer)

        ## enable arrays as part of the vao state
        for each in shaders:
            each.enableAttributeArray('position')
        if self._hasNormals:
            for each in shaders:
                each.enableAttributeArray('normal')
        if self._hasColors:
            for each in shaders:
                each.enableAttributeArray('color')
        if self._hasTextureCoords:
            for each in shaders:
                each.enableAttributeArray('texcoord')

        ## release vao
        self._vao.release()


    def create(self, vertices, normals=None, colors=None, texcoords=None, indices=None, usage=QOpenGLBuffer.StaticDraw):
        """Create object vertex arrays and buffers"""

        ## list of shaders
        shaders = [self._solid_shader, self._wireframe_shader, self._nolight_solid_shader, self._nolight_wireframe_shader]



        ## bind vao
        self._vao.create()
        self._vao.bind()

        ## define total sizes
        vertices = vertices.tostring()
        total_vertices = len(vertices)
        total_normals = 0
        total_colors = 0
        total_texcoords = 0
        self._num_vertices = total_vertices // (np.dtype(np.float32).itemsize * 3)
        #print('total vertices=', self._num_vertices)

        if normals is not None:
            self._hasNormals = True
            normals = normals.tostring()
            total_normals = len(normals)

        if colors is not None:
            self._hasColors = True
            colors = colors.tostring()
            total_colors = len(colors)

        if texcoords is not None:
            self._hasTextureCoords = True
            texcoords = texcoords.tostring()
            total_texcoords = len(texcoords)

        if indices is not None:
            self._hasIndices = True
            indices = indices.tostring()
            total_indices = len(indices)
            self._num_indices = total_indices // np.dtype(np.uint32).itemsize
            #print('total indices=', self._num_indices)

        ## create vertex buffer object
        self._vbo.setUsagePattern(usage)
        self._vbo.create()
        self._vbo.bind()

        ## populate vertex buffer object with data
        offset = 0
        self._vbo.allocate(total_vertices + total_normals + total_colors + total_texcoords)
        self._vbo.write(offset, vertices, total_vertices)
        for each in shaders:
            each.setAttributeBuffer('position', GL.GL_FLOAT, offset, 3, 3 * np.dtype(np.float32).itemsize)
        offset += total_vertices
        self._offsetNormals = offset

        if self._hasNormals:
            self._vbo.write(offset, normals, total_normals)
            for each in shaders:
                each.setAttributeBuffer('normal', GL.GL_FLOAT, offset, 3, 3 * np.dtype(np.float32).itemsize)
            offset += total_normals
        if self._hasColors:
            self._offsetColors = offset
            self._vbo.write(offset, colors, total_colors)
            for each in shaders:
                each.setAttributeBuffer('color', GL.GL_FLOAT, offset, 3, 3 * np.dtype(np.float32).itemsize)
            offset += total_colors
        if self._hasTextureCoords:
            self._offsetTexCoords = offset
            self._vbo.write(offset, texcoords, total_texcoords)
            for each in shaders:
                each.setAttributeBuffer('texcoord', GL.GL_FLOAT, offset, 2, 2 * np.dtype(np.float32).itemsize)
            offset += total_texcoords


        ## release buffer
        self._vbo.release(QOpenGLBuffer.VertexBuffer)

        ## enable arrays as part of the vao state
        for each in shaders:
            each.enableAttributeArray('position')
        if self._hasNormals:
            for each in shaders:
                each.enableAttributeArray('normal')
        if self._hasColors:
            for each in shaders:
                each.enableAttributeArray('color')
        if self._hasTextureCoords:
            for each in shaders:
                each.enableAttributeArray('texcoord')

        ## create index buffer object if required by the actor
        if self._hasIndices:
            self._ibo.setUsagePattern(usage)
            self._ibo.create()
            self._ibo.bind()

            self._ibo.allocate(total_indices)
            self._ibo.write(0, indices, total_indices)

        ## release vao
        self._vao.release()

        ## release ibo
        if self._hasIndices:
            self._ibo.release(QOpenGLBuffer.IndexBuffer)




    def setUniformBindings(self, wireframe=False):
        """Sets up uniform shader bindings"""
        normalMatrix = self._transform.normalMatrix()
        self._active_shader.setUniformValue("modelMatrix", self._transform)
        self._active_shader.setUniformValue("viewMatrix", self._scene.camera.viewMatrix)
        self._active_shader.setUniformValue("projectionMatrix", self._scene.camera.projectionMatrix)
        self._active_shader.setUniformValue("normalMatrix", normalMatrix)


        ## bind active material
        if self.isSelectable() and self.isSelected():
            self._active_shader.setUniformValue("selected", 1.0)
        else:
            self._active_shader.setUniformValue("selected", 0.65)

        ## set highlight color
        if self.isHighlighted():
            self._active_shader.setUniformValue("material.emission", QVector3D(0.25, 0.25, 0.25))
        else:
            self._active_shader.setUniformValue("material.emission", self._active_material.emissionColor)
        self._active_shader.setUniformValue("material.ambient", self._active_material.ambientColor)

        ## set the enabled color
        if self.isEnabled():
            self._active_shader.setUniformValue("material.emission", QVector3D(0.25, 0.25, 0.25))
            self._active_shader.setUniformValue("material.diffuse", self._active_material.diffuseColor)
        else:
            self._active_shader.setUniformValue("material.diffuse", self._active_material.diffuseColor)
        self._active_shader.setUniformValue("material.specular", self._active_material.specularColor)
        self._active_shader.setUniformValue("material.shininess", self._active_material.shininess)

        ## set the error and warning colors
        if self._errorHighlight:
            self._active_shader.setUniformValue("material.ambient", self._errorMaterial.ambientColor)
            self._active_shader.setUniformValue("material.diffuse", self._errorMaterial.diffuseColor)
            self._active_shader.setUniformValue("material.specular", self._errorMaterial.specularColor)
            self._active_shader.setUniformValue("material.shininess", self._errorMaterial.shininess)
        if self._warningHighlight:
            self._active_shader.setUniformValue("material.ambient", self._warningMaterial.ambientColor)
            self._active_shader.setUniformValue("material.diffuse", self._warningMaterial.diffuseColor)
            self._active_shader.setUniformValue("material.specular", self._warningMaterial.specularColor)
            self._active_shader.setUniformValue("material.shininess", self._warningMaterial.shininess)

        if self._shader_name == "BRDF":
            self._active_shader.setUniformValue("material.metallic", self._active_material.metallic)
            self._active_shader.setUniformValue("material.roughness", self._active_material.roughness)
            self._active_shader.setUniformValue("material.cbase", self._active_material.cbase)

        self._active_shader.setUniformValue("spike", self._active_material._spike)
        self._active_shader.setUniformValue("h", self._active_material._spike_h)
        self._active_shader.setUniformValue("w", self._active_material._spike_w)


        self._active_shader.setUniformValue("portalIteration", self._portalInteration)


        ## bind lights
        camera_position = QVector4D(self._scene.camera.position[0], self._scene.camera.position[1], self._scene.camera.position[2], 1.0)
        lightpos = self._scene.light._position
        if self._scene.light.headlight:
            if self._scene.light.directional:
                self._active_shader.setUniformValue("lightPosition", QVector4D(lightpos.x(), lightpos.y(), lightpos.z(), 0.0))
            elif self._scene.light.hemispheric:
                self._active_shader.setUniformValue("lightPosition", QVector4D(lightpos.x(), lightpos.y(), lightpos.z(), 0.2))
            else:
                self._active_shader.setUniformValue("lightPosition", QVector4D(lightpos.x(), lightpos.y(), lightpos.z(), 1.0))
        else:
            self._active_shader.setUniformValue("lightPosition", self._scene.camera.viewMatrix * self._scene.light.position)

        self._active_shader.setUniformValue("light.ambient", self._scene.light.ambientColor)
        self._active_shader.setUniformValue("light.diffuse", self._scene.light.diffuseColor)
        self._active_shader.setUniformValue("light.specular", self._scene.light.specularColor)
        self._active_shader.setUniformValue("lightAttenuation", self._scene.light.attenuation)
        if self._shader_name == "BRDF":
            self._active_shader.setUniformValue("light.color", self._scene.light.color)
            self._active_shader.setUniformValue("light.lradious", self._scene.light.lradious)
            self._active_shader.setUniformValue("light.aconst", self._scene.light.aconst)
            self._active_shader.setUniformValue("light.alinear", self._scene.light.alinear)
            self._active_shader.setUniformValue("light.aquad", self._scene.light.aquad)
            self._active_shader.setUniformValue("light.csky", self._scene.light.csky)
            self._active_shader.setUniformValue("light.cground", self._scene.light.cground)
            if self._isIcosahedron:
                self._active_shader.setUniformValue("isIcosahedron", 1)
            else:
                self._active_shader.setUniformValue("isIcosahedron", 0)

    ## This should set up any required state before any actual rendering happens.
    def beginRendering(self, draw_style, lighting, shading, passNumber):
        ## determine right shader to bind
        if lighting:
            if draw_style == GL.GL_LINE:
                self._active_shader = self._wireframe_shader
                self._active_material = self._material if passNumber == 0 else self._wireframe
            else:
                if shading == GL.GL_SMOOTH:
                    self._active_shader = self._solid_shader
                else:
                    self._active_shader = self._solid_flat_shader
                self._active_material = self._material
        else:
            if draw_style == GL.GL_LINE:
                self._active_shader = self._nolight_wireframe_shader
                self._active_material = self._material if passNumber == 0 else self._wireframe
            else:
                self._active_shader = self._nolight_solid_shader
                self._active_material = self._material

        GL.glPolygonMode(GL.GL_FRONT_AND_BACK, draw_style)

        ## determine rendering type to use
        if self._render_type == self.RenderType.Solid:
            GL.glEnable(GL.GL_DEPTH_TEST)
            GL.glDepthMask(GL.GL_TRUE)
        elif self._render_type == self.RenderType.Transparent:
            GL.glEnable(GL.GL_DEPTH_TEST)
            GL.glDepthMask(GL.GL_FALSE)
        elif self._render_type == self.RenderType.Overlay:
            GL.glDisable(GL.GL_DEPTH_TEST)

        ## bind shader
        self._active_shader.bind()

        ## set up uniform variables
        self.setUniformBindings()

        ## bind shader
        self._vao.bind()


    def render(self):
        """Render this actor"""
        raise NotImplementedError("render() must be implemented in child class")


    def endRendering(self):
        """Finished rendering, clean yourself up"""

        ## unbind vao
        self._vao.release()

        ## unbind shader
        self._active_shader.release()

    def pickFactor(self):
        """Returns the pick factor for intersection calculations"""
        return self._pickFactor


    def setPickFactor(self, value):
        """Sets the pick factor for intersection calculations"""
        self._pickFactor = value


    def intersect(self, ray):
        """Returns intersection if any"""
        tMin = -math.inf
        tMax = math.inf
        obb_xform = self.transform()
        obb_center = QVector3D(obb_xform[0,3], obb_xform[1,3], obb_xform[2,3])
        point = obb_center - ray.origin()
        for i in range(3):
            axis = QVector3D(obb_xform[0,i], obb_xform[1,i], obb_xform[2,i]).normalized()
            half_length = QVector3D(obb_xform[i,0], obb_xform[i,1], obb_xform[i,2]).length() / 2.0
            e = QVector3D.dotProduct(axis, point)
            f = QVector3D.dotProduct(axis, ray.direction())
            if abs(f) > 10E-6:
                t1 = (e + half_length*self._pickFactor) / f
                t2 = (e - half_length*self._pickFactor) / f
                if t1 > t2:
                    w=t1; t1=t2; t2=w
                if t1 > tMin:
                    tMin = t1
                if t2 < tMax:
                    tMax = t2
                if tMin > tMax:
                    return (False, math.inf)
                if tMax < 0:
                    return (False, math.inf)
            elif -e-half_length > 0.0 or -e+half_length < 0.0:
                return (False, math.inf)
        if tMin > 0:
            return (True, tMin)
        return (True, tMax)
