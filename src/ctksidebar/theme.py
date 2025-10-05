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
                 label_indent: Optional[int]=None,
                 label_indent_increment: Optional[int]=None,
                 label_align_ref: Optional[Literal['text', 'icon']]=None,
                 icon_text_margin: Optional[int]=None,
                 separator_line_color: Optional[str|list[str]]=None,
                 separator_line_thickness: Optional[int]=None,
                 separator_height: Optional[int]=None,
                 separator_width: Optional[int]=None,
                 separator_rounded_line_end: Optional[bool]=None,
                 submenu_marker_thickness: Optional[str|list[str]]=None,
                 submenu_marker_padx: Optional[int]=None,
                 submenu_marker_pady: Optional[int]=None,
                ):
        """
        Theme configuration for CTkSidebar and CTkSidebarItem.
        Parameters:
            load_default: 'primary' for main sidebar items, 'secondary' for submenu items.
            bg_color: Background color of the sidebar.
            padx: Horizontal padding inside the sidebar frame.
            pady: Vertical padding inside the sidebar frame.
            submenu_pady: Vertical padding before and after submenu sections. If desired, you can specify a tuple for (top, bottom) padding.
            button_color: Background color of unselected sidebar buttons.
            button_color_hover: Background color when hovering over buttons.
            button_color_selected: Background color of the selected button.
            button_corner_radius: Corner radius of sidebar buttons.
            button_height: Height of sidebar buttons.
            text_color: Text color of unselected sidebar buttons.
            text_color_hover: Text color when hovering over buttons.
            text_color_selected: Text color of the selected button.
            label_indent: Base indentation for sidebar item labels.
            label_indent_increment: Additional indentation per submenu level.
            label_align_ref: Horizontally align labels by their text or icon.
            icon_text_margin: Margin between icon and text in sidebar items.
            separator_line_color: Color of separator lines.
            separator_line_thickness: Thickness of separator lines.
            separator_height: Total height of a separator item.
            separator_width: Width of the (centered) separator line.
            separator_rounded_line_end: Whether separator lines have rounded or 'butt' ends.
            submenu_marker_thickness: Thickness of the submenu expansion marker.
            submenu_marker_padx: Horizontal offset of the submenu marker with respect to the button's left edge.
            submenu_marker_pady: Vertical padding of the submenu marker with respect to the button's top and bottom edges.
        """
        # Load defaults
        default = CTk.ThemeManager.theme
        if load_default == 'primary':
            # Default theme for the 'primary' style (non-submenu items)
            self.bg_color = default["CTkFrame"]["fg_color"]
            self.padx = 10
            self.pady = (10,10)
            self.submenu_pady = (10,10)
            self.button_color = "transparent"
            self.button_color_hover = default["CTkFrame"]["top_fg_color"]
            self.button_color_selected = default["CTkButton"]["fg_color"]
            self.button_corner_radius = 5
            self.button_height = 36
            self.text_color = default["CTkLabel"]["text_color"]
            self.text_color_hover = default["CTkLabel"]["text_color"]
            self.text_color_selected = default["CTkButton"]["text_color"]
            self.label_indent = 50
            self.label_indent_increment = 0
            self.label_align_ref = 'text'
            self.icon_text_margin = 10
            self.separator_line_color = default["CTkEntry"]["border_color"]
            self.separator_line_thickness = 3
            self.separator_height = 15
            self.separator_width = 20
            self.separator_rounded_line_end = True
            self.submenu_marker_thickness = 3
            self.submenu_marker_padx = 5
            self.submenu_marker_pady = 5
        else:
            # Default theme for the 'secondary' style (submenu items)
            self.bg_color = default["CTkFrame"]["top_fg_color"]
            self.padx = 10
            self.pady = (8,8)
            self.submenu_pady = (2,2)
            self.button_color = "transparent"
            self.button_color_hover = ["gray84", "gray24"]
            self.button_color_selected = default["CTkButton"]["fg_color"]
            self.button_corner_radius = 5
            self.button_height = 32
            self.text_color = ["gray30", "gray70"]
            self.text_color_hover = ["gray30", "gray70"]
            self.text_color_selected = default["CTkButton"]["text_color"]
            self.label_indent = 30
            self.label_indent_increment = 20
            self.label_align_ref = 'text'
            self.icon_text_margin = 10
            self.separator_line_color = ["gray84", "gray24"]
            self.separator_line_thickness = 2
            self.separator_height = 10
            self.separator_width = 50
            self.separator_rounded_line_end = False
            self.submenu_marker_thickness = 2
            self.submenu_marker_padx = 8
            self.submenu_marker_pady = 6

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
        if label_indent is not None:
            self.label_indent = label_indent
        if icon_text_margin is not None:
            self.icon_text_margin = icon_text_margin
        if label_indent_increment is not None:
            self.label_indent_increment = label_indent_increment
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
        if label_align_ref is not None:
            self.label_align_ref = label_align_ref
        if submenu_marker_thickness is not None:
            self.submenu_marker_thickness = submenu_marker_thickness
        if submenu_marker_padx is not None:
            self.submenu_marker_padx = submenu_marker_padx
        if submenu_marker_pady is not None:
            self.submenu_marker_pady = submenu_marker_pady