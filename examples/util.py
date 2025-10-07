from PIL import Image
import customtkinter
import os

def colorize_image(original_image, color):
    """Colorize a PIL image with the given color."""

    # Ensure image is in RGBA mode
    image = original_image.convert("RGBA")

    # Create a new image with the same size and a transparent background
    colored_image = Image.new("RGBA", image.size, (0, 0, 0, 0))

    # Get the data of the original image
    data = image.getdata()

    new_data = []
    for item in data:
        # Change all white (also shades of whites)
        # pixels to the given color
        if item[3] > 0:  # Only change non-transparent pixels
            new_data.append((color[0], color[1], color[2], item[3]))
        else:
            new_data.append(item)

    # Update the data of the new image
    colored_image.putdata(new_data)

    return colored_image

def create_colorized_icon(image_path, light_color, dark_color, size=(20, 20)) -> customtkinter.CTkImage:
    """Create a colorized CTkImage for light and dark modes."""
    original_image = Image.open(image_path)
    light_image = colorize_image(original_image, light_color)
    dark_image = colorize_image(original_image, dark_color)
    return customtkinter.CTkImage(light_image=light_image, dark_image=dark_image, size=size)

def get_asset_path(file_path: str) -> str:
    """Get the absolute path to an asset file."""
    return os.path.join(os.path.dirname(__file__), "assets", file_path)

