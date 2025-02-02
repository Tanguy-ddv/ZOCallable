from ZOCallable.ZOCallable import verify_ZOCallable
from ZOCallable.ZOZOCallable import verify_ZOZOCallable
import unittest
class TestZOCallable(unittest.TestCase):

    def test_ZOCallable(self):
        func = lambda x:x
        self.assertTrue(verify_ZOCallable(func, 3), "lambda x:x should be a ZOCallable.")
        func = lambda x:x**2
        self.assertTrue(verify_ZOCallable(func, 3), "lambda x:x**2 should be a ZOCallable.")
        func = lambda x:2*x
        self.assertFalse(verify_ZOCallable(func, 3), "lambda x:2*x shouldn't be a ZOCallable as f(1) = 2.")
        func = lambda x:1-x
        self.assertFalse(verify_ZOCallable(func, 3), "lambda x:(1-x) shouldn't be a ZOCallable as f(0) = 1.")
        func = lambda x:2*x if x <0.75 else 6/4 - x/2 
        self.assertTrue(verify_ZOCallable(func, 3), "lambda x:2*x if x <0.75 else 6/4 - x/2 should be a ZOCallable even if it goes above 1.")
        func = lambda x:-x if x != 1 else 1
        self.assertTrue(verify_ZOCallable(func, 3), "x:-x if x != 1 else 1 should be a ZOCallable even if it goes below 0 and is not continous.")
        func = 1
        self.assertFalse(verify_ZOCallable(func, 3), "1 shouldn't be a ZOCallable as it is not a Callable.")
        func = lambda x,y: x + y
        self.assertFalse(verify_ZOCallable(func, 3), "lambda x,y: x + y shouldn't be a ZOCallable as it has 2 parameters.")

    def test_ZOZOCallable(self):
        func = lambda x:x
        self.assertTrue(verify_ZOZOCallable(func, 3), "lambda x:x should be a ZOZOCallable.")
        func = lambda x:x**2
        self.assertTrue(verify_ZOZOCallable(func, 3), "lambda x:x**2 should be a ZOZOCallable.")
        func = lambda x:2*x
        self.assertFalse(verify_ZOZOCallable(func, 3), "lambda x:2*x shouldn't be a ZOZOCallable as f(1) = 2.")
        func = lambda x:1-x
        self.assertFalse(verify_ZOZOCallable(func, 3), "lambda x:(1-x) shouldn't be a ZOZOCallable as f(0) = 1.")
        func = lambda x:2*x if x <0.75 else 6/4 - x/2 
        self.assertFalse(verify_ZOZOCallable(func, 3), "lambda x:2*x if x <0.75 else 6/4 - x/2 shouldn't be a ZOZOCallable as it goes above 1.")
        func = lambda x:-x if x != 1 else 1
        self.assertFalse(verify_ZOZOCallable(func, 3), "x:-x if x != 1 else 1 shouldn't be a ZOZOCallable even if it goes below 0.")
        func = 1
        self.assertFalse(verify_ZOZOCallable(func, 3), "1 shouldn't be a ZOZOCallable as it is not a Callable.")
        func = lambda x,y: x + y
        self.assertFalse(verify_ZOZOCallable(func, 3), "lambda x,y: x + y shouldn't be a ZOZOCallable as it has 2 parameters.")
