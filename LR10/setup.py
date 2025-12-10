from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize(
        "integrate_cython.pyx",
        annotate=True,
        compiler_directives={
            'language_level': "3",
            'boundscheck': False,
            'wraparound': False,
            'cdivision': True,
        }
    )
)