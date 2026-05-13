import pygame
import sys

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

class TextInput():
    def __init__(self, pColor, pPosition, pFont):
        self.font = pFont
        self.color = pColor
        self.position = pygame.Rect(pPosition)
        self.text = "Нажмите, чтобы вводить текст"
        self.activated = False

    def update(self, events):
        mouse_pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.position.collidepoint(mouse_pos):
                self.activated = not self.activated
                self.text = "" if self.text == "Нажмите, чтобы вводить текст" else "Нажмите, чтобы вводить текст"
        
        for event in events:
            if event.type == pygame.KEYDOWN and self.activated:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

    def draw(self, screen):
        text = self.font.render(self.text, True, (255, 255, 255))
        pygame.draw.rect(screen, self.color, self.position, border_radius=8)
        text_rect = text.get_rect(center=self.position.center)
        screen.blit(text, text_rect)

class TextField():
    def __init__(self, pColor, pPosition, pFont, pText):
        self.font = pFont
        self.color = pColor
        self.position = pygame.Rect(pPosition)
        self.text = pText

    def draw(self, screen):
        text = self.font.render(self.text, True, (255, 255, 255))
        pygame.draw.rect(screen, self.color, self.position, border_radius=8)
        text_rect = text.get_rect(center=self.position.center)
        screen.blit(text, text_rect)
          
class Modal():
    def __init__(self, pColor, pPosition, pFont, pText):
        self.font = pFont
        self.color = pColor
        self.position = pygame.Rect(pPosition)
        self.text = self.font.render(pText, True, (255, 255, 255))
        self.showed = True
        self.close = Button((70, 130, 180), (255, 0, 0), (pPosition[0] + pPosition[2] - 30, pPosition[1], 30, 30), self.font, "X")

    def update(self, events):
        self.close.update(events)
        if self.close.clicked:
            self.showed = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.position, border_radius=8)
        self.close.draw(screen)
        text_rect = self.text.get_rect(center=self.position.center)
        screen.blit(self.text, text_rect)

logged = False
running = True

#while not logged: TODO вход в аккаунт
#    events = pygame.event.get()
#    for event in events:
#        if event.type == pygame.QUIT:
#            running = False
#    screen.fill((20, 20, 25))    
#    pygame.display.flip()

current_chat = "dev"

settings = Button((40, 40, 50), (60, 60, 70), (0, 0, screen_width // 5 * 2, screen_height // 10), font, "Настройки")

input = TextInput((30, 30, 40), (screen_width // 5 * 2, screen_height // 10 * 9, screen_width // 10 * 5, screen_height // 10), font)

name = TextField((25, 25, 35), (screen_width // 5 * 2, 0, screen_width // 5 * 3, screen_height // 10 * 2), font, current_chat)

chats_list = TextField((25, 25, 35), (0, screen_height // 10, screen_width // 5 * 2, screen_height // 10), font, "Список чатов")

send = Button((55, 55, 65), (75, 75, 85), (screen_width // 10 * 9, screen_height // 10 * 9, screen_width // 10, screen_height // 10), font, "»")

close = Button((70, 130, 180), (255, 0, 0), (screen_width - 30, 0, 30, 30), font, "X")

messages = []

chats = []

for i in range(1, 9):
    chats.append(Button((35, 35, 45), (55, 55, 65), (0, screen_height // 10 * 2 + (i - 1) * screen_height // 10, screen_width // 5 * 2, screen_height // 10), font, f"Чат {i}"))

modal_showing = False
modal = None
while running:
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            running = False
    screen.fill((20, 20, 25))

    if modal_showing == True:
        modal.update(events)
        modal.draw(screen)

        if modal.showed == False:
            modal_showing = False
            modal = None
    chats_list.draw(screen)
    for i in range(8):
        chats[i].update(events)
        if chats[i].clicked and f"Чат {i + 1}" != current_chat:
            name.text = f"Чат {i + 1}"
            current_chat = f"Чат {i + 1}"
            messages = []
        chats[i].draw(screen)
    name.draw(screen)
    settings.update(events)
    if settings.clicked:
        modal_showing = not modal_showing
    if modal_showing:
            modal = Modal((45, 45, 55), (screen_width // 2 - 100, screen_height // 2 - 50, 200, 100), font, "нету")
    settings.draw(screen)
    input.update(events)
    send.update(events)
    if send.clicked:
        messages.append(input.text)
        input.text = ""

        #import socket TODO запрос к серверу

        #client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #client.connect(('localhost', 8888))

        #request = messages[-1].encode()
        #client.send(request)

        #response = client.recv(4096)
        #print(response.decode())

        #client.close()

    input.draw(screen)
    send.draw(screen)
    close.update(events)
    if close.clicked:
        running = False
    close.draw(screen)

    last_messages = messages[-7:][::-1]
    for i in range(len(last_messages)):
        message = TextField((0, 0, 0), (screen_width // 5 * 3, screen_height // 10 * (8 - i), screen_width // 5 * 2, screen_height // 10), font, last_messages[i])
        message.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()