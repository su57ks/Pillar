import os
import re
import sys
import json
import time
import pygame
import codecs
import socket

pygame.init()
info = pygame.display.Info()
screen_width = info.current_w 
screen_height = info.current_h 
screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)
pygame.display.set_caption("Pillar")
font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()

class Button():
    def __init__(self, pStandart_color, pClick_color, pPosition, pFont, pText):
        self.font = pFont
        self.t = pText
        self.text = self.font.render(pText, True, (255, 255, 255))
        self.standart_color = pStandart_color
        self.click_color = pClick_color
        self.position = pygame.Rect(pPosition)
        self.current_color = self.standart_color
        self.clicked = False

    def update(self, events):
        self.clicked = False
        mouse_pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.position.collidepoint(mouse_pos):
                self.clicked = True
            
        if self.position.collidepoint(mouse_pos):
            self.current_color = self.click_color

    def draw(self, screen):
        pygame.draw.rect(screen, self.current_color, self.position, border_radius=0)
        text_rect = self.text.get_rect(center=self.position.center)
        screen.blit(self.text, text_rect)
        self.current_color = self.standart_color

class TextField():
    def __init__(self, pColor, pPosition, pFont, pText):
        self.font = pFont
        self.color = pColor
        self.position = pygame.Rect(pPosition)
        self.text = pText

    def draw(self, screen, color = "standart"):
        if color == "standart":
            color = self.color 
        mid_text = self.text
        new_text = self.text
        text = self.font.render(new_text, True, (255, 255, 255))
        if len(self.text) > 50:
            new_text = []
            text_renders = []
            texts = []
            for i in range(len(self.text) // 50 + 1):
                new_text.append(mid_text[:50])
                mid_text = mid_text[50:]
            for i in range(len(new_text)):
                text_rect = text.get_rect(midleft=self.position.midleft)
                text_rect.left = self.position.left + 10
                text_rect.top = self.position.top + 30 * i
                text = self.font.render(new_text[i], True, (255, 255, 255))
                texts.append(text)
                text_renders.append(text_rect)

            pygame.draw.rect(screen, color, pygame.Rect(self.position.x,
                                                        self.position.y, 
                                                        max([text.width for text in text_renders]),
                                                        text_renders[-1].bottom - text_renders[0].top, border_radius=0))
            for text, text_rect in zip(texts, text_renders):
                screen.blit(text, text_rect)
        else:
            pygame.draw.rect(screen, color, self.position)
            text_rect = text.get_rect(midleft=self.position.midleft)
            text_rect.left = self.position.left + 10
            screen.blit(text, text_rect)

class TextInput(TextField):
    def __init__(self, pStandart_color, pClick_color, pPosition, pFont, pText):
        super().__init__(pStandart_color, pPosition, pFont, pText)
        
        self.standart_color = pStandart_color
        self.click_color = pClick_color
        self.current_color = pStandart_color
        self.activated = False
        self.first = True
        self.standart = pText

    def update(self, events):
        mouse_pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.position.collidepoint(mouse_pos):
                    self.activated = not self.activated
                    if self.first:
                        self.text = ""
                        self.first = False
                    if self.text == "" and not self.activated:
                        self.first = True
                        self.text = self.standart
                else:
                    self.activated = False
                    if self.first:
                        self.text = ""
                        self.first = False
                    if self.text == "":
                        self.first = True
                        self.text = self.standart
        
        for event in events:
            if event.type == pygame.KEYDOWN and self.activated:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

        if self.activated:
            self.current_color = self.click_color
        else:
            self.current_color = self.standart_color

    def draw(self, screen):
        super().draw(screen, self.current_color)
          
class Modal():
    def __init__(self, pColor, pPosition, pFont, pText):
        self.font = pFont
        self.color = pColor
        self.position = pygame.Rect(pPosition)
        self.text = self.font.render(pText, True, (255, 255, 255))
        self.showed = True
        self.close = Button((100, 100, 120), (220, 60, 60), (pPosition[0] + pPosition[2] - 30, pPosition[1], 30, 30), self.font, "X")

    def update(self, events):
        self.close.update(events)
        if self.close.clicked:
            self.showed = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.position, border_radius=0)
        self.close.draw(screen)
        text_rect = self.text.get_rect(center=self.position.center)
        screen.blit(self.text, text_rect)

