from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
import sys

setup(
    ext_modules = cythonize([
        Extension("pcap", ["pcap.pyx"], libraries=["pcap"])
            ])
)
