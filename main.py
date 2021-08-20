import threading
from tkinter import colorchooser

from gui import ChatWindow, ColorData
from network import NetworkHandler, encode_packet


class InputHandler:
    net_handler: NetworkHandler
    chat_window: ChatWindow

    connected: bool
    naming: bool

    name: str
    name_color: str

    def __init__(self, net_handler, chat_window):
        self.net_handler = net_handler
        self.chat_window = chat_window

        self.chat_window.input_box.bind("<Return>", self.handle_input)
        self.chat_window.select_color.config(command=self.set_name_color)

        self.name_color = self.chat_window.active_fg

        self.connected = False
        self.naming = True

    def handle_input(self, _):
        msg = self.chat_window.get_entry()
        self.chat_window.clear_entry()

        if self.naming:
            self.name = msg
            self.naming = False

            self.chat_window.log_msg(
                "Type 'host' to host a chat, or type in the ip address of a host you would like to join.")
        elif self.connected:
            msg = "<" + self.name + ">" + " " + msg
            self.net_handler.broadcast(encode_packet(msg, [ColorData(1, len(self.name)+1, self.name_color)]))
            if self.net_handler.hosting:
                self.chat_window.log_msg(msg, [ColorData(1, len(self.name)+1, self.name_color)])
        else:
            try:
                if msg == "host":
                    host_thread = threading.Thread(target=self.net_handler.host_chat, daemon=True)
                    host_thread.start()
                else:
                    self.net_handler.connect(msg)
                self.connected = True
            except Exception as e:
                print(e)

    def set_name_color(self):
        self.name_color = colorchooser.askcolor()[1]


def main():
    chat_window = ChatWindow()
    net_handler = NetworkHandler(chat_window)

    input_handler = InputHandler(net_handler, chat_window)
    net_handler.input_handler = input_handler

    chat_window.log_msg("Enter a name to go by.")
    chat_window.window.mainloop()


if __name__ == "__main__":
    main()