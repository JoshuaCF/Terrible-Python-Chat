from tkinter import *


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
    input_box: Text

    def __init__(self):
        self.window = Tk()
        self.window.config(background=self.bg_color)
        self.window.title("Chat with friends!!!! w")

        self.chat_box = Text(self.window, **self.text_style)
        self.chat_box.insert(END, "Would you like to host or join a chat? Type 'host' or 'join'\n")
        self.chat_box.config(state=DISABLED, width=140, height=50)
        self.chat_box.pack(side=TOP, padx=4, pady=4)

        self.input_box = Text(self.window, **self.text_style)
        self.input_box.config(width=140, height=10)
        # self.input_box.bind("<Return>", user_input)
        self.input_box.pack(side=TOP, padx=4, pady=4)

        self.window.mainloop()

    def log_msg(self, msgs):
        self.chat_box.config(state=NORMAL)

        for msg in msgs:
            self.chat_box.insert(END, msg + "\n")

        self.chat_box.config(state=DISABLED)