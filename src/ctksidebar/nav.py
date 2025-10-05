import customtkinter as CTk
from typing import Any, Optional
from .item import CTkSidebarItem
from .menu import CTkSidebar
from .config import CTkSidebarConfig, CTkSidebarItemConfig

class CTkSidebarNavView(CTk.CTkFrame):
    def __init__(self, master: Any, config : CTkSidebarConfig):
        super().__init__(master, fg_color="transparent")
        self._tabs = {}
        self._current_id = None
        self._sidebar = CTkSidebar(master=self, config=config)
        self._sidebar.pack(side="left", fill="y")
        self._sidebar.bind_change(self._on_change)
        self._config = config
        self._parse_config(config)

    def view(self, id: int|str) -> CTk.CTkFrame:
        """Returns the frame associated with the given ID."""
        item = self._tabs.get(id)
        if item:
            return item
        else:
            raise ValueError(f"Sidebar has no item ID '{id}'")
        
    def set(self, id: int|str):
        """Sets the current view to the frame associated with the given ID."""
        item = self._sidebar.get_item(id)
        if not item:
            raise ValueError(f"Sidebar has no item ID '{id}'")
        item._on_click(None)
        
    def _parse_config(self, config: CTkSidebarConfig):
        for item in config.items:
            if isinstance(item, CTkSidebarItemConfig):
                if item.id is None:
                    raise ValueError(f"When using CTkSidebarNavView, all items must have an ID. Item: '{item.text}'")
                if self._tabs.get(item.id):
                    raise ValueError(f"Duplicate sidebar item ID found: {item.id}. All item IDs must be unique.")
                self._tabs[item.id] = self._create_tab()
                if item.submenu:
                    self._parse_config(item.submenu)

    def _create_tab(self) -> CTk.CTkFrame:
        frame = CTk.CTkFrame(master=self, fg_color="transparent", corner_radius=0)
        return frame
    
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
