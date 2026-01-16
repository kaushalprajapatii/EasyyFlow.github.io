# import matplotlib.pyplot as plt
# from matplotlib.patches import FancyBboxPatch
# import textwrap

# BOX_COLORS = ['#fbc02d', '#00e676', '#64b5f6', '#ff7043', '#ba68c8', '#4db6ac', '#ff8a65']

# # This function remains the same as it's a helper for sizing
# def vertical(title, description):
#     min_width, min_height = 4, 1.1
#     title_width = max(len(line) for line in textwrap.wrap(title, width=20)) * 0.15
#     desc_width = max(len(line) for line in textwrap.wrap(description, width=25)) * 0.12
#     required_width = max(min_width, title_width, desc_width) + 0.5
#     title_lines = len(textwrap.wrap(title, width=20))
#     desc_lines = len(textwrap.wrap(description, width=25))
#     required_height = max(min_height, 0.2 + (title_lines * 0.2) + (desc_lines * 0.18) + 0.3)
#     return required_width, required_height

# # UPDATED: Function signature to accept font properties
# def draw_step(ax, title, description, x, y, color, title_font=None, desc_font=None, shadow_offset=0.15, box_radius=0.2):
#     box_width, box_height = vertical(title, description)
    
#     shadow_box = FancyBboxPatch((x + shadow_offset, y - shadow_offset), box_width, box_height,
#                                 boxstyle=f"round,pad=0.1,rounding_size={box_radius}",
#                                 linewidth=0, facecolor='gray', alpha=0.3, zorder=1)
#     ax.add_patch(shadow_box)

#     box = FancyBboxPatch((x, y), box_width, box_height,
#                          boxstyle=f"round,pad=0.1,rounding_size={box_radius}",
#                          linewidth=1.5, facecolor=color, edgecolor='black', zorder=2)
#     ax.add_patch(box)

#     wrapped_title = textwrap.fill(title, width=40)
#     wrapped_desc = textwrap.fill(description, width=40)
    
#     # UPDATED: Using fontproperties instead of fontsize
#     ax.text(x + box_width/2, y + box_height - 0.1, wrapped_title,
#             ha='center', va='top', fontproperties=title_font, color='white', zorder=3)
    
#     # UPDATED: Using fontproperties instead of fontsize
#     ax.text(x + box_width/2, y + box_height/2 - 0.2, wrapped_desc,
#             ha='center', va='center', fontproperties=desc_font, color='white', zorder=3)
    
#     return box_width, box_height

# def draw_arrow(ax, start_x, start_y, end_x, end_y, color, lw=5):
#     ax.plot([start_x, end_x], [start_y, end_y], color='gray', linewidth=lw, alpha=0.3, zorder=1)
#     ax.plot([start_x, end_x], [start_y, end_y], color=color, linewidth=lw, zorder=3)
#     ax.annotate("", xy=(end_x, end_y), xytext=(start_x, start_y),
#                arrowprops=dict(arrowstyle='->', color=color, lw=lw, mutation_scale=25), zorder=4)

# # UPDATED: Function signature changed to accept font properties
# def create_flowchart(steps, figsize=None, preview_mode=False, title_font=None, desc_font=None):
#     if figsize is None:
#         total_height = sum(vertical(step[0], step[1])[1] * 1.8 for step in steps)
#         figsize = (8, max(6, total_height))
    
#     fig, ax = plt.subplots(figsize=figsize)
    
#     if preview_mode:
#         fig.patch.set_facecolor('white')
#     else:
#         fig.patch.set_alpha(0.0)
#         ax.set_facecolor('none')
    
#     start_y = figsize[1] - 1
    
#     box_widths, box_positions = [], []
#     current_y = start_y
    
#     for title, description, color in steps:
#         width, height = vertical(title, description)
#         box_widths.append(width)
#         box_positions.append(current_y - height)
#         current_y -= height * 1.8
    
#     max_width = max(box_widths) if box_widths else 0
#     x_center = (8 - max_width) / 2
    
#     ax.set_xlim(0, 8)
#     ax.set_ylim(min(box_positions) - 1 if box_positions else 0, start_y + 1)
#     ax.axis('off')

#     for i, (title, description, color) in enumerate(steps):
#         x = x_center + (max_width - box_widths[i]) / 2
#         y = box_positions[i]
        
#         # UPDATED: Passing new font properties to the drawing function
#         box_width, box_height = draw_step(ax, title, description, x, y, color, title_font=title_font, desc_font=desc_font)
        
#         if i < len(steps)-1:
#             next_y = box_positions[i+1] + vertical(steps[i+1][0], steps[i+1][1])[1]
#             draw_arrow(ax, x + box_width/2, y - 0.1, x + box_width/2, next_y + 0.1, color='#555555')

