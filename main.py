import threading

from gui import ChatWindow, ColorData
from network import NetworkHandler


class InputHandler:
    net_handler: NetworkHandler
    chat_window: ChatWindow

    connected: bool
    naming: bool

    name: str

    def __init__(self, net_handler, chat_window):
        self.net_handler = net_handler
        self.chat_window = chat_window

        self.chat_window.input_box.bind("<Return>", self.handle_input)

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
            self.net_handler.broadcast(msg)
            if self.net_handler.hosting:
                self.chat_window.log_msg(msg)
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


def main():
    chat_window = ChatWindow()
    net_handler = NetworkHandler(chat_window)

    InputHandler(net_handler, chat_window)

    chat_window.log_msg("Enter a name to go by.")
    chat_window.window.mainloop()


if __name__ == "__main__":
    main()