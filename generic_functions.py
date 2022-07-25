# This File is for functions that can be used by more Frame-Classes


# event Functions - gets used for widget binds like Mouseclick or Mouse-Hover
def style_change(widget, style, event=None):
    widget["style"] = style


def add_font_underline(widget, font, font_size):
    widget["font"] = (font, font_size, "underline")


def remove_font_underline(widget, font, font_size):
    widget["font"] = (font, font_size)
