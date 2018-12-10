# Agradecimentos

Agradeço ao Marcel Parolin Jackowski pelas aulas de computação gráfica e pelo código base para a montanha-russa disponível em: https://github.com/mjck/mac420

Agradeço ao Matheus Tavares Bernardino pelos códigos dos exercícios programas feitos na disciplina MAC0420. Alguns trechos deles foram incluídos no projeto atual.

Agradeço a todos que me apoiaram e ajudaram a completar esse projeto.

# Setting up MAC0468 Roller Coaster code 

Follow the instructions below based on your OS to set up the requirements
and then follow the steps under **Wrapping up**.

## Windows

1) Download and install latest Python 3 from repository:

   https://www.python.org/ftp/python/3.6.4/python-3.6.4-amd64.exe

   Check option in the installer: Add Python 3.6 to PATH

2) Download latest 'numpy' package from:

	https://pypi.python.org/pypi/numpy/1.13.3

	C:\yourself> pip install "C:\Downloads\numpy-1.13.3-cp36-none-win_amd64.whl"

3) Download lastest 'scipy' package from:

	https://pypi.python.org/pypi/scipy/1.0.0rc2

	C:\yourself> pip install "C:\Downloads\scipy-1.0.0rc2-cp36-none-win_amd64.whl"

6) Now install PyQt5:

	C:\yourself> pip install PyQt5

7) Finish by installing PyOpenGL

	C:\yourself> pip install PyOpenGL PyOpenGL_accelerate

8) And finally download and install git:

	https://git-scm.com/download/win

	Run the installer from the downloads directory and follow instructions.


## macOS

1) Download and install latest Python 3 from repository:

   https://www.python.org/ftp/python/3.6.4/python-3.6.4-macosx10.6.pkg

2) At the prompt, install 'numpy' package:

	> pip3 install numpy

3) At the prompt, install 'scipy' package:

	> pip3 install scipy

4) Now install PyQt5:

	> pip3 install pyqt5

5) Finish by installing PyOpenGL

	> pip3 install pyopengL pyopengl_accelerate


## Ubuntu 16.04, 17.10

1) Make sure you have at least Python 3 installed:

	> python3 -V

   If this is not the case, you must update your system.

2) Make sure you have 'pip3' installed on your system:

	> sudo apt install python3-pip

3) At the prompt, install 'numpy' package:

	> pip3 install numpy

4) Now install PyQt5:

	> pip3 install pyqt5

5) Installing PyOpenGL:

	> pip3 install pyopengl pyopengl_accelerate

6) And finally install git if you do not have it:

	> sudo apt install git


**Wrapping up**

To make sure everything went well, open python3 interpreter session and try
importing the packages:

	> python3

	>>> import numpy

	>>> import PyQt5

	>>> import OpenGL

If you do not see any messages, you were successful. You may now clone
the repository:

	> git clone https://github.com/cesargaspfer/MAC0468_Roller_Coaster.git

