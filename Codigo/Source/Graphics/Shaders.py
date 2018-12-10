from PyQt5.QtCore import QObject
from PyQt5.QtGui import QOpenGLShader, QOpenGLShaderProgram

## singleton shader class
class Shaders(QObject):

    __instance = None

    def __new__(cls):
        if Shaders.__instance is None:
            Shaders.__instance = QObject.__new__(cls)
            Shaders.__instance.initialize()
        return Shaders.__instance


    def initialize(self):
        """Create shader programs"""

        ## create background shader program
        self.__instance._backgroundShader = QOpenGLShaderProgram()
        self.__instance._backgroundShader.addShaderFromSourceCode(QOpenGLShader.Vertex, Shaders.attributeColorNoTransformVertexShader())
        self.__instance._backgroundShader.addShaderFromSourceCode(QOpenGLShader.Fragment, Shaders.simpleFragmentShader())
        self.__instance._backgroundShader.link()

        ## create uniform material shader with no lighting
        self.__instance._wireframeMaterialShader = QOpenGLShaderProgram()
        self.__instance._wireframeMaterialShader.addShaderFromSourceCode(QOpenGLShader.Vertex, Shaders.wireframeMaterialVertexShader())
        self.__instance._wireframeMaterialShader.addShaderFromSourceCode(QOpenGLShader.Fragment, Shaders.simpleFragmentShader())
        self.__instance._wireframeMaterialShader.link()

        ## create uniform material shader with no lighting
        self.__instance._uniformMaterialShader = QOpenGLShaderProgram()
        self.__instance._uniformMaterialShader.addShaderFromSourceCode(QOpenGLShader.Vertex, Shaders.uniformMaterialVertexShader())
        self.__instance._uniformMaterialShader.addShaderFromSourceCode(QOpenGLShader.Fragment, Shaders.simpleFragmentShader())
        self.__instance._uniformMaterialShader.link()

        ## create uniform material with no lighting calculations
        self.__instance._attributeColorShader = QOpenGLShaderProgram()
        self.__instance._attributeColorShader.addShaderFromSourceCode(QOpenGLShader.Vertex, Shaders.attributeColorTransformVertexShader())
        self.__instance._attributeColorShader.addShaderFromSourceCode(QOpenGLShader.Fragment, Shaders.simpleFragmentShader())
        self.__instance._attributeColorShader.link()

        ## create Phong mesh shader
        self.__instance._uniformMaterialPhongShader = QOpenGLShaderProgram()
        self.__instance._uniformMaterialPhongShader.addShaderFromSourceCode(QOpenGLShader.Vertex, Shaders.uniformMaterialPhongVertexShader())
        self.__instance._uniformMaterialPhongShader.addShaderFromSourceCode(QOpenGLShader.Fragment, Shaders.uniformMaterialPhongFragmentShader())
        self.__instance._uniformMaterialPhongShader.link()

        ## create color-based Phong mesh shader
        self.__instance._attributeColorPhongShader = QOpenGLShaderProgram()
        self.__instance._attributeColorPhongShader.addShaderFromSourceCode(QOpenGLShader.Vertex, Shaders.attributeMaterialPhongVertexShader())
        self.__instance._attributeColorPhongShader.addShaderFromSourceCode(QOpenGLShader.Fragment, Shaders.attributeMaterialPhongFragmentShader())
        self.__instance._attributeColorPhongShader.link()

        ## create Phong mesh shader
        self.__instance._uniformMaterialPhongFlatShader = QOpenGLShaderProgram()
        self.__instance._uniformMaterialPhongFlatShader.addShaderFromSourceCode(QOpenGLShader.Vertex, Shaders.uniformMaterialPhongVertexFlatShader())
        self.__instance._uniformMaterialPhongFlatShader.addShaderFromSourceCode(QOpenGLShader.Fragment, Shaders.uniformMaterialPhongFragmentFlatShader())
        self.__instance._uniformMaterialPhongFlatShader.link()

        ## create color-based Phong mesh shader
        self.__instance._attributeColorPhongFlatShader = QOpenGLShaderProgram()
        self.__instance._attributeColorPhongFlatShader.addShaderFromSourceCode(QOpenGLShader.Vertex, Shaders.attributeMaterialPhongVertexFlatShader())
        self.__instance._attributeColorPhongFlatShader.addShaderFromSourceCode(QOpenGLShader.Fragment, Shaders.attributeMaterialPhongFragmentFlatShader())
        self.__instance._attributeColorPhongFlatShader.link()

        ## create BRDF shaders
        ## create BRDF mesh shader
        self.__instance._uniformMaterialBRDFShader = QOpenGLShaderProgram()
        self.__instance._uniformMaterialBRDFShader.addShaderFromSourceCode(QOpenGLShader.Vertex, Shaders.uniformMaterialBRDFVertexShader())
        self.__instance._uniformMaterialBRDFShader.addShaderFromSourceCode(QOpenGLShader.Fragment, Shaders.uniformMaterialBRDFFragmentShader())
        self.__instance._uniformMaterialBRDFShader.link()

        # flat BRDF shader
        self.__instance._uniformMaterialBRDFFlatShader = QOpenGLShaderProgram()
        self.__instance._uniformMaterialBRDFFlatShader.addShaderFromSourceCode(QOpenGLShader.Vertex, Shaders.uniformMaterialBRDFVertexFlatShader())
        self.__instance._uniformMaterialBRDFFlatShader.addShaderFromSourceCode(QOpenGLShader.Fragment, Shaders.uniformMaterialBRDFFragmentFlatShader())
        self.__instance._uniformMaterialBRDFFlatShader.link()


        ## create color-based BRDF mesh shader
        self.__instance._attributeColorBRDFShader = QOpenGLShaderProgram()
        self.__instance._attributeColorBRDFShader.addShaderFromSourceCode(QOpenGLShader.Vertex, Shaders.attributeMaterialBRDFVertexShader())
        self.__instance._attributeColorBRDFShader.addShaderFromSourceCode(QOpenGLShader.Fragment, Shaders.attributeMaterialBRDFFragmentShader())
        self.__instance._attributeColorBRDFShader.link()


        ## create simple textured-based mesh shader
        self.__instance._texturedShader = QOpenGLShaderProgram()
        self.__instance._texturedShader.addShaderFromSourceCode(QOpenGLShader.Vertex, Shaders.texturedVertexShader())
        self.__instance._texturedShader.addShaderFromSourceCode(QOpenGLShader.Fragment, Shaders.texturedFragmentShader())
        self.__instance._texturedShader.link()

        ## create simple textured-based mesh flat shader
        self.__instance._texturedFlatShader = QOpenGLShaderProgram()
        self.__instance._texturedFlatShader.addShaderFromSourceCode(QOpenGLShader.Vertex, Shaders.texturedVertexFlatShader())
        self.__instance._texturedFlatShader.addShaderFromSourceCode(QOpenGLShader.Fragment, Shaders.texturedFragmentFlatShader())
        self.__instance._texturedFlatShader.link()
