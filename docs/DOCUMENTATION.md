# CTkSidebar Documentation
## 1 Installation
Get the latest version from PyPI:
```
pip install ctk-sidebar
```
The only direct dependencies are pillow, and, of course, CustomTkinter itself.

## 2 Component Instantiation
Depending on your requirements, you can either instantiate the `CTkSidebarNavigation` or the `CTkSidebar` component. As the names imply, the navigation component handles automatic view switching,
while the sidebar allows more custom functionality, and only creates the sidebar.

### 2.1 Navigation Component
The navigation component is meant to be used as the toplevel component in your Tk window. It contains a sidebar and containers to display the different views you assign to each menu item.

Example:
```python
import customtkinter as CTk
from ctksidebar import CTkSidebarNavigation

app = CTk.CTk()
app.geometry("640x480")

nav = CTkSidebarNavigation(master=app)
nav.pack(fill="both", expand=True)

side = nav.sidebar
```

Using the API calls described below, you can now populate the side bar and view containers.

### 2.2 Sidebar Component
The sidebar can also be used as a standalone component. In this case, you have to handle (custom) navigation yourself by listening to the commands of each menu item.

Setting up a sidebar on the left side of a parent component can be done as follows:
```python
sidebar = CTkSidebar(master=parent)
sidebar.pack(side="left", fill="y")
```

## 3 API
### `CTkSidebarNavigation`
The toplevel component to be instantiated on your window when needing a side bar with automatic navigation.

#### Constructor

<table>
  <tr>
    <th>Parameter</th>
    <th>Type</th>
    <th>Default</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><code>master</code></td>
    <td><code>Any</code></td>
    <td>-</td>
    <td>The parent Tk component. Required.</td>
  </tr>
  <tr>
    <td><code>width</code></td>
    <td><code>int</code></td>
    <td>220</td>
    <td>The width of the sidebar.</td>
  </tr>
  <tr>
    <td><code>theme</code></td>
    <td><code>CTkSidebarTheme | None</code></td>
    <td>None</td>
    <td>When provided, allows to set a custom theme. See dedicated section on styling.</td>
  </tr>
  <tr>
    <td><code>indent_level</code></td>
    <td><code>int</code></td>
    <td>0</td>
    <td>Sets a custom indentation level for the items in the current menu. Submenus automatically use the next indentation level.</td>
  </tr>
  <tr>
    <td><code>single_expanded_submenu</code></td>
    <td><code>bool</code></td>
    <td>False</td>
    <td>When <code>True</code>, only one submenu per indentation level can be expanded at a time. Other submenus automatically collapse.</td>
  </tr>
</table>

#### Properties
##### `.sidebar`

Type: `CTkSidebar`

A reference to the actual side bar embedded in the navigation container. A side bar is automatically instantiated when calling the `CTkSidebarNavigation` constructor.
This property must be used to populate the side bar with menu items, see description of the `CTkSidebar` class.

#### Methods
##### `.view(id)`

Returns the frame for the view with the passed ID. The ID must match one of the previously added items using `.sidebar..add_item(...)`. Use the return value as the parent when populating the view of each sidebar item.

Return value: `CTk.CTkFrame`
<table>
  <tr>
    <th>Parameter</th>
    <th>Type</th>
    <th>Default</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><code>id</code></td>
    <td><code>int | str</code></td>
    <td>-</td>
    <td>One of the IDs previously passed when adding a menu item. Required.</td>
  </tr>
</table>

Example:
```python
nav = CTkSidebarNavigation(master=app)
nav.sidebar.add_item(id="home", text="Home")
nav.sidebar.add_item(id="orders", text="Orders")
home_frame = nav.view("home")
home_title = CTk.CTkLabel(master=home_frame, text="Home")
```

##### `.set(id)`

Switches the view and selected side bar item to the item with given ID. After populating the side bar, a call to this method is needed to set the initially selected item and view.
Can also be used to programmatically switch to another view.

Return value: `None`
<table>
  <tr>
    <th>Parameter</th>
    <th>Type</th>
    <th>Default</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><code>id</code></td>
    <td><code>int | str</code></td>
    <td>-</td>
    <td>One of the IDs previously passed when adding a menu item. Required.</td>
  </tr>
</table>

Example:
```python
nav = CTkSidebarNavigation()
nav.sidebar.add_item(id="home", text="Home")
nav.sidebar.add_item(id="orders", text="Orders")
nav.set("home")
```

### `CTkSidebar`
#### Constructor

