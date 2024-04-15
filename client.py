import socket, threading, os, argparse

messages = []

def handle_data(sock, username):

    while True:
        data = sock.recv(1024)
        if not data:
            break
        if username not in data.decode():
            print()
        messages.append(data.decode())
        os.system("cls") if os.name == "nt" else os.system("clear")
        print("\n".join(messages))
        print(f"{username}@PYRC ~ $ ", end="", flush=True)




def main(ip, port):
    username = input("Username: ")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    s.send(f"{username}<|?|>I~HAVE~CONNECTED".encode())
    threading.Thread(target=handle_data, args=[s, username]).start()
    while True:
        message = input("")

        s.send(f"{username}<|?|>{message}".encode())


if __name__ == "__main__":
    ip = input("Ip: ")
    port = input("Port: ")

    main(ip, int(port))