import tkinter as tk


# loads images into global variables in order to not get garbage collected
def load_images():
    global glob_img_settings
    global glob_img_add
    global glob_img_copy
    global glob_img_edit
    global glob_img_image_not_found
    global glob_img_delete
    global glob_img_save
    global glob_img_cancel
    glob_img_add = tk.PhotoImage(file="icons/plus16x16.png")
    glob_img_settings = tk.PhotoImage(file="icons/einstellungen.png")
    glob_img_copy = tk.PhotoImage(file="icons/kopieren.png")
    glob_img_edit = tk.PhotoImage(file="icons/bleistift.png")
    glob_img_image_not_found = tk.PhotoImage(file="icons/frage-quadrat.png")
    glob_img_delete = tk.PhotoImage(file="icons/trashcan.png")
    glob_img_save = tk.PhotoImage(file="icons/save16x16.png")
    glob_img_cancel = tk.PhotoImage(file="icons/cross16x16.png")


# returns global image var with specified filename
# glob_img_image_not_found as default image
def get_image(image):
    switch = {
        "einstellungen.png": glob_img_settings,
        "bleistift.png": glob_img_edit,
        "kopieren.png": glob_img_copy,
        "trashcan.png": glob_img_delete,
        "plus16x16.png": glob_img_add,
        "save16x16.png": glob_img_save,
        "cross16x16.png": glob_img_cancel
    }
    return switch.get(image, glob_img_image_not_found)

