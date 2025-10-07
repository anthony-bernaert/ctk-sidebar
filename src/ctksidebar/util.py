from typing import Literal
from PIL import Image
import customtkinter as CTk

def resolve_padding(padding: int|tuple[int, int], index: int) -> int:
    if isinstance(padding, int):
        return padding
    elif isinstance(padding, tuple) and len(padding) == 2:  
        return padding[0 if index == 0 else 1]
    else:
        raise ValueError("Padding must be an int or a tuple of two ints")

def colorize_image(master: CTk.CTkBaseClass, image: Image, color, appearance_mode : Literal['light', 'dark'] = 'light') -> Image:
    if isinstance(color, list):
        color = color[0] if appearance_mode == 'light' else color[1]
    # Create a colored version for normal state
    r, g, b = parse_tk_color(master, color)

    # Convert image to RGBA
    img_rgba = image.convert("RGBA")
    
    # Create normal state image
    normal_data = []
    for item in img_rgba.getdata():
        if item[3] > 0:  # If pixel is not fully transparent
            normal_data.append((r, g, b, item[3]))
        else:
            normal_data.append(item)
    
    colorized_image = Image.new("RGBA", img_rgba.size)
    colorized_image.putdata(normal_data)
    return colorized_image

def parse_tk_color(master: CTk.CTkBaseClass, color):
    # Tk Color to RGB tuple
    try:
        rgb = master.winfo_rgb(color)
        return (rgb[0] // 256, rgb[1] // 256, rgb[2] // 256)
    except Exception:
        pass

    # Handle hex colors
    if color.startswith("#") and len(color) == 7:
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)
        return (r, g, b)

    raise ValueError(f"Invalid color format: {color}")