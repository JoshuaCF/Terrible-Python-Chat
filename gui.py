from tkinter import *
from typing import List


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
        self.chat_box.config(state=DISABLED, width=140, height=50, wrap=WORD)  # TODO: make shit resize
        self.chat_box.pack(side=TOP, padx=4, pady=4)

        self.input_box = Entry(self.window, **self.text_style)
        self.input_box.config(width=140)
        self.input_box.pack(side=TOP, padx=4, pady=4)

        # TODO: Make chat log support colors
        # TODO: Add name box and color wheel

    def log_msg(self, msgs: List[str]):
        self.chat_box.config(state=NORMAL)

        prev_view = self.chat_box.yview()

        for msg in msgs:
            self.chat_box.insert(END, msg + "\n")

        if prev_view[1] == 1:
            self.chat_box.yview_moveto(1)
        self.chat_box.config(state=DISABLED)

    def clear_entry(self):
        self.input_box.delete(0, END)

    def get_entry(self) -> str:
        return self.input_box.get()