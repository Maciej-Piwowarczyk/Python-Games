# The tutorial I was following 
# https://coderslegacy.com/python/python-pygame-tutorial/

######################## 
# IMPORTS #

import pygame, sys
from pygame.locals import *
import random, time

######################## 
# INITIALIZATION #
pygame.init()

######################## 
# COLORS #
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

######################## 
# FONTS #
font = pygame.font.SysFont("Comicsansms", 60)
font_small = pygame.font.SysFont("Verdana", 20)

# FPS
FPS = 30
FramePerSec = pygame.time.Clock()

# Screen information
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 400
SPEED = 5
SCORE = 0

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Dodge THIS")

######################## 
# OBJECTS #
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Images/EnemyIcon.png")
        self.rect = self.image.get_rect()
        random_height = random.randint(-500,-100) 
        self.rect.center=(random.randint(40,SCREEN_WIDTH-40),random_height)
          
    def move(self):
        global SCORE
        self.rect.move_ip(0,SPEED)
        if (self.rect.top > SCREEN_HEIGHT):
            SCORE += 1
            random_height = random.randint(-500,-100)
            self.rect.center = (random.randint(30, SCREEN_WIDTH-30), random_height)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Images/PlayerIcon.png")
        self.rect = self.image.get_rect()
        self.rect.center = (int(SCREEN_WIDTH/2), SCREEN_HEIGHT)
 
    def move(self):
        pressed_keys = pygame.key.get_pressed()
       #if pressed_keys[K_UP]:
            #self.rect.move_ip(0, -5)
       #if pressed_keys[K_DOWN]:
            #self.rect.move_ip(0,5)
         
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(5, 0)

class Centered_Text:
    'Centered Text Class'
    # Constructor
    def __init__(self, text, x,y,w,h, color):
        self.rect = pygame.Rect(x, y, w, h)
        self.txt = font.render(text, True, color)
    # Draw Method
    def draw(self, screen):
        coords = self.txt.get_rect()
        coords.center = self.rect.center
        screen.blit(self.txt, coords)

######################## 
# SPRITES AND GROUPS #

game_over = Centered_Text("GAME OVER",0,0,SCREEN_WIDTH,SCREEN_HEIGHT, (0,0,0))

P1 = Player()
E1 = Enemy()
E2 = Enemy()

enemies = pygame.sprite.Group()
enemies.add(E1)
enemies.add(E2)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(E2)

######################## 
# USER EVENTS #

# Defines a user event that is called once every 1000 milliseconds (1 sec)
# This event speeds up the rate at which objects fall
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

######################## 
# RUNNING THE GAME #

while True:     
    # Cycles through all events occuring
    for event in pygame.event.get():
        if event.type == INC_SPEED:
              SPEED += 0.5
            
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Resets the screen
    DISPLAYSURF.fill(WHITE)
    scores = font_small.render(str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10,10))

    # Moves and redraws sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    if pygame.sprite.spritecollideany(P1, enemies):        
        DISPLAYSURF.fill(BLUE)
        game_over.draw(DISPLAYSURF)

        final_score = font_small.render("Final Score: "+str(SCORE),True,BLACK) 
        DISPLAYSURF.blit(final_score,(int(SCREEN_WIDTH/2)-60, SCREEN_HEIGHT-30))
        
        pygame.display.update()
        for entity in all_sprites:
              entity.kill() 
        time.sleep(2)
        pygame.quit()
        sys.exit()
         
    pygame.display.update()
    FramePerSec.tick(FPS)
