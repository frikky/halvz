import sys
import pygame
import random
import time
import os
from pygame.locals import *
from pygame import mixer

import start
 
pygame.init()

mixer.init() 
#mixer.music.load(r'explode.mp3')
#mixer.music.set_volume(0.2)
#mixer.music.play()

crash_sound = pygame.mixer.Sound("explode.ogg")
pygame.font.init() # you have to call this at the start,

my_font = pygame.font.SysFont('Comic Sans MS', 50)

vec = pygame.math.Vector2  # 2 for two dimensional
 
HEIGHT = 1000 
WIDTH = 1000 
INNRHEIGHT = 600 
INNRWIDTH = 600 
maxlen = start.maxlen

ACC = 0.5
FRIC = -0.12
FPS = 25 
 
FramePerSec = pygame.time.Clock()

boxsize = 50
 
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
bg_img = pygame.image.load('imgs/background.png')
bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))

pygame.display.set_caption("Halvz")
basepos = WIDTH-INNRWIDTH/2 

iterations = 0
start.init()

class Block(pygame.sprite.Sprite):

    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, input_object):
       # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

       # Create an image of the block, and fill it with a color.
       # This could also be an image loaded from the disk.
        self.surf = pygame.Surface((INNRWIDTH/maxlen-1, INNRWIDTH/maxlen-1))
        # self.surf.fill(color)

        if input_object["flag"] == 1:
            self.surf.fill((187,37,40))
        elif input_object["flag"] == 2:
            self.surf.fill((20,107,58))
        else: 
            self.surf.fill((0,255,0))

       # Fetch the rectangle object that has the dimensions of the surf
       # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.surf.get_rect()

        self.rect.x = WIDTH-int(basepos)+(INNRWIDTH/maxlen*input_object["x"]-60)
        self.rect.y = WIDTH-int(basepos)+(INNRWIDTH/maxlen*input_object["y"]-60)

        self.object = input_object.copy()

    def explode(self, y, x):
        exp = images = [
            pygame.image.load("imgs/xp1.png"),
            pygame.image.load("imgs/xp2.png"),
            pygame.image.load("imgs/xp3.png"),
            pygame.image.load("imgs/xp4.png"),
            pygame.image.load("imgs/xp5.png"),
            pygame.image.load("imgs/xp6.png"),
        ]

        mixer.Sound.play(crash_sound)
        rect = self.rect
        
        xstart = WIDTH-int(basepos)+(INNRWIDTH/maxlen*x-60)
        ystart = WIDTH-int(basepos)+(INNRWIDTH/maxlen*y-60)
        #print("Rect: x: %s, y: %s" % (xstart, ystart))
        for item in exp:
            item = pygame.transform.scale(item, (int(INNRWIDTH/maxlen-1), int(INNRWIDTH/maxlen-1)))
            # 1000 = good
            for i in range(0, 200):
                displaysurface.blit(item, (xstart, ystart))


            pygame.display.update()

class platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((INNRWIDTH, 10))
        #self.surf = pygame.Surface((WIDTH, 20))
        self.surf.fill((0,78,29))
        self.rect = self.surf.get_rect(center = (WIDTH/2, INNRWIDTH+INNRWIDTH/2))

PT1 = platform()

all_sprites = pygame.sprite.Group()
all_sprites.add(PT1)

#new_object = start.stepper(maxlen)
#P1 = Box({})
#all_sprites.add(P1)
#    

old_gravity = 0
objects = []
while True:

    event = pygame.event.wait()
    if event.type == QUIT:
        pygame.quit()
        sys.exit()
    elif event.type == KEYDOWN:
        if event.key == pygame.K_c and pygame.key.get_mods() & pygame.KMOD_CTRL:
            print("pressed CTRL-C as an event")
            self.sighandle()

        if event.key == K_f:
            pass
        elif event.key == K_c:
            print("Redrawaaw")
            pass
        else:
            continue


    new_world = start.stepper(maxlen)

    # print("world", new_world)


    if new_world == None:
        print("NONE")
        continue

    for line in new_world:
        # print("line", line)
        for pixel in line:
            if pixel: 
                # print("pixel", pixel)

                # newobj = Box(pixel)
                newobj = Block(pixel)
                all_sprites.add(newobj)
                objects.append(newobj)


    data = start.print_world()
    world = data[0]
    deletes = data[1]
    score = data[2]
    for dels in deletes:
        for item in objects:
            if item.object["uuid"] == dels[2]:
                #print("Del y: %d, x:%d, uuid: %s" % (dels[0], dels[1], dels[2]))
                item.explode(dels[0], dels[1])
                break

    start.deletes = []

    #displaysurface.fill([255,255,255])
    displaysurface.blit(bg_img,(0,0))

    gravity = start.current_gravity*90 
    old_gravity = -1 
    if start.current_gravity != old_gravity:
        print("ANIMATe spin: %d!" % start.current_gravity)
        old_gravity = start.current_gravity 
        arrow = pygame.image.load("imgs/arrow.png")
        arrow = pygame.transform.scale(arrow, (200, 100))
        arrow = pygame.transform.rotate(arrow, gravity-90)

        displaysurface.blit(arrow, (100, 100))

    #pygame.draw.polygon(displaysurface, (0, 0, 0), ((0, 100), (0, 200), (200, 200), (200, 300), (300, 150), (200, 0), (200, 100)))


    scoring = my_font.render('Score: %d' % score, False, (128, 128, 128))
    displaysurface.blit(scoring, (WIDTH/2-50,10))
    gravity = my_font.render('Gravity: %s' % gravity, False, (128, 128, 128))
    displaysurface.blit(gravity, (WIDTH/2-50, 60))

    iterations += 1
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()


    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)

    # Render world
    FramePerSec.tick(FPS)
    pygame.display.update()
    all_sprites.empty() 
