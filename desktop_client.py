import os
import sys
import json
import pygame
import codecs
import socket

pygame.init()
info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)
pygame.display.set_caption("TrueGram")
font = pygame.font.SysFont(None, 36)

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
        pygame.draw.rect(screen, self.current_color, self.position, border_radius=8)
        text_rect = self.text.get_rect(center=self.position.center)
        screen.blit(self.text, text_rect)
        self.current_color = self.standart_color

class TextField():
    def __init__(self, pColor, pPosition, pFont, pText):
        self.font = pFont
        self.color = pColor
        self.position = pygame.Rect(pPosition)
        self.text = pText

    def draw(self, screen):
        new_text = self.text
        if len(self.text) > 50:
            new_text = "..." + self.text[50::]
        text = self.font.render(new_text, True, (255, 255, 255))
        pygame.draw.rect(screen, self.color, self.position, border_radius=8)
        text_rect = text.get_rect(center=self.position.center)
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
        new_text = self.text
        if len(self.text) > 50:
            new_text = "..." + self.text[50::]
        text = self.font.render(new_text, True, (255, 255, 255))
        pygame.draw.rect(screen, self.current_color, self.position, border_radius=8)
        text_rect = text.get_rect(center=self.position.center)
        screen.blit(text, text_rect)
          
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
        pygame.draw.rect(screen, self.color, self.position, border_radius=8)
        self.close.draw(screen)
        text_rect = self.text.get_rect(center=self.position.center)
        screen.blit(self.text, text_rect)

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

def network(request):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client.connect(('localhost', 8888))

    request = json.dumps(request)
    request = str(len(request)) + " " + request
    client.send(request.encode())

    length_str = ""
    while True:
        char = client.recv(1).decode()
        if char == " ":
            break
        length_str += char
    
    message_length = int(length_str)
    
    message_data = client.recv(message_length)
    
    message = json.loads(message_data.decode())
    client.close()
    return message

current_chat = None

