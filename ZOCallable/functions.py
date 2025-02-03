"""The functions submodule contains some ZOCs and ZOZOCs."""
import numpy as np
from .ZOCallable import ZOCallable, normalize_ZOCallable, vectorize_ZOCallable
from .ZOZOCallable import ZOZOCallable

linear = lambda x:x

def power_in(n) -> ZOZOCallable:
    """Power_in functions are the polynomial functions f(x) = x^n."""
    return lambda x: np.pow(x, n)

def power_out(n) -> ZOZOCallable:
    """Power_out functions are the polynomial functions f(x) = 1 - (1-x)^n."""
    return lambda x: 1 - np.pow(1 - x, n)

def power_in_out(n) -> ZOZOCallable:
    """Power_out functions are a combination of a power_in for x < 0.5 and power_out for x > 0.5."""
    return vectorize_ZOCallable(lambda x: (2**(n-1)) *np.pow(x, n) if x < 0.5 else 1 - np.pow(1 - x, n)*(2**(n-1)))

square_in = power_in(2)
square_out = power_out(2)
square_in_out = power_in_out(2)
root_out = lambda x: np.sqrt(x)
root_in = lambda x: 1 - np.sqrt(1 - x)
    
def cubic_bezier(x1, y1, x2, y2, precision: float = 2**(-8)) -> ZOCallable:
    """
    Return a ZOCallable following a cubic bezier curve.
    
    Params:
    ----
    - x1, y1, x2, y2: float, The control points of the bezier curve, with the end and start points at (0, 0) and (1, 1).
    x1 and x2 must be in [0, 1], for the cubic_bezier to be a ZOZOCallable, y1 and y2 must be in [0, 1], otherwise the 
    returned function is only a ZOCallable
    The bezier curve is created following css notations, and can be explored here https://cubic-bezier.com
    - precision: float << 1, used to approximate (see warning below)

    Returns:
    ----
    - ease: ZOCallable, the function y(x) following the bezier curve.
    
    Examples:
    ---
    ```python
    ease = cubic_bezier(0.25, 1., 0.25, 1.)
    ease_in = cubic_bezier(0.12, 0, 0.39, 0)
    ease_out = cubic_bezier(0.61, 1, 0.88, 1)
    ease_in_out = cubic_bezier(0.37, 0, 0.63, 1)
    ```
    these functions are already defined in the same module.
    

    Warning:
    ---
    As bezier curves are parametric (i.e. defined as (x(t), y(t)) with t in [0, 1]) and as there is no mathematical
    formula for y(x), it is approach via a dichotomy method, with a given precision. Thus, for a very smooth curve,
    it is adviced to a high precision. For most applications, 2^(-8) is precise enough. 
    """

    x0 = 0
    y0 = 0
    x3 = 1
    y3 = 1
    bezier_curve_x = lambda t: (1.-t)**3 * x0 + 3*(1.-t)**2*t * x1 + 3*(1.-t)*t**2 * x2 + t**3 * x3
    bezier_curve_y = lambda t: (1.-t)**3 * y0 + 3*(1.-t)**2*t * y1 + 3*(1.-t)*t**2 * y2 + t**3 * y3
    
    def find_y(x):
        if x < 0 or x > 1:
            raise ValueError(f"The input should be inside [0, 1], got {x}")
        if x == 0 or x == 1:
            return x
        t_left = 0.
        t_right = 1.
        x_left = bezier_curve_x(t_left)
        x_right = bezier_curve_x(t_right)
        while abs(x_right - x_left) > precision: # Dichotomy to find the t.
            x_center = bezier_curve_x((t_right + t_left)/2)
            if x_center > x:
                t_right = (t_right + t_left)/2
                x_right = x_center
            else:
                t_left = (t_right + t_left)/2
                x_left = x_center

        return bezier_curve_y((t_right + t_left)/2)
    
    return vectorize_ZOCallable(find_y)

