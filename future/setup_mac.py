"""
Usage: 
    python setup.py py2app
"""
import sys
from setuptools import setup

sys.setrecursionlimit(1500)

APP = ['flipGUI/app.py']
DATA_FILES = []#[('',['inputfiles'])]
OPTIONS = {'iconfile' : 'flipGUI/flipGUI.icns',}

setup(
    name = "flipGUI",
    version = "0.0.1",
    url="https://github.com/3Prophet/flipGUI",
    licence='',#To be filled
    author = "Dmitry Logvinovich",
    author_email = "dlogvinovich@yahoo.com",
    #tests_require=['pytest']
    #install_requires=[]
    app = APP,
    data_files = DATA_FILES,
    options = {'py2app': OPTIONS},
    setup_requires = ['py2app']
        )
