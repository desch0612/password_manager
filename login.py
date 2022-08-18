import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import frame_switcher


# encapsulates entire Login-window
class LoginPage(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.parent = parent

        # Frame placement and Expand-Behaviour
        self.grid(row=0, column=0, sticky="nsew")

        # Styles
        self["style"] = "Main.TFrame"

        # create login box
        self.login_box = LoginBox(self)

        # Place loginbox in the center of the screen
        self.login_box.place(relx=0.5, rely=0.5, anchor="center")


# holds Login entry-fields and buttons
class LoginBox(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.parent = parent

        # Styles
        self["style"] = "Loginbox.TFrame"

        # Create widgets
        self.label = ttk.Label(self, text="Enter your Master password:", style="Loginbox.TLabel")
        self.entry_pw_value = tk.StringVar()    # Variable for entry-field
        self.entry_pw = ttk.Entry(self, textvariable=self.entry_pw_value, width=30)
        self.login_button = ttk.Button(self, text="Login", command=self.validate_master_password)
        self.checkbox_ignore_value = tk.IntVar(value=0)  # Variable for Checkbox
        self.checkbox_ignore = ttk.Checkbutton(self, text="Debug: Ignore password validation",
                                               variable=self.checkbox_ignore_value, style="Loginbox.TCheckbutton")

        # Place widgets
        self.label.grid(row=0, column=0, padx=(10, 0), pady=(10, 0))
        self.entry_pw.grid(row=1, column=0, padx=10, pady=10)
        self.login_button.grid(row=2, column=0, padx=10)
        self.checkbox_ignore.grid(row=3, column=0, padx=10, pady=10)

        # Key events for Enter-Button
        self.login_button.bind("<Return>", lambda e: self.validate_master_password())
        self.entry_pw.bind("<Return>", lambda e: self.validate_master_password())
        self.checkbox_ignore.bind("<Return>", lambda e: self.toggle_checkbox())

    def validate_master_password(self):
        if self.checkbox_ignore_value.get():
            frame_switcher.switch_frame("main_page")
        elif self.entry_pw.get() == "123456":
            frame_switcher.switch_frame("main_page")
        else:
            messagebox.showerror("Incorrect Password", "Password is incorrect")

    def toggle_checkbox(self):
        if self.checkbox_ignore_value.get():
            self.checkbox_ignore_value.set(0)
        else:
            self.checkbox_ignore_value.set(1)
