frames = {}


def add_frame(name, frame):
    frames.update({name: frame})


def switch_frame(name):
    frame = frames.get(name)
    frame.tkraise()
