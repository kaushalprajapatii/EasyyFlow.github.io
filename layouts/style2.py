# # Curved Arrows with Title/Description Separation
# import matplotlib.pyplot as plt
# from matplotlib.patches import FancyBboxPatch, PathPatch
# from matplotlib.path import Path
# import matplotlib.patheffects as pe
# import textwrap
# import math
# from text_utils import apply_text_settings, wrap_text
# SET2_COLORS = plt.cm.Set2.colors

# def draw_curved_arrow(ax, start, end, color, direction='down'):
#     safety_margin = 0.15
#     start_x, start_y = start
#     end_x, end_y = end

#     if direction == 'down':
#         start_y -= safety_margin
#         end_y -= safety_margin
#         control_y = min(start_y, end_y) - 1.0
#     else:
#         start_y += safety_margin
#         end_y += safety_margin
#         control_y = max(start_y, end_y) + 1.0

#     control_x = (start_x + end_x) / 2
#     path = Path([(start_x, start_y), (control_x, control_y), (end_x, end_y)],
#                 [Path.MOVETO, Path.CURVE3, Path.CURVE3])

#     patch = PathPatch(path, fc="none", ec=color, lw=2.5, zorder=2,
#                       path_effects=[pe.withStroke(linewidth=4, foreground="lightgray", alpha=0.4)])
#     ax.add_patch(patch)

#     angle = math.atan2(end_y - control_y, end_x - control_x)
#     arrow_size = 0.2
#     for offset in [math.pi/6, -math.pi/6]:
#         ax.plot([end_x, end_x - arrow_size * math.cos(angle + offset)],
#                 [end_y, end_y - arrow_size * math.sin(angle + offset)],
#                 color=color, lw=5, zorder=50)

# # UPDATED: Function signature changed to accept font properties
# def create_flowchart(steps_text, preview_mode=False, title_font=None, desc_font=None):
#     steps = []
#     for i, line in enumerate(steps_text.split('\n')):
#         if ':' in line:
#             title, desc = line.split(':', 1)
#             steps.append({
#                 'title': title.strip(),
#                 'desc': desc.strip(),
#                 'color': SET2_COLORS[i % len(SET2_COLORS)]
#             })

#     if not steps:
#         fig, ax = plt.subplots()
#         ax.axis('off')
#         return fig

#     fig, ax = plt.subplots(figsize=(max(10, len(steps)*4), 6))
    
#     if preview_mode:
#         fig.patch.set_facecolor('white')
#     else:
#         fig.patch.set_alpha(0)
#         ax.set_facecolor('none')
    
#     ax.set_xlim(-1.5, len(steps)*4)
#     ax.set_ylim(-2.5, 5)
#     ax.axis('off')

#     step_data = []
#     for i, step in enumerate(steps):
#         x, y = i * 4, 1.5
#         title_pos = 'below' if i % 2 == 0 else 'above'
#         color = step["color"]

#         desc_shadow = FancyBboxPatch((x+0.1, y-0.1), 3, 1.5, boxstyle="round,pad=0.1,rounding_size=0.05",
#                                      facecolor='gray', alpha=0.25, linewidth=0, zorder=1)
#         ax.add_patch(desc_shadow)
#         desc_box = FancyBboxPatch((x, y), 3, 1.5, boxstyle="round,pad=0.1,rounding_size=0.05",
#                                   facecolor='white', edgecolor='black', linewidth=1.5, zorder=2)
#         ax.add_patch(desc_box)

#         # UPDATED: Using fontproperties instead of fontsize
#         wrapped_desc = textwrap.fill(step['desc'], width=28)
#         ax.text(x + 1.5, y + 0.75, wrapped_desc,
#                 ha='center', va='center', fontproperties=desc_font, zorder=3, wrap=True)

#         title_y = y - 0.75 if title_pos == 'below' else y + 1.65
#         title_center = (x + 1.5, title_y + 0.3 if title_pos == 'above' else title_y)

