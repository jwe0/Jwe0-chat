import socket
import threading
import tkinter as tk
import argparse

messages = []

class Client:
    def __init__(self, socket, username, ip, port):
        self.s = socket
        self.user = username
        self.ip = ip
        self.port = port

    def handle_data(self):
        while True:
            data = self.s.recv(1024)
            if not data:
                break
            messages.append(data.decode() + "\n")
            self.edit()

    def ui(self):
        window = tk.Tk()
        window.geometry("1000x400")
        greeting = tk.Label(window, text="Welcome to jwe0 chat")
        greeting.pack()
        
        text_frame = tk.Frame(window)
        text_frame.pack(fill=tk.BOTH, expand=True)

        self.text_entry = tk.Text(text_frame, height=20, width=80, state="disabled")
        self.text_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(text_frame, command=self.text_entry.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_entry.config(yscrollcommand=scrollbar.set)
        
        self.entry = tk.Entry(window, width=80)
        self.entry.pack()
        
        sc = tk.Button(window, text="Send", width=10, height=1, command=self.send_message)
        sc.pack()

        threading.Thread(target=self.handle_data).start()
        window.mainloop()

    def edit(self):
        self.text_entry.config(state="normal")
        self.text_entry.delete("1.0", "end")
        self.text_entry.insert("end-1c", "".join(messages))
        self.text_entry.config(state="disabled")

    def send_message(self):
        message = self.entry.get()
        if message: 
            self.s.send(f"{self.user}<|?|>{message}".encode())
            self.entry.delete(0, "end")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Python chat room")
    parser.add_argument("--host", "-hd", help="The host IP")
    parser.add_argument("--port", "-p", help="The port the host is running on")
    parser.add_argument("--username", "-u", help="Your username")
    args = parser.parse_args()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((args.host, int(args.port)))
    s.send(f"I~HAVE~CONNECTED".encode())

    x = Client(s, args.username, args.host, int(args.port))
    threading.Thread(target=x.ui).start() 
