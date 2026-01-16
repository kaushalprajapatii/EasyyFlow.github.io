# transparency.py
import matplotlib.colors as mcolors

def apply_alpha_to_color(color, alpha_value=1.0):
    """
    Takes any Matplotlib-compatible color (hex, name, RGBA) 
    and applies the given alpha (transparency) value.
    Returns an RGBA tuple.
    """
    rgba = list(mcolors.to_rgba(color))
    rgba[-1] = alpha_value
    return tuple(rgba)