#         title_shadow = FancyBboxPatch((x + 0.8 + 0.1, title_y - 0.1), 1.4, 0.6,
#                                       boxstyle="round,pad=0.05", linewidth=0,
#                                       facecolor='gray', alpha=0.3, zorder=1)
#         ax.add_patch(title_shadow)
#         title_box = FancyBboxPatch((x + 0.8, title_y), 1.4, 0.6,
#                                    boxstyle="round,pad=0.05", facecolor=color,
#                                    edgecolor='none', zorder=3)
#         ax.add_patch(title_box)

#         # UPDATED: Using fontproperties instead of fontsize
#         wrapped_title = textwrap.fill(step['title'], width=15)
#         ax.text(x + 1.5, title_y + 0.3, wrapped_title,
#                 ha='center', va='center',
#                 fontproperties=title_font,
#                 color='white', zorder=4,
#                 wrap=True)

#         step_data.append({
#             'title_center': title_center,
#             'desc_box_bottom': (x + 1.5, y - 0.1),
#             'desc_box_top': (x + 1.5, y + 1.5),
#             'color': color
#         })

#     for i in range(len(step_data) - 1):
#         current, next_step = step_data[i], step_data[i+1]
#         if i % 2 == 0:
#             start = (current['title_center'][0], current['title_center'][1] - 0.3)
#             end = (next_step['desc_box_bottom'][0], next_step['desc_box_bottom'][1] + 0.1)
#             draw_curved_arrow(ax, start, end, current['color'], direction='down')
#         else:
#             start = (current['title_center'][0], current['title_center'][1] + 0.3)
#             end = (next_step['desc_box_top'][0], next_step['desc_box_top'][1] - 0.1)
#             draw_curved_arrow(ax, start, end, current['color'], direction='up')

#     plt.tight_layout()
#     return fig

# --- Curved Arrows with Title/Description Separation (Fixed Version) ---
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, PathPatch
from matplotlib.path import Path
import matplotlib.patheffects as pe
import textwrap
import math
from text_utils import apply_text_settings, wrap_text  # make sure this file exists
from transparency import apply_alpha_to_color


SET2_COLORS = plt.cm.Set2.colors

def draw_curved_arrow(ax, start, end, color, direction='down'):
    safety_margin = 0.15
    start_x, start_y = start
    end_x, end_y = end

    if direction == 'down':
        start_y -= safety_margin
        end_y -= safety_margin
        control_y = min(start_y, end_y) - 1.0
    else:
        start_y += safety_margin
        end_y += safety_margin
        control_y = max(start_y, end_y) + 1.0

    control_x = (start_x + end_x) / 2
    path = Path([(start_x, start_y), (control_x, control_y), (end_x, end_y)],
                [Path.MOVETO, Path.CURVE3, Path.CURVE3])

    patch = PathPatch(
        path, fc="none", ec=color, lw=2.5, zorder=2,
        path_effects=[pe.withStroke(linewidth=4, foreground="lightgray", alpha=0.4)]
    )
    ax.add_patch(patch)

    # Arrowhead
    angle = math.atan2(end_y - control_y, end_x - control_x)
    arrow_size = 0.2
    for offset in [math.pi/6, -math.pi/6]:
        ax.plot(
            [end_x, end_x - arrow_size * math.cos(angle + offset)],
            [end_y, end_y - arrow_size * math.sin(angle + offset)],
            color=color, lw=5, zorder=50
        )


