import tkinter as tk
import tkinter.ttk as ttk   # module for modern-style widgets
from tkinter import messagebox
import images
import db_fetch as dbfetch
import generic_functions as func


# Encapsulates darker colored Frame on the top of the Program
class TopBar(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)    # Constructor of super-class
        self.parent = parent

        # load image
        self.img_setting = images.get_image("einstellungen.png")

        # Set up placement and size  of the Top Bar
        self["width"] = 600
        self["height"] = 40
        self.grid(row=0, column=0, sticky=tk.W + tk.E)
        self.columnconfigure(0, weight=1)

        # Title
        self.label_title = ttk.Label(self, text="Password List", font=("", 18))
        self.label_title.grid(row=0, column=0, sticky=tk.W, padx=10)

        # Buttons
        # todo: Change to Label for Styling options like Plus-Button in ListFrame
        ttk.Button(self, image=self.img_setting,
                   command=self.button_settings_click).grid(row=0, column=1, sticky=tk.E, padx=7, pady=10)

        # Styles
        self["style"] = "Top.TFrame"
        self.label_title["style"] = "Top.TLabel"

    def button_settings_click(self):
        messagebox.showinfo("Settings", "Button für Einstellungen")


# Frame for Password List Headlines
class Headline(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)    # Constructor of super-class
        self.parent = parent

        # Set up Frame
        self.grid(row=1, column=0, padx=5, pady=(5, 0), sticky=tk.E + tk.W)
        self.columnconfigure(4, weight=1)

        # Headlines
        self.label_website = ttk.Label(self, text="Website", width=31)
        self.label_password = ttk.Label(self, text="Password", width=30)

        # place widgets
        self.label_website.grid(row=0, column=0, padx=5)
        self.label_password.grid(row=0, column=2, padx=5)

        # Styles
        self["style"] = "Headline.TFrame"
        self.label_website["style"] = "Headline.TLabel"
        self.label_password["style"] = "Headline.TLabel"


