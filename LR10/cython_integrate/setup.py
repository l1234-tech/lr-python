from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy as np
import os

extensions = [
    Extension(
        "integrate_cython",
        ["integrate_cython.pyx"],
        extra_compile_args=['/O2' if os.name == 'nt' else '-O3'],
        libraries=["m"] if os.name != 'nt' else [],
    )
]
setup(
    name="integrate_cython",
    ext_modules=cythonize(
        extensions,
        language_level="3",
        annotate=True
    ),
    include_dirs=[np.get_include()]
)