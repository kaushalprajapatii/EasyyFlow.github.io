# --- Style1 Layout with Transparency Support ---
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from text_utils import wrap_text

# --- COLOR TRANSPARENCY SUPPORT ---
def apply_alpha_to_color(color, alpha_value=1.0):
    """Adds transparency to any color (supports hex or named colors)."""
    import matplotlib.colors as mcolors
    rgba = list(mcolors.to_rgba(color))
    rgba[-1] = alpha_value
    return tuple(rgba)

BOX_COLORS = ['#fbc02d', '#00e676', '#64b5f6', '#ff7043', '#ba68c8', '#4db6ac', '#ff8a65']

def draw_step_style1(ax, title, description, x, y, color, shadow_offset=0.15,
                    preview_mode=False, title_font=None, desc_font=None,
                    title_wrap=None, desc_wrap=None, alpha_value=1.0):
    box_width = 2.8
    box_height = 1.2
    title_box_height = 0.4
    title_box_width = box_width - 0.2

    title_box_x = x + 0.1
    title_box_y = y + box_height - title_box_height - 0.1

    if preview_mode:
        bg_patch = plt.Rectangle((x - 0.2, y - 0.2),
                                 box_width + 0.4, box_height + 0.4,
                                 facecolor='white', edgecolor='none',
                                 alpha=0.95, zorder=0)
        ax.add_patch(bg_patch)

    # Shadow (unchanged)
    shadow_box = FancyBboxPatch((x + shadow_offset, y - shadow_offset),
                                box_width, box_height,
                                boxstyle="round,pad=0.1,rounding_size=0.15",
                                linewidth=0, facecolor='gray',
                                alpha=0.3, zorder=1)
    ax.add_patch(shadow_box)

    # Main box with transparency
    main_box = FancyBboxPatch((x, y), box_width, box_height,
                              boxstyle="round,pad=0.1,rounding_size=0.15",
                              linewidth=1.5,
                              facecolor=apply_alpha_to_color(color, alpha_value),
                              edgecolor='black', zorder=2)
    ax.add_patch(main_box)

    # Title box (white background, no alpha)
    title_box = FancyBboxPatch((title_box_x, title_box_y),
                               title_box_width, title_box_height,
                               boxstyle="round,pad=0.05,rounding_size=0.1",
                               linewidth=1, facecolor='white',
                               edgecolor='black', alpha=0.9, zorder=3)
    ax.add_patch(title_box)

    # Text wrapping and drawing
    wrapped_title = wrap_text(title, title_wrap or 20)
    ax.text(title_box_x + title_box_width / 2, title_box_y + title_box_height / 2,
            wrapped_title, ha='center', va='center',
            fontproperties=title_font, color=color, zorder=4)

    wrapped_desc = wrap_text(description, desc_wrap or 33)
    ax.text(x + box_width / 2, y + (box_height - title_box_height) / 2 - 0.1,
            wrapped_desc, ha='center', va='center',
            fontproperties=desc_font, color='white', zorder=4)

def draw_angled_arrow(ax, start_x, start_y, end_x, end_y, color,
                      lw=10, direction='down', vertical_offset=0.3):
    adjusted_start_y = start_y + vertical_offset
    if direction == 'down':
        turn_x, turn_y1, turn_y2 = (start_x + end_x) / 2, adjusted_start_y - 1.09, end_y + 0.01
    else:
        turn_x, turn_y1, turn_y2 = (start_x + end_x) / 2, adjusted_start_y + 1.4, end_y

    path_x = [start_x, start_x, turn_x, turn_x, end_x]
    path_y = [adjusted_start_y, turn_y1, turn_y1, turn_y2, end_y]

    ax.plot(path_x, path_y, color='gray', linewidth=lw, alpha=0.3, zorder=1)
    ax.plot(path_x, path_y, color=color, linewidth=lw, zorder=3)

    ax.annotate("", xy=(end_x, end_y), xytext=(turn_x, turn_y2),
                arrowprops=dict(arrowstyle='->', color=color,
                                lw=lw, mutation_scale=40), zorder=4)

def create_flowchart(steps, figsize=None, preview_mode=False,
                     title_font=None, desc_font=None,
                     title_wrap=None, desc_wrap=None,
                     alpha_value=1.0):
    if figsize is None:
        figsize = (len(steps) * 3, 8)

    fig, ax = plt.subplots(figsize=figsize)

    if preview_mode:
        fig.patch.set_facecolor('white')
    else:
        fig.patch.set_alpha(0.0)
        ax.set_facecolor('none')

    ax.set_xlim(0, len(steps) * 3 + 1)
    ax.set_ylim(0, 6)
    ax.axis('off')

    for i, (title, description, color) in enumerate(steps):
        x = 1 + i * 3
        y = 4 if i % 2 == 0 else 2

        draw_step_style1(ax, title, description, x, y, color,
                         preview_mode=preview_mode,
                         title_font=title_font,
                         desc_font=desc_font,
                         title_wrap=title_wrap,
                         desc_wrap=desc_wrap,
                         alpha_value=alpha_value)

        if i < len(steps) - 1:
            next_y = 4 if (i + 1) % 2 == 0 else 2
            if y > next_y:
                start_y, end_y, direction = y - 0.6, next_y + 0.6, 'down'
            else:
                start_y, end_y, direction = y + 1.2, next_y + 0.6, 'up'

            draw_angled_arrow(ax, x + 1.25, start_y,
                              x + 3 - 0.1, end_y,
                              color='#555555', direction=direction)

    plt.tight_layout()
    return fig

# Example usage
if __name__ == "__main__":
    steps = [
        ("Input", "Load and validate input data", "#fbc02d"),
        ("Process", "Perform computations and analysis", "#4db6ac"),
        ("Train", "Run training and optimization", "#ba68c8"),
        ("Evaluate", "Generate evaluation report", "#ff7043"),
    ]
    fig = create_flowchart(steps, preview_mode=True, alpha_value=0.85)
    plt.show()