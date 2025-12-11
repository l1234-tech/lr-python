from integrate_1 import integrate
from integrate_2_async import integrate_async
from integrate_3_process import integrate_process
from integrate_cython import integrate_cython
from integrate_5_noGIL import worker, integrate_processes_mp
import unittest
import math

class TestIntegrate_for_1st_task(unittest.TestCase):
    def test_log2(self):
        result = integrate(math.log2, 1, 2, n_iter=1000)
        self.assertAlmostEqual(result, 0.55730, delta=0.001)

    def test_cos(self):
        result = integrate(math.cos, 0, math.pi / 2, n_iter=1000)
        self.assertAlmostEqual(result, 1.0, delta=0.001)

class TestIntegrate_async_for_2st_task(unittest.TestCase):
    def test_log2(self):
        result = integrate_async(math.log2, 1, 2, n_iter=1000 , n_jobs=2)
        self.assertAlmostEqual(result, 0.55730, delta=0.001)

    def test_cos(self):
        result = integrate_async(math.cos, 0, math.pi/2, n_iter=1000)
        self.assertAlmostEqual(result, 1, delta=0.001)

class TestIntegrate_process_for_3st_task(unittest.TestCase):
    def test_log2(self):
        result = integrate_process(math.log2, 1, 2, n_iter=1000 , n_jobs=2)
        self.assertAlmostEqual(result, 0.55730, delta=0.001)

    def test_cos(self):
        result = integrate_process(math.cos, 0, math.pi/2, n_iter=1000)
        self.assertAlmostEqual(result, 1.0, delta=0.001)

class TestIntegrate_cython_for_4st_task(unittest.TestCase):
    def test_log2(self):
        result = integrate_cython(math.log2, 1, 2, n_iter=1000)
        self.assertAlmostEqual(result, 0.55730, delta=0.001)

    def test_cos(self):
        result = integrate_cython(math.cos, 0, math.pi/2, n_iter=1000)
        self.assertAlmostEqual(result, 1.0, delta=0.001)

class TestIntegrate_noGIL_for_5st_task(unittest.TestCase):
    def test_log2(self):
        result = integrate_processes_mp(math.log2, 1, 2, n_jobs=2, n_iter=1000)
        self.assertAlmostEqual(result, 0.55730, delta=0.001)

    def test_cos(self):
        result = integrate_processes_mp(math.cos, 0, math.pi/2, n_jobs= 2, n_iter=1000)
        self.assertAlmostEqual(result, 1.0, delta=0.001)
