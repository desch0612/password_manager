#############################################
#   First Concept of Password Manager GUI   #
#############################################


import tkinter as tk
import tkinter.ttk as ttk   # module for themed widgets - will be used instead of tk if available
import mainpage as mainpage
import images as images
import styles as styles


# Class for initial Window config
class MainApplication(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)    # Constructor of super-class
        self.parent = parent

        # Set up Window Attributes
        self.parent.title("Password Manager")
        self.parent.minsize(width=600, height=400)
        self.parent.rowconfigure(0, weight=1)
        self.parent.columnconfigure(0, weight=1)

        # Load images
        images.load_images()

        # Load Styles
        styles.load_styles()

        # Main Page contains main Window for Password List
        self.main_page = mainpage.MainPage(self.parent)     # todo: Maybe use self instead of root


def main():
    root = tk.Tk()
    pw_manager = MainApplication(root)
    pw_manager.mainloop()


if __name__ == "__main__":
    main()
