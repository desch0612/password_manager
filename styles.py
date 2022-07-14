import tkinter.ttk as ttk


def load_styles():
    style = ttk.Style()  # Styling parameter for ttk-Widgets
    # Top Frame
    style.configure("Top.TFrame", background="#aaaaaa")
    style.configure("Top.TLabel", background="#aaaaaa")

    # Headline Frame
    style.configure("Headline.TFrame", background="white")
    style.configure("Headline.TLabel", background="white")

    # Item Frame
    style.configure("Item1.TFrame", background="#eeeeee")
    style.configure("Item1.TLabel", background="#eeeeee")
    style.configure("Item2.TFrame", background="white")
    style.configure("Item2.TLabel", background="white")
    style.configure("MouseEnter.TFrame", background="#dddddd")
    style.configure("MouseEnter.TLabel", background="#dddddd")

    # List Frame
    style.configure("List.TFrame", background="white")

    # Main Frame
    style.configure("Main.TFrame", background="white")