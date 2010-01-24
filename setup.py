'''
Created on 24.01.2010

@author: t0ster
'''
from distutils.core import setup
import py2exe

setup(name="neuralnet-model",
      version="0.0.1a",
      author="Roman Dolgiy",
      author_email="tosters@gmail.com",
      url="https://bitbucket.org/t0ster/neuralnet-model",
      license="GNU General Public License (GPL)",
#      packages=['neuralnet-model'],
#      package_data={"liftr": ["ui/*"]},
      scripts=["main.py"],
      windows=[{"script": "main.py"}],
      options={"py2exe": {"skip_archive": False, "includes": ["sip"], "bundle_files": 2}})
