import tkinter as tk
import tkinter.ttk as ttk   # module for modern-style widgets
from tkinter import messagebox
import images as images
import db_fetch as dbfetch


# Encapsulates darker colored Frame on the top of the Program
class TopBar(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)    # Constructor of super-class
        self.parent = parent

        # load image
        self.img_setting = images.get_image("einstellungen.png")

        # Set up placement and size  of the Top Bar
        self.top_bar = ttk.Frame(parent, width=600, height=40)
        self.top_bar.grid(row=0, column=0, sticky=tk.W + tk.E)
        self.top_bar.columnconfigure(0, weight=1)

        # Title
        self.label_title = ttk.Label(self.top_bar, text="Password List", font=("", 18))
        self.label_title.grid(row=0, column=0, sticky=tk.W, padx=10)

        # Buttons
        ttk.Button(self.top_bar, image=self.img_setting,
                   command=self.button_settings_click).grid(row=0, column=1, sticky=tk.E, padx=7, pady=10)

        # Styles
        self.top_bar["style"] = "Top.TFrame"
        self.label_title["style"] = "Top.TLabel"

    def button_settings_click(self):
        messagebox.showinfo("Settings", "Button für Einstellungen")


# Frame for Password List Headlines
class Headline(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)    # Constructor of super-class
        self.parent = parent

        # Set up Frame
        self.headline_frame = ttk.Frame(parent)
        self.headline_frame.grid(row=1, column=0, padx=5, pady=(5, 0), sticky=tk.E + tk.W)
        self.headline_frame.columnconfigure(4, weight=1)

        # Headlines
        self.label_website = ttk.Label(self.headline_frame, text="Website", width=31)
        self.label_password = ttk.Label(self.headline_frame, text="Password", width=30)

        # place widgets
        self.label_website.grid(row=0, column=0, padx=5)
        self.label_password.grid(row=0, column=2, padx=5)

        # Styles
        self.headline_frame["style"] = "Headline.TFrame"
        self.label_website["style"] = "Headline.TLabel"
        self.label_password["style"] = "Headline.TLabel"


