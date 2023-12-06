import pygame
import sys
import random
from pygame.locals import *
import threading

mainImg = pygame.image.load("image/title_page.png")
wallImg1 = pygame.image.load("image/wall2.jpg")
wallImg2 = pygame.image.load("image/wall1.jpg")
darkImg = pygame.image.load("image/dark.png")
backgroundImg = pygame.image.load("image/question_back.png")
imgQuestion = pygame.image.load("image/question1.png")
floorImg = [
    pygame.image.load("image/floor.jpg"),
    pygame.image.load("image/floor.jpg"),
    pygame.image.load("image/questionbox.jpg")
]
imgPlayer = [
    pygame.image.load("image/player7.png"),
    pygame.image.load("image/player8.png"),
    pygame.image.load("image/player1.png"),
    pygame.image.load("image/player2.png"),
    pygame.image.load("image/player3.png"),
    pygame.image.load("image/player6.png"),
    pygame.image.load("image/player5.png"),
    pygame.image.load("image/player4.png"),
    pygame.image.load("image/player0.png")
]

v = 1
index = 0
timer = 0
floor = 0
fl_max = 1
welcome = 0

po_x = 0
po_y = 0
po_d = 0
po_a = 0

question_lev = 0
question_x = 0
question_y = 0
question_show = 0

key_command = 0

COMMANDQ1 = ["[1] 43", "[2] 52", "[3] 48", "[4] 58"]
COMMANDQ2 = ["[1] 5638", "[2] 6902", "[3] 7843", "[4] 8679"]
COMMANDQ3 = ["[1] 60", "[2] 70", "[3] 80", "[4] 90"]
COMMANDQ4 = ["[1] 113", "[2]133", "[3]154", "[4]174"]

WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (0,0,0)
RED = (255, 0, 0)
BLINK = [(224,255,255), (192,240,255),(128,224,255),(64,192,255),(128,224,255),(192,240,255)] 

ROOM_W = 11
ROOM_H = 9
map = []

for y in range(ROOM_H):
    map.append([0] * ROOM_W)

ROOM_DEEP_w = ROOM_W * 3
ROOM_DEEP_h = ROOM_H * 3
room = []
for y in range(ROOM_DEEP_h):
    room.append([0] * ROOM_DEEP_w)

def make_room(): 
    XP = [0, 1, 0, -1]
    YP = [-1, 0, 1, 0]

    for x in range(ROOM_W):
        map[0][x] = 1
        map[ROOM_H - 1][x] = 1
    for y in range(1, ROOM_H - 1):
        map[y][0] = 1
        map[y][ROOM_W - 1] = 1
    for y in range(1, ROOM_H - 1):
        for x in range(1, ROOM_W - 1):
            map[y][x] = 0

    map[1][1] = 1
    map[1][2] = 1
    map[1][10] = 1
    for y in range(3,5):
        for x in range(3,6):
            map[y][x] = 1 
    for y in range(6,8):
        for x in range(1,3):
            map[y][x] = 1 
    for y in range(6,8):
        for x in range(7,10):
            map[y][x] = 1 
    
    for y in range(ROOM_DEEP_h):
        for x in range(ROOM_DEEP_w):
            room[y][x] = 9

    for y in range(1, ROOM_H - 1):
        for x in range(1, ROOM_W - 1):
            dx = x * 3 + 1
            dy = y * 3 + 1
            if map[y][x] == 0:
                for ry in range(-1, 2):
                        for rx in range(-1, 2):
                            room[dy + ry][dx + rx] = 0

def draw_room(bg, fnt):
    bg.fill(BLACK)
    for y in range(-4, 6):
        for x in range(-5, 6):
            X = (x + 5) * 80
            Y = (y + 4) * 80
            dx = po_x + x
            dy = po_y + y
            if 0 <= dx and dx < ROOM_DEEP_w and 0 <= dy and dy < ROOM_DEEP_h:
                if room[dy][dx] <= 3:
                    bg.blit(floorImg[room[dy][dx]], [X, Y])
                if room[dy][dx] == 9:
                    bg.blit(wallImg1, [X, Y - 40])
                    if dy >= 1 and room[dy - 1][dx] == 9:
                        bg.blit(wallImg2, [X, Y - 80])
            if x == 0 and y == 0: 
                bg.blit(imgPlayer[po_a], [X, Y - 40])
    bg.blit(darkImg, [0, 0]) 

