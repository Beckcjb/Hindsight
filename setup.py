import os
from setuptools import setup, find_packages

VERSION = 1.0

def setup_package():
    setup(
        name = "Hindsight",
        version = VERSION,
        author = "Adam Paquette",
        author_email = "acp263@nau.edu",
        description = ("Application for detecting dust."),
        packages=find_packages(),
        zip_safe=False,
        install_requires=[
            'pandas',
            'pillow',
            'scipy',
            'numpy',
            'opencv-python',
            'matplotlib'],
    )

if __name__ == '__main__':
    setup_package()
    
    matlab_path = "/Applications/MATLAB_R2017b.app/extern/engines/python"
    os.system("cd " + matlab_path + " \
            && python setup.py install")
