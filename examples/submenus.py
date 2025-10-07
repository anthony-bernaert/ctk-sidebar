import customtkinter
from ctksidebar import CTkSidebarNavigation
from PIL import Image
from util import create_dashboard_view, create_orders_list_view, get_asset_path

# Setup a basic CustomTkinter window
customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green
app = customtkinter.CTk()
app.geometry("840x570")
app.title("CTkSidebar Example - Submenus")

# Create a navigation container filling the window
nav = CTkSidebarNavigation(master=app)
nav.pack(fill="both", expand=True)

# Get sidebar and add some items to it
side = nav.sidebar
header = customtkinter.CTkLabel(side, text="Submenus", font=customtkinter.CTkFont(size=20, weight="bold"), fg_color="transparent", anchor="center", height=70)

# A header
side.add_frame(header)

# A regular menu item
side.add_item(id="home", text="Dashboard", icon=Image.open(get_asset_path("home.png")))

# An item with submenu
orders_submenu = side.add_submenu(id="orders", text="Orders", icon=Image.open(get_asset_path("cart.png")))
orders_submenu.add_item(id="orders/list", text="List")
orders_submenu.add_item(id="orders/create", text="Create")
orders_submenu.add_item(id="orders/reports", text="Reports", icon=Image.open(get_asset_path("info.png")))

# Another regular menu item
side.add_item(id="customers", text="Customers", icon=Image.open(get_asset_path("user.png")))

# A submenu with a nested submenu
settings_submenu = side.add_submenu(id="settings", text="Settings", icon=Image.open(get_asset_path("settings.png")), expanded=False)
settings_submenu.add_item(id="settings/profile", text="Profile")
settings_submenu.add_item(id="settings/notifications", text="Notifications")

system_submenu = settings_submenu.add_submenu(id="settings/system", text="System")
system_submenu.add_item(id="settings/system/configuration", text="Configuration")
system_submenu.add_item(id="settings/system/logs", text="Logs")

# Set the initial view
nav.set("home")

# Create the content views
# Dashboard
home_view = customtkinter.CTkFrame(nav.view("home"), fg_color="transparent")
home_view.pack(fill="both", expand=True, padx=20, pady=20)
create_dashboard_view(home_view)

# Orders
orders_view = customtkinter.CTkFrame(nav.view("orders/list"), fg_color="transparent")
orders_view.pack(fill="both", expand=True, padx=20, pady=20)
create_orders_list_view(orders_view)

# Customers
customers_view = customtkinter.CTkLabel(nav.view("customers"), text="Customers", font=customtkinter.CTkFont(size=20, weight="bold"), fg_color="transparent")
customers_view.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

# Settings
settings_view = customtkinter.CTkLabel(nav.view("settings"), text="Settings", font=customtkinter.CTkFont(size=20, weight="bold"), fg_color="transparent")
settings_view.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

app.mainloop()