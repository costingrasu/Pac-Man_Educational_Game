import copy
from board import boards
import pygame
import math
import time
# import queue
# import socket
# import threading

# # Host+Port socket
# HOST = '127.0.0.1'  # Loopback address for local testing
# PORT = 12345

# received_data_queue = queue.Queue()
# mareString = ""
# mareString_lock = threading.Lock()


# def handle_receive(conn, addr):
#     print("Connected by", addr)
    
#     while True:
#         # Receive data
#         data = conn.recv(1024)
#         if not data:
#             break
#         # Decode data to a string
#         received_string = data.decode()
#         print("Received:", received_string)
       
#         # Put the received string into the queue
#         received_data_queue.put(received_string)
    
#     print("Client disconnected")
#     conn.close()

# def handle_send(conn, addr):
#     interval = 1 / 60.0
#     while True:
#         start_time = time.time()

#         with mareString_lock:
#             mare_string = f"{center_y // ((770-50)// 32)} {center_x // (720 //30)}"  # Adjust as per your logic
#             print(center_y , center_x)
#             conn.sendall(mare_string.encode())

#         elapsed_time = time.time() - start_time
#         if elapsed_time < interval:
#             time.sleep(interval - elapsed_time)

# def start_server():
#     # Create a socket object
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
#         # Bind the socket to the address and port
#         server_socket.bind((HOST, PORT))
#         # Listen for incoming connections
#         server_socket.listen()
#         print("Server is listening on", (HOST, PORT))

#         while True:
#             # Accept a connection
#             conn, addr = server_socket.accept()
#             # Create a new thread to handle the client
#             receive_thread = threading.Thread(target=handle_receive, args=(conn, addr))
#             send_thread = threading.Thread(target=handle_send, args=(conn, addr))
            
#             # Start both threads
#             receive_thread.start()
#             send_thread.start()

# server_thread = threading.Thread(target=start_server)
# server_thread.start()

pygame.init()

OK=0
WIDTH = 720
HEIGHT = 770
screen = pygame.display.set_mode([WIDTH, HEIGHT])
timer = pygame.time.Clock()
fps = 51
font = pygame.font.Font('assets/font.ttf', 20)
level = copy.deepcopy(boards)
color = (51, 85, 255)
colorbck = (0, 0, 51)
font2 = pygame.font.Font('assets/font.ttf', 32)
line1_text = font2.render("Level 1", True, (153, 221, 255))
line2_text = font2.render("Good luck and", True, (153, 221, 255))
line3_text = font2.render("save the planet!!!", True, (153, 221, 255))
font70=pygame.font.Font('assets/font.ttf', 13)
viata = pygame.transform.scale(pygame.image.load(f'assets/player_life.png'), (30, 30))
viata_x = 600
viata_y = 725

intrb = 0
start_time = time.time()
duration = 11
show_text = True

PI = math.pi
player_images = []
for i in range(1,5):
  player_images.append(pygame.transform.scale(pygame.image.load(f'assets/player_images/{i}.png'), (40,40)))

blinky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/fantoma1.png'), (35, 35))
pinky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/fantoma2.png'), (35, 35))
inky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/fantoma3.png'), (35, 35))
clyde_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/fantoma4.png'), (35, 35))
spooked_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/fantoma_powerup.png'), (35, 35))
dead_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/fantoma_moarta.png'), (35, 35))
player_x = 308
player_y = 655
direction = 0
blinky_direction = 0
inky_direction = 2
pinky_direction = 2
clyde_direction = 2
blinky_x = 345
blinky_y = 345
inky_x = 400
inky_y = 345
pinky_x = 285
pinky_y = 345
clyde_x = 345
clyde_y = 300
counter = 0
flicker = False
# R, L, U, D
turns_allowed = [False, False, False, False]
direction_command = 0
player_speed = 2
score = 0
powerup = False
power_counter = 0
eaten_ghost = [False, False, False, False]
targets = [(player_x, player_y), (player_x, player_y), (player_x, player_y), (player_x, player_y)]
blinky_dead = False
inky_dead = False
clyde_dead = False
pinky_dead = False
blinky_box = False
inky_box = False
clyde_box = False
pinky_box = False
moving = False
ghost_speeds = [2, 2, 2, 2]
startup_counter = 0
lives = 2
game_over = False
game_won = False

