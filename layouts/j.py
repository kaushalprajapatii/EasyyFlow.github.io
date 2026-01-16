import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.path as mpath
import textwrap
import inspect
import numpy as np

# --- Icon Drawing Functions ---

def draw_rain_icon(ax, center, radius, color):
    """Draws the data collection/rain icon."""
    icon_center_x, icon_center_y = center
    # Outer container
    ax.add_patch(patches.Circle(center, radius=radius, facecolor='none', edgecolor=color, lw=1.5))
    # Cloud
    cloud_y = icon_center_y + radius * 0.1
    cloud_parts = [
        patches.Circle((icon_center_x - radius * 0.35, cloud_y), radius * 0.22, color=color),
        patches.Circle((icon_center_x + radius * 0.3, cloud_y), radius * 0.3, color=color),
        patches.Circle((icon_center_x, cloud_y - radius * 0.1), radius * 0.35, color=color),
    ]
    for part in cloud_parts:
        ax.add_patch(part)
    # Rain
    for i in range(3):
        x_start = icon_center_x - 0.2 + i * 0.2
        y_start = icon_center_y - radius * 0.3
        ax.plot([x_start, x_start - 0.05], [y_start, y_start - 0.2], color=color, lw=1.5, linestyle='--')

def draw_grid_icon(ax, center, radius, color):
    """Draws the model training/grid icon."""
    size = radius * 1.5
    # Outer container
    ax.add_patch(patches.FancyBboxPatch(
        (center[0] - size / 2, center[1] - size / 2), size, size,
        boxstyle="round,pad=0,rounding_size=0.15",
        facecolor='none', edgecolor=color, lw=1.5))
    # Grid
    inner_size = size * 0.7
    for i in np.linspace(-inner_size / 2, inner_size / 2, 3):
        ax.plot([center[0] + i, center[0] + i], [center[1] - inner_size / 2, center[1] + inner_size / 2], color=color, lw=1)
        ax.plot([center[0] - inner_size / 2, center[0] + inner_size / 2], [center[1] + i, center[1] + i], color=color, lw=1)

def draw_barchart_icon(ax, center, radius, color):
    """Draws the performance evaluation/bar chart icon."""
    # Outer container
    ax.add_patch(patches.Circle(center, radius=radius, facecolor='none', edgecolor=color, lw=1.5))
    # Bars
    bar_width = 0.2
    heights = [0.3, 0.6, 0.4]
    positions = [-0.3, 0, 0.3]
    for h, p in zip(heights, positions):
        ax.add_patch(patches.Rectangle(
            (center[0] + p - bar_width / 2, center[1] - radius * 0.4),
            bar_width, h, color=color))

def draw_flood_icon(ax, center, radius, color):
    """Draws the flood risk/landscape icon."""
    size = radius * 1.8
    # Outer container (diamond)
    diamond = patches.Polygon(
        [[center[0], center[1] + size / 2], [center[0] + size / 2, center[1]],
         [center[0], center[1] - size / 2], [center[0] - size / 2, center[1]]],
        closed=True, facecolor='none', edgecolor=color, lw=1.5)
    ax.add_patch(diamond)
    # Mountain
    mountain_path = [
        (center[0] - 0.4, center[1] - 0.2),
        (center[0] - 0.1, center[1] + 0.2),
        (center[0] + 0.1, center[1] - 0.1),
        (center[0] + 0.4, center[1] + 0.1)
    ]
    ax.plot([p[0] for p in mountain_path], [p[1] for p in mountain_path], color=color, lw=1.5)
    # Water
    water_y = center[1] - 0.2
    water_x = np.linspace(center[0] - 0.4, center[0] + 0.4, 50)
    water_y_vals = water_y + 0.05 * np.sin(water_x * 20)
    ax.plot(water_x, water_y_vals, color=color, lw=1.5)

