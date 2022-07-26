import tkinter as tk
import tkinter.ttk as ttk   # module for modern-style widgets
from tkinter import messagebox
from sys import platform
from enum import Enum
import webbrowser
import images
import db_functions
import generic_functions as func
import generate as gen
import sqlite3




# Enumeration of States for Item-Object
class State(Enum):
    DEFAULT = 1
    EDIT = 2
    CREATE = 3


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
        self["style"] = "Top.TFrame"
        self.grid(row=0, column=0, sticky="ew")
        self.columnconfigure(0, weight=1)

        # Init Widgets
        self.label_title = ttk.Label(self, text="Password List", font=("", 18), style="Top.TLabel")
        self.button_settings = ttk.Button(self, image=self.img_setting, padding="2 2 2 2",
                                          command=self.button_settings_click, style="Item2.TLabel")

        # Place widgets
        self.label_title.grid(row=0, column=0, sticky=tk.W, padx=10)
        self.button_settings.grid(row=0, column=1, sticky=tk.E, padx=7, pady=10)

        # Widgets Bindings
        self.button_settings.bind("<ButtonPress-1>",
                                  lambda e: func.style_change(self.button_settings, "OnClick.TLabel"))
        self.button_settings.bind("<ButtonRelease-1>",
                                  lambda e: func.style_change(self.button_settings, "Item2.TLabel"))
        self.button_settings.bind("<Enter>", lambda e: func.style_change(self.button_settings, "MouseEnter.TLabel"))
        self.button_settings.bind("<Leave>", lambda e: func.style_change(self.button_settings, "Item2.TLabel"))

    # Loads Settings-Page
    def button_settings_click(self):
        messagebox.showinfo("Settings", "Button für Einstellungen")



