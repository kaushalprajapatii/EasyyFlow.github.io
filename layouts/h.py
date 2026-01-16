# # h.py
# import matplotlib.pyplot as plt
# import matplotlib.patches as patches
# import textwrap

# # Color palette for the chevron steps
# COLORS = [
#     {"color": "#4388DC", "box_border_color": "#FFFFFF"},
#     {"color": "#4DC062", "box_border_color": "#FFFFFF"},
#     {"color": "#C1C120", "box_border_color": "#FFFFFF"},
#     {"color": "#A33BC3", "box_border_color": "#FFFFFF"},
#     {"color": "#C73939", "box_border_color": "#FFFFFF"},
#     {"color": "#3AB4B4", "box_border_color": "#FFFFFF"},
# ]

# # UPDATED: Function signature to accept font properties
# def create_chevron_flowchart(steps_data, preview_mode=False, title_font=None, desc_font=None):
#     """
#     Generates an overlapping chevron-style process flowchart with title box below the arrow.
#     """
#     if not steps_data:
#         fig, ax = plt.subplots()
#         ax.text(0.5, 0.5, "Please provide steps data.", ha='center', va='center')
#         ax.axis('off')
#         return fig

#     num_steps = len(steps_data)
    
#     box_width, box_height, arrow_tip_width, gap = 3.5, 4.0, 0.8, 1.25
#     x_increment = box_width - arrow_tip_width + gap

#     total_chevrons_width = (x_increment * (num_steps - 1)) + box_width + arrow_tip_width
#     fig_width = total_chevrons_width + 1
#     fig_height = box_height + 4
#     fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    
#     if preview_mode:
#         fig.patch.set_facecolor('white')
#     else:
#         fig.patch.set_alpha(0.0)
#         ax.set_facecolor('none')
    
#     ax.set_aspect('equal', adjustable='box')
#     plt.axis('off')

#     for i, step in enumerate(steps_data):
#         x_start = i * x_increment
        
#         verts = [(x_start, -box_height / 2), (x_start + box_width, -box_height / 2),
#                  (x_start + box_width + arrow_tip_width, 0), (x_start + box_width, box_height / 2),
#                  (x_start, box_height / 2)]

#         for j in range(7):
#             offset_multiplier = (j + 1) * 0.5
#             shadow_verts = [(x + 0.05 * offset_multiplier, y - 0.05 * offset_multiplier) for x, y in verts]
#             ax.add_patch(patches.Polygon(shadow_verts, facecolor='black', alpha=0.1, lw=0))
        
#         ax.add_patch(patches.Polygon(verts, facecolor=step["color"], lw=0))

#         center_x = x_start + (box_width / 2)
        
#         ax.add_patch(patches.FancyBboxPatch((center_x - 0.5, 1.3 - 0.5), 1.0, 1.0,
#                                             boxstyle="round,pad=0,rounding_size=0.15",
#                                             facecolor='none', edgecolor=step["box_border_color"], lw=2))
#         ax.text(center_x, 1.3, str(i + 1), ha='center', va='center', 
#                 fontsize=22, fontweight='bold', color=step["box_border_color"])

#         title_box_y, title_box_width, title_box_height = -box_height / 2 - 1.2, box_width * 0.8, 0.8
        
#         title_shadow = patches.FancyBboxPatch((center_x - title_box_width/2 + 0.1, title_box_y - 0.1),
#                                               title_box_width, title_box_height,
#                                               boxstyle="round,pad=0,rounding_size=0.1",
#                                               facecolor='black', alpha=0.2, lw=0)
#         ax.add_patch(title_shadow)
        
#         title_box = patches.FancyBboxPatch((center_x - title_box_width/2, title_box_y),
#                                            title_box_width, title_box_height,
#                                            boxstyle="round,pad=0,rounding_size=0.1",
#                                            facecolor='white', edgecolor=step["color"], lw=2)
#         ax.add_patch(title_box)
        
#         # UPDATED: Using fontproperties instead of fontsize
#         wrapped_title = textwrap.fill(step['title'], width=15)
#         ax.text(center_x, title_box_y + title_box_height/2, wrapped_title, 
#                 ha='center', va='center', fontproperties=title_font,
#                 color=step["color"], linespacing=1.1)

#         # UPDATED: Using fontproperties instead of fontsize
#         wrapped_desc = textwrap.fill(step['text'], width=20)
#         ax.text(center_x, 0.1, wrapped_desc, 
#                 ha='center', va='center', fontproperties=desc_font, 
#                 color='white', linespacing=1.2)

