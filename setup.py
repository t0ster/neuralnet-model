'''
Created on 24.01.2010

@author: t0ster
'''
from distutils.core import setup
import py2exe

setup(name="neuralnet-model",
      version="0.0.1",
      author="Roman Dolgiy",
      author_email="tosters@gmail.com",
      url="https://bitbucket.org/t0ster/neuralnet-model",
      license="GNU General Public License (GPL)",
      scripts=["neuralnet.py"],
      windows=[{"script": "neuralnet.py"}],
      data_files=[("", ["netdata.dat"])],
      options={"py2exe": {"skip_archive": False,
                          "includes": ["sip"],
                          "bundle_files": 2,
                          "excludes": ["Tkconstants", "Tkinter", "tcl",
                                       "scipy.sparse", "scipy.linalg", "scipy.special", "numpy.core._dotblas", "ssl", "_ssl"],
#                          "dll_excludes": ["tcl85.dll", "tk85.dll"],
                          "dist_dir": "neuralnet-model"}})