def create_head_flowchart(steps_data):
    """
    Generates a vertical flowchart in the shape of a human head silhouette.
    """
    if not steps_data:
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, "Please enter steps in the format 'Title : Description'", ha='center', va='center')
        ax.axis('off')
        return fig

    num_steps = len(steps_data)
    fig, ax = plt.subplots(figsize=(8, 10))
    fig.patch.set_facecolor('#1e1e1e')
    ax.set_facecolor('#1e1e1e')
    ax.set_aspect('equal', adjustable='box')
    plt.axis('off')

    # Define the path for the head silhouette using Bezier curves
    Path = mpath.Path
    path_data = [
        (Path.MOVETO, (4.5, 0.5)),
        (Path.CURVE4, (3.5, 1.5)), (Path.CURVE4, (2.0, 3.0)), (Path.LINETO, (1.8, 5.0)),
        (Path.CURVE4, (1.8, 7.0)), (Path.CURVE4, (3.0, 9.5)), (Path.LINETO, (4.5, 10.0)),
        (Path.CURVE4, (6.5, 9.8)), (Path.CURVE4, (7.8, 8.5)), (Path.LINETO, (7.5, 7.5)),
        (Path.LINETO, (8.2, 7.0)),
        (Path.LINETO, (7.4, 6.4)),
        (Path.LINETO, (7.6, 6.2)),
        (Path.LINETO, (7.4, 6.0)),
        (Path.CURVE4, (7.8, 5.0)), (Path.CURVE4, (6.5, 4.0)), (Path.LINETO, (6.0, 2.5)),
        (Path.CURVE4, (5.0, 1.0)), (Path.CURVE4, (4.5, 0.5)), (Path.CLOSEPOLY, (4.5, 0.5)),
    ]
    codes, verts = zip(*path_data)
    path = Path(verts, codes)

    # Set plot limits based on path
    y_coords = [v[1] for v in verts]
    y_min, y_max = min(y_coords), max(y_coords)
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 10.5)

    # --- Draw segmented silhouette using clipping ---
    total_y_span = y_max - y_min
    for i in range(num_steps):
        color = steps_data[i]['border_color']
        y_start_clip = y_min + (num_steps - 1 - i) * (total_y_span / num_steps)
        clip_height = total_y_span / num_steps

        clip_rect = patches.Rectangle((0, y_start_clip), width=10, height=clip_height, transform=ax.transData)
        path_patch = patches.PathPatch(path, facecolor='none', edgecolor=color, lw=2, clip_path=clip_rect, clip_on=True)
        ax.add_patch(path_patch)

    # --- Draw Icons and Text ---
    icon_funcs = [draw_rain_icon, draw_grid_icon, draw_barchart_icon, draw_flood_icon]
    icon_radius = 0.6
    for i, step in enumerate(steps_data):
        y_center = y_max - (i + 0.5) * (total_y_span / num_steps)
        icon_x = 3.5
        text_x = 5.0
        
        icon_func = icon_funcs[i % len(icon_funcs)]
        icon_func(ax, center=(icon_x, y_center), radius=icon_radius, color=step['border_color'])
        
        wrapped_desc = textwrap.fill(step['text'], width=35)
        ax.text(text_x, y_center + 0.25, step['title'], ha='left', va='center', fontsize=14, fontweight='bold', color=step['border_color'])
        ax.text(text_x, y_center - 0.2, wrapped_desc, ha='left', va='top', fontsize=12, color='#cccccc', linespacing=1.4)

    # --- Set Plot Title ---
    ax.set_title("Comprehensive Flood Risk Assessment Process", fontsize=18, fontweight='bold', color='white', pad=20)

    return fig

# --- Streamlit App ---
st.set_page_config(layout="wide", page_title="Process Flowchart Generator")
st.title("Process Flowchart Generator 🌊")
st.write("Enter each step on a new line in the format **Title : Description**. The flowchart will update automatically.")

# Colors matching the provided image
COLORS = [
    {"border_color": "#2a9d8f"},  # Green
    {"border_color": "#5eab9d"},  # Lighter Green
    {"border_color": "#e9c46a"},  # Yellow
    {"border_color": "#f4a261"},  # Light Orange
    {"border_color": "#e76f51"},  # Orange/Red
]

default_input = """Data Collection : Gathering essential environmental data
Model Training : Applying modeling techniques to predict river discharge
Performance Evaluation : Assessing the accuracy of predictive models
Flood Risk Assessment : Evaluating potential flood risks based on predictions"""

user_input = st.text_area("Enter Flowchart Steps:", default_input, height=200)

parsed_steps = []
if user_input:
    lines = user_input.strip().split('\n')
    for i, line in enumerate(lines):
        if ':' in line:
            title, description = line.split(':', 1)
            step_info = {
                "title": title.strip(),
                "text": description.strip(),
            }
            step_info.update(COLORS[i % len(COLORS)])
            parsed_steps.append(step_info)

if parsed_steps:
    flowchart_fig = create_head_flowchart(parsed_steps)
    st.pyplot(flowchart_fig, facecolor='#1e1e1e')
else:
    st.warning("Please enter at least one step in the format 'Title : Description'.")

with st.expander("Click to see the final Python code"):
    # Combine the source code of the main function and its helpers
    code_string = inspect.getsource(create_head_flowchart)
    code_string += "\n" + inspect.getsource(draw_rain_icon)
    code_string += "\n" + inspect.getsource(draw_grid_icon)
    code_string += "\n" + inspect.getsource(draw_barchart_icon)
    code_string += "\n" + inspect.getsource(draw_flood_icon)
    st.code(code_string, language='python')