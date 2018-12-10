
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QOpenGLTexture

class Texture:

    def __init__(self, path, load=True):
        self.img = QImage(path, "PNG")
        self.bind_index = None
        if load: self.load()
        self.loaded = load

    @staticmethod
    def preload(path):
        txt = Texture(path, False)
        return txt

    def isLoaded(self):
        return self.loaded

    def load(self):
        self.qtexture = QOpenGLTexture(self.img)
        self.img = None

    def bind(self, index):
        self.qtexture.bind(index)
        self.bind_index = index

    def release(self):
        self.qtexture.release(self.bind_index)
        self.bind_index = None

    def isBinded(self):
        return True if self.bind_index is not None else False
