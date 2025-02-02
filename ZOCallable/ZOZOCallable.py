"""The module ZOZOCallable contains functions that can be use as transitions. ZO stands for Zero-One."""
from typing import Callable
import numpy as np
import inspect

class _ZOZOCMetaclass(type):

    rounding: int = 3
    test_vectorization: bool = False,
    test_values = np.linspace(0, 1, 101)

    def __instancecheck__(self, func) -> bool:
        if not (
            isinstance(func, Callable)
            and len(inspect.signature(func).parameters.keys()) == 1
            and round(func(0), _ZOZOCMetaclass.rounding) == 0
            and round(func(1), _ZOZOCMetaclass.rounding) == 1
        ):
            return False
        if _ZOZOCMetaclass.test_vectorization:
            outputs = func(_ZOZOCMetaclass.test_values)
            if not isinstance(outputs, np.ndarray) or not isinstance(outputs[0], float):
                return False
            return np.all(0 <= np.round(outputs, _ZOZOCMetaclass.rounding) <= 1)
        else:
            return all(0 <= round(func(t), _ZOZOCMetaclass.rounding) <= 1 for t in _ZOZOCMetaclass.test_values)

class ZOZOCallable(metaclass=_ZOZOCMetaclass):
    """
    The ZOZOCallable isn't meant to be instanciated.
    This class is only a type hint for functions f with
    f(0) = 0, f(1) = 1 and f : [0, 1] -> [0, 1].
    """

    def __call__(self, x: float) -> float: ...

def verify_ZOZOCallable(ZOC, rounding: int=3, test_vectorizaiton: bool = False, points: int = 101):
    """Verify if the provided function is a ZOCallable."""
    _ZOZOCMetaclass.rounding = rounding
    _ZOZOCMetaclass.test_vectorization = test_vectorizaiton
    _ZOZOCMetaclass.test_values = np.linspace(0, 1, points)
    return isinstance(ZOC, ZOZOCallable)
