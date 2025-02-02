"""The module ZOZOCallable contains functions that can be use as transitions. ZO stands for Zero-One."""
from typing import Callable
import numpy as np
import inspect

class _ZOZOCMetaclass(type):

    rounding: int = 5
    test_vectorization: bool = False,
    test_values = np.linspace(0, 1, 101)

    def __instancecheck__(self, func) -> bool:
        if not (
            isinstance(func, Callable)
            and len(inspect.signature(func).parameters.keys()) == 1
        ):
            return False
        f0 = func(0.)
        f1 = func(1.)
        if isinstance(f0, np.ndarray):
            f0 = float(f0)
            f1 = float(f1)
        if not (round(f0, _ZOZOCMetaclass.rounding) == 0 and round(f1, _ZOZOCMetaclass.rounding) == 1):
            return False
        if _ZOZOCMetaclass.test_vectorization:
            outputs = func(_ZOZOCMetaclass.test_values)
            if not isinstance(outputs, np.ndarray) or not isinstance(outputs[0], float):
                return False
            return np.all(0 <= np.round(outputs, _ZOZOCMetaclass.rounding) <= 1)
        else:
            return all(0 <= round(float(func(t)), _ZOZOCMetaclass.rounding) <= 1 for t in _ZOZOCMetaclass.test_values)

class ZOZOCallable(metaclass=_ZOZOCMetaclass):
    """
    The ZOZOCallable isn't meant to be instanciated.
    This class is only a type hint for functions f with
    f(0) = 0, f(1) = 1 and f : [0, 1] -> [0, 1].
    """

    def __call__(self, x: float) -> float: ...

def verify_ZOZOCallable(ZOC, rounding: int=5, test_vectorizaiton: bool = False, points: int = 101):
    """Verify if the provided function is a ZOCallable."""
    _ZOZOCMetaclass.rounding = rounding
    _ZOZOCMetaclass.test_vectorization = test_vectorizaiton
    _ZOZOCMetaclass.test_values = np.linspace(0, 1, points)
    return isinstance(ZOC, ZOZOCallable)
