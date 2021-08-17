import socket
import threading


state = 0


def watch_socket(s: socket.socket):
    while True:
        try:
            log_msg([s.recv(2048).decode()])  # I can't find any documentation about what sorts of errors this can throw
        except Exception as e:  # So I'm doing this awfulness.
            # I literally hate Python's docs. I wish it were more like Java's. Java is soo good.
            print(e)


def send_to_socket(s: socket.socket, msg):
    s.send(msg.encode())


connections = []


def host_chat():
    global connections
    log_msg(["Creating chat host..."])
    server = socket.socket()
    server.bind(("", 25565))

    server.listen(5)
    log_msg(["Server created."])
    while True:
        try:
            connection, address = server.accept()
            print("Connection from " + address[0] + ":" + str(address[1]))
            print("Listening for data")
            t = threading.Thread(target=watch_socket, args=(connection, ), daemon=True)
            t.start()

            connections.append(connection)
        except Exception as e:  # :(
            print(e)


# TODO: Literally rewrite all handling of user input. This is shit.
def user_input(_):  # This is a TERRIBLE way of doing this, but this is meant to be a thrown-together program for fun
    global state
    global connections
    msg = inputbox.get("1.0", END)[0:-1]
    if state == 0:  # Determining host or join
        if msg == "join":
            state = 1
            log_msg(["Enter the IP address of who you would like to join"])
        if msg == "host":
            t = threading.Thread(target=host_chat, daemon=True)
            t.start()
            state = 2
    elif state == 1:  # Deciding who to join
        log_msg(["Attempting to connect to " + msg])
        s = socket.socket()
        s.connect((msg, 25565))
        t = threading.Thread(target=watch_socket, args=(s, ))
        t.start()
        connections.append(s)
        log_msg(["Connected"])
        state = 2
    elif state == 2:  # Hosting/has joined a chat
        log_msg([msg])
        for s in connections:
            send_to_socket(s, msg)

    inputbox.delete("1.0", END)


def main():
    pass


if __name__ == "__main__":
    main()