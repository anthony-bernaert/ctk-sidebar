import tkinter
import customtkinter
from ctksidebar import CTkSidebar, CTkSidebarConfig, CTkSidebarItemConfig, CTkSidebarTheme, CTkSidebarSeparatorConfig, CTkSidebarNavView
from PIL import Image

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("red-theme.json")  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.geometry("800x480")
app.grid_columnconfigure(1, weight=1)

def button_function():
    print("button pressed")

home_icon = Image.open("assets/home.png")
settings_icon = Image.open("assets/settings.png")
info_icon = Image.open("assets/info.png")

# Create sidebar navigation
def sidebar_header(master):
    return customtkinter.CTkLabel(master, text="My App", font=customtkinter.CTkFont(size=20, weight="bold"), fg_color="transparent", anchor="center", height=50)

sub_submenu = CTkSidebarConfig()
sub_submenu.add_item(id="more/1/1", text="Sub-subitem 1", command=lambda _: print("Sub-subitem 1 clicked"), icon=home_icon)
sub_submenu.add_item(id="more/1/2", text="Sub-subitem 2", command=lambda _: print("Sub-subitem 2 clicked"), icon=settings_icon)

more_submenu = CTkSidebarConfig()
more_submenu.add_item(id="more/1", text="Subitem 1", command=lambda _: print("Subitem 1 clicked"), icon=home_icon, submenu_expanded=False, submenu=sub_submenu)
more_submenu.add_item(id="more/2", text="Subitem 2", command=lambda _: print("Subitem 2 clicked"), icon=settings_icon)
more_submenu.add_item(id="more/3", text="Subitem 3", command=lambda _: print("Subitem 3 clicked"), icon=info_icon)

sidebar_config = CTkSidebarConfig(width=220, header_factory=sidebar_header)
sidebar_config.add_separator()
sidebar_config.add_separator(height=10, line_thickness=0)
sidebar_config.add_item(id="home", text="Home", command=lambda _: print("Home clicked"), icon=home_icon)
sidebar_config.add_item(id="settings", text="Settings", command=lambda _: print("Settings clicked"), icon=settings_icon)
sidebar_config.add_item(id="more", text="More", submenu=more_submenu)
sidebar_config.add_item(id="about", text="About", command=lambda _: print("About clicked"), icon=info_icon)
sidebar_config.theme = CTkSidebarTheme(pady=(10,0))

app.grid_rowconfigure(0, weight=1)

sidebar_nav = CTkSidebarNavView(master=app, config=sidebar_config)
sidebar_nav.pack(fill="both", expand=True)

home_view = customtkinter.CTkLabel(sidebar_nav.view("home"), text="Home View", font=customtkinter.CTkFont(size=20, weight="bold"), fg_color="transparent")
home_view.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
settings_view = customtkinter.CTkLabel(sidebar_nav.view("settings"), text="Settings View", font=customtkinter.CTkFont(size=20, weight="bold"), fg_color="transparent")
settings_view.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
about_view = customtkinter.CTkLabel(sidebar_nav.view("about"), text="About View", font=customtkinter.CTkFont(size=20, weight="bold"), fg_color="transparent")
about_view.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

sidebar_nav.set("more/1/2")

#sidebar = CTkSidebar(master=app, config= sidebar_config,)
#sidebar.grid(row=0, column=0, sticky="nsw")


## Create main frame for controls
#main_frame = customtkinter.CTkFrame(master=app, fg_color="transparent")
#main_frame.grid(row=0, column=1, rowspan=2, padx=20, pady=20, sticky="nsew")
#
## Configure main frame's grid
#main_frame.grid_columnconfigure(0, weight=1)
#main_frame.grid_columnconfigure(1, weight=1)
#main_frame.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
#
## Add a title label
#title_label = customtkinter.CTkLabel(main_frame, text="CustomTkinter Demo", font=(None, 24), anchor="w")
#title_label.grid(row=0, column=0, columnspan=2, padx=10, pady=0, sticky="w")
#
## Add a button
#demo_button = customtkinter.CTkButton(main_frame, text="Demo Button", command=button_function)
#demo_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
#
## Add an entry field with label
#entry_label = customtkinter.CTkLabel(main_frame, text="Input:")
#entry_label.grid(row=1, column=1, padx=10, pady=10, sticky="w")
#entry = customtkinter.CTkEntry(main_frame, placeholder_text="Type something here")
#entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
#
## Add a checkbox
#checkbox = customtkinter.CTkCheckBox(main_frame, text="CheckBox")
#checkbox.grid(row=2, column=0, padx=10, pady=10, sticky="w")
#
## Add a switch
#switch = customtkinter.CTkSwitch(main_frame, text="Switch")
#switch.grid(row=3, column=0, padx=10, pady=10, sticky="w")
#
## Add a slider
#slider = customtkinter.CTkSlider(main_frame)
#slider.grid(row=3, column=1, padx=10, pady=10, sticky="ew")
#slider.set(0.5)
#
## Add a combobox
#combobox = customtkinter.CTkComboBox(main_frame, values=["Option 1", "Option 2", "Option 3"])
#combobox.grid(row=4, column=0, padx=10, pady=10, sticky="ew")
#combobox.set("Select an option")
#
## Add a text box
#textbox = customtkinter.CTkTextbox(main_frame)
#textbox.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
#textbox.insert("0.0", "This is a customtkinter textbox widget.\n\nYou can write multiple lines of text here.")
#
## Add appearance mode selector
#appearance_mode_label = customtkinter.CTkLabel(main_frame, text="Appearance Mode:")
#appearance_mode_label.grid(row=6, column=0, padx=10, pady=10, sticky="w")
#appearance_mode_menu = customtkinter.CTkOptionMenu(main_frame, values=["System", "Light", "Dark"],
#                                                  command=lambda x: customtkinter.set_appearance_mode(x.lower()))
#appearance_mode_menu.grid(row=6, column=1, padx=10, pady=10, sticky="w")
#appearance_mode_menu.set("System")

app.mainloop()