# Item class encapsulates one Row of the Password List
class Item(ttk.Frame):
    def __init__(self, parent, *args):
        ttk.Frame.__init__(self, parent)    # Constructor of super-class
        self.parent = parent
        self.row_id = args[0]
        self.website = args[1]
        self.password = args[2]
        self.used_plus_button = args[3]     # bool: True if item is added manually with Plus Button

        # load image
        self.img_copy = images.get_image("kopieren.png")
        self.img_delete = images.get_image("trashcan.png")
        self.img_edit = images.get_image("bleistift.png")

        # Set up Frame
        self.item_frame = ttk.Frame(parent)

        # tk variables for entry fields
        self.entry_val_website = tk.StringVar()
        self.entry_val_website.set(self.website)
        self.entry_val_password = tk.StringVar()
        self.entry_val_password.set(self.password)

        # Entry widgets for row values
        self.entry_website = ttk.Entry(self.item_frame, textvariable=self.entry_val_website, state="readonly", width=30)
        self.entry_website.grid(row=self.row_id, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Separator(self.item_frame, orient="vertical").grid(row=self.row_id, column=1, padx=5, sticky=tk.N + tk.S)
        self.entry_password = ttk.Entry(self.item_frame, textvariable=self.entry_val_password, state="readonly", show="*", width=30)
        self.entry_password.grid(row=self.row_id, column=2, padx=5, pady=5, sticky=tk.W)
        ttk.Separator(self.item_frame, orient="vertical").grid(row=self.row_id, column=3, padx=5, sticky=tk.N + tk.S)

        # Buttons
        self.item_copy_button = ttk.Button(self.item_frame, image=self.img_copy, command=self.button_copy_click)
        self.item_delete_button = ttk.Button(self.item_frame, image=self.img_delete, command=self.button_delete_click)
        self.item_edit_button = ttk.Button(self.item_frame, image=self.img_edit, command=self.button_edit_click)

        # alternating Colorscheme of the rows
        # if item is added with Plus Button:
        #   -> setting Colors with row_id gets unreliable when a row in the middle got deleted
        if self.used_plus_button:
            # use first Item color if list is empty
            if not ListFrame.items:
                self.frame_style = "Item1.TFrame"
                self.entry_style = "Item1.TLabel"
            else:
                # Color gets set after evaluating the color of the last item
                if ListFrame.items[-1].frame_style == "Item1.TFrame":
                    self.frame_style = "Item2.TFrame"
                    self.entry_style = "Item2.TLabel"
                else:
                    self.frame_style = "Item1.TFrame"
                    self.entry_style = "Item1.TLabel"
        else:
            if self.row_id % 2 == 1:
                self.frame_style = "Item2.TFrame"
                self.entry_style = "Item2.TLabel"
            else:
                self.frame_style = "Item1.TFrame"
                self.entry_style = "Item1.TLabel"

        # add styling
        self.stylize_item_widgets(self.frame_style, self.entry_style)

        self.item_frame.grid(row=self.row_id, column=0, sticky=tk.E + tk.W)
        # self.item_frame.columnconfigure(2, weight=1)

        # Mouse Hover Event
        self.item_frame.bind('<Enter>', self.mouse_enter)
        self.item_frame.bind('<Leave>', self.mouse_leave)

    # Event - Mouse Hover over Item - highlights row
    def mouse_enter(self, event=None):
        self.item_frame.configure(style="MouseEnter.TFrame")
        self.entry_website.configure(style="MouseEnter.TLabel")
        self.entry_password.configure(style="MouseEnter.TLabel")
        self.item_copy_button.grid(row=self.row_id, column=4)
        self.item_delete_button.grid(row=self.row_id, column=5, padx=5)
        self.item_edit_button.grid(row=self.row_id, column=6, padx=(0, 50))

    # Event - Mouse leaves Item - return to normal color
    def mouse_leave(self, event=None):
        self.item_frame.configure(style=self.frame_style)
        self.entry_website.configure(style=self.entry_style)
        self.entry_password.configure(style=self.entry_style)
        self.item_copy_button.grid_forget()
        self.item_delete_button.grid_forget()
        self.item_edit_button.grid_forget()

    # Copy password to Clipboard
    # uses Tk object to copy to clipboard
    def button_copy_click(self):
        # todo: maybe change to access root
        r = tk.Tk()
        r.withdraw()
        r.clipboard_clear()
        r.clipboard_append(self.entry_password.get())
        r.update()  # now it stays on the clipboard after the window is closed
        r.destroy()

    # Copy password to Clipboard
    def button_delete_click(self):
        # messagebox.showinfo("Delete-Button", "Delete-Button ID: " + str(self.row_id))
        # todo: Delete in Database
        self.item_frame.grid_forget()
        self.item_frame.destroy()
        ListFrame.items.remove(self)
        ListFrame.alternate_colorscheme()
        # ListFrame.row_down_count()

    # Copy password to Clipboard
    def button_edit_click(self):
        messagebox.showinfo("Edit-Button", "Edit-Button ID: " + str(self.row_id))
        # todo: functionality for Edit

    def stylize_item_widgets(self, frame_style, entry_style):
        self.item_frame["style"] = frame_style
        self.entry_website["style"] = entry_style
        self.entry_password["style"] = entry_style


# Encapsulates objects of Item-class
# Frame for Password List
class ListFrame(ttk.Frame):

    # Class Variables
    row_count = 0
    items = []  # ListFrame-Class keeps track of added and deleted Items

    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)    # Constructor of super-class
        self.parent = parent

        # Load images
        self.img_btn_add_row = images.get_image("plus16x16.png")

        # In order to have a Scrollbar for a frame
        # a Canvas needs to be created to hold a scrollable Frame

        # Create Frame for Canvas
        self.canvas_frame = ttk.Frame(parent, relief=tk.GROOVE, padding="2 2 2 2")
        self.canvas_frame.grid(row=2, column=0, padx=5, pady=(0, 5), sticky=tk.N + tk.E + tk.S + tk.W)
        self.canvas_frame.columnconfigure(0, weight=1)     # Expand widget on Window Resize
        self.canvas_frame.rowconfigure(0, weight=1)

        # Create Canvas
        self.canvas = tk.Canvas(self.canvas_frame, highlightthickness=0, background="white")
        self.canvas.grid(row=0, column=0, sticky="nswe")

        # Create Scrollbar - placed inside canvas_frame on the ride side of the Canvas
        self.scrollbar = ttk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        # bind Canvas with Scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind("<Configure>", self.canvas_configure)

        # Mouse over List Frame --> bind Mousewheel to Scrollbar
        self.canvas.bind('<Enter>', self.bind_to_mousewheel)
        self.canvas.bind('<Leave>', self.unbind_to_mousewheel)

        # Create Frame inside Canvas which will hold the actual list
        self.list_frame = ttk.Frame(self.canvas)
        # Put List Frame inside Canvas
        self.canvas.create_window((0, 0), window=self.list_frame, anchor="nw", tags="frame")
        self.list_frame.columnconfigure(0, weight=1)  # Expand widget on Window Resize

        # Create Headline Bar
        self.headline_bar = Headline(self.parent)

        # Styles
        self.list_frame["style"] = "List.TFrame"

        # Create Items
        # Loop sets up items in List format
        # todo: Database fetch of all Password entries
        entries = dbfetch.get_entries()

        for entry in entries:
            # Create new Item and store in List
            ListFrame.items.append(Item(self.list_frame, ListFrame.row_count, entry["name"], entry["pw"], False))
            ListFrame.row_up_count()

        # Label will function as a Button
        # Usage of Label because of Styling options
        self.button_add_row = ttk.Label(self.list_frame, image=self.img_btn_add_row, padding="3 3 3 3")
        self.button_add_row.grid(row=ListFrame.row_count+1, column=0, sticky="w", padx=3, pady=3)
        self.button_add_row.bind("<1>", lambda e: self.add_row("neu", "test123"))
        self.button_add_row.bind("<Enter>",
                                 lambda e: ListFrame.mouse_hover_event(self.button_add_row, "MouseEnter.TLabel"))
        self.button_add_row.bind("<Leave>",
                                 lambda e: ListFrame.mouse_hover_event(self.button_add_row, "Item2.TLabel"))
        self.button_add_row["style"] = "Item2.TLabel"

    # Add new Password Line
    def add_row(self, name, pw, event=None):
        row_id = ListFrame.row_count
        self.button_add_row.grid(row=row_id+1)
        # Create new Item and store in List
        ListFrame.items.append(Item(self.list_frame, row_id, name, pw, True))
        ListFrame.row_up_count()
        self.list_frame.update()    # Frame needs to be redrawn before updating the Scrollbar region
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))     # Update Scrollbar region

    # Resizes the Canvas and the window inside
    def canvas_configure(self, event):
        canvas_width = event.width
        self.canvas.itemconfig("frame", width=canvas_width)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    # Bind Mousewheel to Scrollbar when Mouse enters List Frame
    # self.canvas.bind has no effect
    # Therefore the usage of bind_all - needs to be unbound after Mouse Leave event
    def bind_to_mousewheel(self, event=None):
        self.canvas.bind_all("<MouseWheel>", self.mousewheel_event)

    # Disable Mousewheel bind when Mouse leaves List Frame
    def unbind_to_mousewheel(self, event=None):
        self.canvas.unbind_all("<MouseWheel>")

    # Scrolls List Frame
    def mousewheel_event(self, event):
        # check if Frame is smaller than the canvas - only scroll if false
        if self.canvas.yview() == (0.0, 1.0):
            return
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # Generic Mouse Hover event for ttk Widgets
    # Change style on Mouse Hover
    @staticmethod
    def mouse_hover_event(widget, style, event=None):
        widget["style"] = style

    @staticmethod
    def row_up_count():
        ListFrame.row_count = ListFrame.row_count + 1

    @staticmethod
    def row_down_count():
        ListFrame.row_count = ListFrame.row_count - 1

    # Rearranges Frame colors for alternating colorscheme
    @staticmethod
    def alternate_colorscheme():
        row_count = 0
        for item in ListFrame.items:
            if row_count % 2 == 1:
                item.frame_style = "Item2.TFrame"
                item.entry_style = "Item2.TLabel"
            else:
                item.frame_style = "Item1.TFrame"
                item.entry_style = "Item1.TLabel"

            item.stylize_item_widgets(item.frame_style, item.entry_style)

            row_count = row_count + 1


# Main Page after Login
# Displays Passwords
class MainPage(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)    # Constructor of super-class
        self.parent = parent

        # main_frame will encapsulate every Subframe and widget on MainPage
        self.main_frame = ttk.Frame(parent)

        # Frame placement and Expand-Behaviour
        self.main_frame.grid(row=0, column=0, sticky=tk.N + tk.E + tk.S + tk.W)
        # Expand List Frame on Window Resize
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(2, weight=1)

        # Styles
        self.main_frame["style"] = "Main.TFrame"

        # Create Sub frames
        self.top_bar = TopBar(self.main_frame)
        self.list_frame = ListFrame(self.main_frame)
