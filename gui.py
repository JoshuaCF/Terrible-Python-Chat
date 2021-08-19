from tkinter import *
from typing import List, Union


class ColorData:
    start_index: int
    end_index: int
    color: str

    def __init__(self, start_index: int, end_index: int, color: str):
        self.start_index = start_index
        self.end_index = end_index
        self.color = color


class ChatWindow:
    bg_color = "#303030"
    fg_color = "#d0d0d0"
    active_bg = "#404040"
    active_fg = "#e0e0e0"
    select_bg = "#5050f0"
    default_font = ("Courier", 10)

    button_style = {"background": bg_color,
                    "foreground": fg_color,
                    "activebackground": active_bg,
                    "activeforeground": active_fg,
                    "relief": RAISED,
                    "font": default_font}
    label_style = {"background": bg_color,
                   "foreground": fg_color,
                   "relief": FLAT,
                   "font": default_font}
    frame_style = {"background": bg_color,
                   "borderwidth": 0}
    listbox_style = {"background": active_bg,
                     "foreground": active_fg,
                     "font": default_font,
                     "relief": FLAT,
                     "highlightthickness": 0,
                     "selectbackground": select_bg}
    text_style = {"background": active_bg,
                  "foreground": active_fg,
                  "font": default_font,
                  "relief": FLAT,
                  "highlightthickness": 0,
                  "selectbackground": select_bg,
                  "insertbackground": active_fg}

    window: Tk
    chat_box: Text
    input_box: Entry

    def __init__(self):
        # TODO: Make default size based on native resolution

        self.window = Tk()
        self.window.config(background=self.bg_color)
        self.window.title("Chat with friends!!!! w")

        self.chat_box = Text(self.window, **self.text_style)
        self.chat_box.config(state=DISABLED, width=40, height=8, wrap=WORD)
        self.chat_box.pack(side=TOP, padx=4, pady=4, expand=TRUE, fill=BOTH)

        self.input_box = Entry(self.window, **self.text_style)
        self.input_box.config(width=40)
        self.input_box.pack(side=TOP, padx=4, pady=4, expand=FALSE, fill=X)

        # TODO: Add name box and color wheel

    def log_msg(self, msg: str, colors: Union[List[ColorData], str] = None):
        self.chat_box.config(state=NORMAL)

        view_is_bottomed = self.chat_box.yview()[1] == 1

        self.chat_box.mark_set("prev_end", END + " - 1 chars")  # Weird tk behavior makes the - 1 chars necessary.
        self.chat_box.mark_gravity("prev_end", LEFT)
        self.chat_box.insert(END, msg + "\n")

        if colors is not None:
            if type(colors) == list:
                for col_dat in colors:
                    self.chat_box.tag_add(col_dat.color,
                                          "prev_end + {} chars".format(col_dat.start_index),
                                          "prev_end + {} chars".format(col_dat.end_index))
                    self.chat_box.tag_configure(col_dat.color, foreground=col_dat.color)
            else:
                self.chat_box.tag_add(colors, "prev_end", END + " - 1 chars")
                self.chat_box.tag_configure(colors, foreground=colors)

        if view_is_bottomed:  # If already scrolled down all the way, keep it so
            self.chat_box.yview_moveto(1)

        self.chat_box.config(state=DISABLED)

    def clear_entry(self):
        self.input_box.delete(0, END)

    def get_entry(self) -> str:
        return self.input_box.get()