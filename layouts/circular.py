# # layouts/circular.py
# import matplotlib.pyplot as plt
# from matplotlib.patches import Circle, ConnectionPatch
# from matplotlib.offsetbox import OffsetImage, AnnotationBbox
# import textwrap
# import numpy as np
# import requests
# from io import BytesIO

# # Color palette for the circular steps
# STEP_COLORS = ['#d62828', '#f77f00', '#0077b6', '#38b000', '#7209b7', '#3a0ca3', "#dccf1d", "#34f5eb", "#62F064"]

# def load_image_from_url(url):
#     """Helper function to load an image from a URL for matplotlib."""
#     try:
#         response = requests.get(url, timeout=5)
#         response.raise_for_status() # Raise an exception for bad status codes
#         return plt.imread(BytesIO(response.content))
#     except Exception as e:
#         print(f"Failed to load image from URL {url}: {e}")
#         return None

# # UPDATED: Function signature to accept title_font and desc_font
# def create_flowchart(steps, title="Creative Workflow", figsize=(10, 10), preview_mode=False, title_font=None, desc_font=None):
#     """
#     Generates a circular workflow flowchart with a central icon and an open dotted line.
#     """
#     if not steps:
#         fig, ax = plt.subplots()
#         ax.text(0.5, 0.5, "Please provide steps data.", ha='center', va='center')
#         ax.axis('off')
#         return fig
        
#     fig, ax = plt.subplots(figsize=figsize)
    
#     if preview_mode:
#         fig.patch.set_facecolor('white')
#     else:
#         fig.patch.set_alpha(0.0)
#         ax.set_facecolor('none')
    
#     ax.set_xlim(0, 12)
#     ax.set_ylim(0, 12)
#     ax.axis('off')

#     num_steps = len(steps)
#     center_x, center_y = 6, 6
#     radius = 3.5
#     angles = np.linspace(np.pi / 2, -3 * np.pi / 2, num_steps, endpoint=False)

#     for i, (title_text, desc) in enumerate(steps):
#         angle = angles[i]
#         cx, cy = center_x + radius * np.cos(angle), center_y + radius * np.sin(angle)
#         color = STEP_COLORS[i % len(STEP_COLORS)]

#         ax.add_patch(Circle((cx + 0.1, cy - 0.1), 0.5, color='gray', alpha=0.3, zorder=3))
#         ax.add_patch(Circle((cx, cy), 0.5, color=color, zorder=4))
#         ax.text(cx, cy, f"{i+1:02}", ha='center', va='center', fontsize=15, color='white', weight='bold', zorder=5)

#         tx, ty = center_x + (radius + 1.2) * np.cos(angle), center_y + (radius + 1.2) * np.sin(angle)
#         ax.add_artist(ConnectionPatch((cx + 0.35 * np.cos(angle), cy + 0.35 * np.sin(angle)),
#                                       (tx, ty), "data", "data", color="gray", lw=2))
        
#         align = 'left' if np.cos(angle) >= 0 else 'right'
#         # UPDATED: Using fontproperties instead of fontsize
#         ax.text(tx, ty + 0.2, textwrap.fill(title_text, 22), fontproperties=title_font, color="#000000", va='top', ha=align)
#         # UPDATED: Using fontproperties instead of fontsize
#         ax.text(tx, ty - 0.2, textwrap.fill(desc, 25), fontproperties=desc_font, color="#262424", va='top', ha=align)

#         if i < num_steps - 1:
#             mid_angle = (angle + angles[i + 1]) / 2
#             arrow_x = center_x + radius * np.cos(mid_angle)
#             arrow_y = center_y + radius * np.sin(mid_angle)
#             rotation = np.degrees(mid_angle) - 90
#             ax.text(arrow_x, arrow_y, '➤', fontsize=14, color='#CCCCCC', rotation=rotation, ha='center', va='center', zorder=6)

#     if num_steps > 1:
#         start_angle, end_angle = angles[0], angles[-1]
#         arc_angles = np.linspace(start_angle, end_angle, 200)
#         arc_x, arc_y = center_x + radius * np.cos(arc_angles), center_y + radius * np.sin(arc_angles)
#         ax.plot(arc_x, arc_y, linestyle='dashed', color='#999999', lw=1.5, zorder=2)

#     inner_radius = 2.0
#     ax.add_patch(Circle((center_x + 0.12, center_y - 0.12), inner_radius, facecolor='gray', alpha=0.3, zorder=1))
#     ax.add_patch(Circle((center_x, center_y), inner_radius, facecolor='#fefefe', edgecolor='#4a4a4a', lw=2, zorder=2))
    
#     bulb_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/9/92/Simple_light_bulb_graphic.png/640px-Simple_light_bulb_graphic.png"
#     image = load_image_from_url(bulb_url)
#     if image is not None:
#         imbox = OffsetImage(image, zoom=0.10)
#         ab = AnnotationBbox(imbox, (center_x, center_y + 0.8), frameon=False, box_alignment=(0.5, 0.5), zorder=5)
#         ax.add_artist(ab)
#     else:
#         ax.text(center_x, center_y + 0.8, "💡", fontsize=40, ha='center', va='center', zorder=5)

