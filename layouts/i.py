# # i.py
# import matplotlib.pyplot as plt
# import matplotlib.patches as patches
# import textwrap

# # Color palette for the S-curve steps
# COLORS = [
#     {"fill_color": "#6a0dad", "border_color": "#9b59b6"},
#     {"fill_color": "#2980b9", "border_color": "#3498db"},
#     {"fill_color": "#c0392b", "border_color": "#e74c3c"},
#     {"fill_color": "#16a085", "border_color": "#1abc9c"},
#     {"fill_color": "#f39c12", "border_color": "#f1c40f"},
#     {"fill_color": "#264653", "border_color": "#2a9d8f"},
#     {"fill_color": "#455a64", "border_color": "#607d8b"},
#     {"fill_color": "#e76f51", "border_color": "#f4a261"},
# ]

# def create_s_curve_flowchart(
#     steps_data, 
#     preview_mode=False, 
#     title_font=None, 
#     desc_font=None, 
#     title_desc_gap=0.4  # NEW: adjustable gap between title and description
# ):
#     """
#     Generates a vertical S-curve flowchart with shadows on boxes and lines.
#     """
#     if not steps_data:
#         fig, ax = plt.subplots()
#         ax.text(0.5, 0.5, "Please provide steps data.", ha='center', va='center')
#         ax.axis('off')
#         return fig

#     num_steps = len(steps_data)

#     y_increment, x_offset, box_width, box_height = 4.0, 4.0, 6.0, 3.0
#     circle_radius, outer_ring_radius = 1.2, 1.5

#     fig_height = abs(y_increment * num_steps)
#     fig_width = (x_offset + box_width / 2) * 2 + 2
#     fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    
#     if preview_mode:
#         fig.patch.set_facecolor('white')
#     else:
#         fig.patch.set_alpha(0.0)
#         ax.set_facecolor('none')
    
#     ax.set_aspect('equal', adjustable='box')
#     plt.axis('off')

#     connector_points = []
#     for i, step in enumerate(steps_data):
#         y_pos = i * y_increment
#         direction = 1 if (i + 1) % 2 != 0 else -1
#         circle_x, box_x = -x_offset * direction, x_offset * direction
#         connector_points.append((circle_x, y_pos))

#         # Shadows behind boxes
#         for j in range(10):
#             offset_multiplier = (j + 1) * 0.35
#             ax.add_patch(patches.FancyBboxPatch(
#                 (box_x - box_width/2 + 0.1 * offset_multiplier, y_pos - box_height/2 - 0.1 * offset_multiplier),
#                 box_width, box_height, boxstyle="round,pad=0,rounding_size=0.5",
#                 facecolor='black', alpha=0.05, lw=0
#             ))

#         # Main step box
#         ax.add_patch(patches.FancyBboxPatch(
#             (box_x - box_width/2, y_pos - box_height/2),
#             box_width, box_height, boxstyle="round,pad=0,rounding_size=0.5",
#             facecolor=step["fill_color"], edgecolor=step["border_color"], lw=2
#         ))

#         # Title
#         ax.text(
#             box_x, y_pos + 0.6, 
#             textwrap.fill(step['title'], width=25), 
#             ha='center', va='center',
#             fontproperties=title_font, 
#             color='white', linespacing=1.3
#         )

#         # Description (position adjusted with title_desc_gap)
#         ax.text(
#             box_x, y_pos + 0.2 - title_desc_gap, 
#             textwrap.fill(step['text'], width=38), 
#             ha='center', va='top',
#             fontproperties=desc_font, 
#             color="#ffffff", linespacing=1.3
#         )

#         # Circle indicators
#         ax.add_patch(patches.Circle((circle_x, y_pos), radius=outer_ring_radius, facecolor='none', edgecolor=step["border_color"], lw=2, linestyle='--'))
#         ax.add_patch(patches.Circle((circle_x, y_pos), radius=circle_radius, facecolor=step["fill_color"], lw=0))
#         ax.text(circle_x, y_pos, str(i + 1), ha='center', va='center', fontsize=40, fontweight='bold', color='white')

#     # Connector lines
#     if len(connector_points) > 1:
#         for i in range(len(connector_points) - 1):
#             start_point, end_point = connector_points[i], connector_points[i+1]
#             rad = 0.4 if (i + 1) % 2 != 0 else -0.4
#             line_color = steps_data[i]["border_color"]
#             ax.add_patch(patches.ConnectionPatch(
#                 xyA=start_point, xyB=end_point, 
#                 coordsA='data', coordsB='data', 
#                 connectionstyle=f"arc3,rad={rad}", 
#                 color='black', lw=4, alpha=0.3
#             ))
#             ax.add_patch(patches.ConnectionPatch(
#                 xyA=start_point, xyB=end_point, 
#                 coordsA='data', coordsB='data', 
#                 connectionstyle=f"arc3,rad={rad}", 
#                 color=line_color, lw=2
#             ))