#----------------------------

        ## create BRDF mesh shader with texture
        self.__instance._textureBRDFShader = QOpenGLShaderProgram()
        self.__instance._textureBRDFShader.addShaderFromSourceCode(QOpenGLShader.Vertex, Shaders.textureBRDFVertexShader())
        self.__instance._textureBRDFShader.addShaderFromSourceCode(QOpenGLShader.Fragment, Shaders.textureBRDFFragmentShader())
        self.__instance._textureBRDFShader.link()

        ## create BRDF mesh shader with texture flat
        self.__instance._textureBRDFFlatShader = QOpenGLShaderProgram()
        self.__instance._textureBRDFFlatShader.addShaderFromSourceCode(QOpenGLShader.Vertex, Shaders.textureBRDFFlatVertexShader())
        self.__instance._textureBRDFFlatShader.addShaderFromSourceCode(QOpenGLShader.Fragment, Shaders.textureBRDFFlatFragmentShader())
        self.__instance._textureBRDFFlatShader.link()

        ## create nolight mesh shader with texture
        self.__instance._textureNoLightShader = QOpenGLShaderProgram()
        self.__instance._textureNoLightShader.addShaderFromSourceCode(QOpenGLShader.Vertex, Shaders.textureNoLightVertexShader())
        self.__instance._textureNoLightShader.addShaderFromSourceCode(QOpenGLShader.Fragment, Shaders.textureNoLightFragmentShader())
        self.__instance._textureNoLightShader.link()