#     # UPDATED: Using fontproperties instead of fontsize
#     ax.text(center_x, center_y - 0.6, textwrap.fill(title, 15), ha='center', va='center',
#             fontproperties=title_font, weight='bold', color='#222', zorder=6)

#     return fig





# layouts/circular.py
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, ConnectionPatch
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np
import requests
from io import BytesIO
from text_utils import apply_text_settings, wrap_text
from transparency import apply_alpha_to_color


# Color palette for the circular steps
STEP_COLORS = ["#ff8c8c", "#ffc383", "#70cdff", "#bdff9e", "#d499fb", "#ab86ff", '#dccf1d', '#34f5eb', '#62f064']

def load_image_from_url(url):
    """Helper function to load an image from a URL for matplotlib."""
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status() # Raise an exception for bad status codes
        return plt.imread(BytesIO(response.content))
    except Exception as e:
        print(f"Failed to load image from URL {url}: {e}")
        return None

def create_flowchart(steps, title="Creative Workflow", figsize=(10, 10), preview_mode=False, title_font=None, desc_font=None, title_wrap=None, desc_wrap=None):
    """
    Generates a circular workflow flowchart with a central icon and an open dotted line.
    """
    if not steps:
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, "Please provide steps data.", ha='center', va='center')
        ax.axis('off')
        return fig
        
    fig, ax = plt.subplots(figsize=figsize)
    
    if preview_mode:
        fig.patch.set_facecolor('white')
    else:
        fig.patch.set_alpha(0.0)
        ax.set_facecolor('none')
    
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 12)
    ax.axis('off')

    num_steps = len(steps)
    center_x, center_y = 6, 6
    radius = 3.5
    angles = np.linspace(np.pi / 2, -3 * np.pi / 2, num_steps, endpoint=False)

    # Apply text settings
    steps_with_settings = apply_text_settings(
        [{'title': title, 'text': desc} for title, desc in steps],
        title_font, desc_font, title_wrap, desc_wrap
    )

    for i, step_data in enumerate(steps_with_settings):
        angle = angles[i]
        cx, cy = center_x + radius * np.cos(angle), center_y + radius * np.sin(angle)
        color = STEP_COLORS[i % len(STEP_COLORS)]

        ax.add_patch(Circle((cx + 0.1, cy - 0.1), 0.5, color='gray', alpha=0.3, zorder=3))
        ax.add_patch(Circle((cx, cy), 0.5, color=color, zorder=4))
        ax.text(cx, cy, f"{i+1:02}", ha='center', va='center', fontsize=15, color='white', weight='bold', zorder=5)

        tx, ty = center_x + (radius + 1.2) * np.cos(angle), center_y + (radius + 1.2) * np.sin(angle)
        ax.add_artist(ConnectionPatch((cx + 0.35 * np.cos(angle), cy + 0.35 * np.sin(angle)),
                                      (tx, ty), "data", "data", color="gray", lw=2))
        
        align = 'left' if np.cos(angle) >= 0 else 'right'
        
        # Use processed text and fonts
        ax.text(tx, ty + 0.2, step_data['wrapped_title'], 
                fontproperties=step_data['title_font'], color="#000000", va='top', ha=align)
        
        ax.text(tx, ty - 0.2, step_data['wrapped_text'], 
                fontproperties=step_data['desc_font'], color="#262424", va='top', ha=align)

        if i < num_steps - 1:
            mid_angle = (angle + angles[i + 1]) / 2
            arrow_x = center_x + radius * np.cos(mid_angle)
            arrow_y = center_y + radius * np.sin(mid_angle)
            rotation = np.degrees(mid_angle) - 90
            ax.text(arrow_x, arrow_y, '➤', fontsize=14, color='#CCCCCC', rotation=rotation, ha='center', va='center', zorder=6)

    if num_steps > 1:
        start_angle, end_angle = angles[0], angles[-1]
        arc_angles = np.linspace(start_angle, end_angle, 200)
        arc_x, arc_y = center_x + radius * np.cos(arc_angles), center_y + radius * np.sin(arc_angles)
        ax.plot(arc_x, arc_y, linestyle='dashed', color='#999999', lw=1.5, zorder=2)

    inner_radius = 2.0
    ax.add_patch(Circle((center_x + 0.12, center_y - 0.12), inner_radius, facecolor='gray', alpha=0.3, zorder=1))
    ax.add_patch(Circle((center_x, center_y), inner_radius, facecolor='#fefefe', edgecolor='#4a4a4a', lw=2, zorder=2))
    
    bulb_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/9/92/Simple_light_bulb_graphic.png/640px-Simple_light_bulb_graphic.png"
    image = load_image_from_url(bulb_url)
    if image is not None:
        imbox = OffsetImage(image, zoom=0.10)
        ab = AnnotationBbox(imbox, (center_x, center_y + 0.8), frameon=False, box_alignment=(0.5, 0.5), zorder=5)
        ax.add_artist(ab)
    else:
        ax.text(center_x, center_y + 0.8, "💡", fontsize=40, ha='center', va='center', zorder=5)

    # Use font properties for main title
    ax.text(center_x, center_y - 0.6, wrap_text(title, 15), ha='center', va='center',
            fontproperties=title_font, weight='bold', color='#222', zorder=6)

    return fig