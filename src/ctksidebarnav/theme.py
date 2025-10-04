from typing import Literal, Optional
import customtkinter as CTk

class CTkSidebarTheme:
    def __init__(self,
                 load_default: Literal['primary', 'secondary']='primary',
                 bg_color: Optional[str]=None,
                 padx: Optional[int]=None,
                 pady: Optional[int|tuple[int,int]]=None,
                 submenu_pady: Optional[int|tuple[int,int]]=None,
                 button_color: Optional[str|list[str]]=None,
                 button_color_hover: Optional[str|list[str]]=None,
                 button_color_selected: Optional[str|list[str]]=None,
                 button_corner_radius: Optional[int]=None,
                 button_height: Optional[int]=None,
                 text_color: Optional[str|list[str]]=None,
                 text_color_hover: Optional[str|list[str]]=None,
                 text_color_selected: Optional[str|list[str]]=None,
                 text_indent: Optional[int]=None,
                 text_indent_increment: Optional[int]=None,
                 icon_text_margin: Optional[int]=None,
                 separator_line_color: Optional[str|list[str]]=None,
                 separator_line_thickness: Optional[int]=None,
                 separator_height: Optional[int]=None,
                 separator_width: Optional[int]=None,
                 separator_rounded_line_end: Optional[bool]=None,
                ):
        # Load defaults
        default = CTk.ThemeManager.theme
        if load_default == 'primary':
            # Default theme for the 'primary' style (non-submenu items)
            self.bg_color = default["CTkFrame"]["fg_color"]
            self.padx = 10
            self.pady = (10,10)
            self.submenu_pady = (5,5)
            self.button_color = "transparent"
            self.button_color_hover = default["CTkFrame"]["top_fg_color"]
            self.button_color_selected = default["CTkButton"]["fg_color"]
            self.button_corner_radius = 5
            self.button_height = 36
            self.text_color = default["CTkLabel"]["text_color"]
            self.text_color_hover = default["CTkLabel"]["text_color"]
            self.text_color_selected = default["CTkButton"]["text_color"]
            self.text_indent = 15
            self.text_indent_increment = 0
            self.icon_text_margin = 10
            self.separator_line_color = default["CTkFrame"]["top_fg_color"]
            self.separator_line_thickness = 2
            self.separator_height = 10
            self.separator_width = 50
            self.separator_rounded_line_end = False
        else:
            # Default theme for the 'secondary' style (submenu items)
            self.bg_color = default["CTkFrame"]["top_fg_color"]
            self.padx = 10
            self.pady = (8,8)
            self.submenu_pady = (5,5)
            self.button_color = "transparent"
            self.button_color_hover = ["gray84", "gray24"]
            self.button_color_selected = default["CTkButton"]["fg_color"]
            self.button_corner_radius = 0
            self.button_height = 32
            self.text_color = ["gray30", "gray70"]
            self.text_color_hover = ["gray30", "gray70"]
            self.text_color_selected = default["CTkButton"]["text_color"]
            self.text_indent = 15
            self.text_indent_increment = 15
            self.icon_text_margin = 10
            self.separator_line_color = ["gray84", "gray24"]
            self.separator_line_thickness = 2
            self.separator_height = 10
            self.separator_width = 50
            self.separator_rounded_line_end = False

        # Then override defaults with provided values
        if bg_color is not None:
            self.bg_color = bg_color
        if padx is not None:
            self.padx = padx
        if pady is not None:
            self.pady = pady
        if submenu_pady is not None:
            self.submenu_pady = submenu_pady
        if button_color is not None:
            self.button_color = button_color
        if button_color_hover is not None:
            self.button_color_hover = button_color_hover
        if button_color_selected is not None:
            self.button_color_selected = button_color_selected
        if button_corner_radius is not None:
            self.button_corner_radius = button_corner_radius
        if button_height is not None:
            self.button_height = button_height
        if text_color is not None:
            self.text_color = text_color
        if text_color_hover is not None:
            self.text_color_hover = text_color_hover
        if text_color_selected is not None:
            self.text_color_selected = text_color_selected
        if text_indent is not None:
            self.text_indent = text_indent
        if icon_text_margin is not None:
            self.icon_text_margin = icon_text_margin
        if text_indent_increment is not None:
            self.text_indent_increment = text_indent_increment
        if separator_line_color is not None:
            self.separator_line_color = separator_line_color
        if separator_line_thickness is not None:
            self.separator_line_thickness = separator_line_thickness
        if separator_height is not None:
            self.separator_height = separator_height
        if separator_width is not None:
            self.separator_width = separator_width
        if separator_rounded_line_end is not None:
            self.separator_rounded_line_end = separator_rounded_line_end