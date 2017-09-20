"""Python module for showing alpha key with Tk GUI"""
from tkinter import Tk, Frame, Label, SOLID, LEFT


def alpha_tk_view(title, key, size, row_len):
    """Function starts main loop for showing alpha key"""
    root = Tk()
    root.title(title)
    for i in range(int(row_len)):
        frame = Frame(root, borderwidth=0, relief=SOLID)
        for char in key[i * 8: i * 8 + 8]:
            subframe = Frame(frame, borderwidth=1, relief=SOLID)
            label = Label(subframe, text=char,
                          font=("Liberation Mono", int(size)))
            subframe.pack(side=LEFT)
            label.pack()
        frame.pack()
    root.mainloop()
