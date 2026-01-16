# # radial.py
# import matplotlib.pyplot as plt
# from matplotlib.patches import Polygon, RegularPolygon, Circle
# import textwrap

# STEP_COLORS = [
#     "#f9a825", "#43a047", "#d81b60", "#1e88e5", "#8e24aa",
#     "#fb8c00", "#6d4c41", "#00acc1", "#c2185b", "#00796b"
# ]

# STEP_CIRCLE_RADIUS = 0.7
# STEP_CIRCLE_SHADOW_OFFSET = 0.15

# # UPDATED: Function signature to accept font properties
# def draw_arrow_infographic(steps, title="Arrow Flowchart", preview_mode=False, title_font=None, desc_font=None):
#     """
#     Generates a vertical arrow-style infographic.
#     """
#     if not steps:
#         fig, ax = plt.subplots()
#         ax.text(0.5, 0.5, "Please provide steps data.", ha='center', va='center')
#         ax.axis('off')
#         return fig
        
#     fig, ax = plt.subplots(figsize=(10, len(steps) * 2.2))
    
#     if preview_mode:
#         fig.patch.set_facecolor('white')
#         ax.set_facecolor('white')
#     else:
#         fig.patch.set_alpha(0.0)
#         ax.set_facecolor('none')
    
#     ax.axis("off")
    
#     box_height, box_width, gap = 1.4, 6, 0.65
#     total_height = len(steps) * (box_height + gap)

#     for i, (step_title, step_desc) in enumerate(steps):
#         color = STEP_COLORS[i % len(STEP_COLORS)]
#         x0, y0 = 1, total_height - i * (box_height + gap)

#         shadow_offset = 0.12
#         shadow_verts = [(x0 + shadow_offset, y0 - shadow_offset), (x0 + box_width - 0.5 + shadow_offset, y0 - shadow_offset),
#                         (x0 + box_width + shadow_offset, y0 + box_height / 2 - shadow_offset),
#                         (x0 + box_width - 0.5 + shadow_offset, y0 + box_height + shadow_offset), (x0 + shadow_offset, y0 + box_height + shadow_offset)]
#         ax.add_patch(Polygon(shadow_verts, closed=True, color='black', alpha=0.1, zorder=1))

#         arrow_verts = [(x0, y0), (x0 + box_width - 0.5, y0), (x0 + box_width, y0 + box_height / 2),
#                        (x0 + box_width - 0.5, y0 + box_height), (x0, y0 + box_height)]
#         ax.add_patch(Polygon(arrow_verts, closed=True, color=color, alpha=0.95, zorder=2))

#         hex_x, hex_y = x0 - 1.1, y0 + box_height / 2
#         ax.add_patch(RegularPolygon((hex_x, hex_y), numVertices=6, radius=0.8,
#                                     orientation=0, color=color, ec='white', lw=2, zorder=3))
#         ax.text(hex_x, hex_y, "💡", fontsize=18, ha="center", va="center", color='white', zorder=4)

#         circle_x, circle_y = x0 + box_width + 1.5, y0 + box_height / 2
#         ax.add_patch(Circle((circle_x + STEP_CIRCLE_SHADOW_OFFSET, circle_y - STEP_CIRCLE_SHADOW_OFFSET),
#                             STEP_CIRCLE_RADIUS, facecolor='black', alpha=0.15, zorder=1))
#         ax.add_patch(Circle((circle_x, circle_y), STEP_CIRCLE_RADIUS, facecolor='white',
#                             edgecolor=color, linewidth=2.5, zorder=3))
#         ax.text(circle_x, circle_y, f"{i+1:02}", fontsize=20, ha="center", va="center",
#                 color=color, fontweight='bold', zorder=4)

#         # UPDATED: Using fontproperties instead of fontsize
#         ax.text(x0 + 0.5, y0 + box_height * 0.65, textwrap.fill(step_title.upper(), width=25),
#                 fontproperties=title_font, color="white", weight="bold", zorder=5)
#         ax.text(x0 + 0.5, y0 + box_height * 0.25, textwrap.fill(step_desc, width=45),
#                 fontproperties=desc_font, color="white", zorder=5)

#     ax.set_xlim(0, 13)
#     ax.set_ylim(-1, total_height + 2.5)
#     # UPDATED: Using fontproperties for the main title
#     ax.text(6.5, total_height + 1.5, title, fontproperties=title_font, ha='center', weight='bold', color="#333")

