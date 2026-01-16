# --- Milestone Layout with Transparency Support ---
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle
import numpy as np
from text_utils import wrap_text

# --- COLOR TRANSPARENCY SUPPORT ---
def apply_alpha_to_color(color, alpha_value=1.0):
    """Adds transparency to any color (supports hex or named colors)."""
    import matplotlib.colors as mcolors
    rgba = list(mcolors.to_rgba(color))
    rgba[-1] = alpha_value
    return tuple(rgba)

# --- MAIN FUNCTION ---
def create_flowchart(steps, figsize=(10, 6), preview_mode=False,
                     title_font=None, desc_font=None,
                     title_wrap=None, desc_wrap=None,
                     alpha_value=1.0):
    fig, ax = plt.subplots(figsize=figsize)

    if preview_mode:
        fig.patch.set_facecolor('white')
    else:
        fig.patch.set_alpha(0.0)
        ax.set_facecolor('none')

    ax.set_xlim(0, len(steps)*3 + 2)
    ax.set_ylim(0, 6)
    ax.axis('off')

    step_positions = []
    circle_radius = 0.3

    # --- DRAW TIMELINE LINE ---
    ax.plot([0.5, len(steps)*3 + 1.5], [3, 3], color='gray', lw=3, zorder=1)

    # --- DRAW MILESTONES (with transparency) ---
    for i, (title, description, color) in enumerate(steps):
        x = 1 + i*3
        y = 3

        # Circle (milestone marker)
        circle = Circle((x, y), circle_radius,
                        facecolor=apply_alpha_to_color(color, alpha_value),
                        edgecolor='black', lw=1.5, zorder=2)
        ax.add_patch(circle)

        # Box for description
        desc_y = 3.7 if i % 2 == 0 else 1.5
        desc_box = FancyBboxPatch((x - 1.4, desc_y - 0.4), 2.8, 0.8,
                                  boxstyle="round,pad=0.15,rounding_size=0.2",
                                  linewidth=1.5,
                                  facecolor=apply_alpha_to_color(color, alpha_value),
                                  edgecolor='black', zorder=2)
        ax.add_patch(desc_box)

        # Text (title and description)
        wrapped_title = wrap_text(title, title_wrap or 18)
        wrapped_desc = wrap_text(description, desc_wrap or 25)

        ax.text(x, 3.05, wrapped_title, ha='center', va='bottom',
                fontproperties=title_font, color='black', zorder=3)

        ax.text(x, desc_y, wrapped_desc, ha='center', va='center',
                fontproperties=desc_font, color='white', zorder=3)

        step_positions.append((x, y))

    plt.tight_layout()
    return fig

# Example usage
if __name__ == "__main__":
    steps = [
        ("2008", "Company founded", "#fbc02d"),
        ("2011", "First product launch", "#4db6ac"),
        ("2015", "Expansion into new markets", "#ba68c8"),
        ("2019", "Global recognition achieved", "#ff7043"),
        ("2023", "AI-driven innovation", "#64b5f6")
    ]
    fig = create_flowchart(steps, preview_mode=True, alpha_value=0.8)
    plt.show()