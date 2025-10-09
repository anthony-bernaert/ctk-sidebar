from typing import Literal, Optional, Union
import customtkinter as CTk
import tkinter
from PIL import Image
import sys
from .theme import CTkSidebarTheme
from .util import resolve_padding, colorize_image, parse_tk_color

class CTkSidebarItem(CTk.CTkBaseClass):
    def __init__(self,
                 master,
                 theme : CTkSidebarTheme,
                 id: Optional[int|str]=None,
                 text : str="",
                 width=200,
                 icon : Optional[Image.Image|tuple[CTk.CTkImage, CTk.CTkImage]]=None,
                 icon_size=(20,20),
                 has_submenu : bool = False,
                 submenu_expanded : bool = True,
                 override_text_x : Optional[int]=None,
                 override_icon_x : Optional[int]=None,
                ):
        bg_color = theme.bg_color
        super().__init__(master=master,
                         bg_color=bg_color,
                         width=width - resolve_padding(theme.padx, 0) - resolve_padding(theme.padx, 1),
                         height=theme.button_height)
        self.id = id
        self._selected = False
        self._hover = False
        self._theme = theme
        self._image_selected = None
        self._image = None
        self._click_commands = []
        self._select_commands = []
        self._deselect_commands = []
        self.has_submenu = has_submenu
        self.submenu_expanded = submenu_expanded

        if sys.platform == "darwin":
            self.configure(cursor="pointinghand")
        elif sys.platform.startswith("win"):
            self.configure(cursor="hand2")

        # Create canvas for custom drawing
        self._canvas = CTk.CTkCanvas(master=self,
                                 highlightthickness=0,
                                 width=self._apply_widget_scaling(self._desired_width),
                                 height=self._apply_widget_scaling(self._desired_height))
        self._draw_engine = CTk.DrawEngine(self._canvas)
        self._canvas.pack(fill="x", expand=True)

        # Label text
        self._text_label = CTk.CTkLabel(self, text=text, text_color=theme.text_color, bg_color="transparent")
        text_x = self._get_text_x(icon_size if icon else None) if override_text_x is None else override_text_x
        self._text_label.place(x=text_x, anchor="w", rely=0.5)

        # Hover handlers
        self._text_label.bind("<Enter>", self._on_enter)
        self._text_label.bind("<Leave>", self._on_leave)
        self._canvas.bind("<Enter>", self._on_enter)
        self._canvas.bind("<Leave>", self._on_leave)

        # Label icon
        self._label_image = None
        if icon:
            if isinstance(icon, Image.Image):
                self.image = CTk.CTkImage(light_image=colorize_image(self, icon, theme.text_color, 'light'),
                                        dark_image=colorize_image(self, icon, theme.text_color, 'dark'),
                                        size=icon_size)
                self.image_selected = CTk.CTkImage(light_image=colorize_image(self, icon, theme.text_color_selected, 'light'),
                                                dark_image=colorize_image(self, icon, theme.text_color_selected, 'dark'),
                                                size=icon_size)
            else:
                if not isinstance(icon, tuple) or len(icon) != 2 or not all(isinstance(i, CTk.CTkImage) for i in icon):
                    raise ValueError("Icon must be a PIL Image or a tuple of two CTkImage instances (light, dark).")
                self.image = icon[0]
                self.image_selected = icon[1]
            self._label_image = CTk.CTkLabel(self, text='', image=self.image, bg_color="transparent")
            icon_x = self._get_icon_x(icon_size if icon else None) if override_icon_x is None else override_icon_x
            self._label_image.place(x=icon_x, anchor="w", rely=0.5)
            self._label_image.bind("<Enter>", self._on_enter)
            self._label_image.bind("<Leave>", self._on_leave)
        self._draw() # Initial draw

    def bind_click(self, command):
        self._canvas.bind("<Button-1>", self._on_click)
        self._text_label.bind("<Button-1>", self._on_click)
        if self._label_image:
            self._label_image.bind("<Button-1>", self._on_click)
        self._click_commands.append(command)

    def bind_select(self, command):
        self._select_commands.append(command)
    
    def bind_deselect(self, command):
        self._deselect_commands.append(command)

    def select(self, call_bindings=True):
        if not self._selected:
            if len(self._select_commands) > 0 and call_bindings:
                for cmd in self._select_commands:
                    cmd()
            self._selected = True
            self._draw()

    def deselect(self, call_bindings=True):
        if self._selected:
            if len(self._deselect_commands) > 0 and call_bindings:
                for cmd in self._deselect_commands:
                    cmd()
            self._selected = False
            self._draw()

    def expand(self):
        if not self.submenu_expanded:
            self.submenu_expanded = True
            self._draw()
    
    def collapse(self):
        if self.submenu_expanded:
            self.submenu_expanded = False
            self._draw()

    def _set_scaling(self, *args, **kwargs):
        super()._set_scaling(*args, **kwargs)
        self._canvas.configure(width=self._apply_widget_scaling(self._desired_width),
                               height=self._apply_widget_scaling(self._desired_height))
        self._draw(no_color_updates=True)

    def _get_icon_x(self, icon_size: Optional[tuple[int, int]]) -> int:
        if self._theme.label_align_ref == "icon":
            # All buttons use the same icon x position, i.e. the indent of the theme
            return self._theme.label_indent
        else:
            # The reference is the left position of the text
            return self._theme.label_indent - icon_size[0] - self._theme.icon_text_margin
        
    def _get_text_x(self, icon_size: Optional[tuple[int, int]]) -> int:
        if self._theme.label_align_ref == "icon":
            # All buttons use the same icon x position, i.e. the indent of the theme
            if icon_size is None:
                return self._theme.label_indent
            else:
                return self._theme.label_indent + icon_size[0] + self._theme.icon_text_margin
        else:
            # The reference is the left position of the text
            return self._theme.label_indent

    def _draw(self, no_color_updates=False, update_idletasks=True):
        super()._draw(no_color_updates)
        requires_recoloring = False
        if self.has_submenu: # Draw dropdown arrow if a submenu exists
            requires_recoloring = self._draw_dropdown_arrow(self._apply_widget_scaling(self._current_width - (self._current_height / 2)),
                                                                      self._apply_widget_scaling(self._current_height / 2),
                                                                      self._apply_widget_scaling(8), self.submenu_expanded)
            requires_recoloring |= self._draw_selected_submenu_marker()
        requires_recoloring |= self._draw_engine.draw_rounded_rect_with_border(self._apply_widget_scaling(self._current_width), self._apply_widget_scaling(self._current_height), self._apply_widget_scaling(self._theme.button_corner_radius), 0)

        if no_color_updates is False or requires_recoloring:
            # Select the colors depending on the item's state
            bg_color = self._apply_appearance_mode(self._theme.bg_color)
            button_color = self._resolve_fg_color(self._theme.button_color, self._theme.bg_color)
            text_color = self._resolve_fg_color(self._theme.text_color, button_color)
            if self._selected and not self.has_submenu:
                button_color = self._resolve_fg_color(self._theme.button_color_selected, self._theme.bg_color)
                text_color = self._resolve_fg_color(self._theme.text_color_selected, button_color)
            elif self._hover:
                button_color = self._resolve_fg_color(self._theme.button_color_hover, bg_color)
                text_color = self._resolve_fg_color(self._theme.text_color_hover, button_color)
            self._text_label.configure(bg_color=button_color, text_color=text_color)

            # Update elements of an item with a submenu
            if self.has_submenu:
                marker_color = self._resolve_fg_color(self._theme.button_color_selected if self._selected else button_color, button_color)
                self._canvas.itemconfig("submenu_marker", fill=marker_color)
                if self._selected:
                    text_color = self._resolve_fg_color(self._theme.button_color_selected, button_color)
                self._canvas.itemconfig("dropdown_arrow", fill=text_color)

            # Update canvas items that create the rounded button effect
            self._canvas.itemconfig("border_parts",
                        outline=button_color,
                        fill=button_color)
            self._canvas.itemconfig("inner_parts",
                        outline=button_color,
                        fill=button_color)
            
            # Select which colored label image
            if self._label_image:
                self._label_image.configure(image=self.image_selected if self._selected and not self.has_submenu else self.image, bg_color=button_color)
            self._canvas.configure(bg=bg_color)
        if update_idletasks:
            self._canvas.update_idletasks()

    def _on_click(self, event):
        for cmd in self._click_commands:
            cmd()
        return "break"

    def _on_enter(self, event):
        self._hover = True
        self._draw(update_idletasks=False)
    
    def _on_leave(self, event):
        self._hover = False
        self._draw(update_idletasks=False)
    
    def cget(self, attribute_name: str) -> any:
        if attribute_name == "fg_color":
            return self._theme.button_color_selected if self._selected else self._theme.button_color
        elif attribute_name == "text_color":
            return self._theme.text_color_selected if self._selected else self._theme.text_color
        else:
            return super().cget(attribute_name)
        
    def _draw_dropdown_arrow(self, x_position: Union[int, float], y_position: Union[int, float], size: Union[int, float], point_down : bool = True) -> bool:
        x_position, y_position, size = round(x_position), round(y_position), size
        requires_recoloring = False

        if not self._canvas.find_withtag("dropdown_arrow"):
            self._canvas.create_line(0, 0, 0, 0, tags="dropdown_arrow", width=size / 3, joinstyle=tkinter.ROUND, capstyle=tkinter.ROUND)
            self._canvas.tag_raise("dropdown_arrow")
            requires_recoloring = True

        if point_down:
            self._canvas.coords("dropdown_arrow",
                            x_position - (size / 2),
                            y_position - (size / 5),
                            x_position,
                            y_position + (size / 5),
                            x_position + (size / 2),
                            y_position - (size / 5))
        else:
            self._canvas.coords("dropdown_arrow",
                            x_position - (size / 2),
                            y_position + (size / 5),
                            x_position,
                            y_position - (size / 5),
                            x_position + (size / 2),
                            y_position + (size / 5))

        return requires_recoloring
    
    def _draw_selected_submenu_marker(self) -> bool:
        requires_recoloring = False
        if not self._canvas.find_withtag("submenu_marker"):
            self._canvas.create_line(0, 0, 0, 0, tags="submenu_marker", width=self._apply_widget_scaling(self._theme.submenu_marker_thickness))
            self._canvas.tag_raise("submenu_marker")
            requires_recoloring = True
        self._canvas.coords("submenu_marker",
                                   self._apply_widget_scaling(self._theme.submenu_marker_padx),
                                   self._apply_widget_scaling(self._theme.submenu_marker_pady),
                                   self._apply_widget_scaling(self._theme.submenu_marker_padx),
                                   self._apply_widget_scaling(self._current_height-self._theme.submenu_marker_pady))
        return requires_recoloring
    
    def _resolve_fg_color(self, fg_color : str|list, bg_color : str|list) -> str:
            resolved_fg = self._apply_appearance_mode(fg_color)
            resolved_bg = self._apply_appearance_mode(bg_color)
            if resolved_fg == "transparent":
                return resolved_bg
            return resolved_fg
    

