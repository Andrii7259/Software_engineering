import pygame
import pgzrun
from pgzero.keyboard import keyboard
from pgzero.builtins import Actor
pygame.init()

TITLE = "Гра \"Скок\""
WIDTH = 800
HEIGHT = 500

paddle = Actor("paddleblue.png")
paddle.x = WIDTH / 2
paddle.y = 480

ball = Actor("ballred2.png")
ball.x = WIDTH / 2
ball.y = HEIGHT / 2



ball_speed_x = -3
ball_speed_y = -3
# click_rect = Rect()
bar_list = []


def draw():
    screen.fill((0,128,0))

    for bar in bar_list:
        bar.draw()
        pass
    paddle.draw()
    ball.draw()



def place_bars(x, y, image):
    bar_x = x
    bar_y = y
    for i in range(8):
        bar = Actor(image)
        bar.x = bar_x
        bar.y = bar_y
        bar_x += 70
        bar_list.append(bar)

def update():
    global ball_speed_y
    for bar in bar_list:
        if ball.colliderect(bar):
            bar_list.remove(bar)
            ball_speed_y *= -1
    if ball.colliderect(paddle):
        ball_speed_y *= -1
    update_paddle()
    update_ball()






def update_paddle():
    if keyboard.left:
        paddle.x -= 10
    if keyboard.right:
        paddle.x += 10



def update_ball():
    global ball_speed_x, ball_speed_y, screen
    ball.x += ball_speed_x
    ball.y += ball_speed_y
    print(ball.y)
    if ball.x >= WIDTH-2 or ball.x <= 0:
        screen.fill((128, 128, 128))# ліва, права
        ball_speed_x *= -1  # відбивається
    elif ball.y <= 0:  # верхня
        ball_speed_y *= -1
        screen.fill((128, 128, 128))
    elif ball.y >= HEIGHT:
        screen.fill((128, 128,128))


colored_box_list = ["brick.png", "brick2.png", "brick3.png"]
x = 120
y = 100
for colored_box in colored_box_list:
    place_bars(x, y, colored_box)
    y += 50


pgzrun.go()