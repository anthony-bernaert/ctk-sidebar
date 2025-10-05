import customtkinter
from ctksidebar import CTkSidebarConfig, CTkSidebarNavView
from PIL import Image
from util import create_dashboard_view, get_asset_path

# Setup a basic CustomTkinter window
customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green
app = customtkinter.CTk()
app.geometry("840x570")
app.title("CTkSidebar Example - Basic")

# Define sidebar header
def sidebar_header(master):
    return customtkinter.CTkLabel(master, text="Basic Sidebar", font=customtkinter.CTkFont(size=20, weight="bold"), fg_color="transparent", anchor="center", height=50)

# Define sidebar items
sidebar_config = CTkSidebarConfig(width=220, header_factory=sidebar_header)
sidebar_config.add_item(id="home", text="Dashboard", icon=Image.open(get_asset_path("home.png")))
sidebar_config.add_item(id="orders", text="Orders", icon=Image.open(get_asset_path("cart.png")))
sidebar_config.add_item(id="customers", text="Customers", icon=Image.open(get_asset_path("user.png")))
sidebar_config.add_item(id="settings", text="Settings", icon=Image.open(get_asset_path("settings.png")))

# Create the sidebar view
sidebar_nav = CTkSidebarNavView(master=app, config=sidebar_config)
sidebar_nav.pack(fill="both", expand=True) # Fill the entire window

# Set the initial view
sidebar_nav.set("home")

# Create the content views

# Dashboard
home_view = customtkinter.CTkFrame(sidebar_nav.view("home"), fg_color="transparent")
home_view.pack(fill="both", expand=True, padx=20, pady=20)
create_dashboard_view(home_view)

# Orders
orders_view = customtkinter.CTkLabel(sidebar_nav.view("orders"), text="Orders", font=customtkinter.CTkFont(size=20, weight="bold"), fg_color="transparent")
orders_view.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

# Customers
customers_view = customtkinter.CTkLabel(sidebar_nav.view("customers"), text="Customers", font=customtkinter.CTkFont(size=20, weight="bold"), fg_color="transparent")
customers_view.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

# Settings
settings_view = customtkinter.CTkLabel(sidebar_nav.view("settings"), text="Settings", font=customtkinter.CTkFont(size=20, weight="bold"), fg_color="transparent")
settings_view.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

app.mainloop()