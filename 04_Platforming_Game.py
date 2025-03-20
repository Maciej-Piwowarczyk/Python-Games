######################## 
# IMPORTS #

import pygame, sys
from pygame.locals import *
import random, time

######################## 
# INITIALIZATION #
pygame.init()

######################## 
# CUSTOM FUNCTIONS #
def collidePointAny(group,pointx,pointy):
    for obj in group:
        if obj.rect.collidepoint(pointx,pointy):
            return True
    return False

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

######################## 
# FPS #
FPS = 60
FramePerSec = pygame.time.Clock()

######################## 
# WINDOW #
SCREEN_HEIGHT = 800
SCREEN_WIDTH = 800

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
DISPLAYSURF.fill(BLACK)
pygame.display.set_caption("Platform THIS")

######################## 
# CLASSES #
class Player(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height,color,value):
        super().__init__() 
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.value = value
    
    def move(self):
        global PLAYER_MOMENTUM
        global ON_GROUND
        
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_UP]:
            if ON_GROUND:
                PLAYER_MOMENTUM -= JUMP_HEIGHT
                ON_GROUND = False
        self.rect.move_ip(0,PLAYER_MOMENTUM)
        
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-SPEED,0)
   
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(SPEED,0)     


class Rect(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height,color,value):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.value = value

class Centered_Text:
    'Centered Text Class'
    # Constructor
    def __init__(self, text, x,y,w,h, color):
        self.rect = pygame.Rect(x, y, w, h)
        self.txt = font_small.render(text, True, color)
    # Draw Method
    def draw(self, screen):
        coords = self.txt.get_rect()
        coords.center = self.rect.center
        screen.blit(self.txt, coords)

######################## 
# PLAYER INFO #
PLAYER_POS = [0,0,0,0]
PLAYER_MOMENTUM = 0
PLAYER_WIDTH = 15
PLAYER_HEIGHT = 15
SPEED = 3
JUMP_HEIGHT = 10
ON_GROUND = True

def movePlayer():
    # left, top, bottom, right
    global PLAYER_POS
    PLAYER_POS = [P1.rect.x,P1.rect.y,P1.rect.x+PLAYER_WIDTH,P1.rect.y+PLAYER_HEIGHT]
    P1.move()

    global PLAYER_MOMENTUM
    global ON_GROUND
    
    # checks if any platform is intersecting the player and moves the player to an appropriate place if they are 
    for platform in platform_sprites:
        if pygame.sprite.collide_rect(P1, platform): 
            ALIGNED = False
            if PLAYER_POS[3] <= platform.rect.y:
                PLAYER_MOMENTUM = 0
                ON_GROUND = True
                while not ALIGNED:
                    P1.rect.y += -1
                    if not pygame.sprite.collide_rect(P1, platform):
                        ALIGNED = True
            elif PLAYER_POS[1] >= platform.rect.y + platform.rect.height:
                PLAYER_MOMENTUM = 0
                while not ALIGNED:
                    P1.rect.y += 1
                    if not pygame.sprite.collide_rect(P1, platform):
                        ALIGNED = True
            if PLAYER_POS[2] <= platform.rect.x and not ALIGNED: 
                while not ALIGNED:
                    P1.rect.x += -1
                    if not pygame.sprite.collide_rect(P1, platform):
                        ALIGNED = True
            elif not ALIGNED:
                while not ALIGNED:
                    P1.rect.x += 1
                    if not pygame.sprite.collide_rect(P1, platform):
                        ALIGNED = True

    # checks that either the bottom right or bottom left pixels of the player are above a platform
    if not collidePointAny(platform_sprites,P1.rect.x, P1.rect.y+PLAYER_HEIGHT+1) and not collidePointAny(platform_sprites,P1.rect.x+PLAYER_WIDTH, P1.rect.y+PLAYER_HEIGHT+1):
        ON_GROUND = False
    
    if ON_GROUND:
        P1.image.fill(BLUE)
    else:
        P1.image.fill(RED)

def moveMouse():
    # global MOUSE_POS
    global all_sprites
    global LEVEL_CHANGE
    global LEVEL
        
    MOUSE_POS = pygame.mouse.get_pos()
    MOUSE_PRESSED = pygame.mouse.get_pressed(num_buttons=3)

    for option in all_sprites:
        if option.rect.collidepoint(MOUSE_POS) and MOUSE_PRESSED[0]:
            LEVEL_CHANGE = True
            LEVEL = option.value

######################## 
# USER EVENTS #
GRAVITY = pygame.USEREVENT + 1
pygame.time.set_timer(GRAVITY, 1)

def levelEvents():
    # Cycles through all events occuring
    global PLAYER_MOMENTUM
    for event in pygame.event.get():
        if event.type == GRAVITY:
            if not ON_GROUND:
                PLAYER_MOMENTUM += .04
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

