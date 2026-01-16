# --- Style2 Layout with Transparency Support ---
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, ArrowStyle
import numpy as np
from text_utils import wrap_text

# --- COLOR TRANSPARENCY SUPPORT ---
def apply_alpha_to_color(color, alpha_value=1.0):
    """Adds transparency to any color (supports hex or named colors)."""
    import matplotlib.colors as mcolors
    rgba = list(mcolors.to_rgba(color))
    rgba[-1] = alpha_value
    return tuple(rgba)

BOX_COLORS = ['#d62828', '#f77f00', '#0077b6', '#38b000', '#7209b7', '#3a0ca3', "#dccf1d"]

def draw_step_style2(ax, title, description, x, y, color,
                    shadow_offset=0.12, preview_mode=False,
                    title_font=None, desc_font=None,
                    title_wrap=None, desc_wrap=None,
                    alpha_value=1.0):
    box_width = 2.8
    box_height = 1.3

    # Background shadow
    shadow_box = FancyBboxPatch((x + shadow_offset, y - shadow_offset),
                                box_width, box_height,
                                boxstyle="round,pad=0.15,rounding_size=0.15",
                                linewidth=0, facecolor='gray',
                                alpha=0.3, zorder=1)
    ax.add_patch(shadow_box)

    # Main box (with transparency)
    main_box = FancyBboxPatch((x, y), box_width, box_height,
                              boxstyle="round,pad=0.15,rounding_size=0.15",
                              linewidth=1.5,
                              facecolor=apply_alpha_to_color(color, alpha_value),
                              edgecolor='black', zorder=2)
    ax.add_patch(main_box)

    # Title and description
    wrapped_title = wrap_text(title, title_wrap or 20)
    wrapped_desc = wrap_text(description, desc_wrap or 35)

    ax.text(x + box_width/2, y + box_height*0.7, wrapped_title,
            ha='center', va='center',
            fontproperties=title_font, color='white', zorder=3)
    ax.text(x + box_width/2, y + box_height*0.35 - 0.3, wrapped_desc,
            ha='center', va='center',
            fontproperties=desc_font, color='white', zorder=3)

def draw_arrow_style2(ax, start_x, start_y, end_x, end_y, color, lw=8, direction='right'):
    if direction == 'right':
        ax.annotate('', xy=(end_x, end_y), xytext=(start_x, start_y),
                    arrowprops=dict(arrowstyle='-|>', color=color,
                                    lw=lw, mutation_scale=25), zorder=3)
    else:
        ax.annotate('', xy=(end_x, end_y), xytext=(start_x, start_y),
                    arrowprops=dict(arrowstyle='<|-', color=color,
                                    lw=lw, mutation_scale=25), zorder=3)

def create_flowchart(steps, figsize=None, preview_mode=False,
                     title_font=None, desc_font=None,
                     title_wrap=None, desc_wrap=None,
                     alpha_value=1.0):
    if figsize is None:
        figsize = (len(steps)*3, 6)

    fig, ax = plt.subplots(figsize=figsize)

    if preview_mode:
        fig.patch.set_facecolor('white')
    else:
        fig.patch.set_alpha(0.0)
        ax.set_facecolor('none')

    ax.set_xlim(0, len(steps)*3 + 1)
    ax.set_ylim(0, 5)
    ax.axis('off')

    for i, (title, description, color) in enumerate(steps):
        x = 1 + i*3
        y = 2.5

        draw_step_style2(ax, title, description, x, y, color,
                         preview_mode=preview_mode,
                         title_font=title_font,
                         desc_font=desc_font,
                         title_wrap=title_wrap,
                         desc_wrap=desc_wrap,
                         alpha_value=alpha_value)

        if i < len(steps) - 1:
            start_x = x + 2.8
            end_x = x + 3
            draw_arrow_style2(ax, start_x, y + 0.65, end_x, y + 0.65,
                              color='#444444', lw=3, direction='right')

    plt.tight_layout()
    return fig

# Example usage
if __name__ == "__main__":
    steps = [
        ("Data Collection", "Gather relevant data for analysis", "#d62828"),
        ("Preprocessing", "Clean and normalize the dataset", "#f77f00"),
        ("Training", "Train the machine learning model", "#0077b6"),
        ("Evaluation", "Assess model performance", "#38b000"),
        ("Deployment", "Deploy the model to production", "#7209b7"),
    ]
    fig = create_flowchart(steps, preview_mode=True, alpha_value=0.8)
    plt.show()