#     return fig



# radial.py
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, RegularPolygon, Circle
from text_utils import apply_text_settings, wrap_text
from transparency import apply_alpha_to_color


STEP_COLORS = [
    "#f9a825", "#43a047", "#d81b60", "#1e88e5", "#8e24aa",
    "#fb8c00", "#6d4c41", "#00acc1", "#c2185b", "#00796b"
]

STEP_CIRCLE_RADIUS = 0.7
STEP_CIRCLE_SHADOW_OFFSET = 0.15

def draw_arrow_infographic(steps, title="Arrow Flowchart", preview_mode=False, title_font=None, desc_font=None, title_wrap=None, desc_wrap=None):
    """
    Generates a vertical arrow-style infographic.
    """
    if not steps:
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, "Please provide steps data.", ha='center', va='center')
        ax.axis('off')
        return fig
        
    fig, ax = plt.subplots(figsize=(10, len(steps) * 2.2))
    
    if preview_mode:
        fig.patch.set_facecolor('white')
        ax.set_facecolor('white')
    else:
        fig.patch.set_alpha(0.0)
        ax.set_facecolor('none')
    
    ax.axis("off")
    
    box_height, box_width, gap = 1.4, 6, 0.65
    total_height = len(steps) * (box_height + gap)

    # Apply text settings
    steps_with_settings = apply_text_settings(
        [{'title': title, 'text': desc} for title, desc in steps],
        title_font, desc_font, title_wrap, desc_wrap
    )

    for i, step_data in enumerate(steps_with_settings):
        color = STEP_COLORS[i % len(STEP_COLORS)]
        x0, y0 = 1, total_height - i * (box_height + gap)

        shadow_offset = 0.12
        shadow_verts = [(x0 + shadow_offset, y0 - shadow_offset), (x0 + box_width - 0.5 + shadow_offset, y0 - shadow_offset),
                        (x0 + box_width + shadow_offset, y0 + box_height / 2 - shadow_offset),
                        (x0 + box_width - 0.5 + shadow_offset, y0 + box_height + shadow_offset), (x0 + shadow_offset, y0 + box_height + shadow_offset)]
        ax.add_patch(Polygon(shadow_verts, closed=True, color='black', alpha=0.1, zorder=1))

        arrow_verts = [(x0, y0), (x0 + box_width - 0.5, y0), (x0 + box_width, y0 + box_height / 2),
                       (x0 + box_width - 0.5, y0 + box_height), (x0, y0 + box_height)]
        ax.add_patch(Polygon(arrow_verts, closed=True, color=color, alpha=0.95, zorder=2))

        hex_x, hex_y = x0 - 1.1, y0 + box_height / 2
        ax.add_patch(RegularPolygon((hex_x, hex_y), numVertices=6, radius=0.8,
                                    orientation=0, color=color, ec='white', lw=2, zorder=3))
        ax.text(hex_x, hex_y, "💡", fontsize=18, ha="center", va="center", color='white', zorder=4)

        circle_x, circle_y = x0 + box_width + 1.5, y0 + box_height / 2
        ax.add_patch(Circle((circle_x + STEP_CIRCLE_SHADOW_OFFSET, circle_y - STEP_CIRCLE_SHADOW_OFFSET),
                            STEP_CIRCLE_RADIUS, facecolor='black', alpha=0.15, zorder=1))
        ax.add_patch(Circle((circle_x, circle_y), STEP_CIRCLE_RADIUS, facecolor='white',
                            edgecolor=color, linewidth=2.5, zorder=3))
        ax.text(circle_x, circle_y, f"{i+1:02}", fontsize=20, ha="center", va="center",
                color=color, fontweight='bold', zorder=4)

        # Use processed text and fonts
        ax.text(x0 + 0.5, y0 + box_height * 0.65, step_data['wrapped_title'],
                fontproperties=step_data['title_font'], color="white", weight="bold", zorder=5)
        
        ax.text(x0 + 0.5, y0 + box_height * 0.25, step_data['wrapped_text'],
                fontproperties=step_data['desc_font'], color="white", zorder=5)

    ax.set_xlim(0, 13)
    ax.set_ylim(-1, total_height + 2.5)
    
    # Use font properties for the main title
    ax.text(6.5, total_height + 1.5, title, fontproperties=title_font, ha='center', weight='bold', color="#333")

    return fig