<table>
  <tr>
    <th>Parameter</th>
    <th>Type</th>
    <th>Default</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><code>master</code></td>
    <td><code>Any</code></td>
    <td>-</td>
    <td>The parent Tk component. Required.</td>
  </tr>
  <tr>
    <td><code>width</code></td>
    <td><code>int</code></td>
    <td>220</td>
    <td>The width of the side bar.</td>
  </tr>
  <tr>
    <td><code>theme</code></td>
    <td><code>CTkSidebarTheme | None</code></td>
    <td>None</td>
    <td>When provided, allows to set a custom theme. See dedicated section on styling.</td>
  </tr>
  <tr>
    <td><code>indent_level</code></td>
    <td><code>int</code></td>
    <td>0</td>
    <td>Sets a custom indentation level for the items in the current menu. Submenus automatically use the next indentation level.</td>
  </tr>
  <tr>
    <td><code>single_expanded_submenu</code></td>
    <td><code>bool</code></td>
    <td>False</td>
    <td>When <code>True</code>, only one submenu per indentation level can be expanded at a time. Other submenus automatically collapse.</td>
  </tr>
</table>

#### Methods
##### `.add_item(id, text, command, icon, icon_size, override_text_x, override_icon_x)`

Return type: `None`

Add a new menu item to the side bar.

As an icon you can either pass a PIL `Image.Image` or a `CTk.CTkImage`. When a PIL `Image.Image` is passed, the image automatically gets colorized to match the menu item text.
If this behavior is not desired, you can pass your own tuple of `CTk.CTkImage`s to specify an image for the deselected and selected menu item state.

<table>
  <tr>
    <th>Parameter</th>
    <th>Type</th>
    <th>Default</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><code>id</code></td>
    <td><code>int | str</code></td>
    <td><code>None</code></td>
    <td>A unique ID for this menu item. Required when using the navigation component.</td>
  </tr>
  <tr>
    <td><code>text</code></td>
    <td><code>str</code></td>
    <td>""</td>
    <td>Text label that appears in the side bar.</td>
  </tr>
  <tr>
    <td><code>command</code></td>
    <td><code>Callable[[int|str], None] | None</code></td>
    <td><code>None</code></td>
    <td>A custom callback when this menu item is clicked. The `id` is passed as a parameter.</td>
  </tr>
  <tr>
    <td><code>icon</code></td>
    <td><code>Image.Image | tuple[CTk.CTkImage, CTk.CTkImage] | None</code></td>
    <td><code>None</code></td>
    <td>An optional icon for this menu item. Pass a PIL image if you want automatic colorization, or two <code>CTk.CTkImage</code>s to provide icons for the deselected and selected state of the item.</td>
  </tr>
  <tr>
    <td><code>icon_size</code></td>
    <td><code>tuple[int, int]</code></td>
    <td><code>(20, 20)</code></td>
    <td>The size of the icon.</td>
  </tr>
  <tr>
    <td><code>override_text_x</code></td>
    <td><code>int | None</code></td>
    <td><code>None</code></td>
    <td>Specify a custom X position for the label text on this item, overriding the theme's default.</td>
  </tr>
  <tr>
    <td><code>override_icon_x</code></td>
    <td><code>int | None</code></td>
    <td><code>None</code></td>
    <td>Specify a custom X position for the label icon on this item, overriding the theme's default.</td>
  </tr>
</table>

Example:
```python
import customtkinter as CTk
from PIL import Image
from ctksidebar import CTkSidebar

# <init your app here>

side = CTkSidebar(master=app)

# Automatically colorized icons
side.add_item(id="home", text="Dashboard", icon=Image.open("home.png"))

# Custom icon for deselected and selected state, no colorization
order_icon = (
    CTk.CTkImage(Image.open("order.png")),
    CTk.CTkImage(Image.open("order_selected.png")),
)
side.add_item(id="order_icon", text="Dashboard", icon=order_icon)
```

##### `.add_submenu(id, text, command, icon, icon_size, override_text_x, override_icon_x, indent_level, theme, expanded)`

Add a menu item that has a submenu. Works similarly as `.add_item()`, except that it returns a new `CTkSidebar` object that allows you to populate the submenu.

Return type: `CTkSidebar`

