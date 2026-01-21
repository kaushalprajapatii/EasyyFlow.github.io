
# new1.py

# --- LIBRARY IMPORTS & SETUP ---
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from io import BytesIO
import io
import importlib
from pathlib import Path
import time 
import base64
# in new1.py or any layout file if transparency.py is alongside new1.py
from transparency import apply_alpha_to_color
import os
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold




# from login import login
# from signup import signup

# st.set_page_config(page_title="User Authentication", layout="centered")

# if "user" not in st.session_state:
#     st.session_state["user"] = None
# if "page" not in st.session_state:
#     st.session_state["page"] = "Login"

# def main():
#     if st.session_state["user"] is None:
#         if st.session_state["page"] == "Login":
#             login()
#         else:
#             signup()

#         col1, col2 = st.columns(2)
#         with col1:
#             if st.button("Go to Login"):
#                 st.session_state["page"] = "Login"
#                 st.rerun()
#         with col2:
#             if st.button("Go to Signup"):
#                 st.session_state["page"] = "Signup"
#                 st.rerun()
#         st.stop()

#     show_homepage()

# def show_homepage():
#     st.title(f"Welcome, {st.session_state['user']} 🎉")
#     st.write("✅ You are now logged in. Your website content goes here.")
#     if st.button("Logout"):
#         st.session_state["user"] = None
#         st.session_state["page"] = "Login"
#         st.rerun() 

# if __name__ == "__main__":
#     main()


# Set matplotlib to use a basic style and disable style-related issues
plt.rcParams.update({'figure.facecolor': 'white'})

# --- LOCAL MODULE IMPORTS ---
import ai_model
from layouts import (
    g, h, i, radial, circular, milestone,
    style1, style2, vertical, horizontal, caterpillar,
    golgol
)

# --- DEVELOPMENT UTILITIES ---
importlib.reload(ai_model)

# --- FONT CONFIGURATION ---
# Define the path to your .otf font file using a raw string
FONT_PATH = r"helvetica-255/helvetica-rounded-bold-5871d05ead8de.otf"

