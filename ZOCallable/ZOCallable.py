"""The module ZOCallable the defintion of the ZOCallable class, used to type functions. ZO stands for Zero-One."""
from typing import Callable
import inspect
import numpy as np

class _ZOCMetaclass(type):

    rounding: int = 5

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
        return round(f0, _ZOCMetaclass.rounding) == 0 and round(f1, _ZOCMetaclass.rounding) == 1

class ZOCallable(metaclass=_ZOCMetaclass):
    """
    The ZOCallable isn't meant to be instanciated.
    This class is only a type hint for functions f with
    f(0) = 0, f(1) = 1 and f : [0, 1] -> R.
    """

    def __call__(self, x: float) -> float: ...

def verify_ZOCallable(ZOC, rounding: int=5):
    """Verify if the provided function is a ZOCallable."""
    _ZOCMetaclass.rounding = rounding
    return isinstance(ZOC, ZOCallable)

def verify_step_by_step(ZOC):
    print(isinstance(ZOC, Callable))
    print(list(inspect.signature(ZOC).parameters.keys()))
    print(ZOC(0))
    print(ZOC(1))

def normalize_ZOCallable(unnormalized_callable: Callable[[float], float]):
    """Normalize a function to be a ZOCCallable."""
    u1 = unnormalized_callable(1)
    if u1 == 0:
        raise ValueError("This function cannot be normalized as a ZOCallable.")
    u0 = unnormalized_callable(0)
    return lambda t: (unnormalized_callable(t) - u0) / (u1 - u0)

def vectorize_ZOCallable(unvectorized_ZOC: Callable[[float], float]):
    vectorized_ZOC = np.vectorize(unvectorized_ZOC)
    return lambda x: vectorized_ZOC(x)