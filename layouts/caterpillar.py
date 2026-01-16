# # caterpiller.py
# import matplotlib.pyplot as plt
# from matplotlib.patches import Circle, FancyBboxPatch
# import numpy as np
# import textwrap
# import io
# from PIL import Image, ImageFilter

# # Set matplotlib parameters
# plt.rcParams.update({
#     'figure.facecolor': 'white',
#     'axes.facecolor': 'white',
#     'savefig.facecolor': 'white',
#     'font.family': 'sans-serif'
# })

# STEP_COLORS = ['#f4a300', '#f47e00', '#e55b5b', '#69c768', '#47b8f5', '#144379']

# def draw_flowchart(steps, figsize=(10, 7.0), preview_mode=False, title_font=None, desc_font=None):
#     """Draw a caterpillar-style flowchart"""
#     try:
#         fig, ax = plt.subplots(figsize=figsize, dpi=300)
        
#         if preview_mode:
#             fig.patch.set_facecolor('white')
#             ax.set_facecolor('white')
#         else:
#             fig.patch.set_alpha(0.0)
#             ax.set_alpha(0.0)
        
#         num_steps = len(steps)
#         circle_spacing = 1.5
#         ax.set_xlim(-1, (num_steps - 1) * circle_spacing + 1)
#         ax.set_ylim(-3.0, 3.0)
#         ax.axis('off')

#         # Draw the main timeline
#         ax.plot([-0.5, (num_steps - 1) * circle_spacing + 0.5], [0, 0], 
#                 color="#cccccc", lw=3, zorder=1)

#         for i, (title, desc) in enumerate(steps):
#             x = i * circle_spacing
#             color = STEP_COLORS[i % len(STEP_COLORS)]
#             step_number = f"{i+1:02d}"

#             # Draw circle and its shadow
#             ax.add_patch(Circle((x + 0.08, -0.08), 0.43, color='#000000', alpha=0.2, zorder=1))
#             ax.add_patch(Circle((x, 0), 0.43, color='white', zorder=2, edgecolor='none'))
#             ax.add_patch(Circle((x, 0), 0.4, color=color, zorder=3, edgecolor='none'))
            
#             # Add step number text
#             ax.text(x, 0, step_number, ha='center', va='center', 
#                     color='white', fontsize=15, weight='bold', zorder=4)

#             # Text wrapping
#             wrapped_title = textwrap.fill(title, width=15)
#             box_height = 0.4
#             box_width = 1.4
#             box_x = x - box_width / 2
            
#             # Define padding for description
#             description_padding = 0.2
            
#             if i % 2 == 0:
#                 # Even steps: title above, description above title
#                 line_y = 0.2
#                 title_y_center = 1.2
#                 desc_y = title_y_center + box_height/2 + description_padding
#                 va_desc = 'bottom'
#             else:
#                 # Odd steps: title below, description below title
#                 line_y = -0.4
#                 title_y_center = -1.2
#                 desc_y = title_y_center - box_height/2 - description_padding
#                 va_desc = 'top'

#             # Draw connecting line
#             ax.plot([x, x], [0, line_y], color="#999999", lw=1.5, zorder=2)

#             box_y = title_y_center - box_height / 2
            
#             # Draw title box and its shadow
#             ax.add_patch(FancyBboxPatch(
#                 (box_x + 0.08, box_y - 0.08), box_width, box_height,
#                 boxstyle="round,pad=0.1,rounding_size=0.15", 
#                 facecolor='#000000', alpha=0.2, lw=0, zorder=2
#             ))
#             ax.add_patch(FancyBboxPatch(
#                 (box_x, box_y), box_width, box_height,
#                 boxstyle="round,pad=0.1,rounding_size=0.15", 
#                 facecolor=color, edgecolor='#ffffff', lw=1.5, zorder=3
#             ))
            
#             # Add title text
#             title_font_size = 12
#             if title_font and hasattr(title_font, 'get_size'):
#                 title_font_size = title_font.get_size()
            
#             ax.text(x, title_y_center, wrapped_title, ha='center', va='center', 
#                     fontproperties=title_font, 
#                     fontsize=title_font_size,
#                     color='white', zorder=4, wrap=True)
            
#             # Add description text
#             if desc:
#                 wrapped_desc = textwrap.fill(desc, width=20)
#                 desc_font_size = 10
#                 if desc_font and hasattr(desc_font, 'get_size'):
#                     desc_font_size = desc_font.get_size()
                    
#                 ax.text(x, desc_y, wrapped_desc, ha='center', va=va_desc, 
#                         fontproperties=desc_font,
#                         fontsize=desc_font_size,
#                         color='#555555', zorder=3, wrap=True)