#----------------------------------------------------------TextureBRDF shaders ----------------------------------------------------------
    @classmethod
    def textureBRDFVertexShader(cls):
        vertexShaderSource = """
        #version 330
        layout(location = 0) in vec3 position;
        layout(location = 1) in vec3 normal;
        layout(location = 3) in vec2 texcoord;

        struct Light {
            vec3 ambient;
            vec3 diffuse;
            vec3 specular;
            vec3 color;
            vec3 csky;
            vec3 cground;
            float lradious;
            float aconst;
            float alinear;
            float aquad;
        };

        uniform mat4 modelMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 projectionMatrix;
        uniform mat3 normalMatrix;
        uniform vec4 lightPosition;
        uniform vec3 lightAttenuation;
        uniform Light light;

        smooth out vec4 vertexNormal;
        smooth out vec4 vertexPosition;
        smooth out vec3 lightDirection;
        smooth out float attenuation;
        smooth out vec3 lightColor;
        smooth out vec2 texCoord_;
        out vec2 utex;
        out vec2 vtex;

        void main()
        {
            texCoord_ = texcoord;
            utex = vec2(fract(texcoord.x), fract(texcoord.x + 0.5) - 0.5);
            vtex = vec2(fract(texcoord.y), fract(texcoord.y + 0.5) - 0.5);

            vertexPosition = viewMatrix * modelMatrix * vec4(position, 1.0);
            vertexNormal = viewMatrix * vec4(normalMatrix * normal, 0.0);
            lightColor = light.color;

            if (lightPosition.w <= 0.0) { //Directional light
                lightDirection = normalize(lightPosition.xyz);
                attenuation = 1.0;
            } else if (lightPosition.w == 0.2) {
                lightDirection = vertexNormal.xyz;
                lightColor = mix(light.cground, light.csky, clamp(vertexNormal.y*0.5 + 0.5, 0., 1.));
                attenuation = 1.0;
            } else {
                lightDirection = normalize(lightPosition.xyz - vertexPosition.xyz);
                float distance = length(lightPosition.xyz - vertexPosition.xyz);

                float dem = light.aconst + light.alinear*distance + light.aquad*distance*distance;
                float tlr = distance/light.lradious;
                float clmp = clamp((tlr*tlr)*(tlr*tlr), 0., 1.);
                attenuation = (clmp)*(clmp)/dem;
            }
            gl_Position = projectionMatrix * vertexPosition;

        }
        """
        return vertexShaderSource


    @classmethod
    def textureBRDFFragmentShader(cls):
        fragmentShaderSource = """
        #version 330

        struct Material {
            vec3 emission;
            vec3 ambient;
            vec3 diffuse;
            vec3 specular;
            float shininess;
            float roughness;
            float metallic;
            vec3 cbase;
        };

        struct UseTextures {
            bool baseColor;
            bool specular;
            bool roughness;
            bool normals;
            bool metalness;
        };

        const float pi = 3.1415927;
        const vec3 one3 = vec3(1., 1., 1.);

        smooth in vec4 vertexNormal;
        smooth in vec4 vertexPosition;
        smooth in vec3 lightDirection;
        smooth in float attenuation;
        smooth in vec3 lightColor;
        smooth in vec2 texCoord_;
        in vec2 utex;
        in vec2 vtex;


        uniform Material material;
        uniform sampler2D texBaseColor;
        uniform sampler2D texRoughness;
        uniform sampler2D texMetalness;
        uniform sampler2D texSpecular;
        uniform sampler2D texNormals;
        uniform UseTextures useTextures;
        uniform int isIcosahedron;

        out vec4 fragColor;

        void main()
        {
            vec2 texCoord;
            if (isIcosahedron == 1)
            {
                texCoord.x = (fwidth(utex.x) <= fwidth(utex.y) )? utex.x: utex.y;
                texCoord.y = (fwidth(vtex.x) <= fwidth(vtex.y) )? vtex.x: vtex.y;
            }
            else
                texCoord = texCoord_;

            float roughness = useTextures.roughness ? texture(texRoughness, texCoord).r : material.roughness;
            float metallic = useTextures.metalness ? texture(texMetalness, texCoord).r : material.metallic;
            vec3 cbase = useTextures.baseColor ? texture(texBaseColor, texCoord).rgb : material.cbase;
            vec3 specular = useTextures.specular ? texture(texSpecular, texCoord).rgb : material.specular;


            vec3 cdiff = (1 - metallic)*cbase;
            vec3 cspec = mix(0.08*specular, cbase, metallic);
            vec3 N = normalize(vertexNormal.xyz) ;
            vec3 L = normalize(lightDirection);
            vec3 V = normalize(-vertexPosition.xyz);
            vec3 H = normalize(L + V);
            vec3 T;

            //normal mapping. Code from: https://www.opengl.org/discussion_boards/showthread.php/162857-Computing-the-tangent-space-in-the-fragment-shader
            if (useTextures.normals) {
                	vec3 t_normal = texture2D(texNormals, texCoord).rgb*2.0 - 1.0;
                	// compute tangent T and bitangent B
                	vec3 Q1 = dFdx(vertexPosition.xyz);
                	vec3 Q2 = dFdy(vertexPosition.xyz);
                	vec2 st1 = dFdx(texCoord);
                	vec2 st2 = dFdy(texCoord);
                	vec3 T = normalize(Q1*st2.t - Q2*st1.t);
                	vec3 B = normalize(-Q1*st2.s + Q2*st1.s);

                	// the transpose of texture-to-eye space matrix
                	mat3 TBN = mat3(T, B, vertexNormal);

                	// transform the normal to eye space
                	N = t_normal*TBN;
            }

            // diffuse term
            vec3 diffuse = cdiff/pi;

            //specular
            float alpha = roughness*roughness;
            float nhdot = dot(N, H);
            float vhdot = dot(V, H);
            float D = (alpha*alpha)/(pi*( (nhdot*nhdot)*(alpha*alpha - 1) + 1 ) * ( (nhdot*nhdot)*(alpha*alpha - 1) + 1 ) );
            vec3  F = cspec + (one3 - cspec)*exp2((-5.55473*vhdot - 6.98316)*(vhdot));
            float nvdot = dot(N, V);
            float nldot = max(dot(N, L), 0.0);
            float k = (roughness + 1)*(roughness + 1)/8;
            float G1 = nldot/(nldot*(1 - k) + k);
            float G2 = nvdot/(nvdot*(1 - k) + k);
            float G  = G1*G2;
            vec3 s = (D*F*G)/(4*nldot*nvdot);

            // final color
            vec3 cfinal = attenuation*(lightColor*nldot*(diffuse + s));
            fragColor = vec4(cfinal, 1.0);
        }
        """
        return fragmentShaderSource


    @classmethod
    def textureBRDFFlatVertexShader(cls):
        vertexShaderSource = """
        #version 330
        layout(location = 0) in vec3 position;
        layout(location = 1) in vec3 normal;
        layout(location = 3) in vec2 texcoord;

        struct Light {
            vec3 ambient;
            vec3 diffuse;
            vec3 specular;
            vec3 color;
            vec3 csky;
            vec3 cground;
            float lradious;
            float aconst;
            float alinear;
            float aquad;
        };

        uniform mat4 modelMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 projectionMatrix;
        uniform mat3 normalMatrix;
        uniform vec4 lightPosition;
        uniform vec3 lightAttenuation;
        uniform Light light;

        flat out vec4 vertexNormal;
        flat out vec4 vertexPosition;
        flat out vec3 lightDirection;
        flat out float attenuation;
        flat out vec3 lightColor;
        flat out vec2 texCoord_;
        flat out vec2 utex;
        flat out vec2 vtex;

        void main()
        {
            texCoord_ = texcoord;
            utex = vec2(fract(texcoord.x), fract(texcoord.x + 0.5) - 0.5);
            vtex = vec2(fract(texcoord.y), fract(texcoord.y + 0.5) - 0.5);
            vertexPosition = viewMatrix * modelMatrix * vec4(position, 1.0);
            vertexNormal = viewMatrix * vec4(normalMatrix * normal, 0.0);
            lightColor = light.color;

            if (lightPosition.w <= 0.0) { //Directional light
                lightDirection = normalize(lightPosition.xyz);
                attenuation = 1.0;
            } else if (lightPosition.w == 0.2) {
                lightDirection = vertexNormal.xyz;
                lightColor = mix(light.cground, light.csky, clamp(vertexNormal.y*0.5 + 0.5, 0., 1.));
                attenuation = 1.0;
            } else {
                lightDirection = normalize(lightPosition.xyz - vertexPosition.xyz);
                float distance = length(lightPosition.xyz - vertexPosition.xyz);

                float dem = light.aconst + light.alinear*distance + light.aquad*distance*distance;
                float tlr = distance/light.lradious;
                float clmp = clamp((tlr*tlr)*(tlr*tlr), 0., 1.);
                attenuation = (clmp)*(clmp)/dem;
            }
            gl_Position = projectionMatrix * vertexPosition;

        }
        """
        return vertexShaderSource


    @classmethod
    def textureBRDFFlatFragmentShader(cls):
        fragmentShaderSource = """
        #version 330

        struct Material {
            vec3 emission;
            vec3 ambient;
            vec3 diffuse;
            vec3 specular;
            float shininess;
            float roughness;
            float metallic;
            vec3 cbase;
        };

        struct UseTextures {
            bool baseColor;
            bool specular;
            bool roughness;
            bool normals;
            bool metalness;
        };

        const float pi = 3.1415927;
        const vec3 one3 = vec3(1., 1., 1.);

        flat in vec4 vertexNormal;
        flat in vec4 vertexPosition;
        flat in vec3 lightDirection;
        flat in float attenuation;
        flat in vec3 lightColor;
        flat in vec2 texCoord_;
        flat in vec2 utex;
        flat in vec2 vtex;

        uniform Material material;
        uniform sampler2D texBaseColor;
        uniform sampler2D texRoughness;
        uniform sampler2D texMetalness;
        uniform sampler2D texSpecular;
        uniform UseTextures useTextures;
        uniform int isIcosahedron;

        out vec4 fragColor;

        void main()
        {
            vec2 texCoord;
            if (isIcosahedron == 1)
            {
                texCoord.x = (fwidth(utex.x) <= fwidth(utex.y) )? utex.x: utex.y;
                texCoord.y = (fwidth(vtex.x) <= fwidth(vtex.y) )? vtex.x: vtex.y;
            }
            else
                texCoord = texCoord_;

            float roughness = useTextures.roughness ? texture(texRoughness, texCoord).r : material.roughness;
            float metallic = useTextures.metalness ? texture(texMetalness, texCoord).r : material.metallic;
            vec3 cbase = useTextures.baseColor ? texture(texBaseColor, texCoord).rgb : material.cbase;
            vec3 specular = useTextures.specular ? texture(texSpecular, texCoord).rgb : material.specular;


            vec3 cdiff = (1 - metallic)*cbase;
            vec3 cspec = mix(0.08*specular, cbase, metallic);
            vec3 N = normalize(vertexNormal.xyz) ;
            vec3 L = normalize(lightDirection);
            vec3 V = normalize(-vertexPosition.xyz);
            vec3 H = normalize(L + V);
            vec3 T;

            // diffuse term
            vec3 diffuse = cdiff/pi;

            //specular
            float alpha = roughness*roughness;
            float nhdot = dot(N, H);
            float vhdot = dot(V, H);
            float D = (alpha*alpha)/(pi*( (nhdot*nhdot)*(alpha*alpha - 1) + 1 ) * ( (nhdot*nhdot)*(alpha*alpha - 1) + 1 ) );
            vec3  F = cspec + (one3 - cspec)*exp2((-5.55473*vhdot - 6.98316)*(vhdot));
            float nvdot = dot(N, V);
            float nldot = max(dot(N, L), 0.0);
            float k = (roughness + 1)*(roughness + 1)/8;
            float G1 = nldot/(nldot*(1 - k) + k);
            float G2 = nvdot/(nvdot*(1 - k) + k);
            float G  = G1*G2;
            vec3 s = (D*F*G)/(4*nldot*nvdot);

            // final color
            vec3 cfinal = attenuation*(lightColor*nldot*(diffuse + s));
            fragColor = vec4(cfinal, 1.0);
        }
        """
        return fragmentShaderSource

    @classmethod
    def textureNoLightVertexShader(cls):
        vertexShaderSource = """
        #version 330
        layout(location = 0) in vec3 position;
        layout(location = 3) in vec2 texcoord;

        smooth out vec2 texCoord_;
        smooth out vec2 utex;
        smooth out vec2 vtex;

        uniform mat4 modelMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 projectionMatrix;

        void main()
        {
            texCoord_ = texcoord;
            utex = vec2(fract(texcoord.x), fract(texcoord.x + 0.5) - 0.5);
            vtex = vec2(fract(texcoord.y), fract(texcoord.y + 0.5) - 0.5);
            gl_Position = projectionMatrix * (viewMatrix * modelMatrix * vec4(position, 1.0));
        }
        """
        return vertexShaderSource


    @classmethod
    def textureNoLightFragmentShader(cls):
        fragmentShaderSource = """
        #version 330

        struct Material {
            vec3 emission;
            vec3 ambient;
            vec3 diffuse;
            vec3 specular;
            float shininess;
            float roughness;
            float metallic;
            vec3 cbase;
        };

        struct UseTextures {
            bool baseColor;
            bool specular;
            bool roughness;
            bool normals;
            bool metalness;
        };

        smooth in vec2 texCoord_;
        smooth in vec2 utex;
        smooth in vec2 vtex;

        uniform Material material;
        uniform sampler2D texBaseColor;
        uniform UseTextures useTextures;
        uniform int isIcosahedron;

        out vec4 fragColor;

        void main()
        {
            vec2 texCoord;
            if (isIcosahedron == 1)
            {
                texCoord.x = (fwidth(utex.x) <= fwidth(utex.y) )? utex.x: utex.y;
                texCoord.y = (fwidth(vtex.x) <= fwidth(vtex.y) )? vtex.x: vtex.y;
            }
            else
                texCoord = texCoord_;

            vec3 cbase = useTextures.baseColor ? texture(texBaseColor, texCoord).rgb : material.cbase;

            // final color
            fragColor = vec4(cbase, 1.0);
        }
        """
        return fragmentShaderSource


