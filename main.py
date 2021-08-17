from tkinter import *
import socket
import threading


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

state = 0


def log_msg(msgs):
    chatbox.config(state=NORMAL)

    for msg in msgs:
        chatbox.insert(END, msg + "\n")

    chatbox.config(state=DISABLED)


def watch_socket(s: socket.socket):
    while True:
        log_msg([s.recv(2048).decode()])


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
        connection, address = server.accept()
        print("Connection from " + address[0] + ":" + str(address[1]))
        print("Listening for data")
        t = threading.Thread(target=watch_socket, args=(connection, ))
        t.start()

        connections.append(connection)


def user_input(_):  # This is a TERRIBLE way of doing this, but this is meant to be a thrown-together program for fun
    global state
    global connections
    msg = inputbox.get("1.0", END)[0:-1]
    if state == 0:  # Determining host or join
        if msg == "join":
            state = 1
            log_msg(["Enter the IP address of who you would like to join"])
        if msg == "host":
            t = threading.Thread(target=host_chat)
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
    window = Tk()
    window.config(background=bg_color)
    window.title("Chat with friends!!!! w")

    global chatbox
    chatbox = Text(window, **text_style)
    chatbox.insert(END, "Would you like to host or join a chat? Type 'host' or 'join'\n")
    chatbox.config(state=DISABLED, width=140, height=50)
    chatbox.pack(side=TOP, padx=4, pady=4)

    global inputbox
    inputbox = Text(window, **text_style)
    inputbox.config(width=140, height=10)
    inputbox.bind("<Return>", user_input)
    inputbox.pack(side=TOP, padx=4, pady=4)

    window.mainloop()


if __name__ == "__main__":
    main()