#         plt.tight_layout()
#         return fig
#     except Exception as e:
#         print(f"Error in caterpillar draw_flowchart: {e}")
#         # Return a simple figure in case of error
#         fig, ax = plt.subplots(figsize=(10, 7.0))
#         ax.text(0.5, 0.5, f"Error in caterpillar layout: {e}", ha='center', va='center', transform=ax.transAxes)
#         return fig

# def apply_blur_effect(fig, blur_radius=6, preview_mode=False):
#     """Apply blur effect to the figure"""
#     try:
#         buf = io.BytesIO()
#         save_kwargs = {
#             'format': 'png',
#             'bbox_inches': 'tight',
#             'dpi': 300,
#             'pad_inches': 0.1
#         }
        
#         if preview_mode:
#             save_kwargs['facecolor'] = 'white'
#         else:
#             save_kwargs['transparent'] = True
            
#         fig.savefig(buf, **save_kwargs)
#         buf.seek(0)
#         base = Image.open(buf).convert("RGBA")
#         plt.close(fig)

#         # Create shadow effect
#         shadow = Image.new("RGBA", base.size, (0, 0, 0, 0))
#         blurred = Image.new("RGBA", base.size, (0, 0, 0, 120))
#         shadow.paste(blurred, mask=base.split()[3])
#         shadow_blurred = shadow.filter(ImageFilter.GaussianBlur(radius=blur_radius))

#         # Composite images
#         final = Image.alpha_composite(shadow_blurred, base)
#         return final
#     except Exception as e:
#         print(f"Error in caterpillar apply_blur_effect: {e}")
#         # Return the original figure as bytes
#         try:
#             buf = io.BytesIO()
#             fig.savefig(buf, format='png', bbox_inches='tight', facecolor='white')
#             buf.seek(0)
#             plt.close(fig)
#             return Image.open(buf).convert("RGBA")
#         except:
#             # Final fallback
#             img = Image.new('RGB', (800, 600), color='white')
#             return img

# # Alias for compatibility with milestone layout
# apply_blur_shadow = apply_blur_effect

# def test_caterpillar():
#     """Test function to verify caterpillar layout works"""
#     try:
#         sample_steps = [
#             ("Step One", "First step description with some longer text to test wrapping"),
#             ("Step Two", "Second step description"), 
#             ("Step Three", "Third step description with more details"),
#             ("Step Four", "Fourth step description")
#         ]
        
#         fig = draw_flowchart(sample_steps, preview_mode=True)
#         final_img = apply_blur_effect(fig, preview_mode=True)
#         final_img.save("test_caterpillar.png")
#         print("✅ Caterpillar test completed - check test_caterpillar.png")
#         return True
#     except Exception as e:
#         print(f"❌ Caterpillar test failed: {e}")
#         return False

# if __name__ == "__main__":
#     test_caterpillar() 








# caterpiller.py
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch
import numpy as np
import io
from PIL import Image, ImageFilter
from text_utils import apply_text_settings, wrap_text
from transparency import apply_alpha_to_color


# Set matplotlib parameters
plt.rcParams.update({
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'savefig.facecolor': 'white',
    'font.family': 'sans-serif'
})

STEP_COLORS = ["#FFB6C1", "#FF7F7F", "#FFD580", "#FFFFE0", "#90EE90", "#ADD8E6", "#E0FFFF", "#E6E6FA", "#D3D3D3", "#F08080"]