#----------------------------------------------------------------------------------------------------------------------------------------------------

    @classmethod
    def uniformMaterialBRDFVertexShader(cls):
        vertexShaderSource = """
        #version 330
        layout(location = 0) in vec3 position;
        layout(location = 1) in vec3 normal;

        struct Light {
            vec3 ambient;
            vec3 diffuse;
            vec3 specular;
            vec3 color;
            vec3 csky;
            vec3 cground;
            float lradious;
            float aconst;
            float alinear;
            float aquad;
        };

        uniform mat4 modelMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 projectionMatrix;
        uniform mat3 normalMatrix;
        uniform vec4 lightPosition;
        uniform vec3 lightAttenuation;
        uniform Light light;

        smooth out vec4 vertexNormal;
        smooth out vec4 vertexPosition;
        smooth out vec3 lightDirection;
        smooth out float attenuation;
        smooth out vec3 lightColor;

        void main()
        {
            vertexPosition = viewMatrix * modelMatrix * vec4(position, 1.0);
            vertexNormal = viewMatrix * vec4(normalMatrix * normal, 0.0);
            lightColor = light.color;

            if (lightPosition.w <= 0.0) { //Directional light
                lightDirection = normalize(lightPosition.xyz);
                attenuation = 1.0;
            } else if (lightPosition.w == 0.2) {
                lightDirection = vertexNormal.xyz;
                lightColor = mix(light.cground, light.csky, clamp(vertexNormal.y*0.5 + 0.5, 0., 1.));
                attenuation = 1.0;
            } else {
                lightDirection = normalize(lightPosition.xyz - vertexPosition.xyz);
                float distance = length(lightPosition.xyz - vertexPosition.xyz);

                float dem = light.aconst + light.alinear*distance + light.aquad*distance*distance;
                float tlr = distance/light.lradious;
                float clmp = clamp((tlr*tlr)*(tlr*tlr), 0., 1.);
                attenuation = (clmp)*(clmp)/dem;
            }
            gl_Position = projectionMatrix * vertexPosition;

        }
        """
        return vertexShaderSource


    @classmethod
    def uniformMaterialBRDFFragmentShader(cls):
        fragmentShaderSource = """
        #version 330

        struct Material {
            vec3 emission;
            vec3 ambient;
            vec3 diffuse;
            vec3 specular;
            float shininess;
            float roughness;
            float metallic;
            vec3 cbase;
        };

        const float pi = 3.1415927;
        const vec3 one3 = vec3(1., 1., 1.);

        smooth in vec4 vertexNormal;
        smooth in vec4 vertexPosition;
        smooth in vec3 lightDirection;
        smooth in float attenuation;
        smooth in vec3 lightColor;

        uniform Material material;

        out vec4 fragColor;

        void main()
        {
            vec3 cdiff = (1 - material.metallic)*material.cbase;
            vec3 cspec = mix(0.08*material.specular, material.cbase, material.metallic);
            vec3 N = normalize(vertexNormal.xyz);
            vec3 L = normalize(lightDirection);
            vec3 V = normalize(-vertexPosition.xyz);
            vec3 H = normalize(L + V);

            // diffuse term
            vec3 diffuse = cdiff/pi;

            //specular
            float alpha = material.roughness*material.roughness;
            float nhdot = dot(N, H);
            float vhdot = dot(V, H);
            float D = (alpha*alpha)/(pi*( (nhdot*nhdot)*(alpha*alpha - 1) + 1 ) * ( (nhdot*nhdot)*(alpha*alpha - 1) + 1 ) );
            vec3  F = cspec + (one3 - cspec)*exp2((-5.55473*vhdot - 6.98316)*(vhdot));
            float nvdot = dot(N, V);
            float nldot = max(dot(N, L), 0.0);
            float k = (material.roughness + 1)*(material.roughness + 1)/8;
            float G1 = nldot/(nldot*(1 - k) + k);
            float G2 = nvdot/(nvdot*(1 - k) + k);
            float G  = G1*G2;
            vec3 s = (D*F*G)/(4*nldot*nvdot);

            // final color
            vec3 cfinal = attenuation*lightColor*nldot*(diffuse + s);
            fragColor = vec4(cfinal, 1.0);

        }
        """
        return fragmentShaderSource


    @classmethod
    def attributeMaterialBRDFVertexShader(cls):
        #still uses Phong. This shader do not seems
        #to be used in the program.
        vertexShaderSource = """
        #version 330
        layout(location = 0) in vec3 position;
        layout(location = 1) in vec3 normal;
        layout(location = 2) in vec3 color;
        uniform mat4 modelMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 projectionMatrix;
        uniform mat3 normalMatrix;
        uniform vec4 lightPosition;
        uniform vec3 lightAttenuation;

        smooth out vec4 vertexNormal;
        smooth out vec4 vertexPosition;
        smooth out vec3 lightDirection;
        smooth out float attenuation;
        smooth out vec3 vertexColor;

        void main()
        {
            vertexPosition = viewMatrix * modelMatrix * vec4(position, 1.0);
            vertexNormal = viewMatrix * vec4(normalMatrix * normal, 0.0);
            if (lightPosition.w == 0.0) {
                lightDirection = normalize(lightPosition.xyz);
                attenuation = 1.0;
            } else {
                lightDirection = normalize(lightPosition.xyz - vertexPosition.xyz);
                float distance = length(lightPosition.xyz - vertexPosition.xyz);
                attenuation = 1.0 / (lightAttenuation.x + lightAttenuation.y * distance + lightAttenuation.z * distance * distance);
            }
            vertexColor = color;
            gl_Position = projectionMatrix * vertexPosition;
        }
        """
        return vertexShaderSource


    @classmethod
    def attributeMaterialBRDFFragmentShader(cls):
        fragmentShaderSource = """
        #version 330
        struct Material {
            vec3 emission;
            vec3 ambient;
            vec3 diffuse;
            vec3 specular;
            float shininess;
        };

        struct Light {
            vec3 ambient;
            vec3 diffuse;
            vec3 specular;
        };

        smooth in vec4 vertexNormal;
        smooth in vec4 vertexPosition;
        smooth in vec3 lightDirection;
        smooth in float attenuation;
        smooth in vec3 vertexColor;

        uniform Material material;
        uniform Light light;

        out vec4 fragColor;

        void main()
        {
            // ambient term
            vec3 ambient = material.ambient * light.ambient;

            // diffuse term
            vec3 N = normalize(vertexNormal.xyz);
            vec3 L = normalize(lightDirection);
            vec3 diffuse = light.diffuse * vertexColor * max(dot(N, L), 0.0);

            // specular term
            vec3 E = normalize(-vertexPosition.xyz);
            vec3 R = normalize(-reflect(L, N));
            vec3 specular = light.specular * material.specular * pow(max(dot(R, E), 0.0), material.shininess);

            // final intensity
            vec3 intensity = material.emission + clamp(ambient + attenuation * (diffuse + specular), 0.0, 1.0);
            fragColor = vec4(intensity, 1.0);
        }
        """
        return fragmentShaderSource

    @classmethod
    def uniformMaterialBRDFVertexFlatShader(cls):
        vertexShaderSource = """
        #version 330
        layout(location = 0) in vec3 position;
        layout(location = 1) in vec3 normal;

        struct Light {
            vec3 ambient;
            vec3 diffuse;
            vec3 specular;
            vec3 color;
            vec3 csky;
            vec3 cground;
            float lradious;
            float aconst;
            float alinear;
            float aquad;
        };

        uniform mat4 modelMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 projectionMatrix;
        uniform mat3 normalMatrix;
        uniform vec4 lightPosition;
        uniform vec3 lightAttenuation;
        uniform Light light;

        flat out vec4 vertexNormal;
        smooth out vec4 vertexPosition;
        smooth out vec3 lightDirection;
        smooth out float attenuation;
        smooth out vec3 lightColor;

        void main()
        {
            vertexPosition = viewMatrix * modelMatrix * vec4(position, 1.0);
            vertexNormal = viewMatrix * vec4(normalMatrix * normal, 0.0);
            lightColor = light.color;

            if (lightPosition.w <= 0.0) { //Directional light
                lightDirection = normalize(lightPosition.xyz);
                attenuation = 1.0;
            } else if (lightPosition.w == 0.2) {
                lightDirection = vertexNormal.xyz;
                lightColor = mix(light.cground, light.csky, clamp(vertexNormal.y*0.5 + 0.5, 0., 1.));
                attenuation = 1.0;
            } else {
                lightDirection = normalize(lightPosition.xyz - vertexPosition.xyz);
                float distance = length(lightPosition.xyz - vertexPosition.xyz);

                float dem = light.aconst + light.alinear*distance + light.aquad*distance*distance;
                float tlr = distance/light.lradious;
                float clmp = clamp((tlr*tlr)*(tlr*tlr), 0., 1.);
                attenuation = (clmp)*(clmp)/dem;
            }
            gl_Position = projectionMatrix * vertexPosition;

        }
        """
        return vertexShaderSource

    @classmethod
    def uniformMaterialBRDFFragmentFlatShader(cls):
        fragmentShaderSource = """
        #version 330

        struct Material {
            vec3 emission;
            vec3 ambient;
            vec3 diffuse;
            vec3 specular;
            float shininess;
            float roughness;
            float metallic;
            vec3 cbase;
        };

        const float pi = 3.1415927;
        const vec3 one3 = vec3(1., 1., 1.);

        flat in vec4 vertexNormal;
        smooth in vec4 vertexPosition;
        smooth in vec3 lightDirection;
        smooth in float attenuation;
        smooth in vec3 lightColor;

        uniform Material material;

        out vec4 fragColor;

        void main()
        {
            vec3 cdiff = (1 - material.metallic)*material.cbase;
            vec3 cspec = mix(0.08*material.specular, material.cbase, material.metallic);
            vec3 N = normalize(vertexNormal.xyz);
            vec3 L = normalize(lightDirection);
            vec3 V = normalize(-vertexPosition.xyz);
            vec3 H = normalize(L + V);

            // diffuse term
            vec3 diffuse = cdiff/pi;

            //specular
            float alpha = material.roughness*material.roughness;
            float nhdot = dot(N, H);
            float vhdot = dot(V, H);
            float D = (alpha*alpha)/(pi*( (nhdot*nhdot)*(alpha*alpha - 1) + 1 ) * ( (nhdot*nhdot)*(alpha*alpha - 1) + 1 ) );
            vec3  F = cspec + (one3 - cspec)*exp2((-5.55473*vhdot - 6.98316)*(vhdot));
            float nvdot = dot(N, V);
            float nldot = max(dot(N, L), 0.0);
            float k = (material.roughness + 1)*(material.roughness + 1)/8;
            float G1 = nldot/(nldot*(1 - k) + k);
            float G2 = nvdot/(nvdot*(1 - k) + k);
            float G  = G1*G2;
            vec3 s = (D*F*G)/(4*nldot*nvdot);

            // final color
            vec3 cfinal = attenuation*lightColor*nldot*(diffuse + s);
            fragColor = vec4(cfinal, 1.0);

        }
        """
        return fragmentShaderSource