class CTkSidebarSeparator(CTk.CTkBaseClass):
    def __init__(self,
                 master,
                 bg_color : str|list,
                 width : int,
                 height : int,
                 line_length : int,
                 line_color : str|list,
                 line_thickness : int,
                 rounded_line_end : bool = False
                ):
        super().__init__(master=master,
                         bg_color=bg_color,
                         width=width,
                         height=height)
        self._bg_color = bg_color
        self._line_color = line_color
        self._line_thickness = line_thickness
        self._line_length = line_length
        self._rounded_line_end = rounded_line_end
        self._canvas = None

        # Create canvas for custom drawing, if a line is specified
        self._canvas = CTk.CTkCanvas(master=self,
                                highlightthickness=0,
                                width=self._apply_widget_scaling(self._desired_width),
                                height=self._apply_widget_scaling(self._desired_height))
        self._canvas.pack(fill="x", expand=True)
        self._draw() # Initial draw

    def _draw(self, no_color_updates=False):
        super()._draw(no_color_updates)
        requires_recoloring = False
        if self._line_thickness > 0 and self._line_length > 0:
            self._draw_separator_line()
        if requires_recoloring or no_color_updates is False:
            line_color = self._apply_appearance_mode(self._line_color)
            self._canvas.itemconfig("separator",
                        fill=line_color)
            self._canvas.configure(bg=self._apply_appearance_mode(self._bg_color))
        self._canvas.update_idletasks()

    def _set_scaling(self, *args, **kwargs):
        super()._set_scaling(*args, **kwargs)
        self._canvas.configure(width=self._apply_widget_scaling(self._desired_width),
                               height=self._apply_widget_scaling(self._desired_height))
        self._draw(no_color_updates=True)

    def _draw_separator_line(self) -> bool:
        requires_recoloring = False
        if not self._canvas.find_withtag("separator"):
            self._canvas.create_line(0, 0, 0, 0, tags="separator", width=self._apply_widget_scaling(self._line_thickness), capstyle=tkinter.ROUND if self._rounded_line_end else tkinter.BUTT)
            self._canvas.tag_raise("separator")
            requires_recoloring = True
        self._canvas.coords("separator",
                                   self._apply_widget_scaling((self._current_width - self._line_length) / 2),
                                   self._apply_widget_scaling(self._current_height / 2),
                                   self._apply_widget_scaling((self._current_width + self._line_length) / 2),
                                   self._apply_widget_scaling(self._current_height / 2))
        return requires_recoloring