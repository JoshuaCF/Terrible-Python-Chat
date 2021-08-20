import socket
import threading

from typing import List, Union, TYPE_CHECKING
from gui import ChatWindow, ColorData

if TYPE_CHECKING:
    from main import InputHandler


def encode_packet(msg: str, colors: Union[List[ColorData], str] = None):
    col_count: int

    packet: bytes

    if type(colors) == list:
        col_count = len(colors)
    elif type(colors) == str:
        col_count = 1
        colors = [ColorData(0, len(msg), colors)]
    else:
        col_count = 0

    packet = col_count.to_bytes(1, "big", signed=False)

    if colors is not None:
        for col_dat in colors:
            packet += col_dat.start_index.to_bytes(2, "big", signed=False)
            packet += col_dat.end_index.to_bytes(2, "big", signed=False)
            packet += col_dat.color[1:].encode()

    packet += msg.encode()
    print(packet)
    return packet


def decode_packet(packet: bytes):
    print(packet)
    col_size = 10  # Size in bytes of one ColorData

    col_count = int.from_bytes(packet[0:1], "big", signed=False)
    colors: List[ColorData] = []
    for i in range(col_count):
        start_index = int.from_bytes(packet[1 + col_size * i:3 + col_size * i], "big", signed=False)
        end_index = int.from_bytes(packet[3 + col_size * i:5 + col_size * i], "big", signed=False)
        color = "#" + packet[5 + col_size * i:11 + col_size * i].decode()
        colors.append(ColorData(start_index, end_index, color))
    msg = packet[1 + col_size * col_count:].decode()
    return msg, colors


class NetworkHandler:
    connections: List[socket.socket]
    hosting: bool

    chat_window: ChatWindow
    input_handler: "InputHandler"

    def __init__(self, chat_window: ChatWindow):
        self.chat_window = chat_window
        self.hosting = False
        self.connections = []

    def broadcast(self, packet: bytes):
        try:
            for c in self.connections:
                c.send(packet)
        except Exception as e:
            print(e)

    def monitor_socket(self, s: socket.socket):
        while True:
            try:
                packet = s.recv(4096)
                if self.hosting:
                    self.broadcast(packet)

                msg, colors = decode_packet(packet)
                self.chat_window.log_msg(msg, colors)
            except ConnectionResetError as e:
                print(e)
                if self.hosting:
                    address = s.getsockname()
                    s.close()
                    self.connections.remove(s)

                    dc_msg = "[SERVER] " + address[0] + " has disconnected."
                    server_colors = [ColorData(1, 7, "#CC3333"), ColorData(8, len(dc_msg), "#33AA33")]
                    self.broadcast(encode_packet(dc_msg, server_colors))  # TODO: rainbow text
                    self.chat_window.log_msg(dc_msg, server_colors)
                else:
                    self.connections.remove(s)
                    s.close()
                    self.chat_window.log_msg("Connection to the server has been lost.")
                    self.chat_window.log_msg(
                        "Type 'host' to host a chat, or type in the ip address of a host you would like to join.")
                    self.input_handler.connected = False
                break

    def host_chat(self):
        self.hosting = True

        self.chat_window.log_msg("Hosting chat...")

        try:
            s = socket.socket()

            # I'm using this port because Minecraft uses it and myself along with people I test this
            # program with already have that port open.
            s.bind(("", 25565))

            s.listen(3)
            self.chat_window.log_msg("Done!")
            while True:
                connection, address = s.accept()

                self.connections.append(connection)
                monitor_thread = threading.Thread(target=self.monitor_socket, args=(connection, ), daemon=True)
                monitor_thread.start()

                connect_msg = "[SERVER] " + address[0] + " has connected."

                self.chat_window.log_msg(connect_msg)
                self.broadcast(encode_packet(connect_msg))
        except Exception as e:
            print(e)

    def connect(self, host: str):
        connection = socket.socket()
        connection.connect((host, 25565))

        monitor_thread = threading.Thread(target=self.monitor_socket, args=(connection, ), daemon=True)
        monitor_thread.start()

        self.connections.append(connection)