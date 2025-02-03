"""The module ZOCallable the defintion of the ZOCallable class, used to type functions. ZO stands for Zero-One."""
from typing import Callable
import inspect
import numpy as np

class _ZOCMetaclass(type):
    """
    The Metaclass used to define a ZOCallable.
    Things are done like this to allow the check isinstance(func, ZOCallable) to return
    True if the function satisfies the conditions, even if it is not an instance of the class
    but a function or a lambda function.
    """

    rounding: int = 5 # use to allow a little error on the check of f(0) = 0 and f(1) = 1

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
        return round(f0, _ZOCMetaclass.rounding) == 0 and round(f1, _ZOCMetaclass.rounding) == 1

class ZOCallable(metaclass=_ZOCMetaclass):
    """
    The ZOCallable isn't meant to be instanciated.
    This class is only a type hint for functions f with
    f(0) = 0, f(1) = 1 and f : [0, 1] -> R.
    """

    def __call__(self, x: float) -> float: ...

def verify_ZOCallable(ZOC, rounding: int=5):
    """
    Verify if the provided function is a ZOCallable.

    Params:
    ----
    - rounding: int = 5, the number of significative numbers that are kept to proceed to the float comparisons.
    This is used to allow the calculations errors of python.

    Returns:
    ---
    - is_ZOC: bool, whether the provided function is a ZOCallable.
    """
    _ZOCMetaclass.rounding = rounding
    return isinstance(ZOC, ZOCallable)

def normalize_ZOCallable(unnormalized_callable: Callable[[float], float]):
    """
    Normalize a function to be a ZOCallable.
    
    Params:
    ----
    - unnormalized_callable: Callable (float) -> float. A function to be normalized.

    Returns:
    ----
    - ZOC, a function (float) -> (float) satisfying ZOC(0) = 0 and ZOC(1) = 1.

    Raises:
    ----
    - ValueError if unnormalized_callable cannot be normalized, meaning unnormalized_callable(1) == 0.
    """
    u1 = unnormalized_callable(1)
    if u1 == 0:
        raise ValueError("This function cannot be normalized as a ZOCallable.")
    u0 = unnormalized_callable(0)
    return lambda t: (unnormalized_callable(t) - u0) / (u1 - u0)

def vectorize_ZOCallable(unvectorized_ZOC: Callable[[float], float]):
    """
    Vectorize a ZOCallable.

    In order to be used directly on a numpy array, most functions need to be vectorized.
    However, np.vectorize transforms the params from 'x' (or wathever it was) to (*args, **kwargs)
    while a ZOCallable need to have only one parameter.
    This function perform the vectorization with numpy and replaces the input parameter to be
    accepted as a vectorized ZOCallable.
    """
    vectorized_ZOC = np.vectorize(unvectorized_ZOC)
    return lambda x: vectorized_ZOC(x)