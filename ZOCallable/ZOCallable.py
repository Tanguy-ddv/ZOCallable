"""The module ZOCallable the defintion of the ZOCallable class, used to type functions. ZO stands for Zero-One."""
from typing import Callable
import inspect
import numpy as np

class _ZOCMetaclass(type):
    """
    The Metaclass used to define a ZOZOCallable.
    Things are done like this to allow the check isinstance(func, ZOCallable) to return
    True if the function satisfies the conditions, even if it is not an instance of the class
    but a function or a lambda function.
    """

    rounding: int = 5
    test_vectorization: bool = False,
    test_values = np.linspace(0 + 1/101, 1 - 1/101, 99)

    def __instancecheck__(cls, func) -> bool:
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
        if not (round(f0, _ZOCMetaclass.rounding) == 0 and round(f1, _ZOCMetaclass.rounding) == 1):
            return False
        if cls is ZOCallable: # No further check is the asked class is ZOCallable
            return True
        if _ZOCMetaclass.test_vectorization: # If we test the vectorization, we verify the output is an array of float
            outputs = func(_ZOCMetaclass.test_values)
            if not isinstance(outputs, np.ndarray) or not isinstance(outputs[0], float):
                return False
            # And we verify all these floats are in [0, 1]
            return np.all(0 <= np.round(outputs, _ZOCMetaclass.rounding) <= 1)
        else:
            # If we don't care about vectorization, we still test the range of the function.
            return all(0 <= round(float(func(t)), _ZOCMetaclass.rounding) <= 1 for t in _ZOCMetaclass.test_values)

class ZOCallable(metaclass=_ZOCMetaclass):
    """
    The ZOCallable isn't meant to be instanciated.
    This class is only a type hint for functions f with
    f(0) = 0, f(1) = 1 and f : [0, 1] -> R.
    """

    def __call__(self, x: float) -> float: ...

class ZOZOCallable(ZOCallable, metaclass=_ZOCMetaclass):
    """
    The ZOZOCallable isn't meant to be instanciated.
    This class is only a type hint for functions f with
    f(0) = 0, f(1) = 1 and f : [0, 1] -> [0, 1].
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
    _ZOCMetaclass.rounding = rounding
    _ZOCMetaclass.test_vectorization = test_vectorizaiton
    _ZOCMetaclass.test_values = np.linspace(0 + 1/points, 1 - 1/points, points - 2)
    return isinstance(ZOC, ZOZOCallable)