def create_dashboard_view(master):
    # Row 0 - Title and Period Selection
    home_title_row = customtkinter.CTkFrame(master, fg_color="transparent")
    home_title_row.pack(anchor="nw", fill="x")
    home_title = customtkinter.CTkLabel(home_title_row, text="Dashboard", font=customtkinter.CTkFont(size=20, weight="bold"), anchor="w")
    home_title.pack(anchor="w")
    period_label = customtkinter.CTkLabel(home_title_row, text="Period", anchor="e")
    period_label.place(rely=0.5, relx=1.0, x=-130, anchor="e")
    period_optionmenu = customtkinter.CTkOptionMenu(home_title_row, values=["Last 7 days", "Last 30 days", "Last 90 days"], width=120)
    period_optionmenu.set("Last 7 days")
    period_optionmenu.place(rely=0.5, relx=1.0, anchor="e")

    # Row 1 - Stats
    dashboard_row1 = customtkinter.CTkFrame(master, fg_color="transparent")
    dashboard_row1.pack(anchor="nw", fill="x", pady=10)
    def dashboard_stat(master, title, icon, text, fg_color=None, text_color=None):
        frame = customtkinter.CTkFrame(master, width=250, height=100, corner_radius=20, fg_color=fg_color)
        label_icon = customtkinter.CTkLabel(frame, image=icon, text="", fg_color="transparent")
        label_icon.place(x=10, y=10, anchor="nw")
        label_title = customtkinter.CTkLabel(frame, text=title, text_color=text_color)
        label_title.pack(padx=20, pady=10, anchor="e")
        label_text = customtkinter.CTkLabel(frame, text=text, font=customtkinter.CTkFont(size=20, weight="bold"), text_color=text_color)
        label_text.pack(padx=20, pady=10)
        return frame

    dashboard_sales = dashboard_stat(dashboard_row1, "Sales", create_colorized_icon(get_asset_path("cart.png"), (255, 255, 255), (255, 255, 255), size=(35, 35)), "€ 15.300", fg_color=customtkinter.ThemeManager.theme["CTkButton"]["fg_color"], text_color=customtkinter.ThemeManager.theme["CTkButton"]["text_color"])
    dashboard_sales.grid(row=0, column=0, padx=0, pady=10, sticky="we")
    dashboard_customers = dashboard_stat(dashboard_row1, "Customers", create_colorized_icon(get_asset_path("user.png"), (20, 20, 20), (255, 255, 255), size=(35, 35)), "3.400")
    dashboard_customers.grid(row=0, column=1, padx=10, pady=10, sticky="we")
    dashboard_orders = dashboard_stat(dashboard_row1, "Orders", create_colorized_icon(get_asset_path("cart.png"), (20, 20, 20), (255, 255, 255), size=(35, 35)), "1.200")
    dashboard_orders.grid(row=0, column=2, padx=0, pady=10, sticky="we")
    dashboard_row1.grid_columnconfigure((0,1,2), weight=1)

    # Row 2 - Top Countries and Recent Orders
    dashboard_row2 = customtkinter.CTkFrame(master, fg_color="transparent")
    dashboard_row2.pack(anchor="nw", fill="x", pady=(10, 0))

    countries_frame = customtkinter.CTkFrame(dashboard_row2, corner_radius=20)
    countries_frame.grid(row=0, column=0, padx=(0,10), sticky="nw")
    countries_title = customtkinter.CTkLabel(countries_frame, text="Top Countries", font=customtkinter.CTkFont(size=16, weight="bold"))
    countries_title.pack(padx=20, pady=(15,10), anchor="nw")
    countries_content = customtkinter.CTkFrame(countries_frame, fg_color="transparent", corner_radius=0)
    countries_content.pack(padx=10, pady=(0,10), fill="both", expand=True)
    def country_stat(master, country, orders, percentage):
        frame = customtkinter.CTkFrame(master, fg_color="transparent")
        label_country = customtkinter.CTkLabel(frame, text=country, font=customtkinter.CTkFont(size=14), height=25)
        label_country.grid(row=0, column=0,padx=10, pady=0, sticky="w")
        label_orders = customtkinter.CTkLabel(frame, text=f"Orders: {orders}", font=customtkinter.CTkFont(size=12), text_color="#888888")
        label_orders.grid(row=1, column=0,padx=10, pady=0, sticky="w")
        label_percentage = customtkinter.CTkLabel(frame, text=f"{percentage}%", font=customtkinter.CTkFont(size=12), text_color="#888888")
        label_percentage.grid(row=1, column=1, padx=10, pady=0, sticky="e")
        label_progress_bar = customtkinter.CTkProgressBar(frame, width=150)
        label_progress_bar.set(percentage / 100)
        label_progress_bar.grid(row=2, columnspan=2, padx=10, pady=(0,10), sticky="s")
        return frame
    country1 = country_stat(countries_content, "Belgium", 500, 50)
    country1.pack(padx=10, pady=0, anchor="nw")
    country2 = country_stat(countries_content, "France", 300, 30)
    country2.pack(padx=10, pady=0, anchor="nw")
    country3 = country_stat(countries_content, "The Netherlands", 200, 20)
    country3.pack(padx=10, pady=(0, 10), anchor="nw")

    recent_orders_frame = customtkinter.CTkFrame(dashboard_row2, fg_color="transparent", corner_radius=20, border_width=2, border_color=customtkinter.ThemeManager.theme["CTkFrame"]["top_fg_color"])
    recent_orders_frame.grid(row=0, column=1, padx=(10,0), sticky="nswe")
    recent_orders_title = customtkinter.CTkLabel(recent_orders_frame, text="Recent Orders", font=customtkinter.CTkFont(size=16, weight="bold"))
    recent_orders_title.pack(padx=20, pady=(15, 10), anchor="nw")
    recent_orders_clear_button = customtkinter.CTkButton(recent_orders_frame, text="Clear", width=60)
    recent_orders_clear_button.place(relx=1.0, x=-15, y=15, anchor="ne")
    recent_orders_content = customtkinter.CTkFrame(recent_orders_frame, 
                                                   corner_radius=15,
                                                   )
    recent_orders_content.pack(anchor="nw", padx=15, pady=(0,15), fill="both", expand=True)

    # Set up grid headers
    headers = ["", "Order ID", "Customer", "Amount"]
    for col, header_text in enumerate(headers):
        header = customtkinter.CTkLabel(recent_orders_content, text=header_text, font=customtkinter.CTkFont(weight="bold"))
        header.grid(row=0, column=col, padx=10, pady=(10, 5), sticky="w")
        if header_text == "Amount":
            header.grid(sticky="e")

    # Sample order data - using a single grid system
    orders = [
        (1, "43215", "J. Doe", "243,00", True),
        (2, "43214", "S. Smith", "125,50", True),
        (3, "43210", "M. Brown", "87,20", False),
        (4, "43205", "E. Johnson", "342,75", False)
    ]

    for row_num, (_, order_id, customer, amount, checked) in enumerate(orders, start=1):
        # Checkbox
        checkbox = customtkinter.CTkCheckBox(recent_orders_content, text="", width=30, checkbox_width=20, checkbox_height=20)
        checkbox.grid(row=row_num, column=0, padx=10, pady=(5, 5))
        if checked:
            checkbox.select()
        
        # Order ID
        id_label = customtkinter.CTkLabel(recent_orders_content, text=f"#{order_id}")
        id_label.grid(row=row_num, column=1, padx=10, pady=(5, 5), sticky="w")
        
        # Customer
        customer_label = customtkinter.CTkLabel(recent_orders_content, text=customer)
        customer_label.grid(row=row_num, column=2, padx=10, pady=(5, 5), sticky="w")

        # Amount
        amount_label = customtkinter.CTkLabel(recent_orders_content, text=f"€ {amount}")
        amount_label.grid(row=row_num, column=3, padx=10, pady=(5, 5), sticky="e")

    # Configure grid columns
    recent_orders_content.grid_columnconfigure(0, weight=0)  # Checkbox column
    recent_orders_content.grid_columnconfigure(1, weight=1)  # Order ID column
    recent_orders_content.grid_columnconfigure(2, weight=3)  # Customer column
    recent_orders_content.grid_columnconfigure(3, weight=1)  # Date column
    recent_orders_content.grid_columnconfigure(4, weight=1)  # Amount column

    dashboard_row2.grid_columnconfigure(0, weight=1)
    dashboard_row2.grid_columnconfigure(1, weight=3)

    # Row 3 - Settings
    dashboard_row3 = customtkinter.CTkFrame(master, fg_color="transparent")
    dashboard_row3.pack(anchor="nw", fill="x", pady=(20, 0))

    # Display Scale
    scale_label = customtkinter.CTkLabel(dashboard_row3, text="UI Scale:")

    scale_options = ["80%", "90%", "100%", "110%", "120%"]
    scale_var = customtkinter.StringVar(value="100%")
    scale_menu = customtkinter.CTkOptionMenu(dashboard_row3, values=scale_options, variable=scale_var, width=80,
                                           command=lambda value: customtkinter.set_widget_scaling(float(value.strip("%"))/100))

    # Appearance Mode
    appearance_label = customtkinter.CTkLabel(dashboard_row3, text="Appearance Mode:")

    appearance_options = ["Light", "Dark", "System"]
    appearance_var = customtkinter.StringVar(value="System")
    appearance_menu = customtkinter.CTkOptionMenu(dashboard_row3, values=appearance_options, variable=appearance_var,
                                                command=lambda value: customtkinter.set_appearance_mode(value.lower()))
    appearance_menu.pack(padx=10, pady=10, anchor="w", side="right")
    appearance_label.pack(anchor="w", padx=(20, 10), pady=10, side="right")
    scale_menu.pack(padx=10, pady=10, anchor="w", side="right")
    scale_label.pack(anchor="w", padx=(0, 10), pady=10, side="right")

    # Configure the grid
    dashboard_row3.grid_columnconfigure((0, 2), weight=0)
    dashboard_row3.grid_columnconfigure((1, 3), weight=1)

