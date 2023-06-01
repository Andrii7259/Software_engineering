import pygame
import pygame.mixer
import pgzrun
from pgzero.keyboard import keyboard
from pgzero.builtins import Actor
from random import *


def start():
    pygame.init()


pygame.mixer.init()
TITLE = "Гра \"Скок\""
WIDTH = 800
HEIGHT = 500
'''Ініціалізація екрану'''
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame")
surface = pygame.Surface((20, 200))
pygame.transform.scale(surface, ((100, 100)))
'''Ініціалізуємо ракетку'''
paddle = Actor("paddleblue.png")
'''Ініціалізуємо м'яч'''
ball = Actor("ballred2.png")
'''Характеристики ракетки '''
paddle.x = 100
paddle.y = 480
'''Характеристики м'яча '''
ball.x = 100
ball.y = HEIGHT / 2
ball_speed_x = -3
ball_speed_y = -3
bar_list = []
broke_bar_list = []
lives_list = []
lives = 3
game_over = True
scores = 0
list_of_scores = []
state = "play"
'''Місце зберігання різновидів цеглинок '''
colored_box_list = ["brick.png", "brick2.png", "brick3.png"]
colored_box_list2 = ["brick4.png"]
coin_speed_y = 2
coin_list = []
level = 1
num = 0
'''Ініціалізація звуків'''
sound_ball_rocket = pygame.mixer.Sound("sounds/rocket_ball_sound.wav")
sound_coin_rocket = pygame.mixer.Sound("sounds/money_sound.mp3")
sound_brick_crack = pygame.mixer.Sound("sounds/crack_sound.mp3")
sound_brick_full_crack = pygame.mixer.Sound("sounds/full_crack_sound.mp3")
bg_image = pygame.image.load("images/bg.jpg")
sound_ball_wall = pygame.mixer.Sound("sounds/ball_wall_sound.wav")
restart_image = pygame.image.load("images/restart_image.png")
start_image = pygame.image.load("images/start_image.png")
continue_image = pygame.image.load("images/continue_image.png")


def draw():
    '''Метод відображення ігрових елементів'''
    global scores, state, list_of_scores, coin_list, ball_speed_x, ball_speed_y, coin_speed_y, restart_image, lives

    screen.fill((113, 128, 87))
    w = 300
    h = 75
    new_start_image = pygame.transform.scale(start_image, (w, h))
    window.blit(new_start_image, (250, 100))  # point

    '''Алгоритм початку гри'''
    if not game_over:
        screen.fill((0, 128, 0))
        window.blit(bg_image, (0, 0))

        for bar in bar_list:
            bar.draw()

        paddle.draw()
        ball.draw()
        for coin in coin_list:
            coin.draw()

        for life in lives_list:
            life.draw()
        screen.draw.text("Lives: " + str(lives), topleft=(10, 10))
        screen.draw.text("scores: " + str(scores), topright=(790, 10))
        # screen.draw.text("scores_list: " + str(list_of_scores), topright=(790, 30))


    elif state == "win":
        '''Випадок збиття всіх цеглин (перемога)'''
        ball_speed_x = 0  # заморозив м'яч на місці
        ball_speed_y = 0
        coin_speed_y = 0
        screen.fill("purple")
        screen.draw.text("ВИГРАШ", centerx=WIDTH / 2, centery=HEIGHT / 2)
        screen.draw.text("Ваші бали: {}".format(scores), centerx=WIDTH / 2, centery=HEIGHT / 2 + 20)
        screen.draw.text("Найкращий результат: {}".format(max(list_of_scores)), centerx=WIDTH / 2,
                         centery=HEIGHT / 2 + 40)

        w = 300
        h = 75
        new_continue_image = pygame.transform.scale(continue_image, (w, h))
        window.blit(new_continue_image, (250, 100))  # point

    elif state == "loose":
        '''Випадок нульової кількості життів (програш)'''
        ball_speed_x = 0  # заморозив м'яч на місці
        ball_speed_y = 0
        coin_speed_y = 0

        screen.fill("lightgreen")
        w = 300
        h = 75
        new_restart_image = pygame.transform.scale(restart_image, (w, h))
        window.blit(new_restart_image, (250, 100))  # point
        screen.draw.text("ПРОГРАШ", centerx=WIDTH / 2, centery=HEIGHT / 2)
        screen.draw.text("Ваші бали: {}".format(scores), centerx=WIDTH / 2, centery=HEIGHT / 2 + 20)
        screen.draw.text("Найкращий результат: {}".format(max(list_of_scores)), centerx=WIDTH / 2,
                         centery=HEIGHT / 2 + 40)



class Brick(Actor):
    def __init__(self, image, hits_required):
        super().__init__(image)
        self.hits_required = hits_required
        self.hits = 0


def place_bars(x, y, image, hits_reqired):
    '''Ініціалізація цеглинок'''
    global colored_box_list, num
    bar_x = x
    bar_y = y
    for i in range(num):
        bar = Brick(image, hits_reqired)
        bar.x = bar_x
        bar.y = bar_y
        bar_x += 100
        bar_list.append(bar)


def init_bars(x, y):
    global colored_box_list
    for colored_box in colored_box_list:
        place_bars(x, y, colored_box, "hits_required")
        y += 50


