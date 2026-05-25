import os
import json
import codecs
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 8888))
server.listen(5)
print('Сервер запущен на порту 8888')

if not os.path.exists("data.json"):
    data = {}
    with codecs.open("server_data.json", "w", "utf_8_sig") as f:
        json.dump(data, f)

while True:
    client_socket, addr = server.accept()
    print(f'Подключен {addr}')

    length_str = ""
    while True:
        char = client_socket.recv(1).decode()
        if char == " ":
            break
        length_str += char
    
    message_length = int(length_str)
    
    message_data = client_socket.recv(message_length)
    
    message = json.loads(message_data.decode())
    print(f"Получено сообщение: {message}")
    if message["command"] == "ping":
        response = {"status": 200, "message": "Server active"}
    else:
        with codecs.open("server_data.json", "r", "utf_8_sig") as f:
            data = json.load(f)
        user = data.get(message["login"], None)
        if message["command"] == "login":
            if user == None:
                response = {"status": 404, "message": "No account"}
            elif user["password"] != message["password"]:
                response = {"status": 422, "message": "Invalid password"}
            else:
                response = {"status": 200, "message": "Login successful"}
        elif message["command"] == "registration":
            if user == None:
                response = {"status": 200, "message": "Login registration successful"}
                data[message["login"]] = {}
                data[message["login"]]["password"] = message["password"]
                data[message["login"]]["messages"] = {}
                with codecs.open("server_data.json", "w", "utf_8_sig") as f:
                    json.dump(data, f)
            else:
                response = {"status": 409, "message": "Another user with this login"}
        elif message["command"] == "update messages":
            if user == None:
                response = {"status": 404, "message": "No account"}
            elif user["password"] != message["password"]:
                response = {"status": 422, "message": "Invalid password"}
            else:
                lst = data[message["login"]]["messages"][message["messages"][0]]
                lst.append(message["messages"][1])
                data[message["login"]]["messages"][message["messages"][0]] = lst

                lst = data[message["messages"][0]]["messages"][message["login"]]
                lst.append(message["messages"][1])
                data[message["messages"][0]]["messages"][message["login"]] = lst

                with codecs.open("server_data.json", "w", "utf_8_sig") as f:
                    json.dump(data, f)
                response = {"status": 200, "message": "Updated successful"}
        elif message["command"] == "get messages":
            if user == None:
                response = {"status": 404, "message": "No account"}
            elif user["password"] != message["password"]:
                response = {"status": 422, "message": "Invalid password"}
            else:
                response = {"status": 200, "message": "Updated successful", "messages": user["messages"]}
        elif message["command"] == "new chat":
            if user == None:
                response = {"status": 404, "message": "No account"}
            elif user["password"] != message["password"]:
                response = {"status": 422, "message": "Invalid password"}
            elif message["user"] not in data.keys():
                response = {"status": 404, "message": "No user"}
            else:
                dct = data[message["login"]]["messages"]
                dct[message["user"]] = []
                data[message["login"]]["messages"] = dct

                dct = data[message["user"]]["messages"]
                dct[message["login"]] = []
                data[message["user"]]["messages"] = dct

                with codecs.open("server_data.json", "w", "utf_8_sig") as f:
                    json.dump(data, f)
                response = {"status": 200, "message": "Created successful"}
        elif message["command"] == "remove account":
            if user == None:
                response = {"status": 404, "message": "No account"}
            elif user["password"] != message["password"]:
                response = {"status": 422, "message": "Invalid password"}
            else:
                chats = data[message["login"]]["messages"].keys()
                for chat in chats:
                    del data[chat]["messages"][message["login"]]
                del data[message["login"]]

                with codecs.open("server_data.json", "w", "utf_8_sig") as f:
                    json.dump(data, f)
                response = {"status": 200, "message": "Removed successful"}
            
    response_json = json.dumps(response)
    response_bytes = response_json.encode()
    
    client_socket.send(f"{len(response_bytes)} ".encode() + response_bytes)
    
    client_socket.close()