class SelectModal(Modal):
    def __init__(self, pColor, pPosition, pFont, pText):
        super().__init__(pColor, pPosition, pFont, pText)
        self.yes = Button((100, 100, 120), (0, 255, 0), (pPosition[0] + pPosition[2] // 3, pPosition[1] + screen_height // 10 - 45, 30, 30), self.font, "Да")
        self.no = Button((100, 100, 120), (255, 0, 0), (pPosition[0] + pPosition[2] // 3 * 2, pPosition[1] + screen_height // 10 - 45, 30, 30), self.font, "Нет")
        self.answer = None

    def update(self, events):
        super().update(events)
        self.yes.update(events)
        self.no.update(events)
        if self.yes.clicked:
            self.answer = True
            self.showed = False
        elif self.no.clicked:
            self.answer = False
            self.showed = False
    
    def draw(self, screen):
        super().draw(screen)
        self.yes.draw(screen)
        self.no.draw(screen)

class PositionButton(Button):
    def __init__(self, pStandart_color, pClick_color, pPress_color, pPosition, pFont, pText):
        super().__init__(pStandart_color, pClick_color, pPosition, pFont, pText)
        self.press_color = pPress_color
        self.pressed = False

    def update(self, events):
        self.clicked = False
        mouse_pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.position.collidepoint(mouse_pos):
                self.clicked = True
                self.pressed = not self.pressed

        if self.pressed:
            self.current_color = self.press_color
        else:
            if self.position.collidepoint(mouse_pos):
                self.current_color = self.click_color

    def draw(self, screen):
        super().draw(screen)
    
class ChatButton(PositionButton):
    def __init__(self, pStandart_color, pClick_color, pPress_color, pPosition, pFont, pTitle, pMessage):
        super().__init__(pStandart_color, pClick_color, pPress_color, pPosition, pFont, pTitle)
        self.message = pMessage
        self.message_font = pygame.font.SysFont(None, 30)
        self.new = False

    def update(self, events):
        super().update(events)
        if self.pressed and self.new:
            self.new = False
        if not self.message.get("readed", "") and self.message.get("from", "") != data["login"]:
            self.new = True 

    def draw(self, screen):
        super().draw(screen)
        text = self.message_font.render(self.message.get("text", ""), True, (255, 255, 255))
        text_rect = text.get_rect(center=self.position.center, bottom=self.position.bottom - 10)
        screen.blit(text, text_rect)
        if self.new:
            rect = pygame.Rect(0, 0, 80, 60)
            rect.centery = self.position.centery
            rect.right = self.position.right
            pygame.draw.rect(screen, (255, 0, 0), rect)

class Chat():
    def __init__(self, pLogin, pTitle, pOpponent, pPosition, pFont, pMessages):
        self.login = pLogin
        self.title = pTitle
        self.to = pOpponent
        self.opened = False
        self.clicked = False
        self.messages = pMessages
        self.position = pygame.Rect(pPosition)
        self.font = pFont
        self.offset = 1
        self.to_chat = ChatButton((45, 50, 60), (75, 80, 95), (200, 200, 200), pygame.Rect(pPosition), pFont, pTitle, self.messages[-1] if len(self.messages) != 0 else {})
        self.head = TextField((35, 40, 50), (screen_width // 2, 0, screen_width // 5 * 3, screen_height // 10), font, pTitle)

    def update(self, events):
        self.clicked = False
        self.to_chat.update(events)
        if self.to_chat.clicked:
            self.clicked = True
        if self.to_chat.pressed:
            self.opened = True
            if self.to_chat.clicked:
                for message in self.messages[::-1]:
                    if not message["readed"]:
                        message["readed"] = True
                    else:
                        break
                network({"version": 1, "command": "read chat", "login": self.login, "password": data["password"], "chat": self.to})
        else:
            self.opened = False
        mouse_pos = pygame.mouse.get_pos()
        position = pygame.Rect((screen_width // 2, screen_height // 10, screen_width // 2, screen_height // 10 * 8))
        for event in events:
            if event.type == pygame.MOUSEWHEEL and position.collidepoint(mouse_pos):
                y = event.y
                if y == 1:
                    if self.offset < len(self.messages) - 8:
                        self.offset += 1
                else:
                    if self.offset > 1:
                        self.offset -= 1

    def draw(self, screen):
        self.to_chat.draw(screen)
        if self.opened:
            self.head.draw(screen)
            if self.offset != 1:
                last_messages = self.messages[-(8 + self.offset):-self.offset][::-1]
            else:
                last_messages = self.messages[-8:][::-1]
            for i in range(len(last_messages)):
                if last_messages[i]["from"] == self.login:
                    message = TextField((20, 22, 28), (screen_width // 5 * 3, screen_height // 10 * (8 - i), screen_width // 5 * 2, screen_height // 10), font, last_messages[i]["text"])
                else:
                    message = TextField((100, 100, 100), (screen_width // 2, screen_height // 10 * (8 - i), screen_width // 5 * 2, screen_height // 10), font, last_messages[i]["text"])
                message.draw(screen)

    def __str__(self):
        return (f"user: {self.user}, title: {self.title}, opponent: {self.opponent}, clicked: {self.clicked}, "
                f"opened: {self.opened}, position: {self.position}, messages: {self.messages}")
    
    def send(self, message):
        self.offset = 1
        self.messages.append({"text": message, "from": self.login, "to": self.to, "time": time.time(), "readed": False})
        self.to_chat.message = self.messages[-1]
        network({"version": 1, "command": "update messages", "login": data["login"], "password": data["password"], "messages": [chats[chat].title, self.messages[-1]]})
        input.text = ""

def network(request):
    sock.setblocking(True)
    request = json.dumps(request)
    request = str(len(request)) + " " + request
    sock.send(request.encode())

    length_str = ""
    while True:
        char = sock.recv(1).decode()
        if char == " ":
            break
        length_str += char
    
    message_length = int(length_str)
    
    message_data = sock.recv(message_length)
    
    message = json.loads(message_data.decode())
    sock.setblocking(False)
    return message

def create():
    global chats
    i = 1 
    for key in messages.keys():
        chats.append(Chat(data["login"], key, key, (screen_width // 10, screen_height // 10 * (i - 1), screen_width // 5 * 2, screen_height // 10), font, list(messages[key])))
        i += 1
    sort_chats()

def sort_chats():
    global chats
    chats = sorted(chats, key=lambda chat: chat.messages[-1]["time"] if len(chat.messages) != 0 else 0, reverse=True)
    i = 1 
    for chat in chats:
        chat.to_chat.position = pygame.Rect(screen_width // 10, screen_height // 10 * (i - 1), screen_width // 5 * 2, screen_height // 10)
        i += 1

chat = None

to_registration = Button((70, 75, 85), (100, 105, 120), (screen_width // 5 * 2, screen_height // 10 * 9, screen_width // 5, screen_height // 10), font, "Регистрация")

to_login = Button((70, 75, 85), (100, 105, 120), (screen_width // 5 * 2, screen_height // 10 * 9, screen_width // 5, screen_height // 10), font, "Вход")

to_settings = PositionButton((50, 55, 65), (80, 85, 100), (200, 200, 200), (0, 0, screen_width // 10, screen_height // 10), font, "Настройки")

to_chats = PositionButton((50, 55, 65), (80, 85, 100), (200, 200, 200), (0, screen_height // 10, screen_width // 10, screen_height // 10), font, "Чаты")

to_search = PositionButton((50, 55, 65), (80, 85, 100), (200, 200, 200), (0, screen_height // 5, screen_width // 10, screen_height // 10), font, "Найти по логину")

search_text = TextInput((40, 45, 55), (75, 80, 95), (screen_width // 5 * 2, screen_height // 10 * 3, screen_width // 5, screen_height // 10), font, "Введите логин")

search_button = Button((70, 75, 85), (100, 105, 120), (screen_width // 5 * 2, screen_height // 10 * 9, screen_width // 5, screen_height // 10), font, "Поиск")

input = TextInput((40, 45, 55), (75, 80, 95), (screen_width // 2, screen_height // 10 * 9, screen_width // 10 * 4, screen_height // 10), font, "Нажмите, что бы ввести текст")

send = Button((70, 75, 85), (100, 105, 120), (screen_width // 10 * 9, screen_height // 10 * 9, screen_width // 10, screen_height // 10), font, "»")

close = Button((100, 100, 120), (220, 60, 60), (screen_width - 30, 0, 30, 30), font, "X")

iconify_button = Button((100, 100, 120), (220, 60, 60), (screen_width - 60, 0, 30, 30), font, "-")

login_login = TextInput((40, 45, 55), (75, 80, 95), (screen_width // 5 * 2, screen_height // 10 * 3, screen_width // 5, screen_height // 10), font, "Введите логин")

password_login = TextInput((40, 45, 55), (75, 80, 95), (screen_width // 5 * 2, screen_height // 10 * 5, screen_width // 5, screen_height // 10), font, "Введите пароль")

login_button = Button((70, 75, 85), (100, 105, 120), (screen_width // 5 * 2, screen_height // 10 * 7, screen_width // 5, screen_height // 10), font, "Войти")

login_registration = TextInput((40, 45, 55), (75, 80, 95), (screen_width // 5 * 2, screen_height // 10 * 1, screen_width // 5, screen_height // 10), font, "Введите логин")

password1_registration = TextInput((40, 45, 55), (75, 80, 95), (screen_width // 5 * 2, screen_height // 10 * 3, screen_width // 5, screen_height // 10), font, "Введите пароль")

password2_registration = TextInput((40, 45, 55), (75, 80, 95), (screen_width // 5 * 2, screen_height // 10 * 5, screen_width // 5, screen_height // 10), font, "Подтвердите пароль")

registration_button = Button((70, 75, 85), (100, 105, 120), (screen_width // 5 * 2, screen_height // 10 * 7, screen_width // 5, screen_height // 10), font, "Зарегестрироваться")

leave = Button((70, 75, 85), (100, 105, 120), (screen_width // 5 * 2, screen_height // 10 * 7, screen_width // 5, screen_height // 10), font, "Выйти")

remove_account = Button((70, 75, 85), (100, 105, 120), (screen_width // 5 * 2, screen_height // 10 * 5, screen_width // 5, screen_height // 10), font, "Удалить аккаунт")

change_server = Button((70, 75, 85), (100, 105, 120), (screen_width // 5 * 2, screen_height // 10 * 3, screen_width // 5, screen_height // 10), font, "Сменить сервер")

connect_ip = TextInput((40, 45, 55), (75, 80, 95), (screen_width // 5 * 2, screen_height // 10 * 3, screen_width // 5, screen_height // 10), font, "Введите IP сервера")

connect_port = TextInput((40, 45, 55), (75, 80, 95), (screen_width // 5 * 2, screen_height // 10 * 5, screen_width // 5, screen_height // 10), font, "Введите порт сервера")

connect_button = Button((70, 75, 85), (100, 105, 120), (screen_width // 5 * 2, screen_height // 10 * 7, screen_width // 5, screen_height // 10), font, "Подключиться")

messages = {}

chats = []

place = "LOGIN"

offset = 0

if os.path.exists("data.json"):
    with codecs.open("data.json", "r", "utf_8_sig") as f:
        data = json.load(f)
    messages = data["messages"]
else:
    data = {"login": "", "password": "", "messages": {}, "ip": None, "port": None}
    with codecs.open("data.json", "w", "utf_8_sig") as f:
        json.dump(data, f)

if data.get("ip") is None or data.get("port") is None:
    place = "CONNECTION"
elif data["login"] == "" or data["password"] == "":
    place = "LOGIN"
    sock = socket.socket() 
    sock.connect((data["ip"], data["port"]))
    sock.setblocking(False) 
else:
    sock = socket.socket() 
    sock.connect((data["ip"], data["port"]))
    sock.setblocking(False) 
    place = "CHATS"
    response = network({"version": 1, "command": "login", "login": data["login"], "password": data["password"]})
    messages = network({"version": 1, "command": "get messages", "login": data["login"], "password": data["password"]})["messages"]
    user = TextField((35, 40, 50), (screen_width // 10, 0, screen_width // 10 * 9, screen_height // 10), font, f'Пользователь: {data["login"]} | Пароль: {data["password"]}')
    create()

modal_showing = False
modal = None
running = True
chat = None
while running:
    clock.tick(30)
    events = pygame.event.get()
    screen.fill((6, 14, 33))

    if place == "LOGIN":
        to_registration.update(events)
        if to_registration.clicked:
            place = "REGISTRATION"
        else:
            to_registration.draw(screen)
            login_login.update(events)
            password_login.update(events)
            login_button.update(events)
            if login_button.clicked:
                if not login_login.first and not password_login.first:
                    message = network({"version": 1, "command": "login", "login": login_login.text, "password": password_login.text})
                    if message["status"] == 200:
                        place = "CHATS"
                        data["login"] = login_login.text
                        data["password"] = password_login.text
                        with codecs.open("data.json", "w", "utf_8_sig") as f:
                            json.dump(data, f)
                        user = TextField((35, 40, 50), (screen_width // 10, 0, screen_width // 10 * 9, screen_height // 10), font, f'Пользователь: {data["login"]} | Пароль: {data["password"]}')
                        login_login.activated = False
                        login_login.first = True
                        login_login.text = login_login.standart
                        password_login.activated = False
                        password_login.first = True
                        password_login.text = password_login.standart
                        message = network({"version": 1, "command": "get messages", "login": data["login"], "password": data["password"]})
                        if message["status"] == 200:
                            messages = message["messages"]
                            data["messages"] = messages
                            with codecs.open("data.json", "w", "utf_8_sig") as f:
                                json.dump(data, f)
                            create()
                    elif message["status"] == 404:
                        modal_showing = True
                        modal = Modal((55, 60, 75), (screen_width // 2 - 200, screen_height // 2 - 50, 400, 100), font, "Аккаунта не существует")
                    elif message["status"] == 422:
                        modal_showing = True
                        modal = Modal((55, 60, 75), (screen_width // 2 - 200, screen_height // 2 - 50, 400, 100), font, "Неверный пароль")
                else:
                    modal_showing = True
                    modal = Modal((55, 60, 75), (screen_width // 2 - 200, screen_height // 2 - 50, 400, 100), font, "Вы не ввели логин или пароль")
            else:
                login_button.draw(screen)
                login_login.draw(screen)
                password_login.draw(screen)
    elif place == "CHATS":
        for i in range(len(chats)):
            chats[i].update(events)
            
            if chats[i].clicked:
                if chats[i].opened:
                    chat = i
                    break
                else:
                    chat = None
            if chats[i].opened and chat != None:
                    chat = i

        if chat != None:
            for i in range(len(chats)):
                if i != chat:
                    chats[i].opened = False
                    chats[i].to_chat.pressed = False
                else:
                    chats[i].opened = True
                    chats[i].to_chat.pressed = True
        for i in range(len(chats)):
            chats[i].draw(screen)
        if chat != None:
            input.update(events)
            send.update(events)
            if send.clicked:
                if input.first or input.text == "":
                    modal_showing = True
                    modal = Modal((55, 60, 75), (screen_width // 2 - 200, screen_height // 2 - 50, 400, 100), font, "Вы не ввели сообщение")
                else:
                    chats[chat].send(input.text)
                    sort_chats()

            input.draw(screen)
            send.draw(screen)
        to_settings.update(events)
        to_chats.update(events)
        to_search.update(events)
        
        if to_settings.clicked:
            place = "SETTINGS"
            to_settings.pressed = True
            to_chats.pressed = False
        elif to_search.clicked:
            place = "SEARCH"
            to_chats.pressed = False
        else:
            to_chats.pressed = True
            to_settings.pressed = False
        
        to_search.draw(screen)
        to_settings.draw(screen)
        to_chats.draw(screen)

        try:
            n = sock.recv(1)  
            length_str = n.decode()
            while True:
                char = sock.recv(1).decode()
                if char == " ":
                    break
                length_str += char
            
            message_length = int(length_str)
            
            message_data = sock.recv(message_length)
            
            message = json.loads(message_data.decode())
            if message["command"] == "new message":
                messages[message["chat"]].append(message["message"])
                data["messages"] = messages
                with codecs.open("data.json", "w", "utf_8_sig") as f:
                    json.dump(data, f)
                for chat in chats:
                    if chat.title == message["chat"]:
                        chat.messages.append(message["message"])
                        chat.to_chat.message = message["message"]["text"]
                        if not chat.opened:
                            chat.to_chat.new = True
                        break
                sort_chats()
            elif message["command"] == "new chat":
                messages[message["chat"]] = []
                data["messages"] = messages
                with codecs.open("data.json", "w", "utf_8_sig") as f:
                    json.dump(data, f)
                chats.append(Chat(data["login"], message["chat"], message["chat"], (screen_width // 10, screen_height // 10 * (len(messages.keys()) - 1), screen_width // 5 * 2, screen_height // 10), font, []))
                sort_chats()
        except BlockingIOError:
            pass
        
        
        mouse_pos = pygame.mouse.get_pos()
        position = pygame.Rect((screen_width // 10, 0, screen_width // 5 * 2, screen_height))
        last_offset = offset
        for event in events:
            if event.type == pygame.MOUSEWHEEL and position.collidepoint(mouse_pos):
                y = event.y
                if y == 1:
                    if offset > 0:
                        offset -= 1
                else:
                    if offset < len(messages) - 10:
                        offset += 1
        if last_offset != offset:
            for i in range(len(messages.keys())):
                chats[i].to_chat.position = pygame.Rect((screen_width // 10, screen_height // 10 * i - offset * screen_height // 10, screen_width // 5 * 2, screen_height // 10))
    elif place == "SETTINGS":
        to_settings.update(events)
        to_chats.update(events)
        to_search.update(events)
        
        if to_chats.clicked:
            place = "CHATS"
            to_settings.pressed = False
            to_chats.pressed = True
        elif to_search.clicked:
            place = "SEARCH"
            to_settings.pressed = False
            to_chats.pressed = False
            to_search.pressed = True
        else:
            to_chats.pressed = False
            to_settings.pressed = True
            user.draw(screen)
            leave.update(events)
            to_search.draw(screen)
            to_settings.draw(screen)
            to_chats.draw(screen)
            remove_account.update(events)
            change_server.update(events)
            if leave.clicked:
                screenshot = screen.copy()
                selecting = True
                answer = None
                select = SelectModal((55, 60, 75), (screen_width // 2 - 200, screen_height // 2 - 50, 400, 100), font, "Вы уверены?")
                while selecting:
                    clock.tick(30)
                    events = pygame.event.get()
                    screen.blit(screenshot, (0, 0))
                    select.update(events)
                    for event in events:
                        if event.type == pygame.QUIT:
                            running = False
                            selecting = False

                    close.update(events)
                    if close.clicked:
                        running = False
                        selecting = False
                    close.draw(screen)

                    iconify_button.update(events)
                    if iconify_button.clicked:
                        pygame.display.iconify()
                    iconify_button.draw(screen)
                    if not select.showed:
                        selecting = False
                        if select.answer != None:
                            answer = select.answer
                    else:
                        select.draw(screen)
                    pygame.display.flip()
                if answer == True:
                    messages = {}
                    sock.close()
                    sock = socket.socket() 
                    sock.connect((data["ip"], data["port"]))
                    sock.setblocking(False)
                    data["login"] = ""
                    data["password"] = ""
                    data["messages"] = {}
                    chats = []
                    with codecs.open("data.json", "w", "utf_8_sig") as f:
                        json.dump(data, f)   
                    place = "LOGIN"
                    chat = None
            elif remove_account.clicked:
                chat = None
                network({"version": 1, "command": "remove account", "login": data["login"], "password": data["password"]})
                messages = {}
                data["login"] = ""
                data["password"] = ""
                data["messages"] = {}
                chats = []
                with codecs.open("data.json", "w", "utf_8_sig") as f:
                    json.dump(data, f)   
                place = "LOGIN"
            elif change_server.clicked:
                data = {"login": "", "password": "", "messages": {}, "ip": None, "port": None} 
                chats = []
                with codecs.open("data.json", "w", "utf_8_sig") as f:
                    json.dump(data, f)   
                place = "CONNECTION"
            else:
                leave.draw(screen)
                remove_account.draw(screen)
                change_server.draw(screen)
    elif place == "REGISTRATION":
        to_login.update(events)
        if to_login.clicked:
            place = "LOGIN"
        else:
            to_login.draw(screen)
            login_registration.update(events)
            password1_registration.update(events)
            password2_registration.update(events)
            registration_button.update(events)
            if registration_button.clicked:
                if not login_registration.first and not password1_registration.first and not password2_registration.first:
                    if password1_registration.text == password2_registration.text:
                        message = network({"version": 1, "command": "registration", "login": login_registration.text, "password": password1_registration.text})
                        if message["status"] == 200:
                            place = "CHATS"
                            data["login"] = login_registration.text
                            data["password"] = password1_registration.text
                            with codecs.open("data.json", "w", "utf_8_sig") as f:
                                json.dump(data, f)
                            user = TextField((35, 40, 50), (screen_width // 10, 0, screen_width // 10 * 9, screen_height // 10), font, f'Пользователь: {data["login"]} | Пароль: {data["password"]}')
                            login_registration.activated = False
                            login_registration.first = True
                            login_registration.text = login_login.standart
                            password1_registration.activated = False
                            password1_registration.first = True
                            password1_registration.text = password_login.standart
                            password2_registration.activated = False
                            password2_registration.first = True
                            password2_registration.text = password_login.standart
                        elif message["status"] == 409:
                            place = "REGISTRATION"
                            modal_showing = not modal_showing
                            if modal_showing:
                                    modal = Modal((55, 60, 75), (screen_width // 2 - 200, screen_height // 2 - 50, 400, 100), font, "Пользователь с таким логином уже существует")
                    else:
                        modal_showing = True
                        modal = Modal((55, 60, 75), (screen_width // 2 - 200, screen_height // 2 - 50, 400, 100), font, "Пароли не совпадают")
                else:
                    modal_showing = True
                    modal = Modal((55, 60, 75), (screen_width // 2 - 200, screen_height // 2 - 50, 400, 100), font, "Вы не ввели логин или пароль")
            else:
                login_registration.draw(screen)
                password1_registration.draw(screen)
                password2_registration.draw(screen)
                registration_button.draw(screen)
    elif place == "CONNECTION":
        connect_port.update(events)
        connect_ip.update(events)
        connect_button.update(events)
        if connect_button.clicked:
            pattern = r'^(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$'
            if not re.match(pattern, connect_ip.text):
                modal_showing = True
                modal = Modal((55, 60, 75), (screen_width // 2 - 200, screen_height // 2 - 50, 400, 100), font, "Неверный IP")
            else:
                try:
                    port = int(connect_port.text)
                    if port < 1024 or port > 65535:
                        modal_showing = True
                        modal = Modal((55, 60, 75), (screen_width // 2 - 200, screen_height // 2 - 50, 400, 100), font, "Неверный порт")
                    else:
                        sock = socket.socket() 
                        sock.connect(('localhost', 8888))
                        sock.setblocking(False) 
                        message = network({"version": 1, "command": "ping"})
                        if message["status"] == 200:
                            data["ip"] = connect_ip.text
                            data["port"] = port
                            place = "LOGIN"
                            with codecs.open("data.json", "w", "utf_8_sig") as f:
                                json.dump(data, f)

                except ValueError:
                    modal_showing = True
                    modal = Modal((55, 60, 75), (screen_width // 2 - 200, screen_height // 2 - 50, 400, 100), font, "Неверный порт")
        else:
            connect_ip.draw(screen)
            connect_port.draw(screen)
            connect_button.draw(screen)
    elif place == "SEARCH":
        to_settings.update(events)
        to_chats.update(events)
        to_search.update(events)
        
        if to_settings.clicked:
            place = "SETTINGS"
            to_settings.pressed = True
            to_search.pressed = False
        elif to_chats.clicked:
            place = "CHATS"
            to_search.pressed = False
        else:
            to_search.pressed = True
            to_settings.pressed = False
            search_text.update(events)
            search_button.update(events)
            if search_button.clicked:
                if search_text.text == data["login"]:
                    modal_showing = True
                    modal = Modal((55, 60, 75), (screen_width // 2 - 200, screen_height // 2 - 50, 400, 100), font, f"Вы не можете создать чат с самим собой")
                else:
                    message = network({"version": 1, "command": "new chat", "login": data["login"], "password": data["password"], "user": search_text.text})
                    if message["status"] == 200:
                        messages = network({"version": 1, "command": "get messages", "login": data["login"], "password": data["password"]})["messages"]
                        place = "CHATS"
                        create()
                        chat = None
                        to_search.pressed = False
                        modal_showing = True
                        modal = Modal((55, 60, 75), (screen_width // 2 - 200, screen_height // 2 - 50, 400, 100), font, f"Cоздан чат с пользователем {search_text.text}")
                    elif message["status"] == 404 and message["message"] == "No user":
                        modal_showing = True
                        modal = Modal((55, 60, 75), (screen_width // 2 - 200, screen_height // 2 - 50, 400, 100), font, f"Пользователя {search_text.text} не существует")
                    elif message["status"] == 409:
                        modal_showing = True
                        modal = Modal((55, 60, 75), (screen_width // 2 - 200, screen_height // 2 - 50, 400, 100), font, f"У вас уже есть чат с {search_text.text}")
                    search_text.text = ""
            search_text.draw(screen)
            search_button.draw(screen)
        
        to_search.draw(screen)
        to_settings.draw(screen)
        to_chats.draw(screen)

    if modal_showing == True:
        modal.update(events)
        modal.draw(screen)

        if modal.showed == False:
            modal_showing = False
            modal = None

    for event in events:
        if event.type == pygame.QUIT:
            running = False

    close.update(events)
    if close.clicked:
        running = False
    close.draw(screen)

    iconify_button.update(events)
    if iconify_button.clicked:
        pygame.display.iconify()
    iconify_button.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()