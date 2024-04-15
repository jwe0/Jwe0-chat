import socket, threading, json
from pyfiglet import Figlet

clients = []
users = []

def nameart(name):
    return Figlet(font='big_money-se', width=100).renderText(name)

def loadconfig():
    with open("Deps/server_config.json") as config:
        configuration = json.load(config)

        name = configuration.get("name")
        password = configuration.get("password")
        ip = configuration.get("ip")
        port = configuration.get("port")
        tag = configuration.get("tag")

        return name, ip, port, password, tag

def handle_users(user_sock, user_addr, name, tag):
    while True:
        data = user_sock.recv(1024)
        if not data:
            break
        if data.decode() == f"I~HAVE~CONNECTED":
            welcome_message = f"{nameart(name)}\n{tag}\nWelcome"
            user_sock.send(welcome_message.encode())
            for sock in clients:
                if sock != user_sock:
                    sock.send("New user has connected".encode())
            print("New user has connected")
        else:
            username = data.decode().split("<|?|>")[0]
            users.append(username)
            message = data.decode().split("<|?|>")[1]
            print(f"[{username}] {message}")
            for sock in clients:
                sock.send(f"<@{username}> - {message}".encode())






def start_server():
    config = loadconfig()
    name = config[0]
    ip = config[1]
    port = config[2]
    password = config[3]
    tag = config[4]
    

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[#] Started server")
    s.bind((str(ip), port))
    s.settimeout(1)
    s.listen()
    while True:
        try:
            client_socket, client_address = s.accept()
            print(f"[#] User connected: {client_address}")


            clients.append(client_socket)
            threading.Thread(target=handle_users, args=[client_socket, client_address, name, tag]).start()
        except:
            pass



if __name__ == "__main__":
    start_server()