# import matplotlib.pyplot as plt
# from matplotlib.patches import FancyBboxPatch, Ellipse
# import textwrap
# import io
# import logging

# # Set up logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Color palette for the milestone steps
# STEP_COLORS = ['#7209b7', '#d62828', '#0077b6', '#38b000',
#                '#dccf1d', '#3a0ca3', "#1190ff", "#a30c6e"]

# def validate_steps(steps):
#     """
#     Validate the steps data structure.
#     Returns validated steps or raises an exception.
#     """
#     if not steps:
#         raise ValueError("Steps list cannot be empty")
    
#     validated_steps = []
#     for i, step in enumerate(steps):
#         if len(step) < 2:
#             logger.warning(f"Step {i} has insufficient data. Expected at least 2 elements, got {len(step)}")
#             # Fill missing values with defaults
#             step = list(step)
#             while len(step) < 2:
#                 step.append("Unknown")
#             step = tuple(step)
        
#         validated_steps.append((f"{i+1:02d}", step[0], step[1] if len(step) > 1 else ""))
    
#     return validated_steps

# def draw_flowchart(
#     steps,
#     figsize=(8, 7),
#     preview_mode=False,
#     title_font=None,
#     desc_font=None,
#     title_desc_gap=0.25,   # vertical gap between title and description
#     title_offset=1.0,      # horizontal gap between tower box and title
#     title_wrap=25,         # max characters per line for title
#     desc_wrap=35           # max characters per line for description
# ):
#     """
#     Creates a milestone roadmap flowchart with a perspective road.
#     The 'steps' argument should be a list of tuples, each containing (title, description).
#     Year will be auto-generated as sequential numbers.
#     """
#     try:
#         steps = validate_steps(steps)
#     except ValueError as e:
#         fig, ax = plt.subplots(figsize=figsize)
#         ax.text(0.5, 0.5, str(e), ha='center', va='center')
#         ax.axis('off')
#         return fig
        
#     fig, ax = plt.subplots(figsize=figsize, dpi=600)
#     ax.set_xlim(0, 12)
#     ax.set_ylim(0, len(steps) + 2)
#     ax.axis('off')
    
#     if preview_mode:
#         fig.patch.set_facecolor('white')
#         ax.set_facecolor('white')
#     else:
#         fig.patch.set_alpha(0.0)
#         ax.set_facecolor('none')

#     max_width, min_width = 30, 2

#     # Draw connecting roads
#     for i in range(len(steps) - 1):
#         x_start, x_end = (3, 7) if i % 2 == 0 else (7, 3)
#         y_start, y_end = i + 1, i + 2
#         road_width = max_width - (i * ((max_width - min_width) / (len(steps) - 1)))
        
#         ax.plot([x_start, x_end], [y_start, y_end],
#                 color='#333333', lw=road_width, alpha=0.6,
#                 solid_capstyle='round', zorder=1)
#         ax.plot([x_start, x_end], [y_start, y_end],
#                 color='white', lw=2, alpha=0.9,
#                 linestyle=(0, (4, 6)), zorder=2)

#     # Draw milestones
#     for i, step in enumerate(steps):
#         year, title_text, desc = step
#         y_pos = i + 1
#         is_left = (i % 2 == 0)
#         x_icon = 3 if is_left else 7
#         ha = 'right' if is_left else 'left'
#         color = STEP_COLORS[i % len(STEP_COLORS)]

#         # Tower and year box
#         tower_top_y = y_pos + 1.1
#         ax.plot([x_icon, x_icon], [y_pos + 0.1, tower_top_y],
#                 color=color, lw=3, zorder=3)
#         ax.add_patch(Ellipse((x_icon, y_pos), 0.8, 0.18,
#                              color=color, alpha=0.3, zorder=2))
        
