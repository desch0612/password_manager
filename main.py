#############################################
#   First Concept of Password Manager GUI   #
#############################################


import tkinter as tk
import tkinter.ttk as ttk   # module for themed widgets - will be used instead of tk if available
import mainpage
import login
import images
import styles
import frame_switcher


# Class for initial Window config
class MainApplication(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)    # Constructor of super-class
        self.parent = parent

        # Set up Window Attributes
        self.parent.title("Password Manager")
        self.parent.minsize(width=800, height=500)
        self.parent.rowconfigure(0, weight=1)
        self.parent.columnconfigure(0, weight=1)

        # Load images
        images.load_images()

        # Load Styles
        styles.load_styles()

        # Main Page contains main Window for Password List
        self.main_page = mainpage.MainPage(self.parent)     # todo: Maybe use self instead of root
        # self.login_page = login.LoginPage(self.parent)

        # Add Main- and Login page to frame collection for switch-ability
        frame_switcher.add_frame("main_page", self.main_page)
        # frame_switcher.add_frame("login_page", self.login_page)

        # Show Login page
        # self.login_page.tkraise()


def main():
    root = tk.Tk()
    pw_manager = MainApplication(root)
    pw_manager.mainloop()


if __name__ == "__main__":
    main()