#----------------------------
    @classmethod
    def uniformMaterialPhongVertexFlatShader(cls):
        vertexShaderSource = """
        #version 330
        layout(location = 0) in vec3 position;
        layout(location = 1) in vec3 normal;
        uniform mat4 modelMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 projectionMatrix;
        uniform mat3 normalMatrix;
        uniform vec4 lightPosition;
        uniform vec3 lightAttenuation;

        flat out vec4 vertexNormal;
        smooth out vec4 vertexPosition;
        smooth out vec3 lightDirection;
        smooth out float attenuation;

        void main()
        {
            vertexPosition = viewMatrix * modelMatrix * vec4(position, 1.0);
            vertexNormal = viewMatrix * vec4(normalMatrix * normal, 0.0);
            if (lightPosition.w == 0.0) {
                lightDirection = normalize(lightPosition.xyz);
                attenuation = 1.0;
            } else {
                lightDirection = normalize(lightPosition.xyz - vertexPosition.xyz);
                float distance = length(lightPosition.xyz - vertexPosition.xyz);
                attenuation = 1.0 / (lightAttenuation.x + lightAttenuation.y * distance + lightAttenuation.z * distance * distance);
            }
            gl_Position = projectionMatrix * vertexPosition;
        }
        """
        return vertexShaderSource


    @classmethod
    def uniformMaterialPhongFragmentFlatShader(cls):
        fragmentShaderSource = """
        #version 330
        struct Material {
            vec3 emission;
            vec3 ambient;
            vec3 diffuse;
            vec3 specular;
            float shininess;
        };

        struct Light {
            vec3 ambient;
            vec3 diffuse;
            vec3 specular;
        };

        flat in vec4 vertexNormal;
        smooth in vec4 vertexPosition;
        smooth in vec3 lightDirection;
        smooth in float attenuation;

        uniform Material material;
        uniform Light light;

        out vec4 fragColor;

        void main()
        {
            // ambient term
            vec3 ambient = material.ambient * light.ambient;

            // diffuse term
            vec3 N = normalize(vertexNormal.xyz);
            vec3 L = normalize(lightDirection);
            vec3 diffuse = light.diffuse * material.diffuse * max(dot(N, L), 0.0);

            // specular term
            vec3 E = normalize(-vertexPosition.xyz);
            vec3 R = normalize(-reflect(L, N));
            vec3 specular = light.specular * material.specular * pow(max(dot(R, E), 0.0), material.shininess);

            // final intensity
            vec3 intensity = material.emission + clamp(ambient + attenuation * (diffuse + specular), 0.0, 1.0);
            fragColor = vec4(intensity, 1.0);
        }
        """
        return fragmentShaderSource


    @classmethod
    def attributeMaterialPhongVertexFlatShader(cls):
        vertexShaderSource = """
        #version 330
        layout(location = 0) in vec3 position;
        layout(location = 1) in vec3 normal;
        layout(location = 2) in vec3 color;
        uniform mat4 modelMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 projectionMatrix;
        uniform mat3 normalMatrix;
        uniform vec4 lightPosition;
        uniform vec3 lightAttenuation;

        flat out vec4 vertexNormal;
        smooth out vec4 vertexPosition;
        smooth out vec3 lightDirection;
        smooth out float attenuation;
        smooth out vec3 vertexColor;

        void main()
        {
            vertexPosition = viewMatrix * modelMatrix * vec4(position, 1.0);
            vertexNormal = viewMatrix * vec4(normalMatrix * normal, 0.0);
            if (lightPosition.w == 0.0) {
                lightDirection = normalize(lightPosition.xyz);
                attenuation = 1.0;
            } else {
                lightDirection = normalize(lightPosition.xyz - vertexPosition.xyz);
                float distance = length(lightPosition.xyz - vertexPosition.xyz);
                attenuation = 1.0 / (lightAttenuation.x + lightAttenuation.y * distance + lightAttenuation.z * distance * distance);
            }
            vertexColor = color;
            gl_Position = projectionMatrix * vertexPosition;
        }
        """
        return vertexShaderSource


    @classmethod
    def attributeMaterialPhongFragmentFlatShader(cls):
        fragmentShaderSource = """
        #version 330
        struct Material {
            vec3 emission;
            vec3 ambient;
            vec3 diffuse;
            vec3 specular;
            float shininess;
        };

        struct Light {
            vec3 ambient;
            vec3 diffuse;
            vec3 specular;
        };

        flat in vec4 vertexNormal;
        smooth in vec4 vertexPosition;
        smooth in vec3 lightDirection;
        smooth in float attenuation;
        smooth in vec3 vertexColor;

        uniform Material material;
        uniform Light light;

        out vec4 fragColor;

        void main()
        {
            // ambient term
            vec3 ambient = material.ambient * light.ambient;

            // diffuse term
            vec3 N = normalize(vertexNormal.xyz);
            vec3 L = normalize(lightDirection);
            vec3 diffuse = light.diffuse * vertexColor * max(dot(N, L), 0.0);

            // specular term
            vec3 E = normalize(-vertexPosition.xyz);
            vec3 R = normalize(-reflect(L, N));
            vec3 specular = light.specular * material.specular * pow(max(dot(R, E), 0.0), material.shininess);

            // final intensity
            vec3 intensity = material.emission + clamp(ambient + attenuation * (diffuse + specular), 0.0, 1.0);
            fragColor = vec4(intensity, 1.0);
        }
        """
        return fragmentShaderSource


    @classmethod
    def uniformMaterialPhongVertexShader(cls):
        vertexShaderSource = """
        #version 330
        layout(location = 0) in vec3 position;
        layout(location = 1) in vec3 normal;
        uniform mat4 modelMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 projectionMatrix;
        uniform mat3 normalMatrix;
        uniform vec4 lightPosition;
        uniform vec3 lightAttenuation;

        smooth out vec4 vertexNormal;
        smooth out vec4 vertexPosition;
        smooth out vec3 lightDirection;
        smooth out float attenuation;

        void main()
        {
            vertexPosition = viewMatrix * modelMatrix * vec4(position, 1.0);
            vertexNormal = viewMatrix * vec4(normalMatrix * normal, 0.0);
            if (lightPosition.w == 0.0) {
                lightDirection = normalize(lightPosition.xyz);
                attenuation = 1.0;
            } else {
                lightDirection = normalize(lightPosition.xyz - vertexPosition.xyz);
                float distance = length(lightPosition.xyz - vertexPosition.xyz);
                attenuation = 1.0 / (lightAttenuation.x + lightAttenuation.y * distance + lightAttenuation.z * distance * distance);
            }
            gl_Position = projectionMatrix * vertexPosition;
        }
        """
        return vertexShaderSource


    @classmethod
    def uniformMaterialPhongFragmentShader(cls):
        fragmentShaderSource = """
        #version 330
        struct Material {
            vec3 emission;
            vec3 ambient;
            vec3 diffuse;
            vec3 specular;
            float shininess;
        };

        struct Light {
            vec3 ambient;
            vec3 diffuse;
            vec3 specular;
        };

        smooth in vec4 vertexNormal;
        smooth in vec4 vertexPosition;
        smooth in vec3 lightDirection;
        smooth in float attenuation;

        uniform Material material;
        uniform Light light;

        out vec4 fragColor;

        void main()
        {
            // ambient term
            vec3 ambient = material.ambient * light.ambient;

            // diffuse term
            vec3 N = normalize(vertexNormal.xyz);
            vec3 L = normalize(lightDirection);
            vec3 diffuse = light.diffuse * material.diffuse * max(dot(N, L), 0.0);

            // specular term
            vec3 E = normalize(-vertexPosition.xyz);
            vec3 R = normalize(-reflect(L, N));
            vec3 specular = light.specular * material.specular * pow(max(dot(R, E), 0.0), material.shininess);

            // final intensity
            vec3 intensity = material.emission + clamp(ambient + attenuation * (diffuse + specular), 0.0, 1.0);
            fragColor = vec4(intensity, 1.0);
        }
        """
        return fragmentShaderSource


    @classmethod
    def attributeMaterialPhongVertexShader(cls):
        vertexShaderSource = """
        #version 330
        layout(location = 0) in vec3 position;
        layout(location = 1) in vec3 normal;
        layout(location = 2) in vec3 color;
        uniform mat4 modelMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 projectionMatrix;
        uniform mat3 normalMatrix;
        uniform vec4 lightPosition;
        uniform vec3 lightAttenuation;

        smooth out vec4 vertexNormal;
        smooth out vec4 vertexPosition;
        smooth out vec3 lightDirection;
        smooth out float attenuation;
        smooth out vec3 vertexColor;

        void main()
        {
            vertexPosition = viewMatrix * modelMatrix * vec4(position, 1.0);
            vertexNormal = viewMatrix * vec4(normalMatrix * normal, 0.0);
            if (lightPosition.w == 0.0) {
                lightDirection = normalize(lightPosition.xyz);
                attenuation = 1.0;
            } else {
                lightDirection = normalize(lightPosition.xyz - vertexPosition.xyz);
                float distance = length(lightPosition.xyz - vertexPosition.xyz);
                attenuation = 1.0 / (lightAttenuation.x + lightAttenuation.y * distance + lightAttenuation.z * distance * distance);
            }
            vertexColor = color;
            gl_Position = projectionMatrix * vertexPosition;
        }
        """
        return vertexShaderSource


    @classmethod
    def attributeMaterialPhongFragmentShader(cls):
        fragmentShaderSource = """
        #version 330
        struct Material {
            vec3 emission;
            vec3 ambient;
            vec3 diffuse;
            vec3 specular;
            float shininess;
        };

        struct Light {
            vec3 ambient;
            vec3 diffuse;
            vec3 specular;
        };

        smooth in vec4 vertexNormal;
        smooth in vec4 vertexPosition;
        smooth in vec3 lightDirection;
        smooth in float attenuation;
        smooth in vec3 vertexColor;

        uniform Material material;
        uniform Light light;

        out vec4 fragColor;

        void main()
        {
            // ambient term
            vec3 ambient = material.ambient * light.ambient;

            // diffuse term
            vec3 N = normalize(vertexNormal.xyz);
            vec3 L = normalize(lightDirection);
            vec3 diffuse = light.diffuse * vertexColor * max(dot(N, L), 0.0);

            // specular term
            vec3 E = normalize(-vertexPosition.xyz);
            vec3 R = normalize(-reflect(L, N));
            vec3 specular = light.specular * material.specular * pow(max(dot(R, E), 0.0), material.shininess);

            // final intensity
            vec3 intensity = material.emission + clamp(ambient + attenuation * (diffuse + specular), 0.0, 1.0);
            fragColor = vec4(intensity, 1.0);
        }
        """
        return fragmentShaderSource


    @classmethod
    def attributeColorNoTransformVertexShader(cls):
        vertexShaderSource = """
        #version 330
        layout(location = 0) in vec3 position;
        layout(location = 2) in vec3 color;
        smooth out vec4 vertexColor;

        void main()
        {
            gl_Position = vec4(position, 1.0);
            vertexColor = vec4(color, 1.0);
        }
        """
        return vertexShaderSource


    @classmethod
    def uniformMaterialVertexShader(cls):
        vertexShaderSource = """
        #version 330

        struct Material {
            vec3 emission;
            vec3 ambient;
            vec3 diffuse;
            vec3 specular;
            float shininess;
        };

        layout(location = 0) in vec3 position;

        uniform mat4 modelMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 projectionMatrix;
        uniform Material material;

        smooth out vec4 vertexColor;

        void main()
        {
            gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(position, 1.0);
            vertexColor = vec4(material.diffuse, 1.0);
        }
        """
        return vertexShaderSource


    @classmethod
    def texturedVertexShader(cls):
        vertexShaderSource = """
        #version 330
        layout(location = 0) in vec3 position;
        layout(location = 1) in vec3 normal;
        layout(location = 2) in vec3 color;
        layout(location = 3) in vec2 texcoord;
        uniform mat4 modelMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 projectionMatrix;
        uniform mat3 normalMatrix;
        uniform vec4 lightPosition;
        uniform vec3 lightAttenuation;

        smooth out vec4 vertexNormal;
        smooth out vec4 vertexPosition;
        smooth out vec3 lightDirection;
        smooth out float attenuation;
        smooth out vec2 textureCoord;

        void main()
        {
            vertexPosition = viewMatrix * modelMatrix * vec4(position, 1.0);
            vertexNormal = viewMatrix * vec4(normalMatrix * normal, 0.0);
            if (lightPosition.w == 0.0) {
                lightDirection = normalize(lightPosition.xyz);
                attenuation = 1.0;
            } else {
                lightDirection = normalize(lightPosition.xyz - vertexPosition.xyz);
                float distance = length(lightPosition.xyz - vertexPosition.xyz);
                attenuation = 1.0 / (lightAttenuation.x + lightAttenuation.y * distance + lightAttenuation.z * distance * distance);
            }
            textureCoord = texcoord;
            gl_Position = projectionMatrix * vertexPosition;
        }
        """
        return vertexShaderSource


    @classmethod
    def texturedVertexFlatShader(cls):
        vertexShaderSource = """
        #version 330
        layout(location = 0) in vec3 position;
        layout(location = 1) in vec3 normal;
        layout(location = 2) in vec3 color;
        layout(location = 3) in vec2 texcoord;
        uniform mat4 modelMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 projectionMatrix;
        uniform mat3 normalMatrix;
        uniform vec4 lightPosition;
        uniform vec3 lightAttenuation;

        flat out vec4 vertexNormal;
        smooth out vec4 vertexPosition;
        smooth out vec3 lightDirection;
        smooth out float attenuation;
        smooth out vec2 textureCoord;

        void main()
        {
            vertexPosition = viewMatrix * modelMatrix * vec4(position, 1.0);
            vertexNormal = viewMatrix * vec4(normalMatrix * normal, 0.0);
            if (lightPosition.w == 0.0) {
                lightDirection = normalize(lightPosition.xyz);
                attenuation = 1.0;
            } else {
                lightDirection = normalize(lightPosition.xyz - vertexPosition.xyz);
                float distance = length(lightPosition.xyz - vertexPosition.xyz);
                attenuation = 1.0 / (lightAttenuation.x + lightAttenuation.y * distance + lightAttenuation.z * distance * distance);
            }
            textureCoord = texcoord;
            gl_Position = projectionMatrix * vertexPosition;
        }
        """
        return vertexShaderSource


    @classmethod
    def wireframeMaterialVertexShader(cls):
        vertexShaderSource = """
        #version 330

        struct Material {
            vec3 emission;
            vec3 ambient;
            vec3 diffuse;
            vec3 specular;
            float shininess;
        };

        layout(location = 0) in vec3 position;

        uniform mat4 modelMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 projectionMatrix;
        uniform Material wireframe_material;

        smooth out vec4 vertexColor;

        void main()
        {
            gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(position, 1.0);
            vertexColor = vec4(wireframe_material.diffuse, 1.0);
        }
        """
        return vertexShaderSource


    @classmethod
    def attributeColorTransformVertexShader(cls):
        vertexShaderSource = """
        #version 330
        layout(location = 0) in vec3 position;
        layout(location = 2) in vec3 color;
        uniform mat4 modelMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 projectionMatrix;
        smooth out vec4 vertexColor;

        void main()
        {
            gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(position, 1.0);
            vertexColor = vec4(color, 1.0);
        }
        """
        return vertexShaderSource


    @classmethod
    def simpleFragmentShader(cls):
        fragmentShaderSource = """
        #version 330
        smooth in vec4 vertexColor;
        out vec4 fragColor;

        void main()
        {
            fragColor = vertexColor;
        }
        """
        return fragmentShaderSource


    @classmethod
    def texturedFragmentShader(cls):
        fragmentShaderSource = """
        #version 330
        struct Material {
            vec3 emission;
            vec3 ambient;
            vec3 diffuse;
            vec3 specular;
            float shininess;
        };

        struct Light {
            vec3 ambient;
            vec3 diffuse;
            vec3 specular;
        };

        smooth in vec4 vertexNormal;
        smooth in vec4 vertexPosition;
        smooth in vec3 lightDirection;
        smooth in float attenuation;
        smooth in vec2 textureCoord;

        uniform float selected;
        uniform sampler2D texObject;
        uniform Material material;
        uniform Light light;

        out vec4 fragColor;

        void main()
        {
            // ambient term
            vec3 ambient = material.ambient * light.ambient;

            // diffuse term
            vec3 N = normalize(vertexNormal.xyz);
            vec3 L = normalize(lightDirection);
            vec3 diffuse = light.diffuse * material.diffuse * max(dot(N, L), 0.0);

            // specular term
            vec3 E = normalize(-vertexPosition.xyz);
            vec3 R = normalize(-reflect(L, N));
            vec3 specular = light.specular * material.specular * pow(max(dot(R, E), 0.0), material.shininess);

            // final intensity
            vec3 intensity = material.emission + clamp(ambient + attenuation * (diffuse + specular), 0.0, 1.0);
            vec4 tex = texture(texObject, textureCoord.st);
            fragColor = (1.0 - tex.a) * vec4(intensity, 1.0) + tex.a * vec4(selected * tex.rgb, 1.0);
        }
        """
        return fragmentShaderSource


    @classmethod
    def texturedFragmentFlatShader(cls):
        fragmentShaderSource = """
        #version 330
        struct Material {
            vec3 emission;
            vec3 ambient;
            vec3 diffuse;
            vec3 specular;
            float shininess;
        };

        struct Light {
            vec3 ambient;
            vec3 diffuse;
            vec3 specular;
        };

        flat in vec4 vertexNormal;
        smooth in vec4 vertexPosition;
        smooth in vec3 lightDirection;
        smooth in float attenuation;
        smooth in vec2 textureCoord;

        uniform float selected;
        uniform sampler2D texObject;
        uniform Material material;
        uniform Light light;

        out vec4 fragColor;

        void main()
        {
            // ambient term
            vec3 ambient = material.ambient * light.ambient;

            // diffuse term
            vec3 N = normalize(vertexNormal.xyz);
            vec3 L = normalize(lightDirection);
            vec3 diffuse = light.diffuse * material.diffuse * max(dot(N, L), 0.0);

            // specular term
            vec3 E = normalize(-vertexPosition.xyz);
            vec3 R = normalize(-reflect(L, N));
            vec3 specular = light.specular * material.specular * pow(max(dot(R, E), 0.0), material.shininess);

            // final intensity
            vec3 intensity = material.emission + clamp(ambient + attenuation * (diffuse + specular), 0.0, 1.0);
            vec4 tex = texture(texObject, textureCoord.st);
            fragColor = (1.0 - tex.a) * vec4(intensity, 1.0) + tex.a * vec4(selected * tex.rgb, 1.0);
        }
        """
        return fragmentShaderSource


    def backgroundShader(self):
        return self.__instance._backgroundShader


    def uniformMaterialShader(self):
        return self.__instance._uniformMaterialShader


    def wireframeMaterialShader(self):
        return self.__instance._wireframeMaterialShader


    def attributeColorShader(self):
        return self.__instance._attributeColorShader


    def uniformMaterialPhongShader(self):
        return self.__instance._uniformMaterialPhongShader


    def attributeColorPhongShader(self):
        return self.__instance._attributeColorPhongShader
#--------

    def uniformMaterialBRDFShader(self):
        return self.__instance._uniformMaterialBRDFShader

    def uniformMaterialBRDFFlatShader(self):
        return self.__instance._uniformMaterialBRDFFlatShader

    def attributeColorBRDFShader(self):
        return self.__instance._attributeColorBRDFShader

    def uniformMaterialPhongFlatShader(self):
        return self.__instance._uniformMaterialPhongFlatShader


    def attributeColorPhongFlatShader(self):
        return self.__instance._attributeColorPhongFlatShader


    def texturedShader(self):
        return self.__instance._texturedShader


    def texturedFlatShader(self):
        return self.__instance._texturedFlatShader

#--------

    def textureBRDFShader(self):
        return self.__instance._textureBRDFShader

    def textureBRDFFlatShader(self):
        return self.__instance._textureBRDFFlatShader

    def textureNoLightShader(self):
        return self.__instance._textureNoLightShader
