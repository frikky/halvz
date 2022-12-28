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
pygame.display.set_caption("Halvz")

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
        basepos = WIDTH-INNRWIDTH/2 
        #self.pos = vec((xpos, 150))

        self.rect.x = WIDTH-int(basepos)+(INNRWIDTH/maxlen*input_object["x"]-60)
        self.rect.y = WIDTH-int(basepos)+(INNRWIDTH/maxlen*input_object["y"]-60)

        self.object = input_object.copy()

    def explode(self):
        exp = images = [
            pygame.image.load("imgs/xp1.png"),
            pygame.image.load("imgs/xp2.png"),
            pygame.image.load("imgs/xp3.png"),
            pygame.image.load("imgs/xp4.png"),
            pygame.image.load("imgs/xp5.png"),
            pygame.image.load("imgs/xp6.png"),
        ]

        mixer.Sound.play(crash_sound)
        for item in exp:
            displaysurface.blit(item, (self.rect.x, self.rect.y))
            pygame.display.update()
            time.sleep(0.1)

        #soundObj = mixer.Sound('explode.mp3')
        #soundObj = mixer.music.load(r'explode.mp3')
        #soundObj.play()
        #soundObj.play()

        #pygame.mixer.Sound.play(soundObj)

        #self.pos.y = 0 
        #self.pos.x = 0 
        #self.surf.fill((0,0,0))


        #self.rect.midbottom = self.pos

class Box(pygame.sprite.Sprite):
    def __init__(self, input_object):
        super().__init__()
        #self.surf = pygame.Surface((INNRWIDTH/maxlen, INNRWIDTH/maxlen))
        #self.surf.fill((128,255,40))
        #self.rect = self.surf.get_rect()

        #self.rect = self.surf.get_rect(center = (WIDTH/2, INNRWIDTH+INNRWIDTH/2))
        #print(input_object, xpos)

        #self.surf = pygame.Surface((30, 30))
        self.surf = pygame.Surface((INNRWIDTH/maxlen-1, INNRWIDTH/maxlen-1))

        if input_object["flag"] == 1:
            self.surf.fill((187,37,40))
        elif input_object["flag"] == 2:
            self.surf.fill((20,107,58))
        else: 
            self.surf.fill((0,255,0))

        self.rect = self.surf.get_rect()

        basepos = WIDTH-INNRWIDTH/2 
        xpos = WIDTH-int(basepos)+(INNRWIDTH/maxlen*input_object["x"]-60)
        self.pos = vec((xpos, 150))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.object = input_object.copy()

        #self.rect.midbottom = self.pos

    def explode(self):
        exp = images = [
            pygame.image.load("imgs/xp1.png"),
            pygame.image.load("imgs/xp2.png"),
            pygame.image.load("imgs/xp3.png"),
            pygame.image.load("imgs/xp4.png"),
            pygame.image.load("imgs/xp5.png"),
            pygame.image.load("imgs/xp6.png"),
        ]

        mixer.Sound.play(crash_sound)
        for item in exp:
            displaysurface.blit(item, (self.pos.x-37, self.pos.y-72))
            pygame.display.update()
            time.sleep(0.1)

        #soundObj = mixer.Sound('explode.mp3')
        #soundObj = mixer.music.load(r'explode.mp3')
        #soundObj.play()
        #soundObj.play()

        #pygame.mixer.Sound.play(soundObj)

        #self.pos.y = 0 
        #self.pos.x = 0 
        #self.surf.fill((0,0,0))


        self.rect.midbottom = self.pos

    def move_down(self, pixel):
        if pixel["x"] != self.object["x"]:
            print("change: %d vs %d" % (pixel["x"], self.object["x"]))

        if pixel["y"] >= 8 or self.object["y"] >= 8:
            self.surf.fill([0,0,0])
            return

        if pixel["y"] == self.object["y"]:
            return

        self.acc.y = ACC

        self.pos.y = self.pos.y + INNRWIDTH/maxlen
        self.acc.y += self.vel.y * FRIC

        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        self.rect.midbottom = self.pos
        self.object = pixel.copy()
        #pygame.display.update()

    def manual_move(self):
        self.acc = vec(0,0)

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC

        if pressed_keys[K_UP]:
            self.acc.y = -ACC
        if pressed_keys[K_DOWN]:
            self.acc.y = ACC

        self.acc.x += self.vel.x * FRIC
        self.acc.y += self.vel.y * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        if self.pos.y > HEIGHT:
            self.pos.y = 0
        if self.pos.y < 0:
            self.pos.y = HEIGHT

        self.rect.midbottom = self.pos

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

    data = start.print_world()
    world = data[0]
    deletes = data[1]
    for dels in deletes:
        for item in objects:
            if item.object["uuid"] == dels[2]:
                #print("Del y: %d, x:%d, uuid: %s" % (dels[0], dels[1], dels[2]))
                item.explode()
                break

    start.deletes = []

    new_world = start.stepper(maxlen)

    # print("world", new_world)
    displaysurface.fill([0,0,0])
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
