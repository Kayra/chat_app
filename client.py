from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread
import tkinter


HOST = input('Enter host: ')
PORT = input('Enter port: ')
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)

BUFFERSIZE = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)


def start_app():
    receive_thread = Thread(target=recieve)
    receive_thread.start()
    tkinter.mainloop()


def recieve():
    """
    Handles the recieving of messages.
    """

    while True:

        try:
            message = client_socket.recv(BUFFERSIZE).decode("utf8")
            message_list.insert(tkinter.END, message)
        except OSError:
            break


def send(event=None):
    """
    Handles the sending of messages.
    """

    message = my_message.get()
    my_message.set("")

    client_socket.send(bytes(message, "utf8"))

    if message == "<quit>":
        client_socket.close()
        top.quit()


def on_close(event=None):
    """
    This function is called when the function is closed.
    """
    my_message.set("<quit>")
    send()


def _create_top_level_widget(title="Chater"):
    top = tkinter.Tk()
    top.title(title)
    return top


def _create_my_message(placeholder=""):
    my_message = tkinter.StringVar()
    my_message.set(placeholder)
    return my_message


def _create_messages_frame(top):
    return tkinter.Frame(top)


def _create_scrollbar(messages_frame):
    return tkinter.Scrollbar(messages_frame)


def _create_message_list(messages_frame, height=30, width=100):
    return tkinter.Listbox(messages_frame, height=height, width=width, yscrollcommand=scrollbar.set)


def _create_entry_field(my_message):
    entry_field = tkinter.Entry(top, textvariable=my_message)
    entry_field.bind("<Return>", send)
    return entry_field


def _create_send_button():
    return tkinter.Button(top, text="Send", command=send)


top = _create_top_level_widget()
my_message = _create_my_message()
messages_frame = _create_messages_frame(top)
scrollbar = _create_scrollbar(messages_frame)
message_list = _create_message_list(messages_frame)
entry_field = _create_entry_field(my_message)
send_button = _create_send_button()

scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
message_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
message_list.pack()
messages_frame.pack()
entry_field.pack()
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_close)


start_app()
