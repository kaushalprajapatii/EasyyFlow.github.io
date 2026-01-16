# # layouts/golgol.py
# import matplotlib.pyplot as plt
# import matplotlib.patches as patches
# import textwrap
# import numpy as np

# # Color palette inspired by the target image
# COLORS = [
#     {"border": "#4CB8B0", "text": "#4CB8B0"},  # Teal/Green
#     {"border": "#F2A33C", "text": "#F2A33C"},  # Orange
#     {"border": "#E55A54", "text": "#E55A54"},  # Red
#     {"border": "#A462A9", "text": "#A462A9"},  # Purple
#     {"border": "#4A90E2", "text": "#4A90E2"},  # Blue
# ]

# # UPDATED: Function signature to accept font properties
# def create_golgol_flowchart(steps_data, title="", preview_mode=False, title_font=None, desc_font=None):
#     """
#     Generates a flowchart in the modified "golgol" style.
#     Line is shifted to the right and description is placed beside it.
#     """
#     if not steps_data:
#         fig, ax = plt.subplots(figsize=(12, 6))
#         ax.text(0.5, 0.5, "Please provide steps data.", ha='center', va='center', fontsize=14)
#         ax.axis('off')
#         return fig

#     num_steps = len(steps_data)
    
#     fig_width = max(10, 3 * num_steps + 2)
#     fig_height = 8
    
#     fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    
#     if preview_mode:
#         fig.set_facecolor('#f0f2f5')
#         ax.set_facecolor('#f0f2f5')
#     else:
#         fig.set_facecolor('none')
#         ax.set_facecolor('none')
    
#     ax.set_aspect('equal')
#     ax.axis('off')

#     start_x, y_center, circle_radius = 2.0, 6.0, 1.0
#     horizontal_spacing, line_shift_right, vertical_spacing = 3.5, -0.3, 2.0
#     line_to_desc_horizontal_gap, line_to_desc_vertical_offset = 0.2, 0.0

#     for i, step in enumerate(steps_data):
#         cx = start_x + i * horizontal_spacing
#         color_set = COLORS[i % len(COLORS)]

#         shadow_circle = patches.Circle((cx + 0.08, y_center - 0.08),
#                                        circle_radius, color='black', alpha=0.15, zorder=1)
#         ax.add_patch(shadow_circle)

#         main_circle = patches.Circle((cx, y_center), circle_radius,
#                                      facecolor='#FFFFFF',
#                                      edgecolor=color_set["border"],
#                                      linewidth=4, zorder=2)
#         ax.add_patch(main_circle)

#         # UPDATED: Using fontproperties instead of fontsize
#         wrapped_title = textwrap.fill(step['title'], width=15)
#         ax.text(cx, y_center, wrapped_title,
#                 ha='center', va='center',
#                 fontproperties=title_font,
#                 color='#333333', zorder=3, linespacing=1.2)

#         line_x = cx + line_shift_right
#         line_start_y = y_center - circle_radius
#         line_end_y = line_start_y - vertical_spacing
        
#         ax.plot([line_x, line_x], [line_start_y, line_end_y], 
#                 color=color_set["border"], linewidth=3, zorder=2)

#         desc_x = line_x + line_to_desc_horizontal_gap
#         desc_y = line_start_y - (vertical_spacing / 2) + line_to_desc_vertical_offset
        
#         wrapped_desc = textwrap.fill(step['text'], width=20)
#         # UPDATED: Using fontproperties instead of fontsize
#         ax.text(desc_x, desc_y, wrapped_desc,
#                 ha='left', va='center',
#                 fontproperties=desc_font, color='#555555', zorder=3, 
#                 linespacing=1.3,
#                 bbox=dict(boxstyle="round,pad=0.5", facecolor='white', 
#                          edgecolor=color_set["border"], alpha=0.9, linewidth=1.5))

#         if i < num_steps - 1:
#             arrow_start_x = cx + circle_radius
#             arrow_end_x = cx + horizontal_spacing - circle_radius
            
#             arrow = patches.FancyArrowPatch(
#                 (arrow_start_x, y_center), (arrow_end_x, y_center),
#                 arrowstyle='simple,head_width=8,head_length=10',
#                 color=color_set["border"],
#                 mutation_scale=8,
#                 zorder=1,
#                 alpha=0.7
#             )
#             ax.add_patch(arrow)

#     if title:
#         # UPDATED: Create a larger font property for the main title and use it
#         main_title_font = title_font.copy()
#         main_title_font.set_size(title_font.get_size() + 4)
#         ax.text(start_x + (num_steps - 1) * horizontal_spacing / 2, 
#                 y_center + circle_radius + 1.5, 
#                 title, 
#                 ha='center', va='bottom', 
#                 fontproperties=main_title_font,
#                 color='#2c3e50')

