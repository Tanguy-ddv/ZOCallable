"""
ZOCallable is a python library defining functions ranging from 0 to 1. They can be used as transitions or non-linear gradients for example.
ZO stands for "Zero One".

ZOCallable contains two classes:
- ZOCallable, they represent functions mapping floats of [0, 1] to other floats, and mapping 0 to 0 and 1 to 1.
- ZOZOCallable, they represent functions mapping floats of [0, 1] to [0, 1], and mapping 0 to 0, and 1 to 1.

For both cases, a function called `verify_ZO(ZO)Callable` can be used to verify is another function is a ZO(ZO)Callable.
Multiple functions are defined in the submodule _ZOCallable.functions_, most of them are ZOZOCallables, all of them are ZOCallables. 
"""
from ZOCallable.ZOCallable import ZOCallable, verify_ZOCallable, normalize_ZOCallable, vectorize_ZOCallable
from ZOCallable import functions, plot