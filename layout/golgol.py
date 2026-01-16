# --- Golgol Layout with Transparency Support ---
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
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
def create_flowchart(steps, figsize=None, preview_mode=False,
                     title_font=None, desc_font=None,
                     title_wrap=None, desc_wrap=None,
                     alpha_value=1.0):
    if figsize is None:
        figsize = (len(steps)*3, 7)

    fig, ax = plt.subplots(figsize=figsize)

    if preview_mode:
        fig.patch.set_facecolor('white')
    else:
        fig.patch.set_alpha(0.0)
        ax.set_facecolor('none')

    ax.set_xlim(0, len(steps)*3 + 1)
    ax.set_ylim(0, 6)
    ax.axis('off')

    box_width = 2.6
    box_height = 1.3
    step_positions = []

    # --- DRAW MAIN BOXES (transparency applied) ---
    for i, (title, description, color) in enumerate(steps):
        x = 1 + i*3
        y = 3.2 if i % 2 == 0 else 1.5

        # Shadow
        shadow_box = FancyBboxPatch(
            (x + 0.15, y - 0.15), box_width, box_height,
            boxstyle="round,pad=0.15,rounding_size=0.2",
            linewidth=0, facecolor='gray', alpha=0.3, zorder=1
        )
        ax.add_patch(shadow_box)

        # Main box (transparency added)
        main_box = FancyBboxPatch(
            (x, y), box_width, box_height,
            boxstyle="round,pad=0.15,rounding_size=0.2",
            linewidth=1.8,
            facecolor=apply_alpha_to_color(color, alpha_value),
            edgecolor='black', zorder=2
        )
        ax.add_patch(main_box)

        # Text (title + description)
        wrapped_title = wrap_text(title, title_wrap or 18)
        wrapped_desc = wrap_text(description, desc_wrap or 30)

        ax.text(x + box_width/2, y + box_height*0.7, wrapped_title,
                ha='center', va='center',
                fontproperties=title_font, color='white', zorder=3)

        ax.text(x + box_width/2, y + box_height*0.3, wrapped_desc,
                ha='center', va='center',
                fontproperties=desc_font, color='white', zorder=3)

        step_positions.append((x + box_width/2, y + box_height/2))

    # --- DRAW ARROWS (unchanged) ---
    for i in range(len(step_positions) - 1):
        start_x, start_y = step_positions[i]
        end_x, end_y = step_positions[i + 1]
        rad = 0.25 if i % 2 == 0 else -0.25

        arrow = FancyArrowPatch(
            (start_x + box_width/2 - 0.3, start_y),
            (end_x - box_width/2 + 0.3, end_y),
            connectionstyle=f"arc3,rad={rad}",
            arrowstyle='-|>', mutation_scale=20,
            lw=2.5, color='black',
            path_effects=[pe.withStroke(linewidth=4, foreground="lightgray", alpha=0.4)],
            zorder=2
        )
        ax.add_patch(arrow)

    plt.tight_layout()
    return fig

# Example usage
if __name__ == "__main__":
    steps = [
        ("Start", "Initialize process and load data", "#fbc02d"),
        ("Analyze", "Perform data analysis", "#4db6ac"),
        ("Model", "Train model and tune hyperparameters", "#ba68c8"),
        ("Deploy", "Deploy the trained model", "#ff7043"),
    ]
    fig = create_flowchart(steps, preview_mode=True, alpha_value=0.85)
    plt.show()