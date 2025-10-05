from typing import Callable, Optional
from PIL import Image
import customtkinter as CTk
from .theme import CTkSidebarTheme

class CTkSidebarItemConfig:
    def __init__(self, id : Optional[int|str]=None, text: str="", command: callable=None, icon: Optional[Image.Image|tuple[CTk.CTkImage, CTk.CTkImage]]=None, submenu: Optional["CTkSidebarConfig"]=None, submenu_expanded: bool=True, icon_size : tuple[int, int]=(20,20), text_x: Optional[int]=None, icon_x: Optional[int]=None):
        self.id : Optional[int|str] = id
        self.text : Optional[str] = text
        self.command : Optional[Callable[[int|str], None]] = command
        self.icon : Optional[Image.Image|tuple[CTk.CTkImage, CTk.CTkImage]] = icon
        self.submenu : Optional["CTkSidebarConfig"] = submenu
        self.submenu_expanded : bool = submenu_expanded
        self.icon_size : tuple[int, int] = icon_size
        self.text_x : Optional[int] = text_x
        self.icon_x : Optional[int] = icon_x

class CTkSidebarSeparatorConfig:
    def __init__(self, width: Optional[int]=None, height: Optional[int]=None, line_color: Optional[str|list[str]]=None, line_thickness: Optional[int]=None, rounded_line_end: Optional[bool]=None):
        self.height : Optional[int] = height
        self.width : Optional[int] = width
        self.line_color : Optional[str|list[str]] = line_color
        self.line_thickness : Optional[int] = line_thickness
        self.rounded_line_end : bool = rounded_line_end

class CTkSidebarConfig:
    def __init__(self, 
                 items: Optional[list[CTkSidebarItemConfig|CTkSidebarSeparatorConfig]]=None,
                 header_factory: Optional[callable]=None,
                 theme: Optional[CTkSidebarTheme]=None,
                 width: int=220
                ):
        self.items : list[CTkSidebarItemConfig|CTkSidebarSeparatorConfig] = items
        if self.items is None:
            self.items = []
        self.header_factory : Optional[Callable[[CTk.CTkFrame], CTk.CTkBaseClass]] = header_factory
        self.theme = theme
        self.width = width

    def add_item(self, id : Optional[int|str]=None, text: str="", command: callable=None, icon: Optional[Image.Image|tuple[CTk.CTkImage, CTk.CTkImage]]=None, submenu: Optional["CTkSidebarConfig"]=None, submenu_expanded: bool=True, icon_size : tuple[int, int]=(20,20), text_x : Optional[int]=None, icon_x : Optional[int]=None) -> CTkSidebarItemConfig:
        item = CTkSidebarItemConfig(id=id, text=text, command=command, icon=icon, submenu=submenu, submenu_expanded=submenu_expanded, icon_size=icon_size, text_x=text_x, icon_x=icon_x)
        self.items.append(item)
        return self # return self to allow chaining
    
    def add_separator(self, width: Optional[int]=None, height: Optional[int]=None, line_color: Optional[str|list[str]]=None, line_thickness: Optional[int]=None, rounded_line_end: Optional[bool]=None) -> CTkSidebarSeparatorConfig:
        separator = CTkSidebarSeparatorConfig(width=width, height=height, line_color=line_color, line_thickness=line_thickness, rounded_line_end=rounded_line_end)
        self.items.append(separator)
        return self # return self to allow chaining