#         box_width, box_height = 1.6, 0.4
#         box_x, box_y = x_icon - box_width / 2, tower_top_y
#         ax.add_patch(FancyBboxPatch(
#             (box_x + 0.05, box_y - 0.05), box_width, box_height,
#             boxstyle="round,pad=0.1", fc=color, alpha=0.3, lw=0, zorder=2))
#         ax.add_patch(FancyBboxPatch(
#             (box_x, box_y), box_width, box_height,
#             boxstyle="round,pad=0.1", fc=color, lw=0, zorder=3))
#         ax.text(x_icon, box_y + box_height / 2, str(year),
#                 fontsize=12, weight='bold', color='white',
#                 ha='center', va='center', zorder=4)
        
#         # Font sizes
#         title_fontsize = title_font.get_size() if title_font else 9
#         desc_fontsize = desc_font.get_size() if desc_font else 7

#         # Title beside tower box
#         if is_left:
#             x_title = x_icon - title_offset
#         else:
#             x_title = x_icon + title_offset

#         ax.text(x_title, tower_top_y + box_height/2,
#                 textwrap.fill(str(title_text), title_wrap),
#                 fontproperties=title_font,
#                 fontsize=title_fontsize,
#                 ha=ha, va='center',
#                 color=color, zorder=4)

#         # Description below title
#         ax.text(x_title, tower_top_y + box_height/2 - title_desc_gap,
#                 textwrap.fill(str(desc), desc_wrap),
#                 fontproperties=desc_font,
#                 fontsize=desc_fontsize,
#                 ha=ha, va='top',
#                 color='#333333', zorder=4)

#     return fig

# def create_example_roadmap():
#     """Create an example roadmap for testing."""
#     steps = [
#         ("Project Kickoff", "Initial planning and team formation"),
#         ("Phase 1 Completion", "First major deliverables completed"),
#         ("Beta Launch", "Initial release to selected users"),
#         ("Full Release", "Public launch of the product")
#     ]
    
#     try:
#         fig = draw_flowchart(steps,
#                              title_desc_gap=0.3,
#                              title_offset=2.0,
#                              title_wrap=20,
#                              desc_wrap=40)
#         fig.savefig("milestone_roadmap.png", format="png", dpi=600, bbox_inches="tight", transparent=True)
#         logger.info("Roadmap created successfully without shadows!")
#         return True
#     except Exception as e:
#         logger.error(f"Failed to create roadmap: {e}")
#         return False

# if __name__ == "__main__":
#     create_example_roadmap()




import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Ellipse
import io
import logging
from text_utils import apply_text_settings, wrap_text
from transparency import apply_alpha_to_color


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Color palette for the milestone steps
STEP_COLORS = ['#7209b7', '#d62828', '#0077b6', '#38b000',
               '#dccf1d', '#3a0ca3', "#1190ff", "#a30c6e"]

def validate_steps(steps):
    """
    Validate the steps data structure.
    Returns validated steps or raises an exception.
    """
    if not steps:
        raise ValueError("Steps list cannot be empty")
    
    validated_steps = []
    for i, step in enumerate(steps):
        if len(step) < 2:
            logger.warning(f"Step {i} has insufficient data. Expected at least 2 elements, got {len(step)}")
            # Fill missing values with defaults
            step = list(step)
            while len(step) < 2:
                step.append("Unknown")
            step = tuple(step)
        
        validated_steps.append((f"{i+1:02d}", step[0], step[1] if len(step) > 1 else ""))
    
    return validated_steps

