try:
    import matplotlib.pyplot as plt
except ImportError:
    print("matplotlib couldn't be imported, please install it.")
    import sys
    sys.exit(1)

import numpy as np
from typing import Sequence
from ZOCallable.ZOCallable import ZOCallable, ZOZOCallable

def plot_ZOCallable(*func: tuple[ZOCallable], vectorized = True, save_path: str = "", labels: Sequence[str] = []):
    """
    Plot one or mulitple ZOCallable to visualize.
    
    Params:
    ----
    - func: ZOCallable, the functions to plot.
    - vectorized: bool, specify whether the functions are vectorized or not.
    - save_path: str = "", if specified, the plot isn't showed but saved

    The functions are plotted for x from 0 to 1, x = y is plotted in the background.
    """
    plt.figure()
    plt.plot([0, 1], [0, 1], c='#333', linestyle='--', label='')
    x = np.linspace(0, 1, 101)
    if not labels:
        lbls = ["" for _ in func]
    else:
        lbls = labels
    for f, lbl in zip(func, lbls):
        if vectorized:
            plt.plot(x, f(x), label=lbl)
        else:
            plt.plot(x, [f(t) for t in x], label=lbl)
    plt.grid()
    if labels:
        plt.legend()
    plt.xlim(-0.01, 1.01)
    plt.scatter([0, 1], [0, 1], marker='o', label='', c='k')
    if save_path:
        plt.savefig(save_path)
    else:
        plt.show()

def plot_ZOZOCallable(*func: ZOZOCallable, vectorized = True, save_path: str = "", labels: Sequence[str] = []):
    """
    Plot one or mulitple ZOZOCallable to visualize.
    
    Params:
    ----
    - func: ZOCallable, the functions to plot.
    - vectorized: bool, specify whether the functions are vectorized or not.
    - save_path: str = "", if specified, the plot isn't showed but saved


    The functions are plotted for x from 0 to 1, x = y is plotted in the background.
    As ZOZOCallables should range in [0, 1], the ylim is fixed to [0, 1].
    """
    plt.figure()
    plt.plot([0, 1], [0, 1], c='#333', linestyle='--')
    x = np.linspace(0, 1, 101)
    if not labels:
        lbls = ["" for _ in func]
    else:
        lbls = labels
    for f, lbl in zip(func, lbls):
        if vectorized:
            plt.plot(x, f(x), label=lbl)
        else:
            plt.plot(x, [f(t) for t in x], label=lbl)
    plt.grid()
    if labels:
        plt.legend()
    plt.xlim(-0.01, 1.01)
    plt.ylim(-0.01, 1.01)
    plt.scatter([0, 1], [0, 1], marker='o', c='k')
    if save_path:
        plt.savefig(save_path)
    else:
        plt.show()