class Footer(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.parent = parent

        self.grid(row=4, column=0, sticky="we")
        self.columnconfigure(0, weight=1)

        # GitHub Hyperlink
        self.label_github_link = tk.Label(self, text="GitHub", font=("", 8), fg="blue", cursor="hand2")
        self.label_github_link.bind("<Button-1>", lambda e: webbrowser.open_new("https://github.com/desch0612/password_manager"))
        # Add Underlining on Hover
        self.label_github_link.bind("<Enter>", lambda e: func.add_font_underline(self.label_github_link, "", 8))
        self.label_github_link.bind("<Leave>", lambda e: func.remove_font_underline(self.label_github_link, "", 8))

        # Place Widgets
        self.label_github_link.grid(row=0, column=2, sticky="e", padx=(0, 15))
        ttk.Separator(self, orient="vertical").grid(row=0, column=1, sticky="nse", padx=15)


# Frame for Password List Headlines
class Headline(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)    # Constructor of super-class
        self.parent = parent

        # Set up Frame
        self.grid(row=1, column=0, padx=5, pady=(5, 0), sticky="ew")
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

        # Item can have one of these three states:
        # - DEFAULT: default - Entries not editable
        # - EDIT: when edit button is pressed - Entries in box format and editable
        # - CREATE: when new row gets added with Plus-Button
        #           -> similar to EDIT with special Case: delete row if changes are discarded
        self.state = args[4]   # DEFAULT, EDIT or CREATE (from Enum Class "State")

        # Frame Config
        self.grid(row=self.row_id, column=0, sticky="ew")
        # Event when losing Focus of Item-Frame - Used for State-Change
        self.bind("<FocusOut>", self.frame_lost_focus)

        # Item will revert to these variables if edit is cancelled
        self.website_revert = ""
        self.password_revert = ""

        # Gets used to decide for Eye-Button image
        self.pw_is_hidden = True

        # load image
        self.img_transparent = images.get_image("transparent16x16.png")
        self.img_copy = images.get_image("kopieren.png")
        self.img_delete = images.get_image("trashcan.png")
        self.img_edit = images.get_image("bleistift.png")
        self.img_eye_crossed = images.get_image("eye_crossed16x16.png")
        self.img_eye_crossed_fill = images.get_image("eye_crossed_fill16x16.png")
        self.img_eye = images.get_image("eye16x16.png")
        self.img_eye_fill = images.get_image("eye_fill16x16.png")

        # tk variables for entry fields
        self.entry_val_website = tk.StringVar()
        self.entry_val_website.set(self.website)
        self.entry_val_password = tk.StringVar()
        self.entry_val_password.set(self.password)

        # Init Entry widgets for row values + Separators
        self.entry_website = ttk.Entry(self, textvariable=self.entry_val_website, state="readonly", width=30)
        self.separator_1 = ttk.Separator(self, orient="vertical")
        self.entry_password = ttk.Entry(self, textvariable=self.entry_val_password, state="readonly", show="*", width=30)
        self.separator_2 = ttk.Separator(self, orient="vertical")
        # Init Buttons
        #   Copy Button will change to Save-Changes-Button while in Edit-Mode
        #   Delete Button will change to Discard-Changes-Button while in Edit-Mode
        #   Eye-Button gets Transparent Image as a placeholder to not mess with Widget-Placement
        self.item_eye_button = ttk.Button(self, image=self.img_transparent, command=self.unhide_pw)
        self.item_copy_button = ttk.Button(self, image=self.img_copy, command=self.button_copy_click)
        self.item_delete_button = ttk.Button(self, image=self.img_delete, command=lambda: self.button_delete_click(True))
        self.item_edit_button = ttk.Button(self, image=self.img_edit, command=self.button_edit_click)

        # Place widgets
        self.entry_website.grid(row=self.row_id, column=0, padx=5, pady=5, sticky=tk.W)
        self.entry_password.grid(row=self.row_id, column=2, padx=5, pady=5, sticky=tk.W)
        self.separator_1.grid(row=self.row_id, column=1, padx=5, sticky="ns")
        self.item_eye_button.grid(row=self.row_id, column=3)
        self.separator_2.grid(row=self.row_id, column=4, padx=5, sticky="ns")
        # Buttons will be put on the grid by the mouse_enter event!

        # Widget Bindings
        # Entry-Events
        self.entry_website.bind("<Return>", self.save_changes)
        self.entry_password.bind("<Return>", self.save_changes)
        self.entry_website.bind("<Escape>", self.discard_changes)
        self.entry_password.bind("<Escape>", self.discard_changes)
        # Mouse Hover Events for Item highlighting
        self.bind('<Enter>', self.mouse_enter)
        self.bind('<Leave>', self.mouse_leave)
        # Eye-Image Highlighting
        self.item_eye_button.bind("<Enter>", lambda e: self.eye_button_change(hover=True))
        self.item_eye_button.bind("<Leave>", lambda e: self.eye_button_change(hover=False))

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
        else:   # Alternating color with row_id
            if self.row_id % 2 == 1:
                self.frame_style = "Item2.TFrame"
                self.entry_style = "Item2.TLabel"
            else:
                self.frame_style = "Item1.TFrame"
                self.entry_style = "Item1.TLabel"

        # add styling
        self.stylize_item_widgets(self.frame_style, self.entry_style)

        # Change State if Plus-Button is used
        if self.state == State.CREATE:
            self.change_state(State.CREATE)

    # Event - Mouse Hover over Item - highlights row
    def mouse_enter(self, event=None):
        # don't change colors if ListFrame is in edit-mode
        if self.state == State.DEFAULT:
            self.configure(style="MouseEnter.TFrame")
            self.entry_website.configure(style="MouseEnter.TLabel")
            self.entry_password.configure(style="MouseEnter.TLabel")
            self.item_eye_button.configure(style="MouseEnter.TLabel")
            self.eye_button_change(hover=False)     # Change from Transparent to Eye-Symbol

            # Place Buttons
            self.item_copy_button.grid(row=self.row_id, column=5)
            self.item_delete_button.grid(row=self.row_id, column=6, padx=5)
            self.item_edit_button.grid(row=self.row_id, column=7, padx=(0, 50))

    # Event - Mouse leaves Item - return to normal color
    def mouse_leave(self, event=None):
        # don't change colors if ListFrame is in edit-mode
        if self.state == State.DEFAULT:
            self.configure(style=self.frame_style)
            self.entry_website.configure(style=self.entry_style)
            self.entry_password.configure(style=self.entry_style)
            self.item_eye_button.configure(style=self.entry_style, image=self.img_transparent)  # Return to Transparent
            # Hide Buttons
            self.item_copy_button.grid_remove()
            self.item_delete_button.grid_remove()
            self.item_edit_button.grid_remove()

    def save_changes(self, event=None):
        if self.state != State.DEFAULT:
            # todo: Save Changes to Database
            self.change_state(State.DEFAULT)

    # revert to old values
    def discard_changes(self, event=None):
        if self.state == State.EDIT:
            self.entry_website.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)
            self.entry_website.insert(0, self.website_revert)
            self.entry_password.insert(0, self.password_revert)
            self.change_state(State.DEFAULT)
        # Remove Item if Changes are discarded in CREATE-Mode
        elif self.state == State.CREATE:
            self.button_delete_click(False)

    # if Item loses Focus while in edit-mode, user will be asked if changes should be saved
    def frame_lost_focus(self, event=None):
        if self.state != State.DEFAULT:
            if messagebox.askquestion("Discard change", "Save Changes?") == "no":
                self.discard_changes(event)
            else:
                self.change_state(State.DEFAULT)

    # Changes State of Item into one of these two:
    # - DEFAULT - Entries not editable
    # - EDIT: when edit button is pressed - Entries in box format and editable
    # - CREATE: when new row gets added with Plus-Button
    #    -> similar to EDIT with special Case: delete row if changes are discarded (handled in discard_changes())
    def change_state(self, state):
        self.state = state
        if self.state == State.DEFAULT:
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
            self.item_edit_button["image"] = images.get_image("bleistift.png")
            self.item_copy_button["command"] = self.button_copy_click
            self.item_delete_button["command"] = lambda: self.button_delete_click(True)
            self.item_edit_button["command"] = self.button_edit_click

            self.item_eye_button.configure(style=self.entry_style, image=self.img_transparent)
            self.item_copy_button.grid_remove()
            self.item_delete_button.grid_remove()
            self.item_edit_button.grid_remove()

        else:   # state == EDIT or CREATE
            entry_state = "normal"  # Entry will be editable

            # In Case of Edit-Cancel
            self.website_revert = self.entry_website.get()
            self.password_revert = self.entry_password.get()

            # Change Buttons - Bind Event and image
            self.item_copy_button["image"] = images.get_image("generate16x16.png")
            self.item_delete_button["image"] = images.get_image("save16x16.png")
            self.item_edit_button["image"] = images.get_image("cross16x16.png")
            self.eye_button_change(hover=False)     # show Eye-Image
            self.item_copy_button["command"] = self.generate_pw
            self.item_delete_button["command"] = self.save_changes
            self.item_edit_button["command"] = self.discard_changes

            # Place Buttons for new Entry
            if self.state == State.CREATE:
                self.item_copy_button.grid(row=self.row_id, column=5)
                self.item_delete_button.grid(row=self.row_id, column=6, padx=5)
                self.item_edit_button.grid(row=self.row_id, column=7, padx=(0, 50))
                self.eye_button_change(hover=False)  # Change from Transparent to Eye-Symbol
                # Highlight Item
                self["style"] = "MouseEnter.TFrame"
                self.item_eye_button["style"] = "MouseEnter.TLabel"

            if self.entry_style == "Item1.TLabel":
                entry_style = "Item1.TEntry"
            else:
                entry_style = "Item2.TEntry"

            # set Focus on Website name and mark entire text
            self.entry_website.focus_set()
            self.entry_website.select_range(0, tk.END)

        self.entry_website["state"] = self.entry_password["state"] = entry_state
        self.entry_website["style"] = self.entry_password["style"] = entry_style

    # Copy password to Clipboard
    def button_copy_click(self):
        self.clipboard_clear()
        self.clipboard_append(self.entry_password.get())

    # Replaces Method for Copy-Button on EDIT- or CREATE-State
    # Generates Random Password with Generator-Object
    def generate_pw(self):
        # Access Generator in MainFrame Class
        self.entry_val_password.set(self.parent.parent.generator.generate_pw())

    # Copy password to Clipboard
    def button_delete_click(self, ask_question):
        # todo: Delete in Database
        if ask_question:
            # Color Item-Background red during Delete-Confirmation
            self["style"] = "OnDelete.TFrame"
            self.entry_website["style"] = "OnDelete.TLabel"
            self.entry_password["style"] = "OnDelete.TLabel"
            self.item_eye_button["style"] = "OnDelete.TLabel"
            self.unbind("<Leave>")  # Temporarily unbind Leave-Event, so Item stays red during Delete-Confirmation
            if messagebox.askquestion("Delete Password", f"Delete Password for {self.entry_website.get()}?") == "no":
                self.bind("<Leave>", self.mouse_leave)  # bind again
                self.mouse_leave()  # manual leave event to return to normal colors
                return
        self.delete_item()
        self.parent.update()    # Redraw ListFrame before updating Scrollbar
        self.parent.canvas.configure(scrollregion=self.parent.canvas.bbox("all"))  # Update Scrollbar region
        self.parent.scrollbar_click_configure()

    def delete_item(self):
        self.grid_forget()
        self.destroy()
        ListFrame.items.remove(self)
        ListFrame.alternate_colorscheme()
        # ListFrame.row_down_count()

    def unhide_pw(self):
        self.entry_password["show"] = ""
        self.pw_is_hidden = False
        self.eye_button_change(hover=True)

    def hide_pw(self):
        self.entry_password["show"] = "*"
        self.pw_is_hidden = True
        self.eye_button_change(hover=True)

    # Changes the Image of the Eye-Button, according to the Hiding-State of the password
    # Fill-variant of Image gets used on Mouse-Hover
    def eye_button_change(self, hover):
        if self.pw_is_hidden:
            self.item_eye_button["command"] = self.unhide_pw
            if hover:
                self.item_eye_button["image"] = self.img_eye_fill
            else:
                self.item_eye_button["image"] = self.img_eye
        else:
            self.item_eye_button["command"] = self.hide_pw
            if hover:
                self.item_eye_button["image"] = self.img_eye_crossed_fill
            else:
                self.item_eye_button["image"] = self.img_eye_crossed

    # Copy password to Clipboard
    def button_edit_click(self):
        self.change_state(State.EDIT)

    def stylize_item_widgets(self, frame_style, entry_style):
        self["style"] = frame_style
        self.entry_website["style"] = entry_style
        self.entry_password["style"] = entry_style
        self.item_eye_button["style"] = entry_style


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
        self.grid(row=2, column=0, padx=5, pady=(0, 5), sticky="nsew")
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

        # Create Items
        # Loop sets up items in List format
        # todo: Database fetch of all Password entries
        entries = db_functions.get_entries()
        for entry in entries:
            # Create new Item and store in List
            # self gets passed as second argument as a parent
            ListFrame.items.append(Item(self.list_frame, self, ListFrame.row_count, entry["name"], entry["pw"], False, State.DEFAULT))
            ListFrame.row_up_count()

        # Plus-Button to add a new row
        self.button_add_row = ttk.Button(self.list_frame, image=self.img_btn_add_row, command=self.add_row, padding="3 3 3 3")
        self.button_add_row.grid(row=ListFrame.row_count+1, column=0, sticky="w", padx=3, pady=3)
        # Change background Color on Mouseclick
        self.button_add_row.bind("<ButtonPress-1>", lambda e: func.style_change(self.button_add_row, "OnClick.TLabel"))
        self.button_add_row.bind("<ButtonRelease-1>", lambda e: func.style_change(self.button_add_row, "Item2.TLabel"))
        # Change Background Color on Mouse-Hover
        self.button_add_row.bind("<Enter>",
                                 lambda e: func.style_change(self.button_add_row, "MouseEnter.TLabel"))
        self.button_add_row.bind("<Leave>",
                                 lambda e: func.style_change(self.button_add_row, "Item2.TLabel"))

        # Styles
        self.list_frame["style"] = "List.TFrame"
        self.button_add_row["style"] = "Item2.TLabel"

    # Add new Password Line
    def add_row(self, event=None):
        row_id = ListFrame.row_count
        self.button_add_row.grid(row=row_id+1)
        # Create new Item and store in List
        ListFrame.items.append(Item(self.list_frame, self, row_id, "", "", True, State.CREATE))
        ListFrame.row_up_count()
        self.list_frame.update()    # Frame needs to be redrawn before updating the Scrollbar region
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))     # Update Scrollbar region
        self.scrollbar_click_configure()

    # Resizes the Canvas and the window inside
    def canvas_configure(self, event):
        canvas_width = event.width
        self.canvas.itemconfig("frame", width=canvas_width)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.scrollbar_click_configure()

    # This Method enables/disables the functionality to drag the Scrollbar with Mouseclick
    # if enabled: Leads to weird Behaviour if Content(Password List) is smaller than Canvas:
    #       -> List will be able to scroll down leaving unwanted Space above first List-Entry
    # Solution: Drag-Functionality will be disabled if List is smaller than Canvas (and enabled if otherwise)
    def scrollbar_click_configure(self):
        # Checks if Scrollbar is both at Top- and Bottom-Position
        if self.canvas.yview() == (0.0, 1.0):
            self.scrollbar["command"] = ""
        else:
            self.scrollbar["command"] = self.canvas.yview

    # Bind Mousewheel to Scrollbar when Mouse enters List Frame
    # self.canvas.bind has no effect
    # Therefore the usage of bind_all - needs to be unbound after Mouse Leave event
    def bind_to_mousewheel(self, event=None):
        if platform == "win32" or platform == "darwin":     # Windows-System or MAC OS
            self.canvas.bind_all("<MouseWheel>", self.mousewheel_event)
        elif "linux" in platform:   # older versions of python specify major linux versions (linux2, linux3, ...)
            # Bindings for Up and Down Scroll
            self.canvas.bind_all("<Button-4>", self.mousewheel_event)
            self.canvas.bind_all("<Button-5>", self.mousewheel_event)

    # Disable Mousewheel bind when Mouse leaves List Frame
    def unbind_to_mousewheel(self, event=None):
        if platform == "win32" or platform == "darwin":     # Windows-System or MAC OS
            self.canvas.unbind_all("<MouseWheel>")
        elif "linux" in platform:   # older versions of python specify major linux versions (linux2, linux3, ...)
            # Bindings for Up and Down Scroll
            self.canvas.unbind_all("<Button-4>")
            self.canvas.unbind_all("<Button-5>")

    # Scrolls List Frame
    def mousewheel_event(self, event):
        # check if Frame is smaller than the canvas - only scroll if false
        if self.canvas.yview() == (0.0, 1.0):
            return
        if platform == "win32":     # Windows-System 
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        elif platform == "darwin":  # event.delta doesn't need to be modified on macOS
            self.canvas.yview_scroll(int(-1 * event.delta), "units")
        elif "linux" in platform:   # older versions of python specify major linux versions (linux2, linux3, ...)
            # event.delta can't be used on linux system because it is always 0
            if event.num == 4:  # <Button-4> Downscroll
                self.canvas.yview_scroll(-1, "units")
            if event.num == 5:  # <Button-5> Upscroll
                self.canvas.yview_scroll(+1, "units")

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
        self.grid(row=0, column=0, sticky="nsew")
        # Expand List Frame on Window Resize
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        # Styles
        self["style"] = "Main.TFrame"

        # Create Generator Object for Password-Generator
        self.generator = gen.Generator()

        # Create Sub frames
        self.top_bar = TopBar(self)
        self.list_frame = ListFrame(self)
        ttk.Separator(self, orient="horizontal").grid(row=3, column=0, sticky="we")     # border-top for Footer
        self.footer = Footer(self)
