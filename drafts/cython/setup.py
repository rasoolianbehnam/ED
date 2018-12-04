from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
import sys

setup(
    ext_modules = cythonize([
        #Extension("queue", ["queue.pyx"]), 
        #Extension("stdlib_test", ["stdlib_test.pyx"]),
        Extension("pcap", ["pcap.pyx"], libraries=["pcap"])
            ])
)