def put_quizbox(): 
    global po_x, po_y, po_d, po_a

    room[9][5] = 2
    room[5][14] = 2
    room[11][22] = 2
    room[21][15] = 2

    while True:
        po_x = random.randint(3, ROOM_DEEP_w - 4)
        po_y = random.randint(3, ROOM_DEEP_h - 4)
        if (room[po_y][po_x] == 0):
            break
    po_d = 1
    po_a = 2

def move_player(key):
    global index, timer, po_x, po_y, po_d, po_a, po_life

    if room[po_y][po_x] == 2: 
        if po_y == 9 and po_x == 5:
            room[po_y][po_x] = 0
            index = 10
            timer = 0
            return
        if po_y == 5 and po_x == 14:
            room[po_y][po_x] = 0
            index = 41
            timer = 0
            return
        if po_y == 11 and po_x == 22:
            room[po_y][po_x] = 0
            index = 42
            timer = 0
            return
        if po_y == 21 and po_x == 15:
            room[po_y][po_x] = 0
            index = 43
            timer = 0
            return

    x = po_x
    y = po_y
    if key[K_UP] == 1:
        po_d = 0
        if room[po_y - 1][po_x] != 9:
            po_y = po_y - 1
    if key[K_DOWN] == 1:
        po_d = 1
        if room[po_y + 1][po_x] != 9:
            po_y = po_y + 1
    if key[K_LEFT] == 1:
        po_d = 2
        if room[po_y][po_x - 1] != 9:
            po_x = po_x - 1
    if key[K_RIGHT] == 1:
        po_d = 3
        if room[po_y][po_x + 1] != 9:
            po_x = po_x + 1
    po_a = po_d * 2
    if po_x != x or po_y != y: 
        po_a = po_a + timer % 2  

def draw_text(bg, txt, x, y, fnt, col): 
    show_text = fnt.render(txt, True, BLACK)
    bg.blit(show_text, [x + 1, y + 2])
    show_text = fnt.render(txt, True, col)
    bg.blit(show_text, [x, y])

def display_image(bg, img_path, x, y):
    img = pygame.image.load(img_path)
    bg.blit(img, (x, y))


def init_quiz1(): 
    global imgQuestion, question_lev, question_x, question_y 
    typ = 0
    imgQuestion = pygame.image.load("image/question1.png")
    question_lev = 1
    question_x = 440 - imgQuestion.get_width() / 2
    question_y = 560 - imgQuestion.get_height()

def init_quiz2(): 
    global imgQuestion, question_lev, question_x, question_y
    typ = 1
    imgQuestion = pygame.image.load("image/question2.png")
    question_lev = 1
    question_x = 440 - imgQuestion.get_width() / 2
    question_y = 560 - imgQuestion.get_height()

def init_quiz3(): 
    global imgQuestion, question_lev, question_x, question_y
    typ = 2
    imgQuestion = pygame.image.load("image/question3.png")
    question_lev = 1
    question_x = 440 - imgQuestion.get_width() / 2
    question_y = 560 - imgQuestion.get_height()

def init_quiz4(): 
    global imgQuestion, question_lev, question_x, question_y
    typ = 3
    imgQuestion = pygame.image.load("image/question4.png")
    question_lev = 1
    question_x = 440 - imgQuestion.get_width() / 2
    question_y = 560 - imgQuestion.get_height()

def escape(): 
    global imgQuestion, question_lev, question_x, question_y
    typ = 3
    imgQuestion = pygame.image.load("image/escaped.png")
    question_lev = 1
    question_x = 440 - imgQuestion.get_width() / 2
    question_y = 560 - imgQuestion.get_height()

def draw_quiz(bg, fnt): 
    global question_show
    bx = 0
    by = 0
    bg.blit(backgroundImg, [bx, by])
    if question_lev > 0 and question_show % 2 == 0:
        bg.blit(imgQuestion, [question_x, question_y])
    if question_show > 0:
        question_show = question_show - 1
    for i in range(10):
        draw_text(bg, message[i], 600, 100 + i * 50, fnt, WHITE)

def quiz_command1(bg, fnt, key):
    global key_command
    ent = False
    if key[K_1]:  
        key_command = 0
        ent = True
    if key[K_2]: 
        key_command = 1
        ent = True
    if key[K_3]: 
        key_command = 2
        ent = True
    if key[K_4]:  
        key_command = 3
        ent = True
    if key[K_UP] and key_command > 0: 
        key_command -= 1
    if key[K_DOWN] and key_command < 3:  
        key_command += 1
    if key[K_SPACE] or key[K_RETURN]:
        ent = True
    for i in range(4):
        c = WHITE
        if key_command == i: c = BLINK[timer % 6]
        draw_text(bg, COMMANDQ1[i], 20, 360 + i * 60, fnt, c)
    return ent
    