#     ax.set_xlim(-fig_width / 2, fig_width / 2)
#     ax.set_ylim(-4, y_increment * (num_steps - 1) + 4)

#     return fig



# i.py
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from text_utils import apply_text_settings
from transparency import apply_alpha_to_color


# Color palette for the S-curve steps
COLORS = [
    {"fill_color": "#6a0dad", "border_color": "#9b59b6"},
    {"fill_color": "#2980b9", "border_color": "#3498db"},
    {"fill_color": "#c0392b", "border_color": "#e74c3c"},
    {"fill_color": "#16a085", "border_color": "#1abc9c"},
    {"fill_color": "#f39c12", "border_color": "#f1c40f"},
    {"fill_color": "#264653", "border_color": "#2a9d8f"},
    {"fill_color": "#455a64", "border_color": "#607d8b"},
    {"fill_color": "#e76f51", "border_color": "#f4a261"},
]

def create_s_curve_flowchart(
    steps_data, 
    preview_mode=False, 
    title_font=None, 
    desc_font=None, 
    title_wrap=None,
    desc_wrap=None,
    title_desc_gap=0.4  # adjustable gap between title and description
):
    """
    Generates a vertical S-curve flowchart with shadows on boxes and lines.
    """
    if not steps_data:
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, "Please provide steps data.", ha='center', va='center')
        ax.axis('off')
        return fig

    num_steps = len(steps_data)

    y_increment, x_offset, box_width, box_height = 4.0, 4.0, 6.0, 3.0
    circle_radius, outer_ring_radius = 1.2, 1.5

    fig_height = abs(y_increment * num_steps)
    fig_width = (x_offset + box_width / 2) * 2 + 2
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    
    if preview_mode:
        fig.patch.set_facecolor('white')
    else:
        fig.patch.set_alpha(0.0)
        ax.set_facecolor('none')
    
    ax.set_aspect('equal', adjustable='box')
    plt.axis('off')

    connector_points = []
    
    # Apply text settings
    steps_with_settings = apply_text_settings(steps_data, title_font, desc_font, title_wrap, desc_wrap)

    for i, step in enumerate(steps_with_settings):
        y_pos = i * y_increment
        direction = 1 if (i + 1) % 2 != 0 else -1
        circle_x, box_x = -x_offset * direction, x_offset * direction
        connector_points.append((circle_x, y_pos))

        # Shadows behind boxes
        for j in range(10):
            offset_multiplier = (j + 1) * 0.35
            ax.add_patch(patches.FancyBboxPatch(
                (box_x - box_width/2 + 0.1 * offset_multiplier, y_pos - box_height/2 - 0.1 * offset_multiplier),
                box_width, box_height, boxstyle="round,pad=0,rounding_size=0.5",
                facecolor='black', alpha=0.05, lw=0
            ))

        # Main step box
        ax.add_patch(patches.FancyBboxPatch(
            (box_x - box_width/2, y_pos - box_height/2),
            box_width, box_height, boxstyle="round,pad=0,rounding_size=0.5",
            facecolor=step["fill_color"], edgecolor=step["border_color"], lw=2
        ))

        # Use processed text and fonts
        ax.text(
            box_x, y_pos + 0.6, 
            step['wrapped_title'], 
            ha='center', va='center',
            fontproperties=step['title_font'], 
            color='white', linespacing=1.3
        )

        # Description (position adjusted with title_desc_gap)
        ax.text(
            box_x, y_pos + 0.2 - title_desc_gap, 
            step['wrapped_text'], 
            ha='center', va='top',
            fontproperties=step['desc_font'], 
            color="#ffffff", linespacing=1.3
        )

        # Circle indicators
        ax.add_patch(patches.Circle((circle_x, y_pos), radius=outer_ring_radius, facecolor='none', edgecolor=step["border_color"], lw=2, linestyle='--'))
        ax.add_patch(patches.Circle((circle_x, y_pos), radius=circle_radius, facecolor=step["fill_color"], lw=0))
        ax.text(circle_x, y_pos, str(i + 1), ha='center', va='center', fontsize=40, fontweight='bold', color='white')

    # Connector lines
    if len(connector_points) > 1:
        for i in range(len(connector_points) - 1):
            start_point, end_point = connector_points[i], connector_points[i+1]
            rad = 0.4 if (i + 1) % 2 != 0 else -0.4
            line_color = steps_with_settings[i]["border_color"]
            ax.add_patch(patches.ConnectionPatch(
                xyA=start_point, xyB=end_point, 
                coordsA='data', coordsB='data', 
                connectionstyle=f"arc3,rad={rad}", 
                color='black', lw=4, alpha=0.3
            ))
            ax.add_patch(patches.ConnectionPatch(
                xyA=start_point, xyB=end_point, 
                coordsA='data', coordsB='data', 
                connectionstyle=f"arc3,rad={rad}", 
                color=line_color, lw=2
            ))

    ax.set_xlim(-fig_width / 2, fig_width / 2)
    ax.set_ylim(-4, y_increment * (num_steps - 1) + 4)

    return fig