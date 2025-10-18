import customtkinter
from ctksidebar import CTkSidebarNavigation
from PIL import Image
from util import create_dashboard_view, get_asset_path

# Set up a basic CustomTkinter window
customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green
app = customtkinter.CTk()
app.geometry("790x545")
app.title("CTkSidebar Example - Basic")

# Create a navigation container filling the window
nav = CTkSidebarNavigation(master=app) 
nav.pack(fill="both", expand=True)

# Get sidebar and add some items to it
side = nav.sidebar
header = customtkinter.CTkLabel(side, text="Basic Sidebar", font=customtkinter.CTkFont(size=20, weight="bold"), fg_color="transparent", anchor="center", height=70)
side.add_frame(header)
side.add_item(id="home", text="Dashboard", icon=Image.open(get_asset_path("home.png")))
side.add_item(id="orders", text="Orders", icon=Image.open(get_asset_path("cart.png")))
side.add_item(id="customers", text="Customers", icon=Image.open(get_asset_path("user.png")))
side.add_item(id="settings", text="Settings", icon=Image.open(get_asset_path("settings.png")))
side.add_item(id="about", text="About", icon=Image.open(get_asset_path("info.png")))

# Set the initial view
nav.set("home")

# Create the content views
# Dashboard
home_view = customtkinter.CTkFrame(nav.view("home"), fg_color="transparent")
home_view.pack(fill="both", expand=True, padx=20, pady=20)
create_dashboard_view(home_view)

# Orders
orders_view = customtkinter.CTkLabel(nav.view("orders"), text="Orders", font=customtkinter.CTkFont(size=20, weight="bold"), fg_color="transparent")
orders_view.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

# Customers
customers_view = customtkinter.CTkLabel(nav.view("customers"), text="Customers", font=customtkinter.CTkFont(size=20, weight="bold"), fg_color="transparent")
customers_view.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

# Settings
settings_view = customtkinter.CTkLabel(nav.view("settings"), text="Settings", font=customtkinter.CTkFont(size=20, weight="bold"), fg_color="transparent")
settings_view.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

app.mainloop()