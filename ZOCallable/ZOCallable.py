"""The module ZOCallable the defintion of the ZOCallable class, used to type functions. ZO stands for Zero-One."""
from typing import Callable
import inspect

class _ZOCMetaclass(type):

    rounding: int = 3

    def __instancecheck__(self, func) -> bool:
        return (
            isinstance(func, Callable)
            and len(inspect.signature(func).parameters.keys()) == 1
            and round(func(0), _ZOCMetaclass.rounding) == 0
            and round(func(1), _ZOCMetaclass.rounding) == 1
        )

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

def normalize_ZOCallable(unnormalized_callable: Callable[[float], float]):
    """Normalize a function to be a ZOCCallable."""
    if unnormalized_callable(1) == 0:
        raise ValueError("This function cannot be normalized as a ZOCallable.")
    return lambda t: (unnormalized_callable(t) - unnormalized_callable(0)) / unnormalized_callable(1)