def create_orders_list_view(master):
    orders_list = customtkinter.CTkLabel(master, text="Orders List", font=customtkinter.CTkFont(size=20, weight="bold"), fg_color="transparent")
    orders_list.pack(anchor="nw", pady=(0, 20))

    # Main container for orders
    orders_container = customtkinter.CTkFrame(master, fg_color="transparent")
    orders_container.pack(fill="both", expand=True)

    # Search and filter row
    filter_frame = customtkinter.CTkFrame(orders_container, fg_color="transparent")
    filter_frame.pack(fill="x", pady=(0, 10))

    search_entry = customtkinter.CTkEntry(filter_frame, placeholder_text="Search orders...")
    search_entry.pack(side="left", padx=(0, 10), fill="x", expand=True)

    filter_label = customtkinter.CTkLabel(filter_frame, text="Filter by:")
    filter_label.pack(side="left", padx=(10, 5))

    status_filter = customtkinter.CTkOptionMenu(filter_frame, values=["All", "Pending", "Completed", "Cancelled"])
    status_filter.pack(side="left", padx=(0, 10))

    date_filter = customtkinter.CTkOptionMenu(filter_frame, values=["All time", "Today", "This week", "This month"])
    date_filter.pack(side="left", padx=0)

    # Orders table
    table_frame = customtkinter.CTkFrame(orders_container)
    table_frame.pack(fill="both", expand=True)

    # Table headers
    headers_frame = customtkinter.CTkFrame(table_frame, height=40, fg_color=customtkinter.ThemeManager.theme["CTkFrame"]["top_fg_color"], corner_radius=0)
    headers_frame.pack(fill="x", pady=(0, 1))
    headers_frame.pack_propagate(False)

    headers = ["Order ID", "Customer", "Date", "Total", "Status", "Actions"]
    header_weights = [1, 2, 1, 1, 1, 1]

    for idx, header in enumerate(headers):
        header_label = customtkinter.CTkLabel(headers_frame, text=header, font=customtkinter.CTkFont(weight="bold"), anchor="center")
        header_label.grid(row=0, column=idx, padx=10, pady=5, sticky="w")
        headers_frame.grid_columnconfigure(idx, weight=header_weights[idx])

    # Create a scrollable frame for orders
    scrollable_frame = customtkinter.CTkScrollableFrame(table_frame, fg_color="transparent")
    scrollable_frame.pack(fill="both", expand=True)

    # Sample order data
    orders_data = [
        {"id": "12345", "customer": "John Doe", "date": "2023-05-15", "total": "€249.99", "status": "Completed"},
        {"id": "12346", "customer": "Jane Smith", "date": "2023-05-16", "total": "€59.99", "status": "Pending"},
        {"id": "12347", "customer": "Robert Johnson", "date": "2023-05-17", "total": "€125.50", "status": "Completed"},
        {"id": "12348", "customer": "Emily Brown", "date": "2023-05-18", "total": "€79.98", "status": "Cancelled"},
        {"id": "12349", "customer": "Michael Wilson", "date": "2023-05-19", "total": "€199.96", "status": "Pending"},
        {"id": "12350", "customer": "Sarah Davis", "date": "2023-05-20", "total": "€29.99", "status": "Completed"},
        {"id": "12351", "customer": "David Martinez", "date": "2023-05-21", "total": "€149.97", "status": "Pending"},
        {"id": "12352", "customer": "Jessica Rodriguez", "date": "2023-05-22", "total": "€89.98", "status": "Completed"}
    ]

    # Function to get status color
    def get_status_color(status):
        if status == "Completed":
            return "#4CAF50", "#FFFFFF"  # Green with white text
        elif status == "Pending":
            return "#FFC107", "#000000"  # Yellow with black text
        elif status == "Cancelled":
            return "#F44336", "#FFFFFF"  # Red with white text
        else:
            return None, None

    # Configure column weights in the scrollable frame
    for i, weight in enumerate(header_weights):
        scrollable_frame.grid_columnconfigure(i, weight=weight)

    # Add order rows
    for idx, order in enumerate(orders_data):
        # Alternate row colors
        row_bg = customtkinter.ThemeManager.theme["CTkFrame"]["fg_color"] if idx % 2 == 0 else "transparent"
        
        # Order ID
        id_label = customtkinter.CTkLabel(scrollable_frame, text=order["id"], fg_color=row_bg)
        id_label.grid(row=idx, column=0, padx=10, pady=10, sticky="w")
        
        # Customer
        customer_label = customtkinter.CTkLabel(scrollable_frame, text=order["customer"], fg_color=row_bg)
        customer_label.grid(row=idx, column=1, padx=10, pady=10, sticky="w")
        
        # Date
        date_label = customtkinter.CTkLabel(scrollable_frame, text=order["date"], fg_color=row_bg)
        date_label.grid(row=idx, column=2, padx=10, pady=10, sticky="w")
        
        # Total
        total_label = customtkinter.CTkLabel(scrollable_frame, text=order["total"], fg_color=row_bg)
        total_label.grid(row=idx, column=3, padx=10, pady=10, sticky="w")

        # Status
        status_bg, status_fg = get_status_color(order["status"])
        status_frame = customtkinter.CTkFrame(scrollable_frame, fg_color=status_bg, corner_radius=5)
        status_frame.grid(row=idx, column=4, padx=2, pady=2, sticky="w")
        status_label = customtkinter.CTkLabel(status_frame, text=order["status"].upper(), text_color=status_fg, font=customtkinter.CTkFont(size=9), height=18, corner_radius=3)
        status_label.pack(padx=2, pady=2)
        
        # Actions
        view_button = customtkinter.CTkButton(scrollable_frame, text="View", width=60, height=28, font=customtkinter.CTkFont(size=12))
        view_button.grid(row=idx, column=5, padx=(10, 5), pady=10, sticky="w")

    # Pagination
    pagination_frame = customtkinter.CTkFrame(orders_container, fg_color="transparent")
    pagination_frame.pack(fill="x", pady=(20, 0))

    prev_page_button = customtkinter.CTkButton(pagination_frame, text="← Previous", width=100)
    prev_page_button.pack(side="left", padx=(0, 10))

    page_label = customtkinter.CTkLabel(pagination_frame, text="Page 1 of 3")
    page_label.pack(side="left", padx=10)

    next_page_button = customtkinter.CTkButton(pagination_frame, text="Next →", width=100)
    next_page_button.pack(side="left", padx=(10, 0))

    items_per_page_label = customtkinter.CTkLabel(pagination_frame, text="Items per page:")

    items_per_page_menu = customtkinter.CTkOptionMenu(pagination_frame, values=["10", "25", "50", "100"], width=70)
    items_per_page_menu.pack(side="right", padx=0)
    items_per_page_label.pack(side="right", padx=(0, 10))
    items_per_page_menu.set("10")