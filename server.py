import json
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 8888))
server.listen(5)
print('Сервер запущен на порту 8888')

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
    
    response = {"status": 200, "message": "Login successful"}
    response_json = json.dumps(response)
    response_bytes = response_json.encode()
    
    client_socket.send(f"{len(response_bytes)} ".encode() + response_bytes)
    
    client_socket.close()