#     ax.set_xlim(-1, total_chevrons_width + 1)
#     ax.set_ylim(-fig_height/2 - 1, fig_height/2)

#     return fig



# h.py
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from text_utils import apply_text_settings
from transparency import apply_alpha_to_color

# Color palette for the chevron steps
COLORS = [
    {"color": "#4388DC", "box_border_color": "#FFFFFF"},
    {"color": "#4DC062", "box_border_color": "#FFFFFF"},
    {"color": "#C1C120", "box_border_color": "#FFFFFF"},
    {"color": "#A33BC3", "box_border_color": "#FFFFFF"},
    {"color": "#C73939", "box_border_color": "#FFFFFF"},
    {"color": "#3AB4B4", "box_border_color": "#FFFFFF"},
]

def create_chevron_flowchart(steps_data, preview_mode=False, title_font=None, desc_font=None, title_wrap=None, desc_wrap=None):
    """
    Generates an overlapping chevron-style process flowchart with title box below the arrow.
    """
    if not steps_data:
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, "Please provide steps data.", ha='center', va='center')
        ax.axis('off')
        return fig

    num_steps = len(steps_data)
    
    box_width, box_height, arrow_tip_width, gap = 3.5, 4.0, 0.8, 1.25
    x_increment = box_width - arrow_tip_width + gap

    total_chevrons_width = (x_increment * (num_steps - 1)) + box_width + arrow_tip_width
    fig_width = total_chevrons_width + 1
    fig_height = box_height + 4
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    
    if preview_mode:
        fig.patch.set_facecolor('white')
    else:
        fig.patch.set_alpha(0.0)
        ax.set_facecolor('none')
    
    ax.set_aspect('equal', adjustable='box')
    plt.axis('off')

    # Apply text settings
    steps_with_settings = apply_text_settings(steps_data, title_font, desc_font, title_wrap, desc_wrap)

    for i, step in enumerate(steps_with_settings):
        x_start = i * x_increment
        
        verts = [(x_start, -box_height / 2), (x_start + box_width, -box_height / 2),
                 (x_start + box_width + arrow_tip_width, 0), (x_start + box_width, box_height / 2),
                 (x_start, box_height / 2)]

        for j in range(7):
            offset_multiplier = (j + 1) * 0.5
            shadow_verts = [(x + 0.05 * offset_multiplier, y - 0.05 * offset_multiplier) for x, y in verts]
            ax.add_patch(patches.Polygon(shadow_verts, facecolor='black', alpha=0.1, lw=0))
        
        ax.add_patch(patches.Polygon(verts, facecolor=step["color"], lw=0))

        center_x = x_start + (box_width / 2)
        
        ax.add_patch(patches.FancyBboxPatch((center_x - 0.5, 1.3 - 0.5), 1.0, 1.0,
                                            boxstyle="round,pad=0,rounding_size=0.15",
                                            facecolor='none', edgecolor=step["box_border_color"], lw=2))
        ax.text(center_x, 1.3, str(i + 1), ha='center', va='center', 
                fontsize=22, fontweight='bold', color=step["box_border_color"])

        title_box_y, title_box_width, title_box_height = -box_height / 2 - 1.2, box_width * 0.8, 0.8
        
        title_shadow = patches.FancyBboxPatch((center_x - title_box_width/2 + 0.1, title_box_y - 0.1),
                                              title_box_width, title_box_height,
                                              boxstyle="round,pad=0,rounding_size=0.1",
                                              facecolor='black', alpha=0.2, lw=0)
        ax.add_patch(title_shadow)
        
        title_box = patches.FancyBboxPatch((center_x - title_box_width/2, title_box_y),
                                           title_box_width, title_box_height,
                                           boxstyle="round,pad=0,rounding_size=0.1",
                                           facecolor='white', edgecolor=step["color"], lw=2)
        ax.add_patch(title_box)
        
        # Use processed text and fonts
        ax.text(center_x, title_box_y + title_box_height/2, step['wrapped_title'], 
                ha='center', va='center', fontproperties=step['title_font'],
                color=step["color"], linespacing=1.1)

        # Use processed description text and fonts
        ax.text(center_x, 0.1, step['wrapped_text'], 
                ha='center', va='center', fontproperties=step['desc_font'], 
                color='white', linespacing=1.2)

    ax.set_xlim(-1, total_chevrons_width + 1)
    ax.set_ylim(-fig_height/2 - 1, fig_height/2)

    return fig