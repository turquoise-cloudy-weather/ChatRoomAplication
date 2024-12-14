import tkinter
import socket
from tkinter import *
from threading import Thread


def receive():
    while True:
        try:
            msg = client_socket.recv(1024).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except:
            print("There is an Error. Message not received.")

def send():
    msg = my_msg.get()
    my_msg.set("")
    client_socket.send(bytes(msg, "utf8"))
    if msg=="#quit":
        client_socket.close()
        window.destroy()

def on_closing():
    my_msg.set("#quit")
    send()

window = Tk()
window.title("Chat-Room App")
window.configure(bg="turquoise")

message_frame = Frame(window, height=100, width=100, bg="blue")
message_frame.pack()

my_msg = StringVar()
my_msg.set("")

scroll_bar = Scrollbar(message_frame)
msg_list = Listbox(message_frame, height=15,width=100, bg="green", yscrollcommand=scroll_bar.set)
scroll_bar.pack(side=RIGHT, fill=Y)
msg_list.pack(side=LEFT, fill=BOTH)
msg_list.pack()

label = Label(window, text="Enter message: ", fg="blue", font='Aeria', bg="Lightblue")
label.pack()

entry_feed = Entry(window, textvariable=my_msg, fg="lightblue", width=50)
entry_feed.pack()

send_Button =  Button(window, text = "Send", font = "Aerial", fg='White', command=send)
send_Button.pack()

quit_Button = Button(window, text = "Quit", font = "Aerial", fg = "White", command = on_closing)
quit_Button.pack()

Host = "127.0.0.1"
Port = 8080

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((Host, Port))

receive_Thread = Thread(target=receive)
receive_Thread.start()

mainloop()