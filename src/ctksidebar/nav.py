import customtkinter as CTk
from typing import Any, Optional
from .menu import CTkSidebar
from .theme import CTkSidebarTheme

class CTkSidebarNavigation(CTk.CTkFrame):
    def __init__(self, master: Any, width: int=220, theme: CTkSidebarTheme=None, indent_level: int=0, single_expanded_submenu: bool=False):
        super().__init__(master, fg_color="transparent")
        self._tabs = {}
        self._current_id = None
        self.sidebar : Optional[CTkSidebar] = None
        self.set_sidebar(CTkSidebar(master=self, width=width, theme=theme, indent_level=indent_level, single_expanded_submenu=single_expanded_submenu))

    def set_sidebar(self, sidebar: CTkSidebar):
        if self.sidebar:
            self.sidebar.pack_forget()
        self.sidebar = sidebar
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.bind_change(self._on_change, overwrite=True)
        self.sidebar.bind_add_item(self._on_add_item, overwrite=True)

    def view(self, id: int|str) -> CTk.CTkFrame:
        """Returns the frame associated with the given ID."""
        item = self._tabs.get(id)
        if item:
            return item
        else:
            raise ValueError(f"Sidebar has no item ID '{id}'")
        
    def set(self, id: int|str):
        """Sets the current view to the frame associated with the given ID."""
        item = self.sidebar.get_item(id)
        if not item:
            raise ValueError(f"Sidebar has no item ID '{id}'")
        item._on_click(None)

    def _on_add_item(self, id: int|str) -> None:
        if id is None:
            raise ValueError(f"When using CTkSidebarNavigation, all items must have a non-empty ID. Item: '{item.text}'")
        if self._tabs.get(id):
            raise ValueError(f"Duplicate sidebar item ID: {id}. All item IDs within a CTkSidebarNavigation must be unique.")
        self._tabs[id] = CTk.CTkFrame(master=self, fg_color="transparent", corner_radius=0)
    
    def _on_change(self, id: Optional[int|str]):
        if id in self._tabs:
            # Remove previous tab if it exists
            if self._current_id and self._current_id in self._tabs:
                self._tabs[self._current_id].pack_forget()
            # Show new tab
            tab = self._tabs[id]
            tab.pack(side="left", fill="both", expand=True)
            tab.pack_propagate(False)
            self._current_id = id