<table>
  <tr>
    <th>Parameter</th>
    <th>Type</th>
    <th>Default</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><code>id</code></td>
    <td><code>int | str</code></td>
    <td><code>None</code></td>
    <td>A unique ID for this menu item. Required when using the navigation component.</td>
  </tr>
  <tr>
    <td><code>text</code></td>
    <td><code>str</code></td>
    <td>""</td>
    <td>Text label that appears in the side bar.</td>
  </tr>
  <tr>
    <td><code>command</code></td>
    <td><code>Callable[[int|str], None] | None</code></td>
    <td><code>None</code></td>
    <td>A custom callback when this menu item is clicked. The `id` is passed as a parameter.</td>
  </tr>
  <tr>
    <td><code>icon</code></td>
    <td><code>Image.Image | tuple[CTk.CTkImage, CTk.CTkImage] | None</code></td>
    <td><code>None</code></td>
    <td>An optional icon for this menu item. Pass a PIL image if you want automatic colorization, or two <code>CTk.CTkImage</code>s to provide icons for the deselected and selected state of the item.</td>
  </tr>
  <tr>
    <td><code>icon_size</code></td>
    <td><code>tuple[int, int]</code></td>
    <td><code>(20, 20)</code></td>
    <td>The size of the icon.</td>
  </tr>
  <tr>
    <td><code>override_text_x</code></td>
    <td><code>int | None</code></td>
    <td><code>None</code></td>
    <td>Specify a custom X position for the label text on this item, overriding the theme's default.</td>
  </tr>
  <tr>
    <td><code>override_icon_x</code></td>
    <td><code>int | None</code></td>
    <td><code>None</code></td>
    <td>Specify a custom X position for the label icon on this item, overriding the theme's default.</td>
  </tr>
  <tr>
    <td><code>indent_level</code></td>
    <td><code>int | None</code></td>
    <td><code>None</code></td>
    <td>Specify a custom indentation level for the submenu. When <code>None</code>, the level is automatically incremented relatively to the parent menu.</td>
  </tr>
  <tr>
    <td><code>theme</code></td>
    <td><code>CTkSidebarTheme | None</code></td>
    <td><code>None</code></td>
    <td>Specify a custom theme for the submenu. By default, all submenus get the 'secondary' theme. Also see the description of `CTkSidebarTheme`.</td>
  </tr>
  <tr>
    <td><code>expanded</code></td>
    <td><code>bool</code></td>
    <td><code>True</code></td>
    <td>Whether the submenu is initially expanded.</td>
  </tr>
</table>

Example:
```python
# - Home
# - Orders
#   - List
#   - Reports
sidebar.add_item(id="Home", text="Home")
order_submenu = side.add_submenu(id="orders", text="Orders")
order_submenu.add_item(id="order-list", text="List")
order_submenu.add_item(id="order-reports", text="Reports")
```

##### `.add_frame(frame, pady)`

Adds a custom frame or widget in the side bar. Useful for adding a header or custom separators.

> [!IMPORTANT]
> The `master` of the widget to add must be the `CTkSidebar` on which this call is made. The `CTkSidebar` automatically integrates it in its layout, so no calls to `.pack()`, `.place()` or `.grid()` are needed.
 
Return type: `None`

<table>
  <tr>
    <th>Parameter</th>
    <th>Type</th>
    <th>Default</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><code>frame</code></td>
    <td><code>CTk.CTkBaseClass</code></td>
    <td>-</td>
    <td>The customTkinter widget to add. Required.</td>
  </tr>
  <tr>
    <td><code>pady</code></td>
    <td><code>int | tuple[int,int] | None</code></td>
    <td><code>None</code></td>
    <td>Optional vertical padding to add when inserting it in the side bar.</td>
  </tr>
</table>

##### `.add_separator(width, height, line_color, line_thickness, rounded_line_end)`

Adds a separator line to the side bar.


<table>
  <tr>
    <th>Parameter</th>
    <th>Type</th>
    <th>Default</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><code>width</code></td>
    <td><code>int | None</code></td>
    <td>None</td>
    <td>The width of the (centered) separation line. When `None`, the default from the theme is used.</td>
  </tr>
  <tr>
    <td><code>height</code></td>
    <td><code>int | None</code></td>
    <td><code>None</code></td>
    <td>The total height of the separator. When `None`, the default from the theme is used.</td>
  </tr>
  <tr>
    <td><code>line_color</code></td>
    <td><code>str | tuple[str, str] | None</code></td>
    <td><code>None</code></td>
    <td>The color of the separation line. Can be a single color string, are a tuple for specifying different light/dark colors. When `None`, the default from the theme is used.</td>
  </tr>
  <tr>
    <td><code>line_color</code></td>
    <td><code>bool</code></td>
    <td><code>None</code></td>
    <td>The type of line caps used for drawing the seperation line. Set <code>True</code> for rounded end caps, <code>False</code> for butt caps. When `None`, the default from the theme is used.</td>
  </tr>
</table>

##### `.add_spacing(height)`

Adds empty vertical space to the side bar.

<table>
  <tr>
    <th>Parameter</th>
    <th>Type</th>
    <th>Default</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><code>height</code></td>
    <td><code>int | None</code></td>
    <td>None</td>
    <td>The height of the empty space to add.</td>
  </tr>
</table>

## 4 Styling
TODO