def draw_flowchart(
    steps,
    figsize=(8, 7),
    preview_mode=False,
    title_font=None,
    desc_font=None,
    title_wrap=None,
    desc_wrap=None,
    title_desc_gap=0.25,   # vertical gap between title and description
    title_offset=1.0      # horizontal gap between tower box and title
):
    """
    Creates a milestone roadmap flowchart with a perspective road.
    The 'steps' argument should be a list of tuples, each containing (title, description).
    Year will be auto-generated as sequential numbers.
    """
    try:
        steps = validate_steps(steps)
    except ValueError as e:
        fig, ax = plt.subplots(figsize=figsize)
        ax.text(0.5, 0.5, str(e), ha='center', va='center')
        ax.axis('off')
        return fig
        
    fig, ax = plt.subplots(figsize=figsize, dpi=600)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, len(steps) + 2)
    ax.axis('off')
    
    if preview_mode:
        fig.patch.set_facecolor('white')
        ax.set_facecolor('white')
    else:
        fig.patch.set_alpha(0.0)
        ax.set_facecolor('none')

    max_width, min_width = 30, 2

    # Apply text settings
    steps_with_settings = apply_text_settings(
        [{'title': title, 'text': desc} for _, title, desc in steps],
        title_font, desc_font, title_wrap, desc_wrap
    )

    # Draw connecting roads
    for i in range(len(steps) - 1):
        x_start, x_end = (3, 7) if i % 2 == 0 else (7, 3)
        y_start, y_end = i + 1, i + 2
        road_width = max_width - (i * ((max_width - min_width) / (len(steps) - 1)))
        
        ax.plot([x_start, x_end], [y_start, y_end],
                color='#333333', lw=road_width, alpha=0.6,
                solid_capstyle='round', zorder=1)
        ax.plot([x_start, x_end], [y_start, y_end],
                color='white', lw=2, alpha=0.9,
                linestyle=(0, (4, 6)), zorder=2)

    # Draw milestones
    for i, step in enumerate(steps):
        year, title_text, desc = step
        step_data = steps_with_settings[i]
        y_pos = i + 1
        is_left = (i % 2 == 0)
        x_icon = 3 if is_left else 7
        ha = 'right' if is_left else 'left'
        color = STEP_COLORS[i % len(STEP_COLORS)]

        # Tower and year box
        tower_top_y = y_pos + 1.1
        ax.plot([x_icon, x_icon], [y_pos + 0.1, tower_top_y],
                color=color, lw=3, zorder=3)
        ax.add_patch(Ellipse((x_icon, y_pos), 0.8, 0.18,
                             color=color, alpha=0.3, zorder=2))
        
        box_width, box_height = 1.6, 0.4
        box_x, box_y = x_icon - box_width / 2, tower_top_y
        ax.add_patch(FancyBboxPatch(
            (box_x + 0.05, box_y - 0.05), box_width, box_height,
            boxstyle="round,pad=0.1", fc=color, alpha=0.3, lw=0, zorder=2))
        ax.add_patch(FancyBboxPatch(
            (box_x, box_y), box_width, box_height,
            boxstyle="round,pad=0.1", fc=color, lw=0, zorder=3))
        ax.text(x_icon, box_y + box_height / 2, str(year),
                fontsize=12, weight='bold', color='white',
                ha='center', va='center', zorder=4)
        
        # Title beside tower box
        if is_left:
            x_title = x_icon - title_offset
        else:
            x_title = x_icon + title_offset

        # Use processed text and fonts
        ax.text(x_title, tower_top_y + box_height/2,
                step_data['wrapped_title'],
                fontproperties=step_data['title_font'],
                ha=ha, va='center',
                color=color, zorder=4)

        # Description below title
        ax.text(x_title, tower_top_y + box_height/2 - title_desc_gap,
                step_data['wrapped_text'],
                fontproperties=step_data['desc_font'],
                ha=ha, va='top',
                color='#333333', zorder=4)

    return fig

def create_example_roadmap():
    """Create an example roadmap for testing."""
    steps = [
        ("Project Kickoff", "Initial planning and team formation"),
        ("Phase 1 Completion", "First major deliverables completed"),
        ("Beta Launch", "Initial release to selected users"),
        ("Full Release", "Public launch of the product")
    ]
    
    try:
        fig = draw_flowchart(steps,
                             title_desc_gap=0.3,
                             title_offset=2.0)
        fig.savefig("milestone_roadmap.png", format="png", dpi=600, bbox_inches="tight", transparent=True)
        logger.info("Roadmap created successfully without shadows!")
        return True
    except Exception as e:
        logger.error(f"Failed to create roadmap: {e}")
        return False

if __name__ == "__main__":
    create_example_roadmap()