def quiz_command2(bg, fnt, key):  
    global key_command
    ent = False
    if key[K_1]: 
        key_command = 0
        ent = True
    if key[K_2]:  
        key_command = 1
        ent = True
    if key[K_3]:  
        key_command = 2
        ent = True
    if key[K_4]:  
        key_command = 3
        ent = True
    if key[K_UP] and key_command > 0: 
        key_command -= 1
    if key[K_DOWN] and key_command < 3: 
        key_command += 1
    if key[K_SPACE] or key[K_RETURN]:
        ent = True
    for i in range(4):
        c = WHITE
        if key_command == i: c = BLINK[timer % 6]
        draw_text(bg, COMMANDQ2[i], 20, 360 + i * 60, fnt, c)
    return ent

def quiz_command3(bg, fnt, key):  
    global key_command
    ent = False
    if key[K_1]:  
        key_command = 0
        ent = True
    if key[K_2]: 
        key_command = 1
        ent = True
    if key[K_3]: 
        key_command = 2
        ent = True
    if key[K_4]: 
        key_command = 3
        ent = True
    if key[K_UP] and key_command > 0: 
        key_command -= 1
    if key[K_DOWN] and key_command < 3:  
        key_command += 1
    if key[K_SPACE] or key[K_RETURN]:
        ent = True
    for i in range(4):
        c = WHITE
        if key_command == i: c = BLINK[timer % 6]
        draw_text(bg, COMMANDQ3[i], 20, 360 + i * 60, fnt, c)
    return ent

def quiz_command4(bg, fnt, key):  
    global key_command
    ent = False
    if key[K_1]:  
        key_command = 0
        ent = True
    if key[K_2]:  
        key_command = 1
        ent = True
    if key[K_3]: 
        key_command = 2
        ent = True
    if key[K_4]: 
        key_command = 3
        ent = True
    if key[K_UP] and key_command > 0: 
        key_command -= 1
    if key[K_DOWN] and key_command < 3: 
        key_command += 1
    if key[K_SPACE] or key[K_RETURN]:
        ent = True
    for i in range(4):
        c = WHITE
        if key_command == i: c = BLINK[timer % 6]
        draw_text(bg, COMMANDQ4[i], 20, 360 + i * 60, fnt, c)
    return ent

message = [""] * 10
def init_message():
    for i in range(10):
        message[i] = ""

def set_message(msg):
    for i in range(10):
        if message[i] == "":
            message[i] = msg
            return
    for i in range(9):
        message[i] = message[i + 1]
    message[9] = msg

# def play_music():
#     pygame.mixer.init()
#     pygame.mixer.music.load("sound/title_bgm.wav")
#     pygame.mixer.music.play()

# def check_music_playing():
#     while pygame.mixer.music.get_busy():
#         pass
#     play_music()



