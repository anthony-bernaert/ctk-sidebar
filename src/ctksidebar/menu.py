from typing import Callable, Optional
import customtkinter as CTk
import copy
from .util import resolve_padding
from .theme import CTkSidebarTheme
from .item import CTkSidebarItem, CTkSidebarSeparator
from PIL import Image

class CTkSidebar(CTk.CTkFrame):
    def __init__(self, master=None, width: int=220, theme: CTkSidebarTheme=None, indent_level: int=0, single_expanded_submenu: bool=False):
        self._change_commands : list[Callable[[Optional[str|int]], None]] = []
        self._add_item_commands : list[Callable[[Optional[str|int]], None]] = []
        self._visible = True
        self._is_submenu = False
        self._parent_sidebar_item = None
        self._parent_menu = None
        self._children : list[CTk.CTkBaseClass] = []
        self._indent_level = indent_level
        self._width : int|None = width
        self._single_expanded_submenu = single_expanded_submenu
        self.selected_item : Optional[CTkSidebarItem] = None
        self._content = self
        if theme:
            self._theme = copy.copy(theme)
        else: # Use default theme if none is provided
            self._theme = CTkSidebarTheme(load_default='primary')
        self._theme.label_indent += self._indent_level * self._theme.label_indent_increment
        super().__init__(master, width=width, corner_radius=0, fg_color=self._theme.bg_color)

    def _set_parent(self, parent_menu: "CTkSidebar", parent_item: CTkSidebarItem):
        self._is_submenu = True
        self._parent_menu = parent_menu
        self._parent_sidebar_item = parent_item
    
    def add_frame(self, frame: CTk.CTkBaseClass, pady: Optional[int|tuple[int,int]]=None) -> None:
        self._children.append(frame)
        self._children[-1].grid(row=len(self._children)-1, column=0, sticky="ew", padx=self._theme.padx, pady=pady if pady is not None else 0)

    def add_item(self,
                 id : Optional[int|str]=None,
                 text: str="",
                 command: Optional[Callable[[int|str], None]]=None,
                 icon: Optional[Image.Image|tuple[CTk.CTkImage, CTk.CTkImage]]=None,
                 icon_size : tuple[int, int]=(20,20),
                 override_text_x: Optional[int]=None,
                 override_icon_x: Optional[int]=None
                ) -> None:
        if len(self._children) == 0 and not self._is_submenu and (pady := resolve_padding(self._theme.pady, 0)) > 0:
            self.add_spacing(pady) # Add initial top padding

        ctk_item = CTkSidebarItem(self,
                                  theme=self._theme,
                                  id=id,
                                  text=text,
                                  width=self._width,
                                  icon=icon,
                                  icon_size=icon_size,
                                  has_submenu=False,
                                  submenu_expanded=False,
                                  override_text_x=override_text_x,
                                  override_icon_x=override_icon_x
                                 )
        self._children.append(ctk_item)
        self._children[-1].grid(row=len(self._children)-1, column=0, sticky="ew", padx=self._theme.padx, pady=0)

        ctk_item.bind_click(lambda _=None, id=id: self._on_click(id))
        ctk_item.bind_click(lambda _=None, item=ctk_item: self._select_item(item))
        if command:
            ctk_item.bind_click(lambda _=None, cmd=command, id=id: cmd(id))
        self._on_add_item(id)

    def add_submenu(self, 
                    id : Optional[int|str]=None,
                    text: str="",
                    command: Optional[Callable[[int|str], None]]=None,
                    icon: Optional[Image.Image|tuple[CTk.CTkImage, CTk.CTkImage]]=None,
                    icon_size : tuple[int, int]=(20,20),
                    override_text_x: Optional[int]=None,
                    override_icon_x: Optional[int]=None,
                    indent_level: Optional[int]=None,
                    theme: Optional[CTkSidebarTheme]=None,
                    expanded: bool=True,
                   ) -> "CTkSidebar":
        if len(self._children) == 0 and not self._is_submenu and (pady := resolve_padding(self._theme.pady, 0)) > 0:
            self.add_spacing(pady)

        # Create an item on the current indentation level, with a dropdown
        ctk_item = CTkSidebarItem(self,
                                  theme=self._theme,
                                  id=id,
                                  text=text,
                                  width=self._width,
                                  icon=icon,
                                  icon_size=icon_size,
                                  has_submenu=True,
                                  submenu_expanded=True,
                                  override_text_x=override_text_x,
                                  override_icon_x=override_icon_x
                                 )
        self._children.append(ctk_item)
        self._children[-1].grid(row=len(self._children)-1, column=0, sticky="ew", padx=self._theme.padx, pady=0)

        # Create a new submenu with increased indentation level
        submenu_theme = theme if theme else CTkSidebarTheme(load_default='secondary')
        wrapper = CTkSidebarSubmenu(self, width=self._width, theme=submenu_theme, indent_level=(self._indent_level + 1 if indent_level is None else indent_level))
        submenu = wrapper.sidebar
        submenu._set_parent(self, ctk_item)
        self._children.append(wrapper)
        self._children[-1].grid(row=len(self._children)-1, column=0, sticky="ew", padx=0, pady=self._theme.submenu_pady)
        ctk_item.bind_click(lambda _=None, item=ctk_item, wrapper=wrapper: self._toggle_submenu(item, wrapper))
        ctk_item.bind_select(lambda _=None, item=ctk_item: self._select_item(item))
        ctk_item.bind_deselect(lambda _=None, submenu=submenu: submenu._deselect())
        if command:
            ctk_item.bind_click(lambda _=None, cmd=command, id=id: cmd(id))
        if not expanded:
            wrapper.hide()
            ctk_item.collapse()
        self._on_add_item(id)
        return submenu
    
    def add_separator(self,
                      width: Optional[int]=None,
                      height: Optional[int]=None,
                      line_color: Optional[str|list[str]]=None,
                      line_thickness: Optional[int]=None,
                      rounded_line_end: Optional[bool]=None,
                     ) -> None:
        separator = CTkSidebarSeparator(master=self, width=self._width,
                                        bg_color=self._theme.bg_color,
                                        height=height if height is not None else self._theme.separator_height,
                                        line_length=width if width is not None else self._theme.separator_width,
                                        line_color=line_color if line_color is not None else self._theme.separator_line_color,
                                        line_thickness=line_thickness if line_thickness is not None else self._theme.separator_line_thickness,
                                        rounded_line_end=rounded_line_end if rounded_line_end is not None else self._theme.separator_rounded_line_end
                                       )
        self._children.append(separator)
        self._children[-1].grid(row=len(self._children)-1, column=0, sticky="ew", padx=0, pady=0)

    def add_spacing(self, height: int) -> None:
        self.add_separator(height=height, line_thickness=-1)

    def _select_item(self, item : CTkSidebarItem):
        if self.selected_item and self.selected_item != item:
            self.selected_item.deselect()
        item.select(False)
        self.selected_item = item
        if self._parent_sidebar_item:
            self._parent_sidebar_item.select()

    def _deselect(self):
        if self.selected_item:
            self.selected_item.deselect()
        self.selected_item = None

    def get_item(self, id: int|str) -> Optional[CTkSidebarItem]:
        for child in self._children:
            if isinstance(child, CTkSidebarItem):
                if child.id == id:
                    return child
            elif isinstance(child, CTkSidebar):
                if sub_item := child.get_item(id):
                    return sub_item
        return None

    def bind_change(self, command: Callable[[Optional[str|int]], None], overwrite: bool=False):
        if overwrite:
            self._change_commands = [command]
        else:
            self._change_commands.append(command)

    def bind_add_item(self, command: Callable[[Optional[str|int]], None], overwrite: bool=False):
        if overwrite:
            self._add_item_commands = [command]
        else:
            self._add_item_commands.append(command)

    def _toggle_submenu(self, item : CTkSidebarItem, submenu : "CTkSidebarSubmenu"):
        if item.submenu_expanded:
            item.collapse()
            submenu.hide()
        else:
            item.expand()
            submenu.show()
            if self._single_expanded_submenu:
                # Collapse any other expanded submenu
                for child in self._children:
                    if isinstance(child, CTkSidebarSubmenu) and child != submenu and child._visible:
                        child.hide()
                        child.sidebar._parent_sidebar_item.collapse()
        self._draw()

    def _on_add_item(self, id: Optional[str|int]=None):
        if self._parent_menu:
            self._parent_menu._on_add_item(id)
        for callback in self._add_item_commands:
            callback(id)

    def _draw(self, no_color_updates=False):
        super()._draw(no_color_updates)

    def _on_click(self, id: Optional[str|int]=None):
        if self._parent_menu:
            self._parent_menu._on_click(id)
        else:
            for cmd in self._change_commands:
                cmd(id)

class CTkSidebarSubmenu(CTk.CTkFrame):
    def __init__(self, master=None, width: int=220, theme: CTkSidebarTheme=None, indent_level: int=0, single_expanded_submenu: bool=False):
        super().__init__(master, width=width, corner_radius=0, fg_color=theme.bg_color)
        self.sidebar = CTkSidebar(master=self, width=width, theme=theme, indent_level=indent_level, single_expanded_submenu=single_expanded_submenu)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=0, pady=theme.pady)
        self._visible = True
    
    def _set_scaling(self, *args, **kwargs):
        super()._set_scaling(*args, **kwargs)
        if not self._visible:
            self.grid_remove()

    def hide(self):
        if self._visible:
            self.grid_remove()
            self._visible = False

    def show(self):
        if not self._visible:
            self.grid()
            self._visible = True