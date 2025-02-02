"""The functions submodule contains some ZOCs and ZOZOCs."""
import numpy as np
from .ZOCallable import ZOCallable, normalize_ZOCallable, vectorize_ZOCallable
from .ZOZOCallable import ZOZOCallable

linear = lambda x:x

def power_in(n) -> ZOZOCallable:
    return lambda x: np.pow(x, n)

def power_out(n) -> ZOZOCallable:
    return lambda x: 1 - np.pow(1 - x, n)

def power_in_out(n) -> ZOZOCallable:
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
    - p0, p1, p2, p3: floats, 0 <= p <= 1. The parameters of the curve.
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

def bounce(n: int) -> ZOZOCallable:
    """
    Return a ZOCallable that looks like bounces.
    
    Params:
    ---
    - n: int >= 0, the number of bounces.
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

# add https://github.com/semitable/easing-functions/blob/master/easing_functions/easing.py
