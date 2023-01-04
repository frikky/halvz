import sys
import pygame
import random
import time
import os
import threading
from pygame.locals import *
from pygame import mixer

import start
 
pygame.init()

mixer.init() 
#mixer.music.load(r'explode.mp3')
#mixer.music.set_volume(0.2)
#mixer.music.play()

explode_sound = pygame.mixer.Sound("sound/explode.ogg")
grav_swap = pygame.mixer.Sound("sound/grav_swap_1.ogg")
blipp = pygame.mixer.Sound("sound/blip_grav_1.ogg")

orang = pygame.image.load("imgs/orang.png")
grn = pygame.image.load("imgs/grn.png")
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
FPS = 60 
ADDBLOCK = 15 
 
FramePerSec = pygame.time.Clock()

boxsize = 50
 
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
bg_img = pygame.image.load('imgs/background.png')
bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))
#pygame.draw.rect(work_img, (255,0, 0, opacity),  (0,0, 640,480))

dark = pygame.Surface((bg_img.get_width(), bg_img.get_height()), flags=pygame.SRCALPHA)
dark.fill((50, 50, 50, 0))
bg_img.blit(dark, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
#will subtract 50 from the RGB values of the surface called image.


pygame.display.set_caption("Halvz")
basepos = WIDTH-INNRWIDTH/2 

start.init()

class Block(pygame.sprite.Sprite):

    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, input_object):
        global orang
        global grn 

       # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

       # Create an image of the block, and fill it with a color.
       # This could also be an image loaded from the disk.
        size = int(INNRWIDTH/maxlen-1), int(INNRWIDTH/maxlen-1)
        self.surf = pygame.Surface(size)
        self.surf = self.surf.convert()

        # self.surf.fill(color)

        if input_object["flag"] == 1:
            self.surf.fill((187,37,40))
            
            charRect = pygame.Rect((0,0),(10, 10))
            orang = pygame.transform.scale(orang, size)
            self.surf.blit(orang, charRect)
            
        elif input_object["flag"] == 2:
            self.surf.fill((20,107,58))

            charRect = pygame.Rect((0,0),(10, 10))
            grn = pygame.transform.scale(grn, size)
            self.surf.blit(grn, charRect)

        else: 
            self.surf.fill((255,255,255))

       # Fetch the rectangle object that has the dimensions of the surf
       # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.surf.get_rect()

        self.rect.x = WIDTH-int(basepos)+(INNRWIDTH/maxlen*input_object["x"]-60)
        self.rect.y = WIDTH-int(basepos)+(INNRWIDTH/maxlen*input_object["y"]-60)

        self.object = input_object.copy()

    def explode(self, y, x):
        global orang
        global grn 

        exp = images = [
            pygame.image.load("imgs/xp1.png"),
            pygame.image.load("imgs/xp2.png"),
            pygame.image.load("imgs/xp3.png"),
            pygame.image.load("imgs/xp4.png"),
            pygame.image.load("imgs/xp5.png"),
            pygame.image.load("imgs/xp6.png"),
        ]

        rect = self.rect
        
        xstart = WIDTH-int(basepos)+(INNRWIDTH/maxlen*x-60)
        ystart = WIDTH-int(basepos)+(INNRWIDTH/maxlen*y-60)

        for item in exp:
            item = pygame.transform.scale(item, (int(INNRWIDTH/maxlen-1), int(INNRWIDTH/maxlen-1)))
            # 1000 = good
            for i in range(0, 1):
                displaysurface.blit(item, (xstart, ystart))


            pygame.display.update()


class platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((INNRWIDTH, 10))
        #self.surf = pygame.Surface((WIDTH, 20))
        self.surf.fill((0,78,29))
        self.rect = self.surf.get_rect(center = (WIDTH/2, INNRWIDTH+INNRWIDTH/2))
        #self.rect.center = (self.x, self.y)

    def spin(self):
        #self.angle = (self.angle + 45) * 360
        #arrow = pygame.transform.scale(arrow, (200, 150))
        print("spin")
        pygame.transform.rotate(self.surf, 270)
        pygame.display.update()

def explode(item, dels):
    new_x, new_y = start.reverse_gravity(dels[1], dels[0])
    item.explode(new_y, new_x)

def run_deletes(objects, deletes):
    all_deletes = []
    for dels in deletes:
        for item in objects:
            if item.object["uuid"] == dels[2]:
                x = threading.Thread(target=explode, args=(item, dels, ))
                x.start()
                all_deletes.append(x)
                break

    for item in all_deletes:
        item.join()