#     ax.set_xlim(start_x - circle_radius - 1, start_x + (num_steps - 1) * horizontal_spacing + circle_radius + 2)
#     ax.set_ylim(line_end_y - 1, y_center + circle_radius + (3 if title else 1))

#     plt.tight_layout()
#     return fig


# layouts/golgol.py
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from text_utils import apply_text_settings
from transparency import apply_alpha_to_color


# Color palette inspired by the target image
COLORS = [
    {"border": "#4CB8B0", "text": "#4CB8B0"},  # Teal/Green
    {"border": "#F2A33C", "text": "#F2A33C"},  # Orange
    {"border": "#E55A54", "text": "#E55A54"},  # Red
    {"border": "#A462A9", "text": "#A462A9"},  # Purple
    {"border": "#4A90E2", "text": "#4A90E2"},  # Blue
]

def create_golgol_flowchart(steps_data, title="", preview_mode=False, title_font=None, desc_font=None, title_wrap=None, desc_wrap=None):
    """
    Generates a flowchart in the modified "golgol" style.
    Line is shifted to the right and description is placed beside it.
    """
    if not steps_data:
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.text(0.5, 0.5, "Please provide steps data.", ha='center', va='center', fontsize=14)
        ax.axis('off')
        return fig

    num_steps = len(steps_data)
    
    fig_width = max(10, 3 * num_steps + 2)
    fig_height = 8
    
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    
    if preview_mode:
        fig.set_facecolor('#f0f2f5')
        ax.set_facecolor('#f0f2f5')
    else:
        fig.set_facecolor('none')
        ax.set_facecolor('none')
    
    ax.set_aspect('equal')
    ax.axis('off')

    start_x, y_center, circle_radius = 2.0, 6.0, 1.0
    horizontal_spacing, line_shift_right, vertical_spacing = 3.5, -0.3, 2.0
    line_to_desc_horizontal_gap, line_to_desc_vertical_offset = 0.2, 0.0

    # Apply text settings
    steps_with_settings = apply_text_settings(steps_data, title_font, desc_font, title_wrap, desc_wrap)

    for i, step in enumerate(steps_with_settings):
        cx = start_x + i * horizontal_spacing
        color_set = COLORS[i % len(COLORS)]

        shadow_circle = patches.Circle((cx + 0.08, y_center - 0.08),
                                       circle_radius, color='black', alpha=0.15, zorder=1)
        ax.add_patch(shadow_circle)

        main_circle = patches.Circle((cx, y_center), circle_radius,
                                     facecolor='#FFFFFF',
                                     edgecolor=color_set["border"],
                                     linewidth=4, zorder=2)
        ax.add_patch(main_circle)

        # Use processed text and fonts
        ax.text(cx, y_center, step['wrapped_title'],
                ha='center', va='center',
                fontproperties=step['title_font'],
                color='#333333', zorder=3, linespacing=1.2)

        line_x = cx + line_shift_right
        line_start_y = y_center - circle_radius
        line_end_y = line_start_y - vertical_spacing
        
        ax.plot([line_x, line_x], [line_start_y, line_end_y], 
                color=color_set["border"], linewidth=3, zorder=2)

        desc_x = line_x + line_to_desc_horizontal_gap
        desc_y = line_start_y - (vertical_spacing / 2) + line_to_desc_vertical_offset
        
        # Use processed description text and fonts
        ax.text(desc_x, desc_y, step['wrapped_text'],
                ha='left', va='center',
                fontproperties=step['desc_font'], color='#555555', zorder=3, 
                linespacing=1.3,
                bbox=dict(boxstyle="round,pad=0.5", facecolor='white', 
                         edgecolor=color_set["border"], alpha=0.9, linewidth=1.5))

        if i < num_steps - 1:
            arrow_start_x = cx + circle_radius
            arrow_end_x = cx + horizontal_spacing - circle_radius
            
            arrow = patches.FancyArrowPatch(
                (arrow_start_x, y_center), (arrow_end_x, y_center),
                arrowstyle='simple,head_width=8,head_length=10',
                color=color_set["border"],
                mutation_scale=8,
                zorder=1,
                alpha=0.7
            )
            ax.add_patch(arrow)

    if title:
        # Create a larger font property for the main title and use it
        if title_font:
            main_title_font = title_font.copy()
            main_title_font.set_size(title_font.get_size() + 4)
        else:
            from matplotlib.font_manager import FontProperties
            main_title_font = FontProperties(size=24)
            
        ax.text(start_x + (num_steps - 1) * horizontal_spacing / 2, 
                y_center + circle_radius + 1.5, 
                title, 
                ha='center', va='bottom', 
                fontproperties=main_title_font,
                color='#2c3e50')

    ax.set_xlim(start_x - circle_radius - 1, start_x + (num_steps - 1) * horizontal_spacing + circle_radius + 2)
    ax.set_ylim(line_end_y - 1, y_center + circle_radius + (3 if title else 1))

    plt.tight_layout()
    return fig