# Item class encapsulates one Row of the Password List
# list_frame = extra Frame inside Canvas
# parent = Object of actual ListFrame Class
#
# list_frame gets used for super-class constructor because
# Item-object has to be created in extra Frame of the ListFrame object
class Item(ttk.Frame):
    def __init__(self, list_frame, parent, *args):
        ttk.Frame.__init__(self, list_frame)    # Constructor of super-class
        self.parent = parent
        self.row_id = args[0]
        self.website = args[1]
        self.password = args[2]
        self.used_plus_button = args[3]     # bool: True if item is added manually with Plus Button

        # "normal" -> default State for saved entries
        # "edit" -> Edit-State when Edit-Button is pressed
        # "create" -> When Plus-Button is used to add a Row
        self.state = args[4]   # "normal", "edit" or ""  todo: State maybe has to be put up on ListFrame-Level

        # Item will revert to these variables if edit is cancelled
        self.website_revert = ""
        self.password_revert = ""

        # load image
        self.img_copy = images.get_image("kopieren.png")
        self.img_delete = images.get_image("trashcan.png")
        self.img_edit = images.get_image("bleistift.png")

        # Event when losing Focus of Item-Frame - Used for State-Change
        self.bind("<FocusOut>", self.frame_lost_focus)

        # tk variables for entry fields
        self.entry_val_website = tk.StringVar()
        self.entry_val_website.set(self.website)
        self.entry_val_password = tk.StringVar()
        self.entry_val_password.set(self.password)

        # Entry widgets for row values
        self.entry_website = ttk.Entry(self, textvariable=self.entry_val_website, state="readonly", width=30)
        self.entry_website.grid(row=self.row_id, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Separator(self, orient="vertical").grid(row=self.row_id, column=1, padx=5, sticky=tk.N + tk.S)
        self.entry_password = ttk.Entry(self, textvariable=self.entry_val_password, state="readonly", show="*", width=30)
        self.entry_password.grid(row=self.row_id, column=2, padx=5, pady=5, sticky=tk.W)
        ttk.Separator(self, orient="vertical").grid(row=self.row_id, column=3, padx=5, sticky=tk.N + tk.S)

        # Entry-Events
        self.entry_website.bind("<Return>", self.save_changes)
        self.entry_password.bind("<Return>", self.save_changes)

        # Buttons
        # Copy Button will change to Save-Changes-Button while in Edit-Mode
        # Delete Button will change to Discard-Changes-Button while in Edit-Mode
        self.item_copy_button = ttk.Button(self, image=self.img_copy, command=self.button_copy_click)
        self.item_delete_button = ttk.Button(self, image=self.img_delete, command=self.button_delete_click)
        self.item_edit_button = ttk.Button(self, image=self.img_edit, command=self.button_edit_click)

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

        self.grid(row=self.row_id, column=0, sticky=tk.E + tk.W)
        # self.item_frame.columnconfigure(2, weight=1)

        # Mouse Hover Event
        self.bind('<Enter>', self.mouse_enter)
        self.bind('<Leave>', self.mouse_leave)

        # Change State if Plus-Button is used
        if self.state == "create":
            self.change_state("create")

    # Event - Mouse Hover over Item - highlights row
    def mouse_enter(self, event=None):
        # don't change colors if ListFrame is in edit-mode
        if self.state == "normal":
            self.configure(style="MouseEnter.TFrame")
            self.entry_website.configure(style="MouseEnter.TLabel")
            self.entry_password.configure(style="MouseEnter.TLabel")
            self.item_copy_button.grid(row=self.row_id, column=4)
            self.item_delete_button.grid(row=self.row_id, column=5, padx=5)
            self.item_edit_button.grid(row=self.row_id, column=6, padx=(0, 50))

    # Event - Mouse leaves Item - return to normal color
    def mouse_leave(self, event=None):
        # don't change colors if ListFrame is in edit-mode
        if self.state == "normal":
            self.configure(style=self.frame_style)
            self.entry_website.configure(style=self.entry_style)
            self.entry_password.configure(style=self.entry_style)
            self.item_copy_button.grid_remove()
            self.item_delete_button.grid_remove()
            self.item_edit_button.grid_remove()

    def save_changes(self, event=None):
        if self.state != "normal":
            # todo: Save Changes to Database
            self.change_state("normal")

    # revert to old values
    def discard_changes(self, event=None):
        if self.state == "edit":
            self.entry_website.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)
            self.entry_website.insert(0, self.website_revert)
            self.entry_password.insert(0, self.password_revert)
            self.change_state("normal")
        # Remove Item if Changes are discarded in Create-Mode
        elif self.state == "create":
            self.button_delete_click()

    # if Item loses Focus while in edit-mode, user will be asked if changes should be saved
    def frame_lost_focus(self, event=None):
        if self.state != "normal":
            if messagebox.askquestion("Discard change", "Save Changes?") == "no":
                self.discard_changes(event)
            else:
                self.change_state("normal")

    # Changes State of Item
    def change_state(self, state):
        self.state = state

        if self.state == "normal":
            entry_state = "readonly"  # Entry will not be editable

            if self.entry_style == "Item1.TLabel":
                entry_style = "Item1.TLabel"
                self["style"] = "Item1.TFrame"
            else:
                entry_style = "Item2.TLabel"
                self["style"] = "Item2.TFrame"

            # Change Buttons - Bind Event and image
            self.item_copy_button["image"] = images.get_image("kopieren.png")
            self.item_delete_button["image"] = images.get_image("trashcan.png")
            self.item_copy_button["command"] = self.button_copy_click
            self.item_delete_button["command"] = self.button_delete_click
            # Re-Place Edit-Button
            self.item_edit_button.grid()

            self.item_copy_button.grid_remove()
            self.item_delete_button.grid_remove()
            self.item_edit_button.grid_remove()

        else:   # state == edit or create
            entry_state = "normal"  # Entry will be editable

            # In Case of Edit-Cancel
            self.website_revert = self.entry_website.get()
            self.password_revert = self.entry_password.get()

            # Change Buttons - Bind Event and image
            self.item_copy_button["image"] = images.get_image("save16x16.png")
            self.item_delete_button["image"] = images.get_image("cross16x16.png")
            self.item_copy_button["command"] = self.save_changes
            self.item_delete_button["command"] = self.discard_changes
            self.item_copy_button.grid(row=self.row_id, column=4)
            self.item_delete_button.grid(row=self.row_id, column=5)
            # Edit Button not needed while in Edit-mode
            self.item_edit_button.grid_remove()

            if self.entry_style == "Item1.TLabel":
                entry_style = "Item1.TEntry"
            else:
                entry_style = "Item2.TEntry"

            # set Focus on Website name and mark entire text
            self.entry_website.focus_set()
            self.entry_website.select_range(0, tk.END)

        self.entry_website["state"] = self.entry_password["state"] = entry_state
        self.entry_website["style"] = self.entry_password["style"] = entry_style

        #else:   # "normal"

    # Copy password to Clipboard
    def button_copy_click(self):
        self.clipboard_clear()
        self.clipboard_append(self.entry_password.get())

    # Copy password to Clipboard
    def button_delete_click(self):
        # messagebox.showinfo("Delete-Button", "Delete-Button ID: " + str(self.row_id))
        # todo: Delete in Database
        self.grid_forget()
        self.destroy()
        ListFrame.items.remove(self)
        ListFrame.alternate_colorscheme()
        # ListFrame.row_down_count()

    # Copy password to Clipboard
    def button_edit_click(self):
        # todo: functionality for Edit
        self.change_state("edit")

    def stylize_item_widgets(self, frame_style, entry_style):
        self["style"] = frame_style
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

        # Configure Frame
        self["relief"] = tk.GROOVE
        self["padding"] = "2 2 2 2"
        self.grid(row=2, column=0, padx=5, pady=(0, 5), sticky=tk.N + tk.E + tk.S + tk.W)
        self.columnconfigure(0, weight=1)  # Expand widget on Window Resize
        self.rowconfigure(0, weight=1)

        # Create Canvas
        self.canvas = tk.Canvas(self, highlightthickness=0, background="white")
        self.canvas.grid(row=0, column=0, sticky="nswe")

        # Create Scrollbar - placed inside ListFrame on the ride side of the Canvas
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
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
            # self gets passed as second argument as a parent
            ListFrame.items.append(Item(self.list_frame, self, ListFrame.row_count, entry["name"], entry["pw"], False, "normal"))
            ListFrame.row_up_count()

        # Label will function as a Button
        # Usage of Label because of Styling options
        self.button_add_row = ttk.Button(self.list_frame, image=self.img_btn_add_row, command=self.add_row, padding="3 3 3 3")
        self.button_add_row.grid(row=ListFrame.row_count+1, column=0, sticky="w", padx=3, pady=3)
        self.button_add_row.bind("<ButtonPress-1>", lambda e: func.style_change(self.button_add_row, "OnClick.TLabel"))
        self.button_add_row.bind("<ButtonRelease-1>", lambda e: func.style_change(self.button_add_row, "Item2.TLabel"))
        self.button_add_row.bind("<Enter>",
                                 lambda e: ListFrame.mouse_hover_event(self.button_add_row, "MouseEnter.TLabel"))
        self.button_add_row.bind("<Leave>",
                                 lambda e: ListFrame.mouse_hover_event(self.button_add_row, "Item2.TLabel"))
        self.button_add_row["style"] = "Item2.TLabel"

    # Add new Password Line
    def add_row(self, event=None):
        row_id = ListFrame.row_count
        self.button_add_row.grid(row=row_id+1)
        # Create new Item and store in List
        ListFrame.items.append(Item(self.list_frame, self, row_id, "", "", True, "create"))
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

        # Frame placement and Expand-Behaviour
        self.grid(row=0, column=0, sticky=tk.N + tk.E + tk.S + tk.W)
        # Expand List Frame on Window Resize
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        # Styles
        self["style"] = "Main.TFrame"

        # Create Sub frames
        self.top_bar = TopBar(self)
        self.list_frame = ListFrame(self)