def create_flowchart(
    steps_text, 
    preview_mode=False, 
    title_font=None, 
    desc_font=None,
    title_wrap=None, 
    desc_wrap=None
):
    steps = []
    for i, line in enumerate(steps_text.split('\n')):
        if ':' in line:
            title, desc = line.split(':', 1)
            steps.append({
                'title': title.strip(),
                'desc': desc.strip(),
                'color': SET2_COLORS[i % len(SET2_COLORS)]
            })

    if not steps:
        fig, ax = plt.subplots()
        ax.axis('off')
        return fig

    fig, ax = plt.subplots(figsize=(max(10, len(steps)*4), 6))
    
    if preview_mode:
        fig.patch.set_facecolor('white')
    else:
        fig.patch.set_alpha(0)
        ax.set_facecolor('none')
    
    ax.set_xlim(-1.5, len(steps)*4)
    ax.set_ylim(-2.5, 5)
    ax.axis('off')

    step_data = []
    for i, step in enumerate(steps):
        x, y = i * 4, 1.5
        title_pos = 'below' if i % 2 == 0 else 'above'
        color = step["color"]

        # --- Description Box ---
        desc_shadow = FancyBboxPatch(
            (x+0.1, y-0.1), 3, 1.5,
            boxstyle="round,pad=0.1,rounding_size=0.05",
            facecolor='gray', alpha=0.25, linewidth=0, zorder=1
        )
        ax.add_patch(desc_shadow)
        desc_box = FancyBboxPatch(
            (x, y), 3, 1.5,
            boxstyle="round,pad=0.1,rounding_size=0.05",
            facecolor='white', edgecolor='black', linewidth=1.5, zorder=2
        )
        ax.add_patch(desc_box)

        # --- Description Text ---
        wrapped_desc = wrap_text(step['desc'], desc_wrap or 28)
        ax.text(
            x + 1.5, y + 0.75, wrapped_desc,
            ha='center', va='center',
            fontproperties=desc_font, zorder=3, wrap=True, color='black'
        )

        # --- Title Box ---
        title_y = y - 0.75 if title_pos == 'below' else y + 1.65
        title_center = (x + 1.5, title_y + 0.3 if title_pos == 'above' else title_y)

        title_shadow = FancyBboxPatch(
            (x + 0.8 + 0.1, title_y - 0.1), 1.4, 0.6,
            boxstyle="round,pad=0.05", linewidth=0,
            facecolor='gray', alpha=0.3, zorder=1
        )
        ax.add_patch(title_shadow)
        title_box = FancyBboxPatch(
            (x + 0.8, title_y), 1.4, 0.6,
            boxstyle="round,pad=0.05", facecolor=color,
            edgecolor='none', zorder=3
        )
        ax.add_patch(title_box)

        # --- Title Text ---
        wrapped_title = wrap_text(step['title'], title_wrap or 15)
        ax.text(
            x + 1.5, title_y + 0.3, wrapped_title,
            ha='center', va='center',
            fontproperties=title_font,
            color='white', zorder=4, wrap=True
        )

        step_data.append({
            'title_center': title_center,
            'desc_box_bottom': (x + 1.5, y - 0.1),
            'desc_box_top': (x + 1.5, y + 1.5),
            'color': color
        })

    # --- Connect Steps with Curved Arrows ---
    for i in range(len(step_data) - 1):
        current, next_step = step_data[i], step_data[i+1]
        if i % 2 == 0:
            start = (current['title_center'][0], current['title_center'][1] - 0.3)
            end = (next_step['desc_box_bottom'][0], next_step['desc_box_bottom'][1] + 0.1)
            draw_curved_arrow(ax, start, end, current['color'], direction='down')
        else:
            start = (current['title_center'][0], current['title_center'][1] + 0.3)
            end = (next_step['desc_box_top'][0], next_step['desc_box_top'][1] - 0.1)
            draw_curved_arrow(ax, start, end, current['color'], direction='up')

    plt.tight_layout()
    return fig


# Example Usage
if __name__ == "__main__":
    steps_text = """Step 1: Collect and organize data inputs for the system
Step 2: Process and transform data into usable form
Step 3: Generate results and visualize the outputs"""
    
    fig = create_flowchart(
        steps_text,
        preview_mode=True,
        title_wrap=15,
        desc_wrap=28
    )
    plt.show()
