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

    def test_functions(self):

        from ZOCallable.functions import linear, square_in, square_in_out, square_out, root_in, root_out
        funcs = [linear, square_in, square_out, square_in_out, root_in, root_out]
        for i, func in enumerate(funcs):
            self.assertTrue(verify_ZOCallable(func, 3), f"The {i+1}-th function of the basic list should be a ZOCallable.")
            self.assertTrue(verify_ZOZOCallable(func, 3), f"The {i+1}-th function of the basic list should be a ZOZOCallable.")
        from ZOCallable.functions import power_in, power_in_out, power_out
        funcs = sum([[power_in(i), power_out(i), power_in_out(i)] for i in range(3, 8)], [])
        for i, func in enumerate(funcs):
            self.assertTrue(verify_ZOCallable(func, 3), f"The power_{i%3}({i//3 + 3} function should be a ZOCallable.")
            self.assertTrue(verify_ZOZOCallable(func, 3), f"The power_{i%3}({i//3 + 3} function should be a ZOZOCallable.")
        from ZOCallable.functions import ease, ease_in, ease_in_out, ease_out
        funcs = [ease, ease_in, ease_in_out, ease_out]
        for i, func in enumerate(funcs):
            self.assertTrue(verify_ZOCallable(func, 3), f"The {i+1}-th function of the ease list should be a ZOCallable.")
            self.assertTrue(verify_ZOZOCallable(func, 3), f"The {i+1}-th function of the ease list should be a ZOZOCallable.")
        from ZOCallable.functions import jump, bounce_in, bounce_out
        funcs = sum([[jump(i), bounce_in(i), bounce_out(i)] for i in range(3, 8)], [])
        for i, func in enumerate(funcs):
            self.assertTrue(verify_ZOCallable(func, 3), f"The special{i%3}({i//3} function should be a ZOCallable.")
            self.assertTrue(verify_ZOZOCallable(func, 3), f"The special{i%3}({i//3} function should be a ZOZOCallable.")
        from ZOCallable.functions import exp_in, exp_out, circular_in, circular_in_out, circular_out, back_in, back_in_out, back_out, elastic_in, elastic_in_out, elastic_out
        funcs = [exp_in, exp_out, circular_in, circular_in_out, circular_out, back_in, back_in_out, back_out, elastic_in, elastic_in_out, elastic_out]
        for i, func in enumerate(funcs):
            self.assertTrue(verify_ZOCallable(func, 3), f"The {i+1}-th function of the extra list should be a ZOCallable.")
            if i < 5: # the back ad elastic functions are supposed to not be ZOZOC
                self.assertTrue(verify_ZOZOCallable(func, 3), f"The {i+1}-th function of the extra list should be a ZOZOCallable.")
        
    def test_plots(self):
        from ZOCallable.functions import circular_in, circular_in_out, circular_out, elastic_in, elastic_in_out, elastic_out
        from ZOCallable.plot import plot_ZOCallable, plot_ZOZOCallable
        plot_ZOZOCallable(circular_in, circular_in_out, circular_out, vectorized=True, save_path="ZOZOC.png", labels=["Circular_in", "Circular_in_out", "Circular_out"])
        plot_ZOCallable(elastic_in, elastic_in_out, elastic_out, vectorized=True, save_path="ZOC.png", labels=["Elastic_in", "Elastic_in_out", "Elastic_out"])

