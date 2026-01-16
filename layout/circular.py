# --- Circular Layout with Transparency Support ---
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch
import numpy as np
import matplotlib.patheffects as pe
from text_utils import wrap_text

# --- COLOR TRANSPARENCY SUPPORT ---
def apply_alpha_to_color(color, alpha_value=1.0):
    """Adds transparency to any color (supports hex or named colors)."""
    import matplotlib.colors as mcolors
    rgba = list(mcolors.to_rgba(color))
    rgba[-1] = alpha_value
    return tuple(rgba)

# --- MAIN FUNCTION ---
def create_flowchart(steps, figsize=(8, 8), preview_mode=False,
                     title_font=None, desc_font=None,
                     title_wrap=None, desc_wrap=None,
                     alpha_value=1.0):
    fig, ax = plt.subplots(figsize=figsize)

    if preview_mode:
        fig.patch.set_facecolor('white')
    else:
        fig.patch.set_alpha(0)
        ax.set_facecolor('none')

    ax.set_xlim(-6, 6)
    ax.set_ylim(-6, 6)
    ax.axis('off')

    num_steps = len(steps)
    radius = 3.5
    circle_radius = 0.9
    positions = []

    # --- DRAW MAIN CIRCLES (transparency applied) ---
    for i, (title, description, color) in enumerate(steps):
        angle = 2 * np.pi * i / num_steps
        x = radius * np.cos(angle)
        y = radius * np.sin(angle)

        # Circle background with alpha
        main_circle = Circle((x, y), circle_radius,
                             facecolor=apply_alpha_to_color(color, alpha_value),
                             edgecolor='black', lw=1.8, zorder=2)
        ax.add_patch(main_circle)

        # Title and description
        wrapped_title = wrap_text(title, title_wrap or 15)
        wrapped_desc = wrap_text(description, desc_wrap or 25)

        ax.text(x, y + 0.2, wrapped_title,
                ha='center', va='center',
                fontproperties=title_font, color='white', zorder=3)
        ax.text(x, y - 0.3, wrapped_desc,
                ha='center', va='center',
                fontproperties=desc_font, color='white', zorder=3)

        positions.append((x, y))

    # --- DRAW ARROWS BETWEEN CIRCLES (unchanged) ---
    for i in range(num_steps):
        start_x, start_y = positions[i]
        end_x, end_y = positions[(i + 1) % num_steps]

        arrow = FancyArrowPatch(
            (start_x, start_y),
            (end_x, end_y),
            connectionstyle="arc3,rad=0.3",
            arrowstyle='-|>', mutation_scale=20,
            lw=2.5, color='black',
            path_effects=[pe.withStroke(linewidth=4, foreground="lightgray", alpha=0.4)],
            zorder=1
        )
        ax.add_patch(arrow)

    plt.tight_layout()
    return fig

# Example usage
if __name__ == "__main__":
    steps = [
        ("Idea", "Generate project concept", "#fbc02d"),
        ("Design", "Create layout and flow", "#4db6ac"),
        ("Develop", "Write and test code", "#ba68c8"),
        ("Deploy", "Launch to production", "#ff7043"),
    ]
    fig = create_flowchart(steps, preview_mode=True, alpha_value=0.8)
    plt.show()