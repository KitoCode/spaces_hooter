import pygame
import random
import math
from pygame import mixer
pygame.init()
W = 1024
H = 600
x = -200
y = -200
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("UFO destroyer")
# музыка
pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play(-1,0.0)

#иконки для окна
icon = pygame.image.load('alien.png')
pygame.display.set_icon(icon)
background = pygame.image.load('bg.jpg')

# создание игрока
playerImg = pygame.image.load('spaceship.png')
playerX = 492
playerY = 490
player_speed = 3

#очки
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 42)

#расположение количества очков
textX = 19
textY = 10

#функция отображения очков
def show_score(x,y):
    score = font.render("Score :" + str(score_value), True, (255,255,255))
    screen.blit(score, (x, y))

over_font = pygame.font.Font('freesansbold.ttf', 65)

#функция Конец Игры
def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255,255,255))
    screen.blit(over_text, (400, 250))

# отображение игрока
def player(x,y):
    screen.blit(playerImg, (x, y))

# создание врагов
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemy = 6

for i in range(num_of_enemy):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(3, 955))
    enemyY.append(random.randint(10, 300))
    enemyX_change.append(0.9) # скорость врага
    enemyY_change.append(50) # перемещение врага по У

# отображение врагов
def enemy(x,y,i):
    screen.blit(enemyImg[i], (x, y))

# ведение боя кораблем
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 490 # спаун левого снаряда
bulletY_change = 7 # скорость по У для левого сняряда
bullet_state = "ready"

# отображение снарядов
def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 36, y + 18))

# попадание
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2))+(math.pow(enemyY - bulletY,2)))
    if distance < 30:
        return True
    else:
        return False

# цикл запуска и выхода
running = True
while running:

    screen.fill((0,0,0))

    # задний фон
    screen.blit(background, (x,y))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # движение и границы игрока
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and playerX > 3:
        playerX -= player_speed
        x += 1.2
        #scrollbackground(5, 0)
    if keys[pygame.K_RIGHT] and playerX < 1024 - 104 - 3:
        playerX += player_speed
        x -= 1.2
        #scrollbackground(-5, 0)

    # вызов функции стрельбы
    if keys[pygame.K_SPACE]:
        if bullet_state is "ready":
            bullet_sound = mixer.Sound('laser.wav')
            bullet_sound.play()
            bulletX = playerX
            fire_bullet(bulletX, bulletY)

    #границы и движение врагов
    for i in range(num_of_enemy):

        # конец игры
        if enemyY[i] > 400:
            for j in range(num_of_enemy):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.9
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 955:
            enemyX_change[i] = -0.9
            enemyY[i] += enemyY_change[i]

        #попадание
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('boom.wav')
            explosion_sound.play()
            bulletY = 490 + 18
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(3, 955)
            enemyY[i] = random.randint(10, 300)

        enemy(enemyX[i], enemyY[i], i)

    # несколько снярядов сразу
    if bulletY <= 0:
        bulletY = 490
        bullet_state = "ready"

    # пули не пропадают при вызове
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    #screen.blit(background,(x, 0))
    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
