
import os
from Source.Graphics.Texture import Texture

class Textures():

    txtrs = {}
    bindIDs = {}
    txtrs = {}
    txtrs["baseColor"] = {}
    txtrs["normals"] = {}
    txtrs["metalness"] = {}
    txtrs["roughness"] = {}
    txtrs["specular"] = {}
    bindIDs = {}
    cntr = 0
    using = {}
    for group in txtrs:
        using[group] = -1
        bindIDs[group] = cntr
        cntr += 1
    binded = []
    samples = {}

    @staticmethod
    def loadTextures():
        for group in Textures.txtrs:
            for name in Textures.txtrs[group]:
                txt = Textures.txtrs[group][name]
                if not txt.isLoaded(): txt.load()
                Textures.useTexture(group, name)

    @staticmethod
    def preloadTexture(path, group):
        filename = os.path.basename(path)
        new_filename = filename
        its = 1
        while new_filename in Textures.txtrs[group]:
            new_filename = filename + " (" + str(its) + ")"
            its += 1
        Textures.txtrs[group][new_filename] = Texture.preload(path)
        return new_filename

    @staticmethod
    def addTexture(path, group):
        filename = os.path.basename(path)
        new_filename = filename
        its = 1
        while new_filename in Textures.txtrs[group]:
            new_filename = filename + " (" + str(its) + ")"
            its += 1
        Textures.txtrs[group][new_filename] = Texture(path)
        return new_filename

    @staticmethod
    def useTexture(group, name):
        Textures.using[group] = name

    @staticmethod
    def stopUsingTexture(group):
        Textures.using[group] = -1

    @staticmethod
    def getBindID(group):
        return Textures.bindIDs[group]

    @staticmethod
    def bind():
        for group in Textures.using:
            if Textures.using[group] != -1:
                Textures.txtrs[group][Textures.using[group]].bind(Textures.bindIDs[group])
                Textures.binded.append(Textures.txtrs[group][Textures.using[group]])

    @staticmethod
    def release():
        for txt in Textures.binded:
            txt.release()
        Textures.binded = []

    @staticmethod
    def isUsing(group):
        return True if Textures.using[group] != -1 else False
