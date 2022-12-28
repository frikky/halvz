import sys
import pygame
import random
from pygame.locals import *

import start
 
pygame.init()
vec = pygame.math.Vector2  # 2 for two dimensional
 
HEIGHT = 1000 
WIDTH = 1000 
INNRHEIGHT = 600 
INNRWIDTH = 600 
maxlen = start.maxlen

ACC = 0.5
FRIC = -0.12
FPS = 60
 
FramePerSec = pygame.time.Clock()
boxsize = 50
 
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Halvz")

iterations = 0
start.init()

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

    def move_down(self, pixel):
        if pixel["x"] != self.object["x"]:
            print("change: %d vs %d" % (pixel["x"], self.object["x"]))

        if pixel["y"] == self.object["y"]:
            return

        self.acc.y = ACC

        self.pos.y = self.pos.y + INNRWIDTH/maxlen
        self.acc.y += self.vel.y * FRIC

        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        self.object = pixel.copy()
        self.rect.midbottom = self.pos

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

    new_object = start.stepper(maxlen)
    if new_object: 
        newobj = Box(new_object)
        all_sprites.add(newobj)
        objects.append(newobj)

    world = start.print_world()
    for item in objects:
        if item.object["uuid"] == pixel["uuid"]:
            item.move_down(pixel)
            found = item
            break

    for line in world:
        for pixel in line:
            found = None 
            if not pixel: 
                continue


            if not found: 
                print("NOT FOUND: %s" % pixel)

        #self.object = input_object

    iterations += 1

    #print("Object amount: %d" % len(objects))
    #for item in objects:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()


    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)

    # Render world
    FramePerSec.tick(FPS)
    pygame.display.update()
