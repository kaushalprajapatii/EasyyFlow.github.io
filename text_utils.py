# text_utils.py

import textwrap
from matplotlib.font_manager import FontProperties

# --- TEXT WRAPPING AND FONT SIZE CONFIGURATION ---
def configure_text_properties(title_font=None, desc_font=None, title_wrap=None, desc_wrap=None):
    """
    Configure text properties for titles and descriptions.
    
    Args:
        title_font: FontProperties object for titles
        desc_font: FontProperties object for descriptions  
        title_wrap: Integer for title text wrapping (characters per line)
        desc_wrap: Integer for description text wrapping (characters per line)
    
    Returns:
        dict: Configuration dictionary with text properties
    """
    config = {
        'title_font': title_font,
        'desc_font': desc_font,
        'title_wrap': title_wrap or 25,  # Default 25 chars for titles
        'desc_wrap': desc_wrap or 30,    # Default 30 chars for descriptions
        'title_fontsize': getattr(title_font, 'get_size', lambda: 20)() if title_font else 20,
        'desc_fontsize': getattr(desc_font, 'get_size', lambda: 14)() if desc_font else 14
    }
    return config

def wrap_text(text, width):
    """
    Wrap text to specified width while preserving words.
    
    Args:
        text: String to wrap
        width: Maximum characters per line
    
    Returns:
        str: Wrapped text with newlines
    """
    if not text or not width:
        return text
    
    return '\n'.join(textwrap.wrap(text, width=width))

def process_step_text(step, config):
    """
    Process step text with wrapping and font configuration.
    
    Args:
        step: Step dictionary with 'title' and 'text' keys
        config: Configuration dictionary from configure_text_properties
    
    Returns:
        tuple: (wrapped_title, wrapped_description, font_properties)
    """
    # Apply text wrapping
    wrapped_title = wrap_text(step.get('title', ''), config['title_wrap'])
    wrapped_description = wrap_text(step.get('text', ''), config['desc_wrap'])
    
    # Handle step-specific font sizes if provided
    title_font = config['title_font']
    desc_font = config['desc_font']
    
    # If step has individual font sizes, create new FontProperties
    if 'title_fontsize' in step and title_font:
        title_font = FontProperties(
            fname=getattr(title_font, 'get_file', lambda: None)(),
            size=step['title_fontsize']
        )
    
    if 'desc_fontsize' in step and desc_font:
        desc_font = FontProperties(
            fname=getattr(desc_font, 'get_file', lambda: None)(),
            size=step['desc_fontsize']
        )
    
    return wrapped_title, wrapped_description, title_font, desc_font

def apply_text_settings(steps, title_font=None, desc_font=None, title_wrap=None, desc_wrap=None):
    """
    Apply text wrapping and font settings to all steps.
    
    Args:
        steps: List of step dictionaries
        title_font: FontProperties for titles
        desc_font: FontProperties for descriptions
        title_wrap: Title wrap width
        desc_wrap: Description wrap width
    
    Returns:
        list: Updated steps with wrapped text and font properties
    """
    config = configure_text_properties(title_font, desc_font, title_wrap, desc_wrap)
    
    for step in steps:
        # Apply wrapping and get processed text
        wrapped_title, wrapped_desc, step_title_font, step_desc_font = process_step_text(step, config)
        
        # Store processed data
        step['wrapped_title'] = wrapped_title
        step['wrapped_text'] = wrapped_desc
        step['title_font'] = step_title_font
        step['desc_font'] = step_desc_font
    
    return steps

def create_text_element(ax, x, y, text, font_properties, 
                       ha='center', va='center', color='black', 
                       bbox=None, wrap_width=None):
    """
    Create a text element with proper wrapping and styling.
    
    Args:
        ax: Matplotlib axes object
        x, y: Position coordinates
        text: Text content
        font_properties: FontProperties object
        ha: Horizontal alignment
        va: Vertical alignment  
        color: Text color
        bbox: Box properties for background
        wrap_width: Optional override for wrap width
    
    Returns:
        matplotlib.text.Text: Text object
    """
    # Apply wrapping if needed
    if wrap_width and text:
        text = wrap_text(text, wrap_width)
    
    # Create text element
    text_obj = ax.text(
        x, y, text,
        fontproperties=font_properties,
        ha=ha, va=va, color=color,
        bbox=bbox,
        wrap=True
    )
    
    return text_obj

def get_default_font_properties(font_path=None, size=12):
    """
    Get default font properties.
    
    Args:
        font_path: Path to font file
        size: Font size
    
    Returns:
        FontProperties: Configured font properties
    """
    if font_path:
        return FontProperties(fname=font_path, size=size)
    else:
        return FontProperties(size=size)