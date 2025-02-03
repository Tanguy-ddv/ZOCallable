# ZOCallable

ZOCallable is a python library providing several functions mapping a float from 0 to 1 into a float from 0 to 1, with f(0) = 0 and f(1) = 1, with some tools and type hints for validation. ZO stands for Zero-One

## ZOCallables and ZOZOCallables

The package ZOCallable provides two classes to be used for validation and type hinting: ``ZOCallable`` and ``ZOZOCallable``.
- ``ZOCallable`` is used to represent any function $f$ satifying $f: [0, 1] \mapsto \mathbb{R} \text{ and } f(0) = 0 \text{ and } f(1) = 1$. The function ``verify_ZOCallable`` can be called on any function to verify if it satisfies the conditions, (as well as ``isinstance(func, ZOCallable)``). ``ZOCallable`` can also be used as type hinting.
- ``ZOZOCallable`` is a subclass of ``ZOCallable``, the function must satisfy the same conditions and satifsy $f: [0, 1] \mapsto [0, 1]$. The function ``verify_ZOCallable`` can be called on any function to verify if it satifies the conditions, (as well as ``isinstance(func, ZOZOCallable)``). ``ZOZOCallable`` can also be used as type hinting.

Two other functions are provided in the package, one is ``normalize_ZOCallable``, use to create a function that would satisfy the conditions from another, and ``vectorize_ZOCallable`` used to return a numpy vectorized function satisfying the conditions.

## Functions

On top of these functions, some ZOCallables and ZOZOCallables are already implemented in the library.
Most of these functions are called ``something_in``, ``something_out`` or ``something_in_out``. In most cases, -_in functions are convex, -_out functions are convace, and -_in_out are convex before x = 0.5 and concave after. They can all be found in the ``ZOCallable.functions`` module.

### Basic functions

Some basic ZOZOCallables are:
- ``linear`` (the identity function),
- ``square_in``, ``square_out`` and ``square_in_out`` are based on quadratic equations
- ``power_in(n)``, ``power_out(n)`` and ``power_in_out(n)`` are generalizations based on polynomial equations of degree n.
- ``root_in`` and ``root_out`` are based on the square root.
- ``exp_in`` and ``exp_out`` are based on the exponential function.
- ``jump(n)`` are stairs functions with n jumps.

### cubic bezier curves

The cubic bezier curves have been implemented in order to mimic the capabilities of CSS.
The function ``cubic_bezier(x1, y1, x2, y2)`` allow defining ZOCallables based on cubic bezier curves. Four functions have already been implemnted:
- ``ease``
- ``ease_in``
- ``ease_out``
- ``ease_in_out``

### Advanced functions

Some more advanced functions are also defined:
- ``sin_in``, ``sin_out`` and ``sin_in_out`` are based on sinusoidal functions
- ``circulare_in``, ``circular_out`` and ``circulare_in_out`` are based on circles
- ``elastic_in``,``elastic_out``, ``elastic_in_out``, ``back_in``, ``back_out``, ``back_in_out``, ``bounce_in(n)``, ``bounce_out(n)`` which are more complex non-monotonous functions. (see example)

## Example

You can use the ``ZOCallable`` and ``ZOZOCallable`` for type hints of your own functions for example:

```python

from ZOCallable import ZOZOCallable

def non_linear_gradient(points: int, func: ZOZOCallable):
    if not verify_ZOZOCallable(func, test_vectorisation=True):
        raise ValueError("The provided function isn't a ZOZOCallable")
    return func(np.linspace(0, 1, points))
```
Here, ``lambda x:x**2`` or ``ZOCallable.functions.ease_in`` will satisfy the conditions and so be accepted, while ``lambda x:2*x`` would raise a ValueError

You can also use them for transitions or moves

```python
from ZOCallable.functions import bounce_out

class FallingBall:

    def __init__(self, height: float, bounces: int, duration: int)
        self.z = height
        self.height = height
        self.trajectory = bounce_out(bounces)
        self.duration = duration
        self.time = 0

    def udpate(self, dt):
        self.time += dt
        self.z = self.trajectory(self.time/self.duration)*self.height

    def get_altitude(self):
        return self.z
```

``bounce_out(n)`` being a non-monotonous ZOZOCallable, the fall of the ball here would follow the curve of the bounce_out.
A precomputed trajectory is faster and easier for modelization.

## Demonstration

Some of the functions have been plotted and are shown below.

![Ease function](docs/images/ease.png)

![Elastic functions](docs/images/ZOC.png)

![Circular](docs/images/ZOZOC.png)

## Contributing

Any feedback optimization or new function proposal is welcome.

## License

This library is under a GNU License.