# --- FUNCTION TO LOAD EXTERNAL CSS ---
def load_css(file_name):
    """Opens a CSS file and injects it into the Streamlit app."""
    try:
        with open(file_name) as f:
            css_content = f.read()
            
            # Convert image to base64 and embed in CSS
            bg_image_path = r"D:\Projects\PROJECT 00 - FLOW CHART GENERATOR\easyflow_00\bg.png"
            try:
                with open(bg_image_path, "rb") as img_file:
                    bg_base64 = base64.b64encode(img_file.read()).decode()
                    css_content = css_content.replace("YOUR_BASE64_IMAGE_HERE", bg_base64)
            except FileNotFoundError:
                st.warning(f"Background image not found at: {bg_image_path}. Using default background.")
                # Remove the background image reference if file not found
                css_content = css_content.replace('url("data:image/png;base64,YOUR_BASE64_IMAGE_HERE")', '')
            
            st.markdown(f'<style>{css_content}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"CSS file not found: {file_name}. Make sure it's in the same folder as the Python script.")

# --- HELPER FUNCTIONS ---
def fig_to_bytes(fig, format='png', dpi=300, preview_mode=False):
    """Converts a Matplotlib figure object to a byte buffer."""
    buf = BytesIO()
    if preview_mode:
        fig.savefig(buf, format=format, bbox_inches='tight', dpi=dpi, facecolor='white')
    else:
        fig.savefig(buf, format=format, bbox_inches='tight', dpi=dpi, transparent=True)
    buf.seek(0)
    return buf

def pillow_to_bytes(img, format='PNG'):
    """Converts a Pillow (PIL) Image object to a byte buffer."""
    buf = BytesIO()
    img.save(buf, format=format)
    buf.seek(0)
    return buf

def get_colors_for_steps(color_list, num_steps):
    """Ensures there are enough colors for all steps by cycling through the provided color list."""
    if num_steps <= len(color_list):
        return color_list[:num_steps]
    else:
        repeat_count = (num_steps // len(color_list)) + 1
        extended_colors = color_list * repeat_count
        return extended_colors[:num_steps]

def assign_colors_to_steps(steps, color_module, wrap_width=None):
    """Assign colors from a module to steps, optionally adding wrap_width."""
    for idx, step in enumerate(steps):
        step.update(color_module.COLORS[idx % len(color_module.COLORS)])
        if wrap_width:
            step["wrap_width"] = wrap_width
    return steps

# --- CORE GRAPH GENERATION LOGIC ---
def generate_single_graph(style_name, steps_text, dpi=600, preview_mode=False, 
                         title_fontsize=20, desc_fontsize=14, 
                         title_wrap=None, desc_wrap=None, font_path=None):
    """Generates a single graph image based on the selected style and user text."""
    try:
        # Create FontProperties objects for Matplotlib
        title_font_properties = FontProperties(fname=font_path, size=title_fontsize) if font_path else None
        desc_font_properties = FontProperties(fname=font_path, size=desc_fontsize) if font_path else None
        
        lines = [line.strip() for line in steps_text.split('\n') if line.strip()]
        if not lines:
            return "Error: Input text is empty."
        
        # --- Pillow-Based Layouts ---
        if style_name in ["Milestones Roadmap", "Caterpillar Timeline"]:
            steps = []
            for line in lines:
                parts = line.split(' : ')
                if len(parts) < 2:
                    title = parts[0].strip() if parts else "Untitled"
                    steps.append((title, ""))
                else:
                    title = parts[0].strip()
                    description = ' : '.join(parts[1:]).strip()
                    steps.append((title, description))
            
            final_img = None
            if style_name == "Milestones Roadmap":
                if hasattr(milestone, 'draw_flowchart'):
                    fig = milestone.draw_flowchart(
                        steps, preview_mode=preview_mode, title_font=title_font_properties, 
                        desc_font=desc_font_properties, title_wrap=title_wrap, desc_wrap=desc_wrap
                    )
                    # Use apply_blur_effect for milestone as well
                    if hasattr(milestone, 'apply_blur_effect'):
                        final_img = milestone.apply_blur_effect(fig, preview_mode=preview_mode)
                    elif hasattr(caterpillar, 'apply_blur_effect'):
                        final_img = caterpillar.apply_blur_effect(fig, preview_mode=preview_mode)
                    else:
                        # Fallback: use fig_to_bytes
                        return fig_to_bytes(fig, dpi=dpi, preview_mode=preview_mode)
                else:
                    return "Error: Milestone module missing required functions"
                    
            elif style_name == "Caterpillar Timeline":
                if hasattr(caterpillar, 'draw_flowchart'):
                    fig = caterpillar.draw_flowchart(
                        steps, preview_mode=preview_mode, title_font=title_font_properties, 
                        desc_font=desc_font_properties, title_wrap=title_wrap, desc_wrap=desc_wrap
                    )
                    if hasattr(caterpillar, 'apply_blur_effect'):
                        final_img = caterpillar.apply_blur_effect(fig, preview_mode=preview_mode)
                    else:
                        return fig_to_bytes(fig, dpi=dpi, preview_mode=preview_mode)
                else:
                    return "Error: Caterpillar module missing required functions"
            
            if final_img:
                return pillow_to_bytes(final_img)
            else:
                return "Error: Could not generate final image"

        # --- Matplotlib-Based Layouts ---
        else:
            fig = None
            if style_name == "Curved Arrows":
                if ' : ' not in steps_text:
                    raise ValueError("Incorrect format. Use 'Title : Description'.")
                fig = style2.create_flowchart(
                    steps_text, preview_mode=preview_mode, title_font=title_font_properties, 
                    desc_font=desc_font_properties, title_wrap=title_wrap, desc_wrap=desc_wrap
                )
            else:
                parsed_steps = []
                for line in lines:
                    if ' : ' not in line:
                        title = line.strip()
                        desc = ""
                    else:
                        title, desc = line.split(' : ', 1)
                    parsed_steps.append({"title": title.strip(), "text": desc.strip()})

                # Helper function to pass fonts to Matplotlib layouts
                def create_with_fonts(create_func, *args, **kwargs):
                    return create_func(
                        *args, **kwargs, preview_mode=preview_mode, 
                        title_font=title_font_properties, desc_font=desc_font_properties,
                        title_wrap=title_wrap, desc_wrap=desc_wrap
                    )

                if style_name == "Angled Arrows with Shadows":
                    colors = get_colors_for_steps(style1.BOX_COLORS, len(parsed_steps))
                    fig = create_with_fonts(
                        style1.create_flowchart,
                        [(s["title"], s["text"], colors[i]) for i, s in enumerate(parsed_steps)]
                    )
                
                elif style_name == "Vertical Flowchart":
                    colors = get_colors_for_steps(vertical.BOX_COLORS, len(parsed_steps))
                    fig = create_with_fonts(
                        vertical.create_flowchart,
                        [(s["title"], s["text"], colors[i]) for i, s in enumerate(parsed_steps)]
                    )
                
                elif style_name == "Horizontal Flowchart":
                    colors = get_colors_for_steps(horizontal.BOX_COLORS, len(parsed_steps))
                    fig = create_with_fonts(
                        horizontal.create_flowchart,
                        [(s["title"], s["text"], colors[i]) for i, s in enumerate(parsed_steps)]
                    )
                
                elif style_name == "Circular Workflow":
                    fig = create_with_fonts(
                        circular.create_flowchart,
                        [(s["title"], s["text"]) for s in parsed_steps], 
                        title="Project Lifecycle"
                    )
                
                elif style_name == "Arrow-Style Infographic":
                    fig = create_with_fonts(
                        radial.draw_arrow_infographic,
                        [(s["title"], s["text"]) for s in parsed_steps], 
                        title=""
                    )
                
                elif style_name == "S-Curve Process Flowchart":
                    parsed_steps = assign_colors_to_steps(parsed_steps, i)
                    fig = create_with_fonts(i.create_s_curve_flowchart, parsed_steps)
                
                elif style_name == "Chevron Process Flowchart":
                    parsed_steps = assign_colors_to_steps(parsed_steps, h)
                    fig = create_with_fonts(h.create_chevron_flowchart, parsed_steps)
                
                elif style_name == "Zigzag Stairs Flowchart":
                    parsed_steps = assign_colors_to_steps(parsed_steps, g, wrap_width=25)
                    fig = create_with_fonts(g.create_zigzag_stairs_flowchart, parsed_steps)
                
                elif style_name == "Golgol Flowchart":
                    fig = create_with_fonts(
                        golgol.create_golgol_flowchart,
                        parsed_steps, title="Process Flow"
                    )

            if fig:
                img_bytes_io = fig_to_bytes(fig, format='png', dpi=dpi, preview_mode=preview_mode)
                plt.close(fig)
                return img_bytes_io

        return "Error: Unknown style or generation failed."
    except Exception as e:
        st.error(f"An error occurred while generating '{style_name}': {e}")
        return f"Preview not available. ({e})"

# --- STREAMLIT PAGE CONFIGURATION ---
st.set_page_config(layout="wide", page_title="EasyFlow | AI Flowchart Generator")

# --- LOAD OUR EXTERNAL CSS ---
load_css("style.css")

# --- GLOBAL VARIABLES & CONSTANTS ---
STYLES = [
    "Angled Arrows with Shadows", "Vertical Flowchart", "Horizontal Flowchart",
    "Milestones Roadmap", "Caterpillar Timeline", "Circular Workflow",
    "Curved Arrows", "Arrow-Style Infographic", "S-Curve Process Flowchart",
    "Chevron Process Flowchart", "Zigzag Stairs Flowchart",
    "Golgol Flowchart"
]

# --- SESSION STATE INITIALIZATION ---
if 'steps_text' not in st.session_state: 
    st.session_state.steps_text = "Step 1 : Describe the first action\nStep 2 : Explain the next phase\nStep 3 : Detail the final outcome"
if 'previews' not in st.session_state: 
    st.session_state.previews = {}
if 'selected_graph_style' not in st.session_state: 
    st.session_state.selected_graph_style = None
if 'high_res_image' not in st.session_state: 
    st.session_state.high_res_image = None
if 'layout_settings' not in st.session_state:
    # Store settings for each layout individually
    st.session_state.layout_settings = {}
    for style in STYLES:
        st.session_state.layout_settings[style] = {
            'title_fontsize': 20,
            'desc_fontsize': 14,
            'title_wrap': 25,
            'desc_wrap': 30
        }

# ======================================================================
# --- MAIN APPLICATION UI ---
# ======================================================================

# --- UI: HEADER & TITLE ---
st.markdown("""
<div class="title-container">
    <div class="title-glow">EasyFlow</div>
    <p class="subtitle">Intelligent Flowchart & Diagram Generation</p>
</div>
""", unsafe_allow_html=True)

# --- UI: CONTENT INPUT SECTION ---
st.markdown("<h2 class='section-header'>❶ Input Your Content</h2>", unsafe_allow_html=True)

input_tabs = st.tabs(["✍ Enter Manually", "🤖 Generate with AI"])
with input_tabs[0]:
    edited_text = st.text_area("Enter or edit steps:", value=st.session_state.steps_text, height=250, label_visibility="collapsed")
    st.session_state.steps_text = edited_text
    
with input_tabs[1]:
    with st.form(key="ai_form"):
        ai_topic = st.text_input("Enter a topic:", placeholder="e.g., The process of photosynthesis")
        ai_num_steps = st.number_input("Number of steps:", min_value=2, max_value=15, value=5)
        
        if st.form_submit_button("✨ Generate Steps", use_container_width=True):
            if ai_topic:
                with st.spinner("🧠 AI is crafting your steps..."):
                    st.session_state.steps_text = ai_model.generate_flowchart_steps(ai_topic, ai_num_steps)
                st.success("AI steps generated! Edit them or generate previews.")
            else:
                st.warning("Please enter a topic for the AI.")

if st.button("🎨 Generate All Previews", use_container_width=True, type="primary"):
    st.session_state.previews = {}
    st.session_state.selected_graph_style = None
    st.session_state.high_res_image = None
    
    progress_bar = st.progress(0, text="Generating previews...")
    with st.spinner("Generating all graph previews with default settings... this may take a moment."):
        for idx, style_name in enumerate(STYLES):
            # Use default settings for previews
            preview_data = generate_single_graph(
                style_name, 
                st.session_state.steps_text, 
                dpi=90, 
                preview_mode=True, 
                title_fontsize=20,  # Default for previews
                desc_fontsize=14,   # Default for previews
                title_wrap=25,      # Default for previews
                desc_wrap=30,       # Default for previews
                font_path=FONT_PATH
            )
            st.session_state.previews[style_name] = preview_data
            progress_bar.progress((idx + 1) / len(STYLES), text=f"Generated: {style_name}")
    progress_bar.empty()
    st.success("All previews generated with default settings! Select a layout to customize.")

# --- UI: PREVIEW GALLERY ---
if st.session_state.previews:
    st.markdown("<h2 class='section-header'>❷ Click a Preview to Select</h2>", unsafe_allow_html=True)
    st.info("💡 All previews are generated with default settings. Select a layout to customize text appearance.")
    
    cols = st.columns(4)
    for idx, style_name in enumerate(STYLES):
        col = cols[idx % 4]
        with col:
            preview_data = st.session_state.previews.get(style_name)
            
            with st.container():
                if st.button("Select " + style_name, key=f"btn_{idx}", use_container_width=True):
                    if isinstance(preview_data, io.BytesIO):
                        if st.session_state.selected_graph_style != style_name:
                            st.session_state.selected_graph_style = style_name
                            st.session_state.high_res_image = None
                            st.rerun()
                    else:
                        st.toast(f"Cannot select '{style_name}' as its preview is unavailable.", icon="⚠")
                
                if isinstance(preview_data, io.BytesIO):
                    st.image(preview_data, use_container_width=True)
                else:
                    st.markdown(f'<div class="error-container">{preview_data}</div>', unsafe_allow_html=True)
                
                st.markdown(f'<p style="text-align: center; font-weight: bold; margin-bottom: 0;">{style_name}</p>', unsafe_allow_html=True)

# --- UI: FINAL GRAPH DISPLAY & DOWNLOAD ---
if st.session_state.selected_graph_style:
    style_name = st.session_state.selected_graph_style
    
    st.markdown(f"<h2 class='section-header'>❸ Customize & Download: {style_name}</h2>", unsafe_allow_html=True)
    
    # Get current settings for this layout
    current_settings = st.session_state.layout_settings[style_name]
    
    # Text customization controls for the selected layout
    st.markdown("### 🎨 Customize Text Appearance")
    st.info(f"Adjust text settings for **{style_name}** layout only")
    
    custom_col1, custom_col2 = st.columns(2)
    
    with custom_col1:
        st.markdown("**📝 Font Sizes**")
        with st.container(border=True):
            new_title_fontsize = st.number_input(
                "Title Font Size", 
                min_value=1, 
                max_value=50, 
                value=current_settings['title_fontsize'], 
                step=1,
                key=f"title_size_{style_name}",
                help="Font size for titles (1-50)"
            )
            new_desc_fontsize = st.number_input(
                "Description Font Size", 
                min_value=1, 
                max_value=50, 
                value=current_settings['desc_fontsize'], 
                step=1,
                key=f"desc_size_{style_name}",
                help="Font size for descriptions (1-50)"
            )

    with custom_col2:
        st.markdown("**🔤 Text Wrapping**")
        with st.container(border=True):
            new_title_wrap = st.number_input(
                "Title Wrap Width", 
                min_value=10, 
                max_value=100, 
                value=current_settings['title_wrap'],
                step=1,
                key=f"title_wrap_{style_name}",
                help="Characters per line for titles (10-100)"
            )
            new_desc_wrap = st.number_input(
                "Description Wrap Width", 
                min_value=10, 
                max_value=100, 
                value=current_settings['desc_wrap'],
                step=1,
                key=f"desc_wrap_{style_name}",
                help="Characters per line for descriptions (10-100)"
            )
    
    # Apply customization for this specific layout
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 Apply Customization to This Layout", use_container_width=True, type="primary"):
            # Update settings for this specific layout
            st.session_state.layout_settings[style_name] = {
                'title_fontsize': new_title_fontsize,
                'desc_fontsize': new_desc_fontsize,
                'title_wrap': new_title_wrap,
                'desc_wrap': new_desc_wrap
            }
            st.session_state.high_res_image = None  # Force regeneration
            st.success(f"Customization applied to {style_name}! Generating updated version...")
            st.rerun()
    
    # Show current settings
    st.info(f"**Current Settings for {style_name}:** "
            f"Title Size: {current_settings['title_fontsize']}px, "
            f"Description Size: {current_settings['desc_fontsize']}px, "
            f"Title Wrap: {current_settings['title_wrap']} chars, "
            f"Description Wrap: {current_settings['desc_wrap']} chars")
    
    with st.container():
        if st.session_state.high_res_image is None:
            with st.spinner(f"Generating high-quality 600 DPI version of {style_name} with your customization..."):
                high_res_data = generate_single_graph(
                    style_name, 
                    st.session_state.steps_text, 
                    dpi=600, 
                    preview_mode=False,
                    title_fontsize=current_settings['title_fontsize'],
                    desc_fontsize=current_settings['desc_fontsize'],
                    title_wrap=current_settings['title_wrap'],
                    desc_wrap=current_settings['desc_wrap'],
                    font_path=FONT_PATH
                )
                if isinstance(high_res_data, io.BytesIO):
                    st.session_state.high_res_image = high_res_data
                    st.success(f"High-quality {style_name} generated with your customization!")
                else:
                    st.error("Could not generate high-quality version.")
        
        if st.session_state.high_res_image:
            # For display, generate a preview with current settings
            display_data = generate_single_graph(
                style_name, 
                st.session_state.steps_text, 
                dpi=150, 
                preview_mode=True,
                title_fontsize=current_settings['title_fontsize'],
                desc_fontsize=current_settings['desc_fontsize'],
                title_wrap=current_settings['title_wrap'],
                desc_wrap=current_settings['desc_wrap'],
                font_path=FONT_PATH
            )
            if isinstance(display_data, io.BytesIO):
                st.image(display_data, caption=f"{style_name} (with your customization)", use_container_width=True)
            
            # Download button
            st.download_button(
                "📥 Download 600 DPI PNG",
                data=st.session_state.high_res_image,
                file_name=f"{style_name.replace(' ', '_')}_600dpi.png",
                mime="image/png",
                use_container_width=True,
                type="primary"
            )
            
            # Option to reset to defaults
            if st.button("🔄 Reset to Default Settings", use_container_width=True):
                st.session_state.layout_settings[style_name] = {
                    'title_fontsize': 20,
                    'desc_fontsize': 14,
                    'title_wrap': 25,
                    'desc_wrap': 30
                }
                st.session_state.high_res_image = None
                st.success(f"Reset {style_name} to default settings!")
                st.rerun()




