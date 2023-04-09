import pygame
import keyboard
import random
import numpy as np

color = "black"  # колір рішітки
chance = 5  # кількість життів

pygame.init()  # запускаємо цикл гри
pygame.mixer.init()

# Load sound effects
click_sound = pygame.mixer.Sound("music/click_sound.wav")
error_sound = pygame.mixer.Sound("music/error_sound.wav")
background_music = pygame.mixer.Sound("music/background_music.mp3")

# Play background music
background_music.play(-1)
# функція для виводу тексту на екран
def text(text, x, y,size):
    font = pygame.font.SysFont("Source Code Pro", 15)
    img = font.render(text, True, (81, 90, 216))
    screen.blit(img, (x, y))
# функція для переводу масиву значень клітинок у рядку або ствопчику у масив з декількома блоками зі значенням
def array_comb(array):
    arrayx = []
    result = []
    for i in range(len(array)):
        if array[i] == 0:
            arrayx.append(i + 1)
    if arrayx[len(arrayx) - 1] != 10:
        arrayx.append(11)
    if arrayx[0] != 1:
        arrayx = [0] + arrayx
    for f in range(len(arrayx) - 1):
        if not arrayx[f + 1] - arrayx[f] - 1 == 0:
            result.append(arrayx[f + 1] - arrayx[f] - 1)
    return result
def draw_grid(scr):
    for i in range(1, 12):
        pygame.draw.line(scr, "grey", (60, 60 * i), (660, 60 * i), 1)
        if i % 5 == 1:
            pygame.draw.line(scr, color, (60, 60 * i), (660, 60 * i), 3)
    for i in range(1, 12):
        pygame.draw.line(scr, "grey", (60 * i, 60), (60 * i, 660), 1)
        if i % 5 == 1:
            pygame.draw.line(scr, color, (60 * i, 60), (60 * i, 660), 3)
def graw_k(scr, y, x, z,color=(52, 72, 97)):
    if 11 > x and x > 0 and 11 > y and y > 0:
        if z == 1:
            pygame.draw.polygon(scr,color,[(60 * x + 60, 60 * y),(60 * x, 60 * y),(60 * x, 60 * y + 60),(60 * x + 60, 60 * y + 60),],)
        elif z == 0:
            pygame.draw.line(scr, (52, 72, 97), (60 * x, 60 * y), (60 * x + 60, 60 * y + 60), 3)
            pygame.draw.line(scr, (52, 72, 97), (60 * x + 60, 60 * y), (60 * x, 60 * y + 60), 3)
def text_on_screen():
    for i in range(1, 11):
        text1 = str(array_comb(field[i - 1]))[1:-1]
        text(text1, 2, 60 * (i) + 14, 16)
    for i in range(1, 11):
        text1 = str(array_comb(dim_2[i - 1]))[1:-1]
        text(text1, 60 * (i) + 14, 25, 16)
def check():
    for i in range(10):
        if ''.join([str(x) for x in real[i]]).replace("x",'0') == ''.join([str(x) for x in field[i]]):
            for g in range(10):
                if real[i][g] == 'x':
                    graw_k(screen, i + 1, g + 1, 0)
        if ''.join([str(x) for x in dim_real_2[i]]).replace("x",'0') == ''.join([str(x) for x in dim_2[i]]):
            for f in range(10):
                if dim_real_2[i][f] == 'x':
                    graw_k(screen, f + 1, i + 1, 0)
                    
                    
def diment(array_2, array_1):
    for f in range(10):
        for y in range(10):
            array_1[f][y] = array_2[y][f]
def randomize(n=15):
    x,y=[random.randint(1, 10)for i in range(n)],[random.randint(1, 10)for i in range(n)]
    for d,g in zip(x,y):
        graw_k(screen, d, g, field[d - 1][g - 1])
        real[d - 1][g - 1] = field[d - 1][g - 1]
def erase(scr, y, x):
    graw_k(scr,y,x,1,'white')
def caption():
    pygame.display.set_caption( f"{str(figure[score_n % 2])} Nonogram {str(work[score_g % 2])}, you have {'❤'*chance} lives")
SCREEN_SIZE = (720, 720)
window = pygame.display.set_mode(SCREEN_SIZE)
screen = pygame.Surface(SCREEN_SIZE)
screen.fill((255, 255, 255))

field = [[random.randint(0, 1) for r in range(10)] for i in range(10)]
field=np.random.randint(2,size=100).reshape(10,10)
dim_2 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0] for i in range(10)]
real, dim_real_2 = [['x','x','x','x','x','x','x','x','x','x'] for i in range(10)],[['x','x','x','x','x','x','x','x','x','x'] for i in range(10)]
randomize()
diment(field,dim_2)
text_on_screen()
mainloop = True
score_n, score_g, figure, work = 1, 1, ["X", "⬛"], ["erase", "draw"]
caption()



while mainloop and chance >= 1:
    if real == field:
        print("you won")
        mainloop = False
    diment(real, dim_real_2)
    check()
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainloop = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if 0 < pos[1] // 60 < 11 and 0 < pos[0] // 60 < 11:
                try:
                    click_sound.play()
                    if work[score_g % 2] == "erase":
                        erase(screen, pos[1] // 60, pos[0] // 60)
                        real[pos[1] // 60 - 1][pos[0] // 60 - 1] = 'x'
                    elif real[pos[1] // 60 - 1][pos[0] // 60 - 1] == 'x':
                        real[pos[1] // 60 - 1][pos[0] // 60 - 1] = field[pos[1] // 60 - 1][pos[0] // 60 - 1]
                        if field[pos[1] // 60 - 1][pos[0] // 60 - 1] != score_n % 2:
                            chance -= 1
                            error_sound.play()
                            graw_k(screen, pos[1] // 60, pos[0] // 60, (score_n + 1) % 2)
                        else:
                            graw_k(screen, pos[1] // 60, pos[0] // 60, score_n % 2)
                except IndexError:
                    pass
        if keyboard.is_pressed("Tab"):
            score_n += 1
        if keyboard.is_pressed("F2"):
            score_g += 1
    caption()
    draw_grid(screen)
    window.blit(screen, (0, 0))
    pygame.display.update()
