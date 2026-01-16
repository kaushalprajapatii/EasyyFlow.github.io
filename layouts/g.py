# # layouts/g.py
# import matplotlib.pyplot as plt
# import matplotlib.patches as patches
# import textwrap

# # Color palette for the steps, can be accessed from the main app
# COLORS = [
#     {"color": "#cde2f5", "text_color": "#3a6a9e"},
#     {"color": "#b8e6c1", "text_color": "#3c864d"},
#     {"color": "#d9e7a8", "text_color": "#7c8c3f"},
#     {"color": "#c4e6e8", "text_color": "#4a8a8d"},
#     {"color": "#f8c9c9", "text_color": "#d1495b"},
#     {"color": "#f0e1f7", "text_color": "#8e6c9a"},
#     {"color": "#fde4cf", "text_color": "#c27c4f"},
# ]

# def create_zigzag_stairs_flowchart(steps_data, preview_mode=False, title_font=None, desc_font=None):
#     """
#     Generates a dynamic staircase flowchart using matplotlib.
#     """
#     if not steps_data:
#         fig, ax = plt.subplots()
#         ax.text(0.5, 0.5, "Please provide steps data.", ha='center', va='center')
#         ax.axis('off')
#         return fig

#     fig, ax = plt.subplots(figsize=(14, 12))
    
#     if preview_mode:
#         fig.patch.set_facecolor('white')
#         ax.set_facecolor('white')
#     else:
#         fig.patch.set_alpha(0.0)
#         ax.set_facecolor('none')
    
#     ax.set_aspect('equal', adjustable='box')
#     plt.axis('off')

#     num_steps = len(steps_data)
#     riser_height, tread_width, thickness = 1.1, 2.5, 0.8
#     shadow_offset = (0.15, -0.15)
#     connector_points, x, y = [], 0, 0

#     # Get font sizes from FontProperties objects
#     title_fontsize = title_font.get_size() if title_font else 12
#     desc_fontsize = desc_font.get_size() if desc_font else 10

#     for i, step in enumerate(steps_data):
#         shadow_color, shadow_alpha = '#000000', 0.2
#         sx, sy = x + shadow_offset[0], y + shadow_offset[1]

#         riser_shadow_verts = [(sx, sy), (sx + thickness, sy - thickness), (sx + thickness, sy + riser_height - thickness), (sx, sy + riser_height)]
#         ax.add_patch(patches.Polygon(riser_shadow_verts, facecolor=shadow_color, alpha=shadow_alpha, lw=0))
#         tread_shadow_verts = [(sx, sy + riser_height), (sx + tread_width, sy + riser_height), (sx + tread_width + thickness, sy + riser_height - thickness), (sx + thickness, sy + riser_height - thickness)]
#         ax.add_patch(patches.Polygon(tread_shadow_verts, facecolor=shadow_color, alpha=shadow_alpha, lw=0))

#         riser_verts = [(x, y), (x + thickness, y - thickness), (x + thickness, y + riser_height - thickness), (x, y + riser_height)]
#         ax.add_patch(patches.Polygon(riser_verts, facecolor=step["color"], lw=0.5, edgecolor='black', alpha=0.95))
#         y += riser_height
#         tread_verts = [(x, y), (x + tread_width, y), (x + tread_width + thickness, y - thickness), (x + thickness, y - thickness)]
#         ax.add_patch(patches.Polygon(tread_verts, facecolor=step["color"], lw=0.5, edgecolor='black', alpha=0.95))

#         num_x, num_y = x + tread_width / 2 + thickness * 0.5, y - thickness / 2
#         ax.add_patch(patches.Circle((num_x, num_y), radius=0.35, color='white', alpha=0.9))
#         ax.text(num_x, num_y, str(i + 1), ha='center', va='center', fontsize=12, color='black', fontweight='bold')

#         # --- Text Positioning Logic ---
#         connector_x = x + tread_width / 2
#         horizontal_offset = 0.3

#         if (i + 1) % 2 != 0: # Odd-numbered steps
#             text_x, ha, title_va, desc_va = connector_x - horizontal_offset, 'right', 'bottom', 'top'
#             title_y, desc_y = y + 2.5, y + 2.4
#             connector_end_y = title_y + 1.2
#         else: # Even-numbered steps
#             text_x, ha, title_va, desc_va = connector_x + horizontal_offset, 'left', 'top', 'bottom'
#             title_y, desc_y = y - riser_height - 1.5, y - riser_height - 1.4
#             connector_end_y = title_y - 1

#         connector_points.append({'start': (connector_x, y), 'end': (connector_x, connector_end_y)})

#         # Use font size instead of fontproperties for compatibility
#         wrapped_title = textwrap.fill(step['title'], width=step['wrap_width'])
#         wrapped_desc = textwrap.fill(step['text'], width=step['wrap_width'])
#         ax.text(text_x, title_y, wrapped_title, ha=ha, va=title_va, fontsize=title_fontsize, 
#                 weight='bold', color=step["text_color"], linespacing=1.4)
#         ax.text(text_x, desc_y, wrapped_desc, ha=ha, va=desc_va, fontsize=desc_fontsize, 
#                 color='black', linespacing=1.4)

#         x += tread_width

#     for i in range(num_steps):
#         points = connector_points[i]
#         shrink_a = 10 if (i + 1) % 2 != 0 else 45
#         connector = patches.FancyArrowPatch(
#             points['start'], points['end'], arrowstyle='-', shrinkA=shrink_a,
#             shrinkB=30, color='gray', lw=1
#         )
#         ax.add_patch(connector)