#     plt.tight_layout()
#     return fig





import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from text_utils import apply_text_settings, wrap_text
from transparency import apply_alpha_to_color


BOX_COLORS = ['#fbc02d', '#00e676', '#64b5f6', '#ff7043', '#ba68c8', '#4db6ac', '#ff8a65']

# This function remains the same as it's a helper for sizing
def vertical(title, description):
    min_width, min_height = 4, 1.1
    title_width = max(len(line) for line in wrap_text(title, 20).split('\n')) * 0.15
    desc_width = max(len(line) for line in wrap_text(description, 25).split('\n')) * 0.12
    required_width = max(min_width, title_width, desc_width) + 0.5
    title_lines = len(wrap_text(title, 20).split('\n'))
    desc_lines = len(wrap_text(description, 25).split('\n'))
    required_height = max(min_height, 0.2 + (title_lines * 0.2) + (desc_lines * 0.18) + 0.3)
    return required_width, required_height

def draw_step(ax, title, description, x, y, color, title_font=None, desc_font=None, shadow_offset=0.15, box_radius=0.2, title_wrap=None, desc_wrap=None):
    box_width, box_height = vertical(title, description)
    
    shadow_box = FancyBboxPatch((x + shadow_offset, y - shadow_offset), box_width, box_height,
                                boxstyle=f"round,pad=0.1,rounding_size={box_radius}",
                                linewidth=0, facecolor='gray', alpha=0.3, zorder=1)
    ax.add_patch(shadow_box)

    box = FancyBboxPatch((x, y), box_width, box_height,
                         boxstyle=f"round,pad=0.1,rounding_size={box_radius}",
                         linewidth=1.5, facecolor=color
, edgecolor='black', zorder=2)
    ax.add_patch(box)

    # Use wrap_text function for consistent wrapping
    wrapped_title = wrap_text(title, title_wrap or 40)
    wrapped_desc = wrap_text(description, desc_wrap or 40)
    
    # Use font properties
    ax.text(x + box_width/2, y + box_height - 0.1, wrapped_title,
            ha='center', va='top', fontproperties=title_font, color='white', zorder=3)
    
    ax.text(x + box_width/2, y + box_height/2 - 0.2, wrapped_desc,
            ha='center', va='center', fontproperties=desc_font, color='white', zorder=3)
    
    return box_width, box_height

def draw_arrow(ax, start_x, start_y, end_x, end_y, color, lw=5):
    ax.plot([start_x, end_x], [start_y, end_y], color='gray', linewidth=lw, alpha=0.3, zorder=1)
    ax.plot([start_x, end_x], [start_y, end_y], color=color, linewidth=lw, zorder=3)
    ax.annotate("", xy=(end_x, end_y), xytext=(start_x, start_y),
               arrowprops=dict(arrowstyle='->', color=color, lw=lw, mutation_scale=25), zorder=4)

def create_flowchart(steps, figsize=None, preview_mode=False, title_font=None, desc_font=None, title_wrap=None, desc_wrap=None):
    if figsize is None:
        total_height = sum(vertical(step[0], step[1])[1] * 1.8 for step in steps)
        figsize = (8, max(6, total_height))
    
    fig, ax = plt.subplots(figsize=figsize)
    
    if preview_mode:
        fig.patch.set_facecolor('white')
    else:
        fig.patch.set_alpha(0.0)
        ax.set_facecolor('none')
    
    start_y = figsize[1] - 1
    
    box_widths, box_positions = [], []
    current_y = start_y
    
    for title, description, color in steps:
        width, height = vertical(title, description)
        box_widths.append(width)
        box_positions.append(current_y - height)
        current_y -= height * 1.8
    
    max_width = max(box_widths) if box_widths else 0
    x_center = (8 - max_width) / 2
    
    ax.set_xlim(0, 8)
    ax.set_ylim(min(box_positions) - 1 if box_positions else 0, start_y + 1)
    ax.axis('off')

    for i, (title, description, color) in enumerate(steps):
        x = x_center + (max_width - box_widths[i]) / 2
        y = box_positions[i]
        
        # Pass new font properties and wrap settings to the drawing function
        box_width, box_height = draw_step(ax, title, description, x, y, color, 
                                        title_font=title_font, desc_font=desc_font,
                                        title_wrap=title_wrap, desc_wrap=desc_wrap)
        
        if i < len(steps)-1:
            next_y = box_positions[i+1] + vertical(steps[i+1][0], steps[i+1][1])[1]
            draw_arrow(ax, x + box_width/2, y - 0.1, x + box_width/2, next_y + 0.1, color='#555555')

    plt.tight_layout()
    return fig