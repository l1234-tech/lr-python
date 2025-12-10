from integrate_1 import integrate
from integrate_2_async import integrate_async
from integrate_3_process import integrate_process
import unittest
import math

class TestIntegrate_for_1st_task(unittest.TestCase):
    def test_log2(self):
        result = integrate(math.log2, 1, 2, n_iter=1000)
        self.assertAlmostEqual(result, 0.55680, delta=0.01)

    def test_cos(self):
        result = integrate(math.cos, 0, math.pi / 2, n_iter=100)
        self.assertAlmostEqual(result, 1.0, delta=0.01)

class TestIntegrate_async_for_2st_task(unittest.TestCase):
    def test_log2(self):
        result = integrate_async(math.log2, 1, 2, n_iter=1000 , n_jobs=2)
        self.assertAlmostEqual(result, 0.55730, delta=0.01)

    def test_cos(self):
        result = integrate_async(math.log, 1, 3, n_iter=1000)
        self.assertAlmostEqual(result, 1.2958, delta=0.01)

class TestIntegrate_process_for_3st_task(unittest.TestCase):
    def test_log2(self):
        result = integrate_process(math.log2, 1, 2, n_iter=1000 , n_jobs=2)
        self.assertAlmostEqual(result, 0.55730, delta=0.01)

    def test_cos(self):
        result = integrate_process(math.log, 1, 3, n_iter=1000)
        self.assertAlmostEqual(result, 1.2958, delta=0.01)