#!/usr/bin/env python3
import sys
import platform
import argparse

from OpenGL import GL
from PyQt5 import Qt, QtCore
from Source.GUI.MainWindow import MainWindow

def main():

	parser = argparse.ArgumentParser()
	parser.add_argument("--glversion", help="use specific OpenGL version")
	parser.add_argument("--glsamples", help="use specific number of samples for rendering")

	args = parser.parse_args()

	## determine what OpenGL version to ask for
	if args.glversion:
		gl_major_version = int(args.glversion.split(".")[0])
		gl_minor_version = int(args.glversion.split(".")[1])
	else:
		gl_major_version = gl_minor_version = 3

	## determine number of samples for multisampling
	if args.glsamples:
		gl_samples = int(args.glsamples)
	else:
		gl_samples = 8

	## use desktop OpenGL and share contexts
	QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_UseDesktopOpenGL)
	QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)

	## set up OpenGL version and profile requested
	glformat = Qt.QSurfaceFormat()
	glformat.setDepthBufferSize(24)
	glformat.setRedBufferSize(8)
	glformat.setGreenBufferSize(8)
	glformat.setBlueBufferSize(8)
	if "Darwin" not in platform.platform():
		glformat.setAlphaBufferSize(8)
	glformat.setSamples(gl_samples)
	glformat.setStencilBufferSize(8)
	glformat.setSwapInterval(0)
	glformat.setVersion(gl_major_version, gl_minor_version)
	glformat.setProfile(Qt.QSurfaceFormat.CoreProfile)

	## set default format
	Qt.QSurfaceFormat.setDefaultFormat(glformat)

	## create Qt app
	app = Qt.QApplication(sys.argv)
	
	## create main window and show
	mainWindow = MainWindow()
	mainWindow.show()

	## run...
	sys.exit(app.exec_())

	print("End of story.")

if __name__ == '__main__':
    
    main()
