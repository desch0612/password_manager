import tkinter.ttk as ttk
from sys import platform


# Colors
RED = "#ffaaaa"
LIGHT_GRAY = "#eeeeee"
LIGHTER_GRAY = "#f3f3f3"
DARK_GRAY = "#dddddd"
DARKER_GRAY = "#aaaaaa"


def load_styles():
    style = ttk.Style()  # Styling parameter for ttk-Widgets
    if platform == "darwin":    # Mac OS
        style.theme_use('default')

    # Top Frame
    style.configure("Top.TFrame", background="white")
    style.configure("Top.TLabel", background="white")

    # Footer
    style.configure("Footer.TFrame", background=LIGHTER_GRAY)

    # Headline Frame
    style.configure("Headline.TFrame", background="white")
    style.configure("Headline.TLabel", background="white")

    # Item Frame
    style.configure("Item1.TFrame", background=LIGHT_GRAY)
    style.configure("Item1.TLabel", background=LIGHT_GRAY)
    style.configure("Item1.TEntry", background=LIGHT_GRAY)
    style.configure("Item2.TFrame", background="white")
    style.configure("Item2.TLabel", background="white")
    style.configure("Item2.TEntry", background="white")
    style.configure("OnDelete.TFrame", background=RED)
    style.configure("OnDelete.TLabel", background=RED)
    style.configure("MouseEnter.TFrame", background=DARK_GRAY)
    style.configure("MouseEnter.TLabel", background=DARK_GRAY)
    style.configure("OnClick.TLabel", background=DARKER_GRAY)

    # List Frame
    style.configure("List.TFrame", background="white")

    # Main Frame
    style.configure("Main.TFrame", background="white")

    # LoginPage
    style.configure("Loginbox.TLabel", background=DARK_GRAY)
    style.configure("Loginbox.TFrame", background=DARK_GRAY)
    style.configure("Loginbox.TCheckbutton", background=DARK_GRAY)