just_button = PositionButton((50, 55, 65), (80, 85, 100), (200, 200, 200), (0, 0, screen_width // 5 * 2, screen_height // 10), font, "Чаты")

to_settings = PositionButton((50, 55, 65), (80, 85, 100), (200, 200, 200), (0, 0, screen_width // 10, screen_height // 10), font, "Н")

to_chats = PositionButton((50, 55, 65), (80, 85, 100), (200, 200, 200), (0, screen_height // 10, screen_width // 10, screen_height // 10), font, "Ч")

input = TextInput((40, 45, 55), (75, 80, 95), (screen_width // 5 * 2, screen_height // 10 * 9, screen_width // 10 * 5, screen_height // 10), font, "Нажмите, что бы ввести текст")

name = TextField((35, 40, 50), (screen_width // 5 * 2, 0, screen_width // 5 * 3, screen_height // 10), font, current_chat)

send = Button((70, 75, 85), (100, 105, 120), (screen_width // 10 * 9, screen_height // 10 * 9, screen_width // 10, screen_height // 10), font, "»")

close = Button((100, 100, 120), (220, 60, 60), (screen_width - 30, 0, 30, 30), font, "X")

login_login = TextInput((40, 45, 55), (75, 80, 95), (screen_width // 5 * 2, screen_height // 10 * 3, screen_width // 5, screen_height // 10), font, "Введите логин")

password_login = TextInput((40, 45, 55), (75, 80, 95), (screen_width // 5 * 2, screen_height // 10 * 5, screen_width // 5, screen_height // 10), font, "Введите пароль")

login_button = Button((70, 75, 85), (100, 105, 120), (screen_width // 5 * 2, screen_height // 10 * 7, screen_width // 5, screen_height // 10), font, "Войти")

login_registration = TextInput((40, 45, 55), (75, 80, 95), (screen_width // 5 * 2, screen_height // 10 * 1, screen_width // 5, screen_height // 10), font, "Введите логин")

password1_registration = TextInput((40, 45, 55), (75, 80, 95), (screen_width // 5 * 2, screen_height // 10 * 3, screen_width // 5, screen_height // 10), font, "Введите пароль")

password2_registration = TextInput((40, 45, 55), (75, 80, 95), (screen_width // 5 * 2, screen_height // 10 * 5, screen_width // 5, screen_height // 10), font, "Подтвердите пароль")

registration_button = Button((70, 75, 85), (100, 105, 120), (screen_width // 5 * 2, screen_height // 10 * 7, screen_width // 5, screen_height // 10), font, "Зарегестрироваться")

leave = Button((70, 75, 85), (100, 105, 120), (screen_width // 5 * 2, screen_height // 10 * 7, screen_width // 5, screen_height // 10), font, "Выйти")

messages = {}

chats = []

place = "LOGIN"

if os.path.exists("data.json"):
    with codecs.open("data.json", "r", "utf_8_sig") as f:
        data = json.load(f)
    messages = data["messages"]
else:
    data = {"login": "", "password": "", "messages": {}}
    with codecs.open("data.json", "w", "utf_8_sig") as f:
        json.dump(data, f)
    for i in range(1, 9):
        messages[f"Чат {i}"] = []

if data["login"] == "" or data["password"] == "":
    place = "LOGIN"
else:
    place = "CHATS"
    user = TextField((35, 40, 50), (screen_width // 5 * 2, 0, screen_width // 5 * 3, screen_height // 10), font, f"Пользователь: {data["login"]} | Пароль: {data["password"]}")
    message = network({"version": 1, "command": "get messages", "login": data["login"], "password": data["password"]})
    if message["status"] == 200:
        messages = message["messages"]
        data["messages"] = messages
        with codecs.open("data.json", "w", "utf_8_sig") as f:
            json.dump(data, f)
        i = 1 
        for key in data["messages"].keys():
            chats.append(PositionButton((45, 50, 60), (75, 80, 95), (200, 200, 200), (screen_height // 10 * 2, screen_height // 10 * (i - 1), screen_width // 5 * 2, screen_height // 10), font, key))
            i += 1

modal_showing = False
modal = None
running = True
while running:
    events = pygame.event.get()
    screen.fill((12, 14, 18))

    if place == "LOGIN":
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
                    user = TextField((35, 40, 50), (screen_width // 5 * 2, 0, screen_width // 5 * 3, screen_height // 10), font, f"Пользователь: {data["login"]} | Пароль: {data["password"]}")
                    login_login.activated = False
                    login_login.first = True
                    login_login.text = login_login.standart
                    password_login.activated = False
                    password_login.first = True
                    password_login.text = password_login.standart

                    message1 = network({"version": 1, "command": "get messages", "login": data["login"], "password": data["password"]})
                    if message1["status"] == 200:
                        messages = message1["messages"]
                        data["messages"] = messages
                        with codecs.open("data.json", "w", "utf_8_sig") as f:
                            json.dump(data, f)
                        i = 1 
                        for key in data["messages"].keys():
                            chats.append(PositionButton((45, 50, 60), (75, 80, 95), (200, 200, 200), (0, screen_height // 10 * 2 + (i - 1) * screen_height // 10, screen_width // 5 * 2, screen_height // 10), font, f"Чат {i}"))
                            i += 1
                elif message["status"] == 404:
                    place = "REGISTRATION"
                    modal_showing = not modal_showing
                    if modal_showing:
                            modal = Modal((55, 60, 75), (screen_width // 2 - 200, screen_height // 2 - 50, 400, 100), font, "Аккаунта не существует")
                elif message["status"] == 422:
                    modal_showing = not modal_showing
                    if modal_showing:
                            modal = Modal((55, 60, 75), (screen_width // 2 - 200, screen_height // 2 - 50, 400, 100), font, "Неверный пароль")
            else:
                modal_showing = not modal_showing
                if modal_showing:
                        modal = Modal((55, 60, 75), (screen_width // 2 - 200, screen_height // 2 - 50, 400, 100), font, "Вы не ввели логин или пароль")
        else:
            login_button.draw(screen)
            login_login.draw(screen)
            password_login.draw(screen)
    elif place == "CHATS":
        chat = -1
        j = 0
        for key in messages.keys():
            chats[j].update(events)
            if chats[j].clicked:
                chat = j
                name.text = key
                current_chat = key
                if chats[j].t == current_chat and not chats[j].pressed:
                    current_chat = None
            j += 1
        if chat != -1:
            for i in range(j):
                if i != chat:
                    chats[i].pressed = False
        for i in range(j):
            chats[i].draw(screen)
        if current_chat != None:
            name.draw(screen)
            input.update(events)
            send.update(events)
            if send.clicked:
                if input.first or input.text == "":
                    modal_showing = not modal_showing
                    if modal_showing:
                            modal = Modal((55, 60, 75), (screen_width // 2 - 200, screen_height // 2 - 50, 400, 100), font, "Вы не ввели сообщение")
                else:
                    if current_chat != None:
                        messages[current_chat].append(input.text)
                        print(messages)
                        input.text = ""
                        data["messages"] = messages
                        with codecs.open("data.json", "w", "utf_8_sig") as f:
                            json.dump(data, f)

                    message = network({"version": 1, "command": "update messages", "login": data["login"], "password": data["password"], "messages": messages})

            input.draw(screen)
            send.draw(screen)
        to_settings.update(events)
        to_chats.update(events)
        
        if to_settings.clicked:
            place = "SETTINGS"
            to_settings.pressed = True
            to_chats.pressed = False
        else:
            to_chats.pressed = True
            to_settings.pressed = False
        
        to_settings.draw(screen)
        to_chats.draw(screen)
        if current_chat != None:
            last_messages = messages[current_chat][-7:][::-1]
            for i in range(len(last_messages)):
                message = TextField((20, 22, 28), (screen_width // 5 * 3, screen_height // 10 * (8 - i), screen_width // 5 * 2, screen_height // 10), font, last_messages[i])
                message.draw(screen)
    elif place == "SETTINGS":
        to_settings.update(events)
        to_chats.update(events)
        
        if to_chats.clicked:
            place = "CHATS"
            to_settings.pressed = False
            to_chats.pressed = True
        else:
            to_chats.pressed = False
            to_settings.pressed = True
            user.draw(screen)
            leave.update(events)
            if leave.clicked:
                messages = {}
                for i in range(1, 9):
                    messages[f"Чат {i}"] = []
                data = {"login": "", "password": "", "messages": messages}
                with codecs.open("data.json", "w", "utf_8_sig") as f:
                    json.dump(data, f)   
                    place = "LOGIN"
            else:
                leave.draw(screen)
        to_settings.draw(screen)
        to_chats.draw(screen)
    elif place == "REGISTRATION":
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
                        user = TextField((35, 40, 50), (screen_width // 5 * 2, 0, screen_width // 5 * 3, screen_height // 10), font, f"Пользователь: {data["login"]} | Пароль: {data["password"]}")
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
                    modal_showing = not modal_showing
                    if modal_showing:
                        modal = Modal((55, 60, 75), (screen_width // 2 - 200, screen_height // 2 - 50, 400, 100), font, "Пароли не совпадают")
            else:
                modal_showing = not modal_showing
                if modal_showing:
                        modal = Modal((55, 60, 75), (screen_width // 2 - 200, screen_height // 2 - 50, 400, 100), font, "Вы не ввели логин или пароль")
        else:
            login_registration.draw(screen)
            password1_registration.draw(screen)
            password2_registration.draw(screen)
            registration_button.draw(screen)

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

    pygame.display.flip()

pygame.quit()
sys.exit()