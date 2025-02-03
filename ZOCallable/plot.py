try:
    import matplotlib.pyplot as plt
except ImportError:
    print("matplotlib couldn't be imported, please install it.")
    import sys
    sys.exit(1)

import numpy as np
from typing import Sequence
from ZOCallable.ZOCallable import ZOCallable
from ZOCallable.ZOZOCallable import ZOZOCallable

def plot_ZOCallable(func: ZOCallable | Sequence[ZOZOCallable], vectorized = True):
    """Plot one or mulitple ZOCallable to visualize."""
    plt.figure()
    plt.hlines([0, 1], 0, 1, colors='k', linestyles='--')
    plt.plot([0, 1], [0, 1], c='#aaa', linestyle='--')
    plt.scatter([0, 1], [0, 1], marker='o')
    x = np.linspace(0, 1, 101)
    if isinstance(func, Sequence):
        for f in func:
            if vectorized:
                plt.plot(x, f(x))
            else:
                plt.plot(x, [f(t) for t in x])
    else:
        if vectorized:
            plt.plot(x, func(x))
        else:
            plt.plot(x, [func(t) for t in x])
    plt.grid()
    plt.xlim(-0.05, 1.05)
    plt.show()

def plot_ZOZOCallable(func: ZOZOCallable | Sequence[ZOZOCallable], vectorized = True):
    """Plot one or mulitple ZOZOCallable to visualize."""
    plt.figure()
    plt.hlines([0, 1], 0, 1, colors='k', linestyles='--')
    plt.plot([0, 1], [0, 1], c='#aaa', linestyle='--')
    plt.scatter([0, 1], [0, 1], marker='o')
    x = np.linspace(0, 1, 101)
    if isinstance(func, Sequence):
        for f in func:
            if vectorized:
                plt.plot(x, f(x))
            else:
                plt.plot(x, [f(t) for t in x])
    else:
        if vectorized:
            plt.plot(x, func(x))
        else:
            plt.plot(x, [func(t) for t in x])
    plt.grid()
    plt.xlim(-0.05, 1.05)
    plt.ylim(-0.05, 1.05)
    plt.show()
