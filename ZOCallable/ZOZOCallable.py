"""The module ZOZOCallable contains functions that can be use as transitions. ZO stands for Zero-One."""
from typing import Callable
import numpy as np
import inspect

class _ZOZOCMetaclass(type):
    """
    The Metaclass used to define a ZOZOCallable.
    Things are done like this to allow the check isinstance(func, ZOCallable) to return
    True if the function satisfies the conditions, even if it is not an instance of the class
    but a function or a lambda function.
    """

    rounding: int = 5
    test_vectorization: bool = False,
    test_values = np.linspace(0 + 1/101, 1 - 1/101, 99)

    def __instancecheck__(self, func) -> bool:
        if not (
            isinstance(func, Callable) #The func must be a callable
            and len(inspect.signature(func).parameters.keys()) == 1 # the func must have one parameter
        ):
            return False
        f0 = func(0.)
        f1 = func(1.)
        if isinstance(f0, np.ndarray): # if the output is an array, the function is vectorized.
            try:
                f0 = float(f0)
                f1 = float(f1) # we assume f1 is also a np.ndarray in this case
            except ValueError:
                return False # We need to be sure the output is a float
         # The function must satisfy f(0) = 0 and f(1) = 1, it checkes also if the output is a number.
        if not (round(f0, _ZOZOCMetaclass.rounding) == 0 and round(f1, _ZOZOCMetaclass.rounding) == 1):
            return False
        if _ZOZOCMetaclass.test_vectorization: # If we test the vectorization, we verify the output is an array of float
            outputs = func(_ZOZOCMetaclass.test_values)
            if not isinstance(outputs, np.ndarray) or not isinstance(outputs[0], float):
                return False
            # And we verify all these floats are in [0, 1]
            return np.all(0 <= np.round(outputs, _ZOZOCMetaclass.rounding) <= 1)
        else:
            # If we don't care about vectorization, we still test the range of the function.
            return all(0 <= round(float(func(t)), _ZOZOCMetaclass.rounding) <= 1 for t in _ZOZOCMetaclass.test_values)

class ZOZOCallable(metaclass=_ZOZOCMetaclass):
    """
    The ZOZOCallable isn't meant to be instanciated.
    This class is only a type hint for functions f with
    f(0) = 0, f(1) = 1 and f : [0, 1] -> [0, 1].
    """

    def __call__(self, x: float) -> float: ...

def verify_ZOZOCallable(ZOC, rounding: int=5, test_vectorizaiton: bool = False, points: int = 101):
    """
    Verify if the provided function is a ZOZOCallable.

    Params:
    ----
    - rounding: int = 5, the number of significative numbers that are kept to proceed to the float comparisons.
    This is used to allow the calculations errors of python.
    - test_vectorization: bool = False. If true, the function is also tested if it is vectorized.
    - points: int = 101, >= 3 the number of points used to test the assertion 0 <= f(x) <= 1.

    Returns:
    ---
    - is_ZOZOC: bool, whether the provided function is a ZOZOCallable.

    Raises:
    ----
    - ValueError: if points is <= 2.
    """
    if points <= 2:
        raise ValueError(f"{points} points are not enough.")
    _ZOZOCMetaclass.rounding = rounding
    _ZOZOCMetaclass.test_vectorization = test_vectorizaiton
    _ZOZOCMetaclass.test_values = np.linspace(0 + 1/points, 1 - 1/points, points - 2)
    return isinstance(ZOC, ZOZOCallable)
