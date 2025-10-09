# Sidebar Control for CustomTkinter
This is a custom widget that adds a sidebar to your CustomTkinter app and handles navigation.

<img width="950" alt="CTkSidebar on macOS " src="https://github.com/user-attachments/assets/a5431186-93fa-410b-97e0-6a251ce0a7ce" />

<img width="950" alt="CTkSidebar on Windows" src="https://github.com/user-attachments/assets/9125a544-d606-4049-81b3-5d0c76ea9bd5" />

## Features
- Modern look
- Handles navigation: each menu item gets a separate view
- Easy to configure
- Customizable styles
- Supports submenus (tree structure)

## Installation
Get the latest version from PyPI:
```
pip install ctk-sidebar
```

## Getting started
Import required modules:
```python
import customtkinter
from ctksidebar import CTkSidebarNavigation
```

Instantiate a `CTkSidebarNavigation` component on your app's toplevel and get a reference to the sidebar:
```python
app = customtkinter.CTk()
app.geometry("640x480")

nav = CTkSidebarNavigation(master=app) 
nav.pack(fill="both", expand=True)
side = nav.sidebar
```

Add a header:
```python
header = customtkinter.CTkLabel(side, text="My App", font=customtkinter.CTkFont(size=20, weight="bold"), fg_color="transparent", anchor="center", height=70)
side.add_frame(header)
```

Add some menu items:
```python
side.add_item(id="home", text="Dashboard")
side.add_item(id="orders", text="Orders")
side.add_item(id="customers", text="Customers")
```

Populate the view of each menu item by using `nav.view(<your_id>)` as the master:
```python
home_view = customtkinter.CTkLabel(nav.view("home"), text="Home", font=customtkinter.CTkFont(size=20, weight="bold"), fg_color="transparent")
home_view.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

orders_view = customtkinter.CTkLabel(nav.view("orders"), text="Orders", font=customtkinter.CTkFont(size=20, weight="bold"), fg_color="transparent")
orders_view.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

customers_view = customtkinter.CTkLabel(nav.view("customers"), text="Customers", font=customtkinter.CTkFont(size=20, weight="bold"), fg_color="transparent")
customers_view.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
```

Finally, set the startup view and launch the application:
```python
nav.set("home")
app.mainloop()
```

# Documentation
See the [documentation](docs/DOCUMENTATION.md) page for a detailed description of this component.

See the [examples](examples/) folder for the demo applications shown in the screenshots above.
