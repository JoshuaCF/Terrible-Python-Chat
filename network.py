import socket
import threading
from typing import List, TYPE_CHECKING


if TYPE_CHECKING:
    from gui import ChatWindow


class NetworkHandler:
    connections: List[socket.socket]
    hosting: bool

    chat_window: "ChatWindow"  # I don't really know what to call this variable.

    def __init__(self, chat_window: "ChatWindow"):
        self.chat_window = chat_window
        self.hosting = False
        self.connections = []

    def broadcast(self, msg: str):
        try:
            for c in self.connections:
                c.send(msg.encode())
        except Exception as e:
            print(e)

    def monitor_socket(self, s: socket.socket):
        while True:
            try:
                msg = s.recv(4096).decode()
                if self.hosting:
                    self.chat_window.log_msg([msg])
                    self.broadcast(msg)
                else:
                    self.chat_window.log_msg([msg])
            except Exception as e:
                print(e)

    def host_chat(self):
        self.hosting = True

        self.chat_window.log_msg(["Hosting chat..."])

        try:
            s = socket.socket()

            # I'm using this port because Minecraft uses it and myself along with people I test this
            # program with already have that port open.
            s.bind(("", 25565))

            s.listen(3)
            self.chat_window.log_msg(["Done!"])
            while True:
                connection, address = s.accept()

                self.connections.append(connection)
                monitor_thread = threading.Thread(target=self.monitor_socket, args=(connection, ), daemon=True)
                monitor_thread.start()

                connect_msg = "[SERVER] " + address[0] + ":" + str(address[1]) + " has connected."

                self.chat_window.log_msg([connect_msg])
                self.broadcast(connect_msg)
        except Exception as e:
            print(e)

    def connect(self, host: str):
        connection = socket.socket()
        connection.connect((host, 25565))

        monitor_thread = threading.Thread(target=self.monitor_socket, args=(connection, ), daemon=True)
        monitor_thread.start()

        self.connections.append(connection)