init_bars(120, 70)


def place_lives(x_l, y_l, image_l):
    global lives
    '''Ініціалізація життів'''
    life_x = x_l
    life_y = y_l
    for i in range(lives):
        life = Actor(image_l)
        life.x = life_x
        life.y = life_y
        life_x += 40
        lives_list.append(life)


place_lives(30, 30, "heart.png")


def update():
    global coin_speed_y, coin_list, ball_speed_y, ball_speed_x, scores, bar_list, state, game_over, list_of_scores, colored_box_list2, broke_bar_list
    '''Оновлення стану гри'''
    # shuffle = [3, 2, 1]
    # random_x = choice(shuffle)
    # random_y = choice(shuffle)

    for bar in bar_list:
        if ball.colliderect(bar):

            bar.hits += 1
            '''Алгоритм зміни графіки цеглинки після першого збиття'''
            if bar.hits == 1:
                sound_brick_crack.play()
                # ball_speed_y *= -1
                if bar.image == "brick.png":
                    bar.image = "brick4.png"
                elif bar.image == "brick2.png":
                    bar.image = "brick5.png"
                elif bar.image == "brick3.png":
                    bar.image = "brick6.png"

            elif bar.hits == 2:
                '''Алгоритм видалення зруйнованої цеглинки'''
                bar_list.remove(bar)
                sound_brick_full_crack.play()
                coin = Actor("m1f.png")
                coin.x = bar.x
                coin.y = bar.y
                coin_list.append(coin)

            scores += 10
            if len(bar_list) == 0:
                '''Нарахування балів за пройдений рівень'''
                scores += 1000
                list_of_scores.append(scores)
                state = "win"
                game_over = True
                ball_speed_x = 0
                ball_speed_y = 0
                coin_speed_y = 0
            ball_speed_y *= -1

            rand = randint(0, 1)
            if rand:
                ball_speed_x *= -1

    if ball.colliderect(paddle) and ball_speed_y > 0:

        ball_speed_y *= -1
        sound_ball_rocket.play()
        rand = randint(0, 1)
        if rand:
            ball_speed_x *= -1

    update_paddle()
    update_ball()
    update_coin()


def update_paddle():
    '''Взаємодія користувача з ракеткою'''
    if keyboard.left and paddle.x > 70:
        paddle.x -= 10
    if keyboard.right and paddle.x < WIDTH - 70:
        paddle.x += 10
    if keyboard.up:
        paddle.y -= 10
    if keyboard.down:
        paddle.y += 10


def update_coin():
    global coin_speed_y, coin_list, scores
    '''Алгоритм створення монетки, що випадає з цеглинки'''
    for coin in coin_list:
        coin_speed_y = 2
        coin.y += coin_speed_y
        if coin.colliderect(paddle) and not game_over:
            coin_list.remove(coin)
            scores += 100
            sound_coin_rocket.play()
        elif coin.y > HEIGHT:
            coin_list.remove(coin)


def update_ball():
    '''Оновлення м'яча'''
    global ball_speed_x, ball_speed_y, screen, game_over, lives, state, scores, list_of_scores, coin_speed_y
    if not game_over:
        ball.x += ball_speed_x
        ball.y += ball_speed_y
        if ball.x >= WIDTH - 2 or ball.x <= 0:
            ball_speed_x *= -1
            sound_ball_wall.play()
        elif ball.y <= 0:
            ball_speed_y *= -1
            sound_ball_wall.play()
        elif ball.y >= HEIGHT:
            ball_speed_y *= -1
            sound_ball_wall.play()

            if len(lives_list) > 0:
                lives_list.pop(int(len(lives_list) - 1))  # Видаляємо останнє серце зі списку
                lives -= 1

    if lives == 0:
        list_of_scores.append(scores)
        if state == "play":
            state = "loose"
        game_over = True  # Кінець гри
        ball_speed_x = 0  # заморозив м'яч на місці
        ball_speed_y = 0
        coin_speed_y = 0


def restart_game():
    '''Перезапуск гри'''
    global game_over, lives, ball_speed_x, ball_speed_y, scores, lives_box, state, lives_list, scores, coin_list
    coin_list = []
    game_over = False
    state = 'play'
    lives = 3
    paddle.x = WIDTH / 2
    paddle.y = 480
    init_bars(120, 70)
    ball_speed_x = -3
    ball_speed_y = -3
    ball.x = WIDTH / 2
    ball.y = HEIGHT / 2

    if ball.y >= HEIGHT:
        ball_speed_y *= -1
        if len(lives_list) > 0:
            lives_list.pop(int(len(lives_list) - 1))  # Видаляємо останнє серце зі списку
            lives -= 1


def on_mouse_down(pos):
    '''Взаємодія користувача з клавішами меню'''
    global lives, state, scores, level, num
    x, y = pos
    if 1 < x < 100 and 1 < y < 100:
        start()
    elif 250 <= x <= 550 and 75 <= y <= 175:
        if state == 'loose':
            scores = 0
            num = 1
        level += 1
        num += 1
        restart_game()


def start():
    global game_over
    game_over = False


pgzrun.go()