ease = cubic_bezier(0.25, 1., 0.25, 1.)
ease_in = cubic_bezier(0.12, 0, 0.39, 0)
ease_out = cubic_bezier(0.61, 1, 0.88, 1)
ease_in_out = cubic_bezier(0.37, 0, 0.63, 1)

def bounce_out(n: int) -> ZOZOCallable:
    """
    Return a ZOCallable that looks like bounces for large values.
    
    Params:
    ---
    - n: int >= 0, the number of bounces.

    Raises:
    ----
    ValueError, if n < 0.
    """
    if n < 0 or not isinstance(n, int):
        raise ValueError(f"{n} is not an acceptable argument for the number of bounce.")
    def bounce_n(x):
        if x == 0:  # Handle the edge case to avoid division by zero
            return x
        new_x = (n+1) * np.pi * np.power(x, 3/2)
        sinc = np.sin(new_x) / new_x
        return 1 - np.abs(sinc)
    bounce_n = vectorize_ZOCallable(bounce_n)
    return bounce_n

def bounce_in(n: int):
    """
    Return a ZOCallable that looks like bounces for small values.
    
    Params:
    ---
    - n: int >= 0, the number of bounces.

    Raises:
    ----
    ValueError, if n < 0.
    """

    bounce_in_n = bounce_out(n)
    return lambda x:1 - bounce_in_n(1 - x)

def jump(n: int) -> ZOZOCallable:
    """
    Return a ZOCallable being successive jumps.
    
    Params:
    ---
    - n: int >= 0, the number of jump.

    Returns:
    ----
    jump_n: a ZOZOCallable, whose graph looks like jumps, or stairs. The function as 1 jump at t = 1, the other are evenly spread between t = 0 and t = 1

    Raises:
    ----
    ValueError, if n <= 0.
    """

    if n <= 0:
        raise ValueError(f"{n} is not an acceptable argument for the number of jumps.")
    return lambda x: np.round(x*n)/n

exp_in = normalize_ZOCallable(np.exp)
exp_out = normalize_ZOCallable(lambda t: 1 - (1 - np.exp(t)))


# functions taken from https://github.com/semitable/easing-functions/blob/master/easing_functions/easing.py

sin_in = lambda x: np.sin((x - 1) * np.pi / 2) + 1
sin_out = lambda x: np.sin(x * np.pi / 2)
sin_in_out = lambda x: 0.5 * (1 - np.cos(x * np.pi))

circular_in = lambda x: 1 - root_in(1 - square_out(x))
circular_out = lambda x: 1 - root_out(1 - square_in(x))
circular_in_out = vectorize_ZOCallable(lambda x: 0.5 * (np.sqrt(-((2 * x) - 3) * ((2 * x) - 1)) + 1) if x > 0.5 else 0.5 * (1 - np.sqrt(1 - 4 * np.pow(x, 2))))

elastic_in = lambda x: np.sin(13 * np.pi / 2 * x)  / np.pow(2, 10 * (1 - x))
elastic_out = lambda x: np.sin(-13 * np.pi / 2 * (x + 1)) * np.pow(2, -10 * x) + 1
elastic_in_out = vectorize_ZOCallable(
    lambda x: (
        0.5 * np.sin(13 * np.pi / 2 * (2 * x)) * np.pow(2, 10 * ((2 * x) - 1))
    ) if x< 0.5 else (
        0.5 * ( np.sin(-13 * np.pi / 2 * ((2 * x - 1) + 1)) * np.pow(2, -10 * (2 * x - 1)) + 2)
    )
)

back_in = lambda x: np.pow(x, 3) - x * np.sin(x * np.pi)
back_out = lambda x: 1 - back_in(1 - x)
back_in_out = vectorize_ZOCallable(lambda x: 0.5*back_in(2*x) if x < 0.5 else 0.5*(1- back_in(1 - 2*x)))

