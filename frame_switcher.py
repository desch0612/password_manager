frames = {}


def add_frame(name, frame):
    frames.update({name: frame})


def switch_frame(name):
    frame = frames.get(name)
    frame.tkraise()
    if name == "login_page":
        frame.show_frame()