#     ax.set_ylim(-thickness - 4, y + 4)
#     ax.set_xlim(-2, x + thickness + 2)

#     return fig






# layouts/g.py
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from text_utils import apply_text_settings
from transparency import apply_alpha_to_color


# Color palette for the steps, can be accessed from the main app
COLORS = [
    {"color": "#cde2f5", "text_color": "#3a6a9e"},
    {"color": "#b8e6c1", "text_color": "#3c864d"},
    {"color": "#d9e7a8", "text_color": "#7c8c3f"},
    {"color": "#c4e6e8", "text_color": "#4a8a8d"},
    {"color": "#f8c9c9", "text_color": "#d1495b"},
    {"color": "#f0e1f7", "text_color": "#8e6c9a"},
    {"color": "#fde4cf", "text_color": "#c27c4f"},
]

def create_zigzag_stairs_flowchart(steps_data, preview_mode=False, title_font=None, desc_font=None, title_wrap=None, desc_wrap=None):
    """
    Generates a dynamic staircase flowchart using matplotlib.
    """
    if not steps_data:
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, "Please provide steps data.", ha='center', va='center')
        ax.axis('off')
        return fig

    fig, ax = plt.subplots(figsize=(14, 12))
    
    if preview_mode:
        fig.patch.set_facecolor('white')
        ax.set_facecolor('white')
    else:
        fig.patch.set_alpha(0.0)
        ax.set_facecolor('none')
    
    ax.set_aspect('equal', adjustable='box')
    plt.axis('off')

    num_steps = len(steps_data)
    riser_height, tread_width, thickness = 1.1, 2.5, 0.8
    shadow_offset = (0.15, -0.15)
    connector_points, x, y = [], 0, 0

    # Apply text settings
    steps_with_settings = apply_text_settings(steps_data, title_font, desc_font, title_wrap, desc_wrap)

    for i, step in enumerate(steps_with_settings):
        shadow_color, shadow_alpha = '#000000', 0.2
        sx, sy = x + shadow_offset[0], y + shadow_offset[1]

        riser_shadow_verts = [(sx, sy), (sx + thickness, sy - thickness), (sx + thickness, sy + riser_height - thickness), (sx, sy + riser_height)]
        ax.add_patch(patches.Polygon(riser_shadow_verts, facecolor=shadow_color, alpha=shadow_alpha, lw=0))
        tread_shadow_verts = [(sx, sy + riser_height), (sx + tread_width, sy + riser_height), (sx + tread_width + thickness, sy + riser_height - thickness), (sx + thickness, sy + riser_height - thickness)]
        ax.add_patch(patches.Polygon(tread_shadow_verts, facecolor=shadow_color, alpha=shadow_alpha, lw=0))

        riser_verts = [(x, y), (x + thickness, y - thickness), (x + thickness, y + riser_height - thickness), (x, y + riser_height)]
        ax.add_patch(patches.Polygon(riser_verts, facecolor=step["color"], lw=0.5, edgecolor='black', alpha=0.95))
        y += riser_height
        tread_verts = [(x, y), (x + tread_width, y), (x + tread_width + thickness, y - thickness), (x + thickness, y - thickness)]
        ax.add_patch(patches.Polygon(tread_verts, facecolor=step["color"], lw=0.5, edgecolor='black', alpha=0.95))

        num_x, num_y = x + tread_width / 2 + thickness * 0.5, y - thickness / 2
        ax.add_patch(patches.Circle((num_x, num_y), radius=0.35, color='white', alpha=0.9))
        ax.text(num_x, num_y, str(i + 1), ha='center', va='center', fontsize=12, color='black', fontweight='bold')

        # --- Text Positioning Logic ---
        connector_x = x + tread_width / 2
        horizontal_offset = 0.3

        if (i + 1) % 2 != 0: # Odd-numbered steps
            text_x, ha, title_va, desc_va = connector_x - horizontal_offset, 'right', 'bottom', 'top'
            title_y, desc_y = y + 2.5, y + 2.4
            connector_end_y = title_y + 1.2
        else: # Even-numbered steps
            text_x, ha, title_va, desc_va = connector_x + horizontal_offset, 'left', 'top', 'bottom'
            title_y, desc_y = y - riser_height - 1.5, y - riser_height - 1.4
            connector_end_y = title_y - 1

        connector_points.append({'start': (connector_x, y), 'end': (connector_x, connector_end_y)})

        # Use processed text and fonts
        ax.text(text_x, title_y, step['wrapped_title'], ha=ha, va=title_va, 
                fontproperties=step['title_font'], 
                weight='bold', color=step["text_color"], linespacing=1.4)
        
        ax.text(text_x, desc_y, step['wrapped_text'], ha=ha, va=desc_va, 
                fontproperties=step['desc_font'], 
                color='black', linespacing=1.4)

        x += tread_width

    for i in range(num_steps):
        points = connector_points[i]
        shrink_a = 10 if (i + 1) % 2 != 0 else 45
        connector = patches.FancyArrowPatch(
            points['start'], points['end'], arrowstyle='-', shrinkA=shrink_a,
            shrinkB=30, color='gray', lw=1
        )
        ax.add_patch(connector)

    ax.set_ylim(-thickness - 4, y + 4)
    ax.set_xlim(-2, x + thickness + 2)

    return fig