def mouseEvents():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

######################## 
# INITIALIZE FOR ALL LEVELS #

text_sprites = []
platform_sprites = pygame.sprite.Group() 
all_sprites = pygame.sprite.Group()
reset_sprites = pygame.sprite.Group()

wallLeft = Rect(0,0,10,SCREEN_HEIGHT,(0,0,0),1)
wallRigh = Rect(SCREEN_WIDTH-10,0,10,SCREEN_HEIGHT,(0,0,0),1)
platFloo = Rect(0,SCREEN_HEIGHT-10,SCREEN_WIDTH,10,(0,0,0),1)
platCeil = Rect(0,0,SCREEN_WIDTH,10,(0,0,0),1)

def initLevel():
    global text_sprites
    text_sprites = []
    platform_sprites.empty()
    all_sprites.empty()
    reset_sprites.empty()
    
    platform_sprites.add(wallLeft)
    platform_sprites.add(wallRigh)
    platform_sprites.add(platFloo)
    platform_sprites.add(platCeil)

    all_sprites.add(wallLeft)
    all_sprites.add(wallRigh)
    all_sprites.add(platFloo)
    all_sprites.add(platCeil)

######################## 
# lEVELS #

# Start at the menu
LEVEL = 0

def levels(levelNumber):
    global PLAYER_MOMENTUM
    PLAYER_MOMENTUM = 0

    global text_sprites
    global all_sprites
    global platform_sprites
    global LEVEL
    initLevel()

    pygame.mouse.set_visible(False)

    if levelNumber == 0:
        pygame.mouse.set_visible(True)

        text_sprites+=[("Level Select",0,0,SCREEN_WIDTH,50,WHITE)]
      
        topLeft = [0.1*SCREEN_WIDTH,0.3*SCREEN_HEIGHT]
        rows = 2
        columns = 5
        box_height = 0.6*SCREEN_HEIGHT//rows 
        box_width = 0.6*SCREEN_HEIGHT//columns
        for i in range(1,6):
            all_sprites.add(Rect(topLeft[0]+10,topLeft[1]+10,box_width-10,box_height-10,WHITE,i))
            text_sprites += [(str(i),topLeft[0]+10,topLeft[1]+10,box_width-10,box_height-10, BLACK)]
            topLeft[0] += box_width
            
        return 0, [0,0,0,0], all_sprites, platform_sprites, reset_sprites
        
    elif levelNumber == 1:
        P1 = Player(100,100,PLAYER_WIDTH,PLAYER_HEIGHT,(255,0,0),1)
        PLAYER_POS = [100,100,100+PLAYER_WIDTH,100+PLAYER_HEIGHT]
        all_sprites.add(P1)
    
        plat01 = Rect(30,700,100,50,(255,0,0),1)
        platform_sprites.add(plat01)
        all_sprites.add(plat01)

        plaD01 = Rect(400,700,100,50,(0,255,0),1)
        reset_sprites.add(plaD01)
        all_sprites.add(plaD01)
    
        return P1, PLAYER_POS, all_sprites, platform_sprites, reset_sprites

    elif levelNumber == 2:
        P1 = Player(100,100,PLAYER_WIDTH,PLAYER_HEIGHT,(255,0,0),1)
        PLAYER_POS = [100,100,100+PLAYER_WIDTH,100+PLAYER_HEIGHT]
        all_sprites.add(P1)
    
        plat01 = Rect(120,700,100,50,(255,0,0),1)
        platform_sprites.add(plat01)
        all_sprites.add(plat01)
    
        return P1, PLAYER_POS, all_sprites, platform_sprites, reset_sprites

######################## 
# RUNNING THE GAME #

levels(0)
LEVEL_CHANGE = False
while True:     
    if LEVEL_CHANGE:
        P1, PLAYER_POS, all_sprites, platform_sprites, reset_sprites = levels(LEVEL)
        LEVEL_CHANGE = False
    
    # Resets the screen
    DISPLAYSURF.fill(BLACK)

    # Moves and redraws sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)

    for text in text_sprites:
        temp = Centered_Text(text[0],text[1],text[2],text[3],text[4],text[5])
        temp.draw(DISPLAYSURF)

    # For when in menu
    if LEVEL == 0:
        mouseEvents()
        moveMouse()
    # For when in level
    else:
        levelEvents()
        movePlayer()

    for resetObj in reset_sprites:
        if pygame.sprite.collide_rect(P1, resetObj):
            LEVEL_CHANGE = True

    if pygame.key.get_pressed()[K_ESCAPE]:     
        LEVEL_CHANGE, LEVEL = True, 0
        
    pygame.display.update()
    FramePerSec.tick(FPS)
    
