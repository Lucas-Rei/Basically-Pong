from pygame import *
from random import randint
import pygame

# GameSprite class
class GameSprite(sprite.Sprite): 
    def __init__(self, sprite_image, xpos, ypos, size1, size2, speed):
        super().__init__()
        self.size1 = size1
        self.size2 = size2
        self.image = transform.scale(pygame.image.load(sprite_image), (self.size1, self.size2))
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.speed = speed

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# Player class
class Manual(GameSprite): 
    def update_l(self):
        key_list = key.get_pressed()
        if key_list[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        if key_list[K_s] and self.rect.y < 700 - self.size1:
            self.rect.y += self.speed

    def update_r(self):
        key_list = key.get_pressed()
        if key_list[K_DOWN] and self.rect.y < 700 - self.size1:
            self.rect.y += self.speed
        if key_list[K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed

# Ball class
class Ball(GameSprite):
    def update(self):
        pass

# creation
window = display.set_mode((700, 500))
display.set_caption("Poooooooooooonnnng")

paddle_l = Manual("racket.png", 50, 100, 30, 150, 3)
paddle_r = Manual("racket.png", 620, 100, 30, 150, 3)
ball = Ball("tenis_ball.png", 350, 250, 40, 40, 3)

# text
font.init()
text = font.SysFont("Arial", 30)

# game loop
run = True
finish = False

FPS = 60
clock = time.Clock()

while run:

    # events
    key_list = key.get_pressed()
    for e in event.get():
        if e.type == QUIT:
            menu = False 

    # blit things
    window.fill((199, 220, 255))
    
    paddle_l.reset()
    paddle_r.reset()
    ball.reset()

    if not finish:
        paddle_l.update_l()
        paddle_r.update_r()

    display.update()
    clock.tick(FPS)