class Ghost:
    def __init__(self, x_coord, y_coord, target, speed, img, direct, dead, box, id):
        self.x_pos = x_coord
        self.y_pos = y_coord
        self.center_x = self.x_pos + 19
        self.center_y = self.y_pos + 19
        self.target = target
        self.speed = speed
        self.img = img
        self.direction = direct
        self.dead = dead
        self.in_box = box
        self.id = id
        self.turns, self.in_box = self.check_collisions()
        self.rect = self.draw()

    def draw(self):
        if (not powerup and not self.dead) or (eaten_ghost[self.id] and powerup and not self.dead):
            screen.blit(self.img, (self.x_pos, self.y_pos))
        elif powerup and not self.dead and not eaten_ghost[self.id]:
            screen.blit(spooked_img, (self.x_pos, self.y_pos))
        else:
            screen.blit(dead_img, (self.x_pos, self.y_pos))
        ghost_rect = pygame.rect.Rect((self.center_x - 18, self.center_y - 18), (29, 29))
        return ghost_rect

    def check_collisions(self):
        # R, L, U, D
        num1 = ((HEIGHT - 50) // 32)
        num2 = (WIDTH // 30)
        num3 = 12
        self.turns = [False, False, False, False]
        if 0 < self.center_x // 24 < 29:
            if level[(self.center_y - num3) // num1][self.center_x // num2] == 9:
                self.turns[2] = True
            if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
                    or (level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[1] = True
            if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
                    or (level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[0] = True
            if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                    or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[3] = True
            if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                    or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[2] = True

            if self.direction == 2 or self.direction == 3:
                if 12 <= self.center_x % num2 <= 18:
                    if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[3] = True
                    if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[2] = True
                if 12 <= self.center_y % num1 <= 18:
                    if level[self.center_y // num1][(self.center_x - num2) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x - num2) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[1] = True
                    if level[self.center_y // num1][(self.center_x + num2) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x + num2) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[0] = True

            if self.direction == 0 or self.direction == 1:
                if 12 <= self.center_x % num2 <= 18:
                    if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[3] = True
                    if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[2] = True
                if 12 <= self.center_y % num1 <= 18:
                    if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[1] = True
                    if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[0] = True
        else:
            self.turns[0] = True
            self.turns[1] = True
        if 280 < self.x_pos < 440 and 296 < self.y_pos < 384:
            self.in_box = True
        else:
            self.in_box = False
        return self.turns, self.in_box

    def move_clyde(self):
        # r, l, u, d
        # clyde is going to turn whenever advantageous for pursuit
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.direction = 1
                self.x_pos -= self.speed
            elif self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 720
        elif self.x_pos > 720:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction

    def move_blinky(self):
        # r, l, u, d
        # blinky is going to turn whenever colliding with walls, otherwise continue straight
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[2]:
                self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[3]:
                self.y_pos += self.speed
    
        if self.x_pos < -30:
            self.x_pos = 720
        elif self.x_pos > 720:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction

    def move_inky(self):
        # r, l, u, d
        # inky turns up or down at any point to pursue, but left and right only on collision
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 720
        elif self.x_pos > 720:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction

    def move_pinky(self):
        # r, l, u, d
        # inky is going to turn left or right whenever advantageous, but only up or down on collision
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.direction = 1
                self.x_pos -= self.speed
            elif self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 720
        elif self.x_pos > 720:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction

def draw_lives():
    lives_text = font.render(f'Lives: ', True, color)
    screen.blit(lives_text, (400, 732))
    if lives == 2:
        screen.blit(viata, (viata_x, viata_y))
        screen.blit(viata, (viata_x - 35, viata_y))
        screen.blit(viata, (viata_x - 70, viata_y))
    if lives == 1:
        screen.blit(viata, (viata_x - 35, viata_y))
        screen.blit(viata, (viata_x - 70, viata_y))
    if lives == 0:
        screen.blit(viata, (viata_x - 70, viata_y))
    if lives == -1:
        game_over = True


def draw_score():
    score_text = font.render(f'Score: {score}', True, color)
    screen.blit(score_text, (10, 732))

def draw_misc():
    for i in range(lives):
        screen.blit(pygame.transform.scale(player_images[0], (30, 30)), (650 + i * 40, 915))
    if game_over:
        pygame.draw.rect(screen, colorbck, [0, 200, 800, 300],0, 10)
        gameover_text = font2.render('Game over!',True,color)
        gameover2_text = font2.render('Space bar to restart!', True, color)
        screen.blit(gameover_text, (200, 300))
        screen.blit(gameover2_text, (50, 350))
    if game_won:
        OK = 1
        pygame.draw.rect(screen, colorbck, [0, 200, 800, 300],0, 10)
        gameover_text = font2.render('Victory!', True, color)
        gameover2_text = font2.render('Space bar to Level 2!', True, color)
        screen.blit(gameover_text, (200, 300))
        screen.blit(gameover2_text, (50, 350))

def check_collisions(scor, power, power_count, eaten_ghosts):
    global intrb
    num1 = (HEIGHT - 50) // 32
    num2 = WIDTH // 30
    if 0 < player_x < 696:
        passedQ = False
        if level[center_y // num1][center_x // num2] == 1:
            level[center_y // num1][center_x // num2] = 0
            scor += 10
        if level[center_y // num1][center_x // num2] == 2:
            intrb = intrb + 1
            level[center_y // num1][center_x // num2] = 0
            
            if intrb == 1:
                moving = False

                # Set up the display
                WIDTH1, HEIGHT1 =720, 770
                screen1 = pygame.display.set_mode((WIDTH1, HEIGHT1))
                pygame.display.set_caption("Question Time")

                # Set up fonts
                font = pygame.font.Font('assets/font.ttf', 11)
                small_font = pygame.font.Font('assets/font.ttf', 13)

                # Set up colors
                colorbck = (77, 134, 156)
                colorquestions = (205, 232, 229)
                colorbuttons = (122, 178, 178)
                RED = (255, 0, 0)
                GREEN = (0, 255, 0)


                # Set up the question and answers
                question1 = "What is the primary source of pathogens "
                question2 = "(disease-causing microorganisms) and putrescible organic"
                question3 = " substances in water pollution?"
                answers = ["a)Industrial manufacturing", "b)Agriculture", "c)Sewage & wastewater ", "d)Marine dumping"]
                correct_answer = 2  # Index of the correct answer

                # Button dimensions
                button_width = 670
                button_height = 50
                button_padding = 20

                # Calculate button positions
                button_x = (WIDTH1 - button_width) // 2
                buttons_y = [(HEIGHT1 // 2) + i * (button_height + button_padding) for i in range(len(answers))]

                # Game loop
                running = True
                while running:
                    screen1.fill(colorbck)

                    # Draw the question
                    question1_text = font.render(question1, True, colorquestions)
                    question1_rect = question1_text.get_rect(center=(WIDTH1 // 2, HEIGHT1 // 4))
                    screen1.blit(question1_text, question1_rect)

                    question2_text = font.render(question2, True, colorquestions)
                    question2_rect = question2_text.get_rect(center=(WIDTH1 // 2, HEIGHT1 // 4 + 30))
                    screen1.blit(question2_text, question2_rect)

                    question3_text = font.render(question3, True, colorquestions)
                    question3_rect = question3_text.get_rect(center=(WIDTH1 // 2, HEIGHT1 // 4 + 60))
                    screen1.blit(question3_text, question3_rect)

                    # Draw the buttons with answers
                    for i, answer in enumerate(answers):
                        button_y = buttons_y[i]
                        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
                        pygame.draw.rect(screen1, colorbuttons, button_rect)
                        answer_text = small_font.render(answer, True, colorquestions)
                        answer_rect = answer_text.get_rect(center=button_rect.center)
                        screen1.blit(answer_text, answer_rect)

                    # Check for events
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_x, mouse_y = event.pos
                            for i, button_y in enumerate(buttons_y):
                                button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
                                if button_rect.collidepoint(mouse_x, mouse_y):
                                    if i == correct_answer:
                                        print("Correct!")
                                        passedQ = True
                                        result_text = font.render("Correct!", True, GREEN)
                                    else:
                                        print("Incorrect!")
                                        passedQ = False
                                        result_text = font.render("Incorrect!", True, RED)
                                    result_rect = result_text.get_rect(center=(WIDTH1 // 2, HEIGHT1 // 1.5))
                                    screen1.blit(result_text, result_rect)
                                    pygame.display.flip()
                                    pygame.time.wait(2000)
                                    running = False

                    pygame.display.flip()
            if intrb == 2:
                moving = False

                # Set up the display
                WIDTH2, HEIGHT2 =720, 770
                screen2 = pygame.display.set_mode((WIDTH2, HEIGHT2))
                pygame.display.set_caption("Question Time")

                # Set up fonts
                font = pygame.font.Font('assets/font.ttf', 15)
                small_font = pygame.font.Font('assets/font.ttf', 13)

                # Set up colors
                colorbck = (77, 134, 156)
                colorquestions = (205, 232, 229)
                colorbuttons = (122, 178, 178)
                RED = (255, 0, 0)
                GREEN = (0, 255, 0)


                # Set up the question and answers
                question1 = "Which of the following is NOT"
                question2 = " a solution to prevent "
                question3 = "water pollution?"
                answers = ["a) Wastewater Treatment", "b)Reducing Plastic Waste", "c)Burning Fossil Fuels ", "d)Water Conservation"]
                correct_answer = 2  # Index of the correct answer

                # Button dimensions
                button_width = 670
                button_height = 50
                button_padding = 20

                # Calculate button positions
                button_x = (WIDTH2 - button_width) // 2
                buttons_y = [(HEIGHT2 // 2) + i * (button_height + button_padding) for i in range(len(answers))]

                # Game loop
                running = True
                while running:
                    screen2.fill(colorbck)

                    # Draw the question
                    question1_text = font.render(question1, True, colorquestions)
                    question1_rect = question1_text.get_rect(center=(WIDTH2 // 2, HEIGHT2 // 4))
                    screen2.blit(question1_text, question1_rect)

                    question2_text = font.render(question2, True, colorquestions)
                    question2_rect = question2_text.get_rect(center=(WIDTH2 // 2, HEIGHT2 // 4 + 30))
                    screen2.blit(question2_text, question2_rect)

                    question3_text = font.render(question3, True, colorquestions)
                    question3_rect = question3_text.get_rect(center=(WIDTH2 // 2, HEIGHT2 // 4 + 60))
                    screen2.blit(question3_text, question3_rect)

                    # Draw the buttons with answers
                    for i, answer in enumerate(answers):
                        button_y = buttons_y[i]
                        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
                        pygame.draw.rect(screen2, colorbuttons, button_rect)
                        answer_text = small_font.render(answer, True, colorquestions)
                        answer_rect = answer_text.get_rect(center=button_rect.center)
                        screen2.blit(answer_text, answer_rect)

                    # Check for events
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_x, mouse_y = event.pos
                            for i, button_y in enumerate(buttons_y):
                                button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
                                if button_rect.collidepoint(mouse_x, mouse_y):
                                    if i == correct_answer:
                                        print("Correct!")
                                        passedQ = True
                                        result_text = font.render("Correct!", True, GREEN)
                                    else:
                                        print("Incorrect!")
                                        result_text = font.render("Incorrect!", True, RED)
                                    result_rect = result_text.get_rect(center=(WIDTH2 // 2, HEIGHT2 // 1.5))
                                    screen2.blit(result_text, result_rect)
                                    pygame.display.flip()
                                    pygame.time.wait(2000)
                                    running = False

                    pygame.display.flip()
            if intrb == 3:
                moving = False

                # Set up the display
                WIDTH3, HEIGHT3 =720, 770
                screen3 = pygame.display.set_mode((WIDTH3, HEIGHT3))
                pygame.display.set_caption("Question Time")

                # Set up fonts
                font = pygame.font.Font('assets/font.ttf', 15)
                small_font = pygame.font.Font('assets/font.ttf', 13)

                # Set up colors
                colorbck = (77, 134, 156)
                colorquestions = (205, 232, 229)
                colorbuttons = (122, 178, 178)
                RED = (255, 0, 0)
                GREEN = (0, 255, 0)


                # Set up the question and answers
                question1 = "What is the process of converting"
                question2 = " nitrates into nitrogen gas"
                question3 = " to prevent groundwater contamination?"
                answers = ["a) Green Agriculture", "b)Denitrification", "c)Stormwater Management", "d)Ozone Wastewater Treatment"]
                correct_answer = 1 # Index of the correct answer

                # Button dimensions
                button_width = 670
                button_height = 50
                button_padding = 20

                # Calculate button positions
                button_x = (WIDTH3 - button_width) // 2
                buttons_y = [(HEIGHT3 // 2) + i * (button_height + button_padding) for i in range(len(answers))]

                # Game loop
                running = True
                while running:
                    screen3.fill(colorbck)

                    # Draw the question
                    question1_text = font.render(question1, True, colorquestions)
                    question1_rect = question1_text.get_rect(center=(WIDTH3 // 2, HEIGHT3 // 4))
                    screen3.blit(question1_text, question1_rect)

                    question2_text = font.render(question2, True, colorquestions)
                    question2_rect = question2_text.get_rect(center=(WIDTH3 // 2, HEIGHT3 // 4 + 30))
                    screen3.blit(question2_text, question2_rect)

                    question3_text = font.render(question3, True, colorquestions)
                    question3_rect = question3_text.get_rect(center=(WIDTH3 // 2, HEIGHT3 // 4 + 60))
                    screen3.blit(question3_text, question3_rect)

                    # Draw the buttons with answers
                    for i, answer in enumerate(answers):
                        button_y = buttons_y[i]
                        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
                        pygame.draw.rect(screen3, colorbuttons, button_rect)
                        answer_text = small_font.render(answer, True, colorquestions)
                        answer_rect = answer_text.get_rect(center=button_rect.center)
                        screen3.blit(answer_text, answer_rect)

                    # Check for events
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_x, mouse_y = event.pos
                            for i, button_y in enumerate(buttons_y):
                                button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
                                if button_rect.collidepoint(mouse_x, mouse_y):
                                    if i == correct_answer:
                                        print("Correct!")
                                        passedQ = True
                                        result_text = font.render("Correct!", True, GREEN)
                                    else:
                                        print("Incorrect!")
                                        result_text = font.render("Incorrect!", True, RED)
                                    result_rect = result_text.get_rect(center=(WIDTH3 // 2, HEIGHT3 // 1.5))
                                    screen3.blit(result_text, result_rect)
                                    pygame.display.flip()
                                    pygame.time.wait(2000)
                                    running = False

                    pygame.display.flip()
            if intrb == 4:
                    moving = False
                    # Set up the display
                    WIDTH4, HEIGHT4 =720, 770
                    screen4 = pygame.display.set_mode((WIDTH4, HEIGHT4))
                    pygame.display.set_caption("Question Time")

                    # Set up fonts
                    font = pygame.font.Font('assets/font.ttf', 15)
                    small_font = pygame.font.Font('assets/font.ttf', 13)

                    # Set up colors
                    colorbck = (77, 134, 156)
                    colorquestions = (205, 232, 229)
                    colorbuttons = (122, 178, 178)
                    RED = (255, 0, 0)
                    GREEN = (0, 255, 0)

                    # Set up the question and answers
                    question1 = "Which action is recommended to reduce"
                    question2 = " plastic waste in water systems?"
                    answers = ["a)Use alternatives like reusable utensils,grocery bags", "b)Increase the use of single-use plastic products", "c)Discard plastic waste in water bodies", "d) Shop globally for plastic products"]
                    correct_answer = 0 # Index of the correct answer

                    # Button dimensions
                    button_width = 670
                    button_height = 50
                    button_padding = 20

                    # Calculate button positions
                    button_x = (WIDTH4 - button_width) // 2
                    buttons_y = [(HEIGHT4 // 2) + i * (button_height + button_padding) for i in range(len(answers))]

                    # Game loop
                    running = True
                    while running:
                        screen4.fill(colorbck)

                        # Draw the question
                        question1_text = font.render(question1, True, colorquestions)
                        question1_rect = question1_text.get_rect(center=(WIDTH4 // 2, HEIGHT4 // 4))
                        screen4.blit(question1_text, question1_rect)

                        question2_text = font.render(question2, True, colorquestions)
                        question2_rect = question2_text.get_rect(center=(WIDTH4 // 2, HEIGHT4 // 4 + 30))
                        screen4.blit(question2_text, question2_rect)


                        # Draw the buttons with answers
                        for i, answer in enumerate(answers):
                            button_y = buttons_y[i]
                            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
                            pygame.draw.rect(screen4, colorbuttons, button_rect)
                            answer_text = small_font.render(answer, True, colorquestions)
                            answer_rect = answer_text.get_rect(center=button_rect.center)
                            screen4.blit(answer_text, answer_rect)

                        # Check for events
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                running = False
                            elif event.type == pygame.MOUSEBUTTONDOWN:
                                mouse_x, mouse_y = event.pos
                                for i, button_y in enumerate(buttons_y):
                                    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
                                    if button_rect.collidepoint(mouse_x, mouse_y):
                                        if i == correct_answer:
                                            print("Correct!")
                                            passedQ = True
                                            result_text = font.render("Correct!", True, GREEN)
                                        else:
                                            print("Incorrect!")
                                            result_text = font.render("Incorrect!", True, RED)
                                        result_rect = result_text.get_rect(center=(WIDTH4 // 2, HEIGHT4 // 1.5))
                                        screen4.blit(result_text, result_rect)
                                        pygame.display.flip()
                                        pygame.time.wait(2000)
                                        running = False

                        pygame.display.flip()      

        if passedQ:
            moving = True
            scor += 50
            power = True
            power_count = 0
            eaten_ghosts = [False, False, False, False]
        else:
            moving = True
    return scor, power, power_count, eaten_ghosts


def draw_board(screen, level, OK, flicker, color, HEIGHT, WIDTH):
    num1 = (HEIGHT - 50) // 32
    num2 = WIDTH // 30

    # Load images once
    sticker_sticla = pygame.image.load('assets/dots_images/sticker_sticla.png')
    sticker_dot = pygame.image.load('assets/dots_images/sticker_dot.png')
    sticker_sticla2 = pygame.image.load('assets/dots_images/sticker_sticla2.png')
    sticker_leaf = pygame.image.load('assets/dots_images/sticker_leaf.png')

    # Function to scale and draw image
    def draw_image(image, j, i, scaled_width, scaled_height):
        scaled_image = pygame.transform.scale(image, (scaled_width, scaled_height))
        rect = scaled_image.get_rect()
        rect.center = (j * num2 + 0.5 * num2, i * num1 + 0.5 * num1)
        screen.blit(scaled_image, rect)

    for i in range(len(level)):
        for j in range(len(level[i])):  # j = column, i = row
            sticker_image = None  # Initialize sticker_image to ensure it has a value

            if level[i][j] == 1:
                sticker_image = sticker_dot if OK else sticker_sticla
                draw_image(sticker_image, j, i, 8, 15)
            elif level[i][j] == 2 and not flicker:
                sticker_image = sticker_leaf if OK else sticker_sticla2
                draw_image(sticker_image, j, i, 12, 23)
            elif level[i][j] == 3:
                pygame.draw.line(screen, color, (j * num2 + (0.5 * num2), i * num1),
                                 (j * num2 + (0.5 * num2), i * num1 + num1), 3)
            elif level[i][j] == 4:
                pygame.draw.line(screen, color, (j * num2, i * num1 + (0.5 * num1)),
                                 (j * num2 + num2, i * num1 + (0.5 * num1)), 3)
            elif level[i][j] == 5:
                pygame.draw.arc(screen, color, [(j * num2 - 0.5 * num2), i * num1 + 0.5 * num1, num2, num1], 0, PI / 2,
                                3)
            elif level[i][j] == 6:
                pygame.draw.arc(screen, color, [(j * num2 + 0.5 * num2), i * num1 + 0.5 * num1, num2, num1],
                                PI / 2, PI, 3)
            elif level[i][j] == 7:
                pygame.draw.arc(screen, color, [(j * num2 + 0.5 * num2), i * num1 - 0.5 * num1, num2, num1], PI,
                                3 * PI / 2, 3)
            elif level[i][j] == 8:
                pygame.draw.arc(screen, color, [(j * num2 - 0.5 * num2), i * num1 - 0.5 * num1, num2, num1],
                                3 * PI / 2, 2 * PI, 3)
            elif level[i][j] == 9:
                pygame.draw.line(screen, 'white', (j * num2, i * num1 + (0.5 * num1)),
                                 (j * num2 + num2, i * num1 + (0.5 * num1)), 3)


def draw_player():
    # 0-RIGHT, 1-LEFT, 2-UP, 3-DOWN
    if direction == 0:
        screen.blit(player_images[counter // 5], (player_x, player_y))
    elif direction == 1:
        screen.blit(pygame.transform.flip(player_images[counter // 5], True, False), (player_x, player_y))
    elif direction == 2:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 90), (player_x, player_y))
    elif direction == 3:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 270), (player_x, player_y))


def check_position(centerx, centery):
    turns = [False, False, False, False]
    num1 = (HEIGHT - 50) // 32
    num2 = (WIDTH // 30)
    num3 = 9
    if centerx // 24 < 29:
        if direction == 0:
            if level[centery // num1][(centerx - num3) // num2] < 3:
                turns[1] = True
        if direction == 1:
            if level[centery // num1][(centerx + num3) // num2] < 3:
                turns[0] = True
        if direction == 2:
            if level[(centery + num3) // num1][centerx // num2] < 3:
                turns[3] = True
        if direction == 3:
            if level[(centery - num3) // num1][centerx // num2] < 3:
                turns[2] = True

        if direction == 2 or direction == 3:
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num3) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num3) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 12 <= centery % num1 <= 18:
                if level[centery // num1][(centerx - num2) // num2] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx + num2) // num2] < 3:
                    turns[0] = True
        if direction == 0 or direction == 1:
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num1) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num1) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 12 <= centery % num1 <= 18:
                if level[centery // num1][(centerx - num3) // num2] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx + num3) // num2] < 3:
                    turns[0] = True
    else:
        turns[0] = True
        turns[1] = True

    return turns


def move_player(play_x, play_y):
    # r, l, u, d
    if direction == 0 and turns_allowed[0]:
        play_x += player_speed
    elif direction == 1 and turns_allowed[1]:
        play_x -= player_speed
    if direction == 2 and turns_allowed[2]:
        play_y -= player_speed
    elif direction == 3 and turns_allowed[3]:
        play_y += player_speed
    return play_x, play_y


def get_targets(blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y):
    if player_x < 360:
        runaway_x = 720
    else:
        runaway_x = 0
    if player_y < 360:
        runaway_y = 720
    else:
        runaway_y = 0
    return_target = (304, 320)
    if powerup:
        if not blinky.dead and not eaten_ghost[0]:
            blink_target = (runaway_x, runaway_y)
        elif not blinky.dead and eaten_ghost[0]:
            if 272 < blink_x < 448 and 272 < blink_y < 400:
                blink_target = (320, 80)
            else:
                blink_target = (player_x, player_y)
        else:
            blink_target = return_target
        if not inky.dead and not eaten_ghost[1]:
            ink_target = (runaway_x, player_y)
        elif not inky.dead and eaten_ghost[1]:
            if 272 < ink_x < 448 and 272 < ink_y < 400:
                ink_target = (320, 80)
            else:
                ink_target = (player_x, player_y)
        else:
            ink_target = return_target
        if not pinky.dead:
            pink_target = (player_x, runaway_y)
        elif not pinky.dead and eaten_ghost[2]:
            if 272 < pink_x < 448 and 272 < pink_y < 400:
                pink_target = (320, 80)
            else:
                pink_target = (player_x, player_y)
        else:
            pink_target = return_target
        if not clyde.dead and not eaten_ghost[3]:
            clyd_target = (360, 360)
        elif not clyde.dead and eaten_ghost[3]:
            if 272 < clyd_x < 448 and 272 < clyd_y < 400:
                clyd_target = (320, 80)
            else:
                clyd_target = (player_x, player_y)
        else:
            clyd_target = return_target
    else:
        if not blinky.dead:
            if 272 < blink_x < 448 and 272 < blink_y < 400:
                blink_target = (320, 80)
            else:
                blink_target = (player_x, player_y)
        else:
            blink_target = return_target
        if not inky.dead:
            if 272 < ink_x < 448 and 272 < ink_y < 400:
                ink_target = (320, 80)
            else:
                ink_target = (player_x, player_y)
        else:
            ink_target = return_target
        if not pinky.dead:
            if 272 < pink_x < 448 and 272 < pink_y < 400:
                pink_target = (320, 80)
            else:
                pink_target = (player_x, player_y)
        else:
            pink_target = return_target
        if not clyde.dead:
            if 272 < clyd_x < 448 and 272 < clyd_y < 400:
                clyd_target = (320, 80)
            else:
                clyd_target = (player_x, player_y)
        else:
            clyd_target = return_target
    return [blink_target, ink_target, pink_target, clyd_target]

def draw_help_menu():
    menu_width, menu_height = 725, 200
    menu_x, menu_y = (WIDTH - menu_width) // 2, (HEIGHT - menu_height) // 2

    texts = [
        "Use arrow keys to move:",
        "Left/Right - Move sideways",
        "Up/Down - Move up/down",
        "",
        "Goal:",
        "Save the planet by collecting",
        "all items and avoiding enemies."
    ]

    for i, text in enumerate(texts):
        text_surface = font.render(text, True, (153, 221, 255))
        screen.blit(text_surface, (menu_x + 20, menu_y + 20 + i * 30))

def draw_credentials_menu():
    menu_width, menu_height = 600, 120
    menu_x, menu_y = 0, 0

    texts = [
        "Credentials:",
        "EU Programme Erasmus+",
        "",

        "Project title:",
        "Gender, Digitalization, Green:",
        "Ensuring a Sustainable Future for all in Europe ",
        "Module 6",
        "",

        "Project No:",
        "2023-1-RO01- KA220-HED-000154433",
        "",

        "Students:",
        "Stefan Bucur",
        "stefan.bucur0707@stud.acs.upb.ro",

        "Silvia Cioroiu",
        "silvia.cioroiu@stud.acs.upb.ro",
        "Costin-Alexandru Grasu",
        "costin.grasu@stud.acs.upb.ro",
        "Daria Magureanu",
        "daria.magureanu@stud.acs.upb.ro",
        "Evelina-Maria Pintea",
        "evelina.pintea@stud.acs.upb.ro",
        "Miruna Tancu",
        "miruna.tancu@stud.acs.upb.ro"
        "",
        "Teachers:Prof M. Caramihai & D Chis"

    ]

    for i, text in enumerate(texts):
        text_surface =font70.render(text, True, (153, 221, 255))
        screen.blit(text_surface, (menu_x + 20, menu_y + 20 + i * 30))

class GameState:
    PLAYING, SHOW_LEVEL, SHOW_HELP, SHOW_CREDENTIALS= range(4)


game_state = GameState.SHOW_CREDENTIALS
level1_display_time = 3 
help_menu_display_time = 4
credentials_display_time = 4

run = True
while run:
    timer.tick(fps)
    if counter < 19:
        counter += 1
        if counter > 3:
            flicker = False
    else:
        counter = 0
        flicker = True
    if powerup and power_counter < 600:
        power_counter += 1
    elif powerup and power_counter >= 600:
        power_counter = 0
        powerup = False
        eaten_ghost = [False, False, False, False]
    if startup_counter < 180 and not game_over and not game_won:
        moving = False
        startup_counter += 1
    else:
        moving = True

    screen.fill(colorbck)

    current_time = time.time()

    draw_board(screen, level, OK, flicker, color, HEIGHT, WIDTH)
    draw_score()
    draw_lives()

    center_x = player_x + 18
    center_y = player_y + 17
    if powerup:
        ghost_speeds = [1, 1, 1, 1]
    else:
        ghost_speeds = [2, 2, 2, 2]
    if eaten_ghost[0]:
        ghost_speeds[0] = 2
    if eaten_ghost[1]:
        ghost_speeds[1] = 2
    if eaten_ghost[2]:
        ghost_speeds[2] = 2
    if eaten_ghost[3]:
        ghost_speeds[3] = 2
    if blinky_dead:
        ghost_speeds[0] = 4
    if inky_dead:
        ghost_speeds[1] = 4
    if pinky_dead:
        ghost_speeds[2] = 4
    if clyde_dead:
        ghost_speeds[3] = 4

    game_won = True
    for i in range(len(level)):
        if 1 in level[i] or 2 in level[i]:
            game_won = False

    player_circle = pygame.draw.circle(screen, 'black', (center_x, center_y), 12, 2)
    draw_player()
    blinky = Ghost(blinky_x, blinky_y, targets[0], ghost_speeds[0], blinky_img, blinky_direction, blinky_dead,
                   blinky_box, 0)
    inky = Ghost(inky_x, inky_y, targets[1], ghost_speeds[1], inky_img, inky_direction, inky_dead,
                 inky_box, 1)
    pinky = Ghost(pinky_x, pinky_y, targets[2], ghost_speeds[2], pinky_img, pinky_direction, pinky_dead,
                  pinky_box, 2)
    clyde = Ghost(clyde_x, clyde_y, targets[3], ghost_speeds[3], clyde_img, clyde_direction, clyde_dead,
                  clyde_box, 3)
    draw_misc()
    targets = get_targets(blinky_x, blinky_y, inky_x, inky_y, pinky_x, pinky_y, clyde_x, clyde_y)

    turns_allowed = check_position(center_x, center_y)
    
   
    if time.time() - start_time >= duration:
        show_text = False

    if show_text:
        pygame.draw.rect(screen, colorbck, (0, 0, 720, 770))

    if game_state == GameState.SHOW_CREDENTIALS:
        if current_time - start_time <= credentials_display_time:
            moving = False  
            draw_credentials_menu()
        else:
            game_state = GameState.SHOW_LEVEL
            level_start_time = current_time  

    elif game_state == GameState.SHOW_LEVEL:
        if current_time - level_start_time <= level1_display_time:
            moving = False
            screen.blit(line1_text, (250, 310))
            screen.blit(line2_text, (170, 360))
            screen.blit(line3_text, (100, 410))
        else:
            game_state = GameState.SHOW_HELP
            help_menu_start_time = current_time 

    elif game_state == GameState.SHOW_HELP:
        if current_time - help_menu_start_time <= help_menu_display_time:
            moving = False
            draw_help_menu()
        else:
            game_state = GameState.PLAYING
            moving = True  

    elif game_state == GameState.PLAYING:
        pass

    if moving:
        player_x, player_y = move_player(player_x, player_y)
        if not blinky_dead and not blinky.in_box:
            blinky_x, blinky_y, blinky_direction = blinky.move_blinky()
        else:
            blinky_x, blinky_y, blinky_direction = blinky.move_clyde()
        if not pinky_dead and not pinky.in_box:
            pinky_x, pinky_y, pinky_direction = pinky.move_pinky()
        else:
            pinky_x, pinky_y, pinky_direction = pinky.move_clyde()
        if not inky_dead and not inky.in_box:
            inky_x, inky_y, inky_direction = inky.move_inky()
        else:
            inky_x, inky_y, inky_direction = inky.move_clyde()
        clyde_x, clyde_y, clyde_direction = clyde.move_clyde()
    score, powerup, power_counter, eaten_ghost = check_collisions(score, powerup, power_counter, eaten_ghost)

     
    if not powerup:
        if (player_circle.colliderect(blinky.rect) and not blinky.dead) or \
                (player_circle.colliderect(inky.rect) and not inky.dead) or \
                (player_circle.colliderect(pinky.rect) and not pinky.dead) or \
                (player_circle.colliderect(clyde.rect) and not clyde.dead):
            if lives > 0:
                lives -= 1
                startup_counter = 0
                powerup = False
                power_counter = 0
                player_x = 308
                player_y = 655
                direction = 0
                direction_command = 0
                blinky_direction = 2
                inky_direction = 2
                pinky_direction = 2
                clyde_direction = 2
                blinky_x = 345
                blinky_y = 345
                inky_x = 400
                inky_y = 345
                pinky_x = 285
                pinky_y = 345
                clyde_x = 345
                clyde_y = 300
                eaten_ghost = [False, False, False, False]
                blinky_dead = False
                inky_dead = False
                clyde_dead = False
                pinky_dead = False
            else:
                game_over = True
                moving = False
                startup_counter = 0
    if powerup and player_circle.colliderect(blinky.rect) and eaten_ghost[0] and not blinky.dead:
        if lives > 0:
            lives -= 1
            startup_counter = 0
            powerup = False
            power_counter = 0
            player_x = 308
            player_y = 655
            direction = 0
            direction_command = 0
            blinky_direction = 2
            inky_direction = 2
            pinky_direction = 2
            clyde_direction = 2
            blinky_x = 345
            blinky_y = 345
            inky_x = 400
            inky_y = 345
            pinky_x = 285
            pinky_y = 345
            clyde_x = 345
            clyde_y = 300
            eaten_ghost = [False, False, False, False]
            blinky_dead = False
            inky_dead = False
            clyde_dead = False
            pinky_dead = False
        else:
            game_over = True
            moving = False
            startup_counter = 0
    if powerup and player_circle.colliderect(inky.rect) and eaten_ghost[1] and not inky.dead:
        if lives > 0:
            lives -= 1
            startup_counter = 0
            powerup = False
            power_counter = 0
            player_x = 308
            player_y = 655
            direction = 0
            direction_command = 0
            blinky_direction = 2
            inky_direction = 2
            pinky_direction = 2
            clyde_direction = 2
            blinky_x = 345
            blinky_y = 345
            inky_x = 400
            inky_y = 345
            pinky_x = 285
            pinky_y = 345
            clyde_x = 345
            clyde_y = 300
            eaten_ghost = [False, False, False, False]
            blinky_dead = False
            inky_dead = False
            clyde_dead = False
            pinky_dead = False
        else:
            game_over = True
            moving = False
            startup_counter = 0
    if powerup and player_circle.colliderect(pinky.rect) and eaten_ghost[2] and not pinky.dead:
        if lives > 0:
            lives -= 1
            startup_counter = 0
            powerup = False
            power_counter = 0
            player_x = 308
            player_y = 655
            direction = 0
            direction_command = 0
            blinky_direction = 2
            inky_direction = 2
            pinky_direction = 2
            clyde_direction = 2
            blinky_x = 345
            blinky_y = 345
            inky_x = 400
            inky_y = 345
            pinky_x = 285
            pinky_y = 345
            clyde_x = 345
            clyde_y = 300
            eaten_ghost = [False, False, False, False]
            blinky_dead = False
            inky_dead = False
            clyde_dead = False
            pinky_dead = False
        else:
            game_over = True
            moving = False
            startup_counter = 0
    if powerup and player_circle.colliderect(clyde.rect) and eaten_ghost[3] and not clyde.dead:
        if lives > 0:
            lives -= 1
            startup_counter = 0
            powerup = False
            power_counter = 0
            player_x = 308
            player_y = 655
            direction = 0
            direction_command = 0
            blinky_direction = 2
            inky_direction = 2
            pinky_direction = 2
            clyde_direction = 2
            blinky_x = 345
            blinky_y = 345
            inky_x = 400
            inky_y = 345
            pinky_x = 285
            pinky_y = 345
            clyde_x = 345
            clyde_y = 300
            eaten_ghost = [False, False, False, False]
            blinky_dead = False
            inky_dead = False
            clyde_dead = False
            pinky_dead = False
        else:
            game_over = True
            moving = False
            startup_counter = 0
    if powerup and player_circle.colliderect(blinky.rect) and not blinky.dead and not eaten_ghost[0]:
        blinky_dead = True
        eaten_ghost[0] = True
        score += (2 ** eaten_ghost.count(True)) * 100
    if powerup and player_circle.colliderect(inky.rect) and not inky.dead and not eaten_ghost[1]:
        inky_dead = True
        eaten_ghost[1] = True
        score += (2 ** eaten_ghost.count(True)) * 100
    if powerup and player_circle.colliderect(pinky.rect) and not pinky.dead and not eaten_ghost[2]:
        pinky_dead = True
        eaten_ghost[2] = True
        score += (2 ** eaten_ghost.count(True)) * 100
    if powerup and player_circle.colliderect(clyde.rect) and not clyde.dead and not eaten_ghost[3]:
        clyde_dead = True
        eaten_ghost[3] = True
        score += (2 ** eaten_ghost.count(True)) * 100



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direction_command = 0
            if event.key == pygame.K_LEFT:
                direction_command = 1
            if event.key == pygame.K_UP:
                direction_command = 2
            if event.key == pygame.K_DOWN:
                direction_command = 3
            if event.key == pygame.K_SPACE and (game_over==False or game_won):
                powerup = False
                power_counter = 0
                lives -= 1
                startup_counter = 0
                player_x = 308
                player_y = 655
                direction = 0
                direction_command = 0
                blinky_direction = 2
                inky_direction = 2
                pinky_direction = 2
                clyde_direction = 2
                blinky_x = 345
                blinky_y = 345
                inky_x = 400
                inky_y = 345
                pinky_x = 285
                pinky_y = 345
                clyde_x = 345
                clyde_y = 300
                intrb = 0
                eaten_ghost = [False, False, False, False]
                blinky_dead = False
                inky_dead = False
                clyde_dead = False
                pinky_dead = False
                score = 0
                lives = 2
                level = copy.deepcopy(boards)
                game_over = False
                game_won = False
                colorbck = (26, 77, 46)
                color =(122, 186, 120)
                OK = 1
            if event.key == pygame.K_SPACE and (game_over==True):
                powerup = False
                power_counter = 0
                lives -= 1
                startup_counter = 0
                player_x = 308
                player_y = 655
                direction = 0
                direction_command = 0
                blinky_direction = 2
                inky_direction = 2
                pinky_direction = 2
                clyde_direction = 2
                blinky_x = 345
                blinky_y = 345
                inky_x = 400
                intrb = 0
                inky_y = 345
                pinky_x = 285
                pinky_y = 345
                clyde_x = 345
                clyde_y = 300
                eaten_ghost = [False, False, False, False]
                blinky_dead = False
                inky_dead = False
                clyde_dead = False
                pinky_dead = False
                score = 0
                lives = 2
                level = copy.deepcopy(boards)
                game_over = False
                game_won = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT and direction_command == 0:
                direction_command = direction
            if event.key == pygame.K_LEFT and direction_command == 1:
                direction_command = direction
            if event.key == pygame.K_UP and direction_command == 2:
                direction_command = direction
            if event.key == pygame.K_DOWN and direction_command == 3:
                direction_command = direction

    if direction_command == 0 and turns_allowed[0]:
        direction = 0
    if direction_command == 1 and turns_allowed[1]:
        direction = 1
    if direction_command == 2 and turns_allowed[2]:
        direction = 2
    if direction_command == 3 and turns_allowed[3]:
        direction = 3

    if player_x > 720:
        player_x = 0
    elif player_x < 0:
        player_x = 720

    if blinky.in_box and blinky_dead:
        blinky_dead = False
    if inky.in_box and inky_dead:
        inky_dead = False
    if pinky.in_box and pinky_dead:
        pinky_dead = False
    if clyde.in_box and clyde_dead:
        clyde_dead = False

    pygame.display.flip()
pygame.quit()