def draw_flowchart(steps, figsize=(10, 7.0), preview_mode=False, title_font=None, desc_font=None, title_wrap=None, desc_wrap=None):
    """Draw a caterpillar-style flowchart"""
    try:
        fig, ax = plt.subplots(figsize=figsize, dpi=300)
        
        if preview_mode:
            fig.patch.set_facecolor('white')
            ax.set_facecolor('white')
        else:
            fig.patch.set_alpha(0.0)
            ax.set_alpha(0.0)
        
        num_steps = len(steps)
        circle_spacing = 1.5
        ax.set_xlim(-1, (num_steps - 1) * circle_spacing + 1)
        ax.set_ylim(-3.0, 3.0)
        ax.axis('off')

        # Draw the main timeline
        ax.plot([-0.5, (num_steps - 1) * circle_spacing + 0.5], [0, 0], 
                color="#cccccc", lw=3, zorder=1)

        # Apply text settings
        steps_with_settings = apply_text_settings(
            [{'title': title, 'text': desc} for title, desc in steps],
            title_font, desc_font, title_wrap, desc_wrap
        )

        for i, step_data in enumerate(steps_with_settings):
            x = i * circle_spacing
            color = STEP_COLORS[i % len(STEP_COLORS)]
            step_number = f"{i+1:02d}"

            # Draw circle and its shadow
            ax.add_patch(Circle((x + 0.08, -0.08), 0.43, color='#000000', alpha=0.2, zorder=1))
            ax.add_patch(Circle((x, 0), 0.43, color='white', zorder=2, edgecolor='none'))
            ax.add_patch(Circle((x, 0), 0.4, color=color, zorder=3, edgecolor='none'))
            
            # Add step number text
            ax.text(x, 0, step_number, ha='center', va='center', 
                    color='white', fontsize=15, weight='bold', zorder=4)

            # Get wrapped text from processed steps
            wrapped_title = step_data['wrapped_title']
            
            box_height = 0.4
            box_width = 1.4
            box_x = x - box_width / 2
            
            # Define padding for description
            description_padding = 0.2
            
            if i % 2 == 0:
                # Even steps: title above, description above title
                line_y = 0.2
                title_y_center = 1.2
                desc_y = title_y_center + box_height/2 + description_padding
                va_desc = 'bottom'
            else:
                # Odd steps: title below, description below title
                line_y = -0.4
                title_y_center = -1.2
                desc_y = title_y_center - box_height/2 - description_padding
                va_desc = 'top'

            # Draw connecting line
            ax.plot([x, x], [0, line_y], color="#999999", lw=1.5, zorder=2)

            box_y = title_y_center - box_height / 2
            
            # Draw title box and its shadow
            ax.add_patch(FancyBboxPatch(
                (box_x + 0.08, box_y - 0.08), box_width, box_height,
                boxstyle="round,pad=0.1,rounding_size=0.15", 
                facecolor='#000000', alpha=0.2, lw=0, zorder=2
            ))
            ax.add_patch(FancyBboxPatch(
                (box_x, box_y), box_width, box_height,
                boxstyle="round,pad=0.1,rounding_size=0.15", 
                facecolor=color, edgecolor='#ffffff', lw=1.5, zorder=3
            ))
            
            # Add title text with font properties
            ax.text(x, title_y_center, wrapped_title, ha='center', va='center', 
                    fontproperties=step_data['title_font'],
                    color='white', zorder=4, wrap=True)
            
            # Add description text
            if step_data['wrapped_text']:
                wrapped_desc = step_data['wrapped_text']
                ax.text(x, desc_y, wrapped_desc, ha='center', va=va_desc, 
                        fontproperties=step_data['desc_font'],
                        color='#555555', zorder=3, wrap=True)

        plt.tight_layout()
        return fig
    except Exception as e:
        print(f"Error in caterpillar draw_flowchart: {e}")
        # Return a simple figure in case of error
        fig, ax = plt.subplots(figsize=(10, 7.0))
        ax.text(0.5, 0.5, f"Error in caterpillar layout: {e}", ha='center', va='center', transform=ax.transAxes)
        return fig

def apply_blur_effect(fig, blur_radius=6, preview_mode=False):
    """Apply blur effect to the figure"""
    try:
        buf = io.BytesIO()
        save_kwargs = {
            'format': 'png',
            'bbox_inches': 'tight',
            'dpi': 300,
            'pad_inches': 0.1
        }
        
        if preview_mode:
            save_kwargs['facecolor'] = 'white'
        else:
            save_kwargs['transparent'] = True
            
        fig.savefig(buf, **save_kwargs)
        buf.seek(0)
        base = Image.open(buf).convert("RGBA")
        plt.close(fig)

        # Create shadow effect
        shadow = Image.new("RGBA", base.size, (0, 0, 0, 0))
        blurred = Image.new("RGBA", base.size, (0, 0, 0, 120))
        shadow.paste(blurred, mask=base.split()[3])
        shadow_blurred = shadow.filter(ImageFilter.GaussianBlur(radius=blur_radius))

        # Composite images
        final = Image.alpha_composite(shadow_blurred, base)
        return final
    except Exception as e:
        print(f"Error in caterpillar apply_blur_effect: {e}")
        # Return the original figure as bytes
        try:
            buf = io.BytesIO()
            fig.savefig(buf, format='png', bbox_inches='tight', facecolor='white')
            buf.seek(0)
            plt.close(fig)
            return Image.open(buf).convert("RGBA")
        except:
            # Final fallback
            img = Image.new('RGB', (800, 600), color='white')
            return img

# Alias for compatibility with milestone layout
apply_blur_shadow = apply_blur_effect

def test_caterpillar():
    """Test function to verify caterpillar layout works"""
    try:
        sample_steps = [
            ("Step One", "First step description with some longer text to test wrapping"),
            ("Step Two", "Second step description"), 
            ("Step Three", "Third step description with more details"),
            ("Step Four", "Fourth step description")
        ]
        
        fig = draw_flowchart(sample_steps, preview_mode=True)
        final_img = apply_blur_effect(fig, preview_mode=True)
        final_img.save("test_caterpillar.png")
        print("✅ Caterpillar test completed - check test_caterpillar.png")
        return True
    except Exception as e:
        print(f"❌ Caterpillar test failed: {e}")
        return False

if __name__ == "__main__":
    test_caterpillar()