from typing import Optional
import customtkinter as CTk
import copy
from .config import CTkSidebarConfig, CTkSidebarItemConfig, CTkSidebarSeparatorConfig
from .theme import CTkSidebarTheme
from .item import CTkSidebarItem, CTkSidebarSeparator
from PIL import Image
from .util import resolve_padding

class CTkSidebarNav(CTk.CTkFrame):
    def __init__(self, master=None, config: CTkSidebarConfig=None, parent_sidebar_item: Optional[CTkSidebarItem]=None, indent_level: int=0):
        if config is None:
            raise ValueError("CTkSidebarNav requires a CTkSidebarConfig object")
        self.sidebar_config : CTkSidebarConfig = config
        self._is_submenu = parent_sidebar_item is not None
        self._parent_sidebar_item = parent_sidebar_item
        self._children : list[CTk.CTkBaseClass] = []
        self._indent_level = indent_level
        self._width : int|None = None
        self.selected_item : Optional[CTkSidebarItem] = None
        super().__init__(master)
        self._load_config(self.sidebar_config)

    def _load_config(self, config : CTkSidebarConfig):
        if config.theme:
            self._theme = copy.copy(config.theme)
        else: # Use default theme if none is provided
            self._theme = CTkSidebarTheme(load_default='primary' if not self._is_submenu else 'secondary')
        self._theme.text_indent += self._indent_level * self._theme.text_indent_increment
        if config.width:
            self._width = config.width
        else: # Use default width if none is provided
            self._width = 220
        if config.header_factory:
            # If a header factory is provided, call it to create the header widget
            header_widget = config.header_factory(self)
            if isinstance(header_widget, CTk.CTkBaseClass):
                self._children.append(header_widget)
                header_widget.grid(row=len(self._children)-1, column=0, sticky="ew")
        if config.items:
            pady_top, pady_bottom = resolve_padding(self._theme.pady, 0), resolve_padding(self._theme.pady, 1)
            if pady_top > 0:
                self._add_spacing(height=pady_top)
            for item in config.items:
                if isinstance(item, CTkSidebarSeparatorConfig):
                    self._add_separator(item)
                elif isinstance(item, CTkSidebarItemConfig):
                    ctk_item = self._add_item(item)
                    if item.submenu:
                        submenu_frame, submenu = self._add_submenu(item.submenu, ctk_item)
                        ctk_item.bind_click(lambda _=None, item=ctk_item, subnav=submenu_frame: self.toggle_submenu(item, subnav))
                        ctk_item.bind_select(lambda _=None, item=ctk_item: self.select_item(item, self._parent_sidebar_item))
                        ctk_item.bind_deselect(lambda _=None, subnav=submenu: subnav.deselect())
                        if not item.submenu_expanded:
                            submenu_frame.grid_remove()
                    else:
                        ctk_item.bind_click(lambda _=None, item=ctk_item: self.select_item(item, self._parent_sidebar_item))
            if pady_bottom > 0:
                self._add_spacing(height=pady_bottom)

        # Configure the sidebar container frame
        self.configure(corner_radius=0,
                       fg_color=self._theme.bg_color,
                       width=self._width)

    def _add_item(self, item_config : CTkSidebarItemConfig) -> CTkSidebarItem:
        has_submenu = item_config.submenu is not None
        ctk_item = CTkSidebarItem(self,
                                  theme=self._theme,
                                  text=item_config.text,
                                  width=self._width,
                                  icon=item_config.icon,
                                  icon_size=item_config.icon_size,
                                  has_submenu=has_submenu,
                                  submenu_expanded=item_config.submenu_expanded
                                 )
        self._children.append(ctk_item)
        self._children[-1].grid(row=len(self._children)-1, column=0, sticky="ew", padx=self._theme.padx, pady=0)
        return ctk_item

    def _add_submenu(self, submenu_config : CTkSidebarConfig, parent_item : CTkSidebarItem) -> tuple[CTk.CTkFrame,"CTkSidebarNav"]:
        # Recursively add a CTkSidebarNav as a submenu
        submenu_config.width = self._width
        submenu_frame = CTk.CTkFrame(self, fg_color=self._theme.bg_color, corner_radius=0)
        margin_top = CTk.CTkFrame(submenu_frame, height=resolve_padding(self._theme.submenu_pady, 0), fg_color="transparent", corner_radius=0)
        margin_top.grid(row=0, column=0, sticky="ew")
        submenu_nav = CTkSidebarNav(submenu_frame, config=submenu_config, parent_sidebar_item=parent_item, indent_level=self._indent_level + 1)
        submenu_nav.grid(row=1, column=0, sticky="ew")
        margin_bottom = CTk.CTkFrame(submenu_frame, height=resolve_padding(self._theme.submenu_pady, 1), fg_color="transparent", corner_radius=0)
        margin_bottom.grid(row=2, column=0, sticky="ew")
        self._children.append(submenu_frame)
        self._children[-1].grid(row=len(self._children)-1, column=0, sticky="ew", padx=0, pady=0)
        return submenu_frame, submenu_nav
    
    def _add_separator(self, config: CTkSidebarSeparatorConfig) -> CTkSidebarSeparator:
        separator = CTkSidebarSeparator(master=self, width=self._width,
                                        bg_color=self._theme.bg_color,
                                        height=config.height if config.height is not None else self._theme.separator_height,
                                        line_length=config.width if config.width is not None else self._theme.separator_width,
                                        line_color=config.line_color if config.line_color is not None else self._theme.separator_line_color,
                                        line_thickness=config.line_thickness if config.line_thickness is not None else self._theme.separator_line_thickness,
                                        rounded_line_end=config.rounded_line_end if config.line_thickness is not None else self._theme.separator_rounded_line_end
                                       )
        self._children.append(separator)
        self._children[-1].grid(row=len(self._children)-1, column=0, sticky="ew", padx=0, pady=0)
        return separator
    
    def _add_spacing(self, height: int) -> CTkSidebarSeparator:
        return self._add_separator(CTkSidebarSeparatorConfig(height=height, line_thickness=-1))

    def select_item(self, item : CTkSidebarItem, parent_item : Optional[CTkSidebarItem]=None):
        if self.selected_item and self.selected_item != item:
            self.selected_item.deselect()
        item.select(False)
        self.selected_parent_item = parent_item
        self.selected_item = item
        if parent_item:
            parent_item.select()

    def deselect(self):
        if self.selected_item:
            self.selected_item.deselect()
        self.selected_item = None
        
    def toggle_submenu(self, item : CTkSidebarItem, submenu_frame : CTk.CTkFrame):
        if item.submenu_expanded:
            print("collapsing submenu")
            item.collapse()
            submenu_frame.grid_remove()
        else:
            print("expanding submenu")
            item.expand()
            submenu_frame.grid()

    def _draw(self, no_color_updates=False):
        super()._draw(no_color_updates)
        if self._children:
            for item in self._children:
                item._draw(no_color_updates)