def main(): 
    global v, index, timer, floor, fl_max, welcome
    global po_a
    global question_lev, question_show
    stack = 0

    pygame.init()
    pygame.display.set_caption("Quiz Room")
    screen = pygame.display.set_mode((880, 720))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 40)
    fontS = pygame.font.Font(None, 30)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_s:
                    v = v + 1
                    if v == 4:
                        v = 1

        timer = timer + 1
        key = pygame.key.get_pressed()

        if index == 0: 
            if timer == 1:
                pygame.mixer.music.load("sound/title_bgm.wav")
                pygame.mixer.music.play(-1)
            screen.fill(BLACK)
            screen.blit(mainImg, [40, 60])
            draw_text(screen, "Press Space Key", 320, 560, font, BLINK[timer % 6])
            if key[K_SPACE] == 1:
                make_room()
                put_quizbox()
                floor = 1
                welcome = 15
                index = 1
        
        elif index == 1:  
            move_player(key)
            draw_room(screen, fontS)
            if stack==40:
                index = 100
                timer = 29
            if welcome > 0:
                welcome = welcome - 1
               
        elif index == 2: 
            draw_room(screen, fontS)
            if 1 <= timer and timer <= 5:
                h = 80 * timer
                pygame.draw.rect(screen, BLACK, [0, 0, 880, h])
                pygame.draw.rect(screen, BLACK, [0, 720 - h, 880, h])
            if timer == 5:
                floor = floor + 1
                if floor > fl_max:
                    fl_max = floor
                welcome = 15
                make_room()
                put_quizbox()
            if 6 <= timer and timer <= 9:
                h = 80 * (10 - timer)
                pygame.draw.rect(screen, BLACK, [0, 0, 880, h])
                pygame.draw.rect(screen, BLACK, [0, 720 - h, 880, h])
            if timer == 10:
                index = 1

        elif index == 9:  
            if timer <= 30:
                PL_TURN = [2, 4, 0, 6]
                po_a = PL_TURN[timer % 4]
                if timer == 30: po_a = 8  
                draw_room(screen, fontS)
            elif timer == 31:
                draw_text(screen, "You died.", 360, 240, font, RED)
                draw_text(screen, "Game over.", 360, 380, font, RED)
            elif timer == 100:
                index = 0
                timer = 0

        elif index == 10: 
            if timer == 1:
                init_quiz1()
                init_message()
            elif timer <= 4:
                bx = (4 - timer) * 220
                by = 0
                screen.blit(backgroundImg, [bx, by])
            elif timer <= 16:
                draw_quiz(screen, fontS)
            else:
                index = 51
                timer = 0

        elif index == 41:  
            if timer == 1:
                init_quiz2()
                init_message()
            elif timer <= 4:
                bx = (4 - timer) * 220
                by = 0
                screen.blit(backgroundImg, [bx, by])
            elif timer <= 16:
                draw_quiz(screen, fontS)
            else:
                index = 52
                timer = 0

        elif index == 42:  
            if timer == 1:
                init_quiz3()
                init_message()
            elif timer <= 4:
                bx = (4 - timer) * 220
                by = 0
                screen.blit(backgroundImg, [bx, by])
            elif timer <= 16:
                draw_quiz(screen, fontS)
            else:
                index = 53
                timer = 0

        elif index == 43:  
            if timer == 1:
                init_quiz4()
                init_message()
            elif timer <= 4:
                bx = (4 - timer) * 220
                by = 0
                screen.blit(backgroundImg, [bx, by])
            elif timer <= 16:
                draw_quiz(screen, fontS)
            else:
                index = 54
                timer = 0

        elif index == 51:  
            draw_quiz(screen, fontS)
            if quiz_command1(screen, font, key) == True:
                if key_command == 0:
                    index = 15
                    timer = 0
                if key_command == 1:
                    stack = stack + 10
                    index = 16
                    timer = 0
                if key_command == 2:
                    index = 15
                    timer = 0
                if key_command == 3:
                    index = 15
                    timer = 0

        elif index == 52: 
            draw_quiz(screen, fontS)
            if quiz_command2(screen, font, key) == True:
                if key_command == 0:
                    index = 15
                    timer = 0
                if key_command == 1:
                    index = 15
                    timer = 0
                if key_command == 2:
                    index = 15
                    timer = 0
                if key_command == 3:
                    stack = stack + 10
                    index = 16
                    timer = 0

        elif index == 53: 
            draw_quiz(screen, fontS)
            if quiz_command3(screen, font, key) == True:
                if key_command == 0:
                    stack = stack + 10
                    index = 16
                    timer = 0
                if key_command == 1:
                    index = 15
                    timer = 0
                if key_command == 2:
                    index = 15
                    timer = 0
                if key_command == 3:
                    index = 15
                    timer = 0

        elif index == 54: 
            draw_quiz(screen, fontS)
            if quiz_command4(screen, font, key) == True:
                if key_command == 0:
                    index = 15
                    timer = 0
                if key_command == 1:
                    stack = stack + 10
                    index = 16
                    timer = 0
                if key_command == 2:
                    index = 15
                    timer = 0
                if key_command == 3:
                    index = 15
                    timer = 0
            
        elif index == 15: 
            draw_quiz(screen, fontS)
            if timer == 1:
                set_message("Wrong Answer.")
            if timer == 11:
                index = 9
                timer = 29

        elif index == 16:  
            draw_quiz(screen, fontS)
            if timer == 1:
                set_message("You are correct!")
            if timer == 28:
                index = 22
 
        elif index == 22:  
            index = 1
 
        elif index == 24:
            draw_text(screen, "You died.", 360, 240, font, RED)
            index = 1
 
        elif index == 100: 
            if timer <= 30:
                PL_TURN = [2, 4, 0, 6]
                po_a = PL_TURN[timer % 4]
                escape()
            elif timer == 31:
                display_image(screen, "image/escaped.png", 60, 60)
            elif timer == 100:
                index = 0
                timer = 0
                running = False

        pygame.display.update()
        clock.tick(4 + 2 * v)
    pygame.quit()

if __name__ == '__main__':
    main()