import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import frame_switcher
import db_functions


# encapsulates entire Login-window
class LoginPage(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.is_registered = False

        # Frame placement and Expand-Behaviour
        self.grid(row=0, column=0, sticky="nsew")

        # Styles
        self["style"] = "Main.TFrame"

        # Check if user already made a master password
        self.is_registered = db_functions.check_table_existence("User")

        if self.is_registered:
            # create login box
            self.box = LoginBox(self)
        else:
            # create Register box
            self.box = RegisterBox(self)

        # Place box in the center of the screen
        self.box.place(relx=0.5, rely=0.5, anchor="center")


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
        self.entry_pw = ttk.Entry(self, textvariable=self.entry_pw_value, width=30, show="*")
        self.login_button = ttk.Button(self, text="Login", command=self.validate_master_password)
        self.checkbox_ignore_value = tk.IntVar(value=0)  # Variable for Checkbox
        self.checkbox_autologin_value = tk.IntVar(value=0)  # Variable for Checkbox
        self.checkbox_autologin = ttk.Checkbutton(self, text="Automatic login",
                                               variable=self.checkbox_autologin_value, style="Loginbox.TCheckbutton")
        self.checkbox_ignore = ttk.Checkbutton(self, text="Debug: Ignore password validation",
                                               variable=self.checkbox_ignore_value, style="Loginbox.TCheckbutton")

        # Place widgets
        self.label.grid(row=0, column=0, padx=(10, 0), pady=(10, 0))
        self.entry_pw.grid(row=1, column=0, padx=10, pady=10)
        self.login_button.grid(row=2, column=0, padx=10)
        self.checkbox_autologin.grid(row=3, column=0, padx=10, pady=(10, 0), sticky="w")
        self.checkbox_ignore.grid(row=4, column=0, padx=10, pady=10, sticky="w")

        # Key events for Enter-Button
        self.login_button.bind("<Return>", lambda e: self.validate_master_password())
        self.entry_pw.bind("<Return>", lambda e: self.validate_master_password())
        self.checkbox_ignore.bind("<Return>", lambda e: self.toggle_checkbox(self.checkbox_ignore_value))
        self.checkbox_autologin.bind("<Return>", lambda e: self.toggle_checkbox(self.checkbox_autologin_value))

        # set focus on entry
        self.entry_pw.focus_set()

    def validate_master_password(self):
        if self.checkbox_ignore_value.get():
            frame_switcher.switch_frame("main_page")
        elif self.entry_pw.get() == db_functions.fetch_mp():   # todo: hash self.entry_pw
            frame_switcher.switch_frame("main_page")
        else:
            messagebox.showerror("Incorrect Password", "Password is incorrect")

    @staticmethod
    def toggle_checkbox(checkbox):
        if checkbox.get():
            checkbox.set(0)
        else:
            checkbox.set(1)


# holds Login entry-fields and buttons
class RegisterBox(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.parent = parent

        # Styles
        self["style"] = "Loginbox.TFrame"

        # Create widgets
        self.label = ttk.Label(self, text="Enter your new Master password:", style="Loginbox.TLabel")
        self.label_confirm = ttk.Label(self, text="Confirm your password:", style="Loginbox.TLabel")
        self.entry_pw_value = tk.StringVar()    # Variable for entry-field
        self.entry_pw_confirm_value = tk.StringVar()  # Variable for entry-field
        self.entry_pw = ttk.Entry(self, textvariable=self.entry_pw_value, width=30, show="*")
        self.entry_pw_confirm = ttk.Entry(self, textvariable=self.entry_pw_confirm_value, width=30, show="*")
        self.register_button = ttk.Button(self, text="Register", command=self.register_master_password)

        # Place widgets
        self.label.grid(row=0, column=0, padx=(10, 0), pady=(10, 0))
        self.entry_pw.grid(row=1, column=0, padx=10, pady=10)
        self.label_confirm.grid(row=2, column=0, padx=(10, 0), pady=(10, 0))
        self.entry_pw_confirm.grid(row=3, column=0, padx=10, pady=10)
        self.register_button.grid(row=4, column=0, padx=10, pady=(0, 10))

        # Key events for Enter-Button
        self.register_button.bind("<Return>", lambda e: self.register_master_password())
        self.entry_pw.bind("<Return>", lambda e: self.register_master_password())
        self.entry_pw_confirm.bind("<Return>", lambda e: self.register_master_password())

        # set focus on entry
        self.entry_pw.focus_set()

    def register_master_password(self):
        mp = self.entry_pw.get()

        if mp:
            # password entry is not empty
            # check for confirmation match
            if self.entry_pw.get() == self.entry_pw_confirm.get():
                # todo: hash master_password
                db_functions.create_user_table(mp)
                frame_switcher.switch_frame("main_page")
            else:
                messagebox.showerror("Master password", "Confirm doesn't match entered password")
        else:
            messagebox.showerror("Master password", "Please enter a master password")
