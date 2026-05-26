import os
import json
import codecs
import socket
import select

connected_clients = {}
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 8888))
server.listen(5)
print('Сервер запущен на порту 8888')

if not os.path.exists("server_data.json"):
    data = {}
    with codecs.open("server_data.json", "w", "utf_8_sig") as f:
        json.dump(data, f)
else:
    with codecs.open("server_data.json", "r", "utf_8_sig") as f:
        data = json.load(f)

server.setblocking(False)
sockets_list = [server]
buffers = {}  # {socket: ""}

while True:
    ready_sockets, _, _ = select.select(sockets_list, [], [], 0.1)
    
    for sock in ready_sockets:
        if sock == server:
            client_socket, addr = server.accept()
            client_socket.setblocking(False)
            sockets_list.append(client_socket)
            buffers[client_socket] = ""
            print(f'Подключен {addr}')
        else:
            try:
                chunk = sock.recv(4096).decode()
                if not chunk:
                    # клиент отключился
                    # Удаляем из connected_clients
                    for login, s in list(connected_clients.items()):
                        if s == sock:
                            del connected_clients[login]
                            break
                    sockets_list.remove(sock)
                    del buffers[sock]
                    sock.close()
                    continue
                
                buffers[sock] += chunk
                
                # Разбираем буфер (формат: "длина пробел json")
                while True:
                    space = buffers[sock].find(" ")
                    if space == -1:
                        break
                    try:
                        msg_len = int(buffers[sock][:space])
                        if len(buffers[sock]) - space - 1 >= msg_len:
                            json_str = buffers[sock][space+1:space+1+msg_len]
                            buffers[sock] = buffers[sock][space+1+msg_len:]
                            message = json.loads(json_str)
                            
                            # === ТВОЯ ЛОГИКА ОБРАБОТКИ ===
                            print(f"Получено сообщение: {message}")
                            
                            if message["command"] == "ping":
                                response = {"status": 200, "message": "Server active"}
                                response_json = json.dumps(response)
                                sock.send(f"{len(response_json)} {response_json}".encode())
                            
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
                                        connected_clients[message["login"]] = sock
                                        response = {"status": 200, "message": "Login successful"}
                                
                                elif message["command"] == "registration":
                                    if user == None:
                                        response = {"status": 200, "message": "Login registration successful"}
                                        connected_clients[message["login"]] = sock
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
                                        
                                        # push получателю
                                        print(connected_clients)
                                        print(message["messages"][0])
                                        if message["messages"][0] in connected_clients:
                                            to_user = {"command": "new message", "chat": message["login"], "message": message["messages"][1]}
                                            print(to_user)
                                            to_json = json.dumps(to_user)
                                            print(to_json)
                                            connected_clients[message["messages"][0]].send(f"{len(to_json)} {to_json}".encode())
                                            print("sended")
                                
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
                                    elif message["user"] in data[message["login"]]["messages"].keys():
                                        response = {"status": 409, "message": "chat already exists"}
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

                                        print(connected_clients)
                                        print(message["user"])
                                        if message["user"] in connected_clients:
                                            to_user = {"command": "new chat", "chat": message["login"]}
                                            print(to_user)
                                            to_json = json.dumps(to_user)
                                            print(to_json)
                                            try:
                                                connected_clients[message["user"]].send(f"{len(to_json)} {to_json}".encode())
                                                print("sended")
                                            except:
                                                print("oh no")
                                
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
                                
                                # Отправляем ответ
                                response_json = json.dumps(response)
                                sock.send(f"{len(response_json)} {response_json}".encode())
                            
                        else:
                            break
                    except:
                        buffers[sock] = ""
                        break
                        
            except:
                for login, s in list(connected_clients.items()):
                    if s == sock:
                        del connected_clients[login]
                        break
                if sock in sockets_list:
                    sockets_list.remove(sock)
                if sock in buffers:
                    del buffers[sock]
                sock.close()