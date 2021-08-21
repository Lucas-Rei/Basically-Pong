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
            
        if key_list[K_s] and self.rect.y < 500 - self.size2:
            self.rect.y += self.speed       

    def update_r(self):
        key_list = key.get_pressed()
        if key_list[K_DOWN] and self.rect.y < 500 - self.size2:
            self.rect.y += self.speed          

        if key_list[K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed

# Ball class
# perhaps create seperate barriers on the top and bottom of a paddle and configure the ball to bounce off in opposite direction when colliding with top and bottom
class Ball(GameSprite):
    def update(self):
        if sprite.collide_rect(paddle_left, self) or sprite.collide_rect(paddle_right, self) and not sprite.collide_rect(block_right, self) and not sprite.collide_rect(block_left, self):
            x_change = False
            y_change = False

            if self.speed[0] < 0:
                x_change = True
            
            if self.speed[1] < 0:
                y_change = True
            
            self.speed = [randint(5, 6), randint(5, 6)]

            if x_change:
                self.speed[0] *= -1
            if y_change:
                self.speed[1] *= -1 

            self.speed[0] *= -1
        
        if self.rect.y >= 500 - self.size1 or self.rect.y <= 0 and not sprite.collide_rect(block_right, self) and not sprite.collide_rect(block_left, self):
            x_change = False
            y_change = False

            if self.speed[0] < 0:
                x_change = True
            
            if self.speed[1] < 0:
                y_change = True
            
            self.speed = [randint(5, 6), randint(5, 6)]

            if x_change:
                self.speed[0] *= -1
            if y_change:
                self.speed[1] *= -1 

            self.speed[1] *= -1
        
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]

# creation
window = display.set_mode((700, 500))
display.set_caption("Poooooooooooonnnng")

paddle_left = Manual("racket.png", 50, 250, 30, 150, 3)
paddle_right = Manual("racket.png", 620, 250, 30, 150, 3)
ball = Ball("tenis_ball.png", 350, 250, 40, 40, [3, 5])

block_left = GameSprite("gap.png", 35, 0, 30, 600, 3)
block_right = GameSprite("gap.png", 635, 0, 30, 600, 3)


# game loop
run = True
finish = False

FPS = 60
clock = time.Clock()

switch = 1

start_timer = 40
restart_timer = 180

player1_score = 0
player2_score = 0

# text
font.init()
text = font.SysFont(None, 50)
score_text = font.SysFont(None, 75)

lose1 = text.render("Player 1 loses", True, (230, 10, 10))
lose2 = text.render("Player 2 loses", True, (230, 10, 10))

while run:

    # events
    key_list = key.get_pressed()
    for e in event.get():
        if e.type == QUIT:
            menu = False 

    # blit things
    window.fill((199, 220, 255))

    paddle_left.reset()
    paddle_right.reset()
    ball.reset()

    block_right.reset()
    block_left.reset()


    score1 = score_text.render(str(player1_score), True, (0, 0, 0))
    score2 = score_text.render(str(player2_score), True, (0, 0, 0))
    window.blit(score1, (300, 30))
    window.blit(score2, (400, 30))

    # update
    if not finish and start_timer <= 0:
        paddle_left.update_l()
        paddle_right.update_r()

        ball.update()

    if finish:
        restart_timer -= 1

        if restart_timer <= 0:
            ball.rect.x = 350
            ball.rect.y = 250
            ball.speed = [3, 5]

            paddle_left.rect.y = 250
            paddle_right.rect.y = 250

            start_timer = 40
            restart_timer = 180

            finish = False


    # losing conditions
    if ball.rect.x <= 0:
        if not finish:
            player2_score += 1
        finish = True
        window.blit(lose1, (250, 200))
        

    if ball.rect.x >= 700 - ball.size1:
        if not finish:
            player1_score += 1
        finish = True
        window.blit(lose2, (250, 200))
        

        
    start_timer -= 1
    display.update()
    clock.tick(FPS)
