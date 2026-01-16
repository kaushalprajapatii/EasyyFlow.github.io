# --- Vertical Layout with Transparency Support ---
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
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
def create_flowchart(steps, figsize=(6, 10), preview_mode=False,
                     title_font=None, desc_font=None,
                     title_wrap=None, desc_wrap=None,
                     alpha_value=1.0):
    fig, ax = plt.subplots(figsize=figsize)

    if preview_mode:
        fig.patch.set_facecolor('white')
    else:
        fig.patch.set_alpha(0.0)
        ax.set_facecolor('none')

    ax.set_xlim(0, 6)
    ax.set_ylim(0, len(steps)*3)
    ax.axis('off')

    box_width = 4.5
    box_height = 1.2

    for i, (title, description, color) in enumerate(steps):
        x = 0.8
        y = len(steps)*3 - (i+1)*3 + 0.6

        # Shadow box
        shadow_box = FancyBboxPatch((x + 0.15, y - 0.15), box_width, box_height,
                                    boxstyle="round,pad=0.15,rounding_size=0.15",
                                    linewidth=0, facecolor='gray', alpha=0.3, zorder=1)
        ax.add_patch(shadow_box)

        # Main box (transparency applied)
        main_box = FancyBboxPatch((x, y), box_width, box_height,
                                  boxstyle="round,pad=0.15,rounding_size=0.15",
                                  linewidth=1.5,
                                  facecolor=apply_alpha_to_color(color, alpha_value),
                                  edgecolor='black', zorder=2)
        ax.add_patch(main_box)

        # Text
        wrapped_title = wrap_text(title, title_wrap or 22)
        wrapped_desc = wrap_text(description, desc_wrap or 38)

        ax.text(x + box_width/2, y + box_height*0.7, wrapped_title,
                ha='center', va='center',
                fontproperties=title_font, color='white', zorder=3)
        ax.text(x + box_width/2, y + box_height*0.3 - 0.2, wrapped_desc,
                ha='center', va='center',
                fontproperties=desc_font, color='white', zorder=3)

        # Draw arrow (unchanged)
        if i < len(steps) - 1:
            ax.annotate('', xy=(x + box_width/2, y - 0.2),
                        xytext=(x + box_width/2, y - 1.8),
                        arrowprops=dict(arrowstyle='-|>',
                                        color=color,
                                        lw=3,
                                        path_effects=[pe.withStroke(linewidth=5,
                                                                    foreground="lightgray",
                                                                    alpha=0.5)]),
                        zorder=3)

    plt.tight_layout()
    return fig

# Example usage
if __name__ == "__main__":
    steps = [
        ("Data Input", "Collect input data and files", "#d62828"),
        ("Preprocessing", "Clean and normalize dataset", "#f77f00"),
        ("Model Training", "Train machine learning model", "#0077b6"),
        ("Evaluation", "Compute accuracy and metrics", "#38b000"),
        ("Deployment", "Deploy model into production", "#7209b7")
    ]
    fig = create_flowchart(steps, preview_mode=True, alpha_value=0.8)
    plt.show()