def run_game():
    global maxlen 
    global ADDBLOCK 

    all_sprites = pygame.sprite.Group()

    old_gravity = 0
    iterations = 1
    clicks = 1
    difficulty = 1

    objects = []
    running = False

    while True:
        keys = pygame.key.get_pressed()  
        changed = False
        if keys[pygame.K_UP]:
            changed = start.gravity_swap(2)
        elif keys[pygame.K_DOWN]:
            changed = start.gravity_swap(0)
        elif keys[pygame.K_LEFT]:
            changed = start.gravity_swap(3)
        elif keys[pygame.K_RIGHT]:
            changed = start.gravity_swap(1)
        elif keys[27]:
            show_menu("pause", start.score)
            return

        if changed == True:
            clicks += 1
            if clicks % 10 == 0:
                start.distance_check += 1

            if clicks % 3 == 0:
                if ADDBLOCK > 1:
                    ADDBLOCK -= 1

            if clicks % 5 == 0:
                difficulty += 1

                start.maxlen += 1
                maxlen += 1

                x = [] 
                for i in range(0, maxlen):
                    x.append(None)

                start.world.append(x.copy())

        iterations += 1
        start.iterations += 1

        new_world = start.stepper(maxlen, iterations % ADDBLOCK != 0)
        if new_world == None:
            show_menu("lose", start.score)
            return
    
        if len(objects) >= maxlen*maxlen*4:
            objects = objects[maxlen*maxlen*2:]
    
        for line in new_world:
            for pixel in line:
                if pixel: 
                    newobj = Block(pixel)
                    all_sprites.add(newobj)
                    objects.append(newobj)
    
    
        data = start.print_world()
        world = data[0]
        deletes = data[1]
        score = data[2]


        # Animations :)
        run_deletes(objects, deletes)

    
        start.deletes = []
    
        displaysurface.blit(bg_img,(0,0))
    
        gravity = start.current_gravity*90 
        old_gravity = -1 
        if start.current_gravity != old_gravity:
            old_gravity = start.current_gravity 
    
            arrow = pygame.image.load("imgs/arrow.png")
            arrow = pygame.transform.scale(arrow, (200, 150))
            arrow = pygame.transform.rotate(arrow, gravity-90)
    
            displaysurface.blit(arrow, (100, 100))
    
        filled = start.added
        maxadded = int(maxlen*maxlen*start.auto_swap_check)
        if filled >= maxlen*maxlen-1 or start.maxlen >= 32:
            print("Lost!")
            show_menu("lose", start.score)
            return

        scoring = my_font.render('Score: %d' % score, False, (128, 128, 128))
        displaysurface.blit(scoring, (WIDTH/2-50,10))

        filled_amount = my_font.render('Filled: %.2f%s' % ((filled/maxadded)*100, "%"), False, (128, 128, 128))
        displaysurface.blit(filled_amount, (WIDTH/2-50, 60))

        difficulty_text = my_font.render('Difficulty: %d, %dx%d, %.1f/sec)' % (start.distance_check, start.maxlen, start.maxlen, FPS/ADDBLOCK), False, (128, 128, 128))

        displaysurface.blit(difficulty_text, (WIDTH/2-50, 110))
    
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

# This is shitty and running inside itself rofl
def show_menu(status, points):
    global maxlen
    global ADDBLOCK 

    all_sprites = pygame.sprite.Group()
    displaysurface.blit(bg_img,(0,0))

    if status == "pause":
        start_text = my_font.render('Press Space to Continue', False, (128, 128, 128))
        displaysurface.blit(start_text, (WIDTH/2-190, HEIGHT/2-25))
    elif status == "lose":
        start_text = my_font.render('You lost. Press Space to try again', False, (128, 128, 128))
        displaysurface.blit(start_text, (WIDTH/2-290, HEIGHT/2-25))

        score = my_font.render('Score: %d' % points, False, (128, 128, 128))
        displaysurface.blit(score, (WIDTH/2-100, HEIGHT/2+25))

        start.score = 0
        start.iterations = 0
        start.current_gravity = 0
        start.prev_gravity_swap = 0
        start.gravity_swaps = 0
        start.maxlen = start.original_maxlen

        maxlen = start.maxlen
        ADDBLOCK = 15 


        start.world = []
        start.init()

        #filled_amount = my_font.render('Paused', False, (128, 128, 128))
        #displaysurface.blit(filled_amount, (WIDTH/2-60, HEIGHT/2+25))
    else:
        start_text = my_font.render('Press Space to start', False, (128, 128, 128))
        displaysurface.blit(start_text, (WIDTH/2-150, HEIGHT/2-25))


    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYUP:
                if event.key == 32:
                    run_game()
                    return

if __name__ == "__main__":
    show_menu("start", 0)
    #run_game()
