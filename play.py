
import pygame
from pygame.locals import *
from pygame import mixer

pygame.init()
FramePerSec = pygame.time.Clock()

WIDTH = 1000 
HEIGHT = 1000 
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60 

all_sprites = pygame.sprite.Group()
pygame.display.set_caption("Rocketto")
orange_img = pygame.image.load("imgs/rocket.png")
my_font = pygame.font.SysFont('Comic Sans MS', 30)
size = (35, 35)

class Block(pygame.sprite.Sprite):
    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self):
        global orange_img
        global size

        # Meaning acceleration needs to be more than 9.81 to move
        # 9.81/60 (fps) = 0.1635/frame?

        #self.gravity = 9.81
        self.gravity = 9.81
        self.rotation = 0 
        self.altitude = 0
        self.speed = 0
        self.acceleration = 0
        self.acceleration_constant = 0.1
        self.max_speed = 500
        self.rotational_friction = 100

        # How much of mass is fuel?
        self.fuel_consumption = 0.1 # % decrase/frame 
        self.fuel = 100  # Max fuel (%)
        self.fuel_mass = 9000 # Fuel mass (kg)
        self.fuel_mass_consumption = self.fuel_mass-(self.fuel_mass*(100-self.fuel_consumption)/100)

        self.base_mass = 1000
        self.mass = self.fuel_mass+self.base_mass   # Total mass (kg)
        self.start_mass = self.fuel_mass+self.base_mass

       # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.surf = pygame.Surface(size)
        self.surf = self.surf.convert()

        charRect = pygame.Rect((0,0),(10, 10))
        orange = pygame.transform.scale(orange_img, size)

        charRect[0] = WIDTH/2-size[0]/2 
        charRect[1] = HEIGHT-HEIGHT/5

        self.rect = charRect
        self.surf.blit(orange, charRect)

        displaysurface.blit(orange, charRect)

    # Normal gravity step
    def step(self, skip):
        global FPS
        global size
        global WIDTH
        global HEIGHT

        surf = pygame.Surface((WIDTH, HEIGHT))
        surf.fill((0,0,0))
        displaysurface.blit(surf,(0,0))

        run_calculation = True
        if not skip:
            if self.acceleration > self.gravity or self.altitude > 0:
                #self.acceleration = self.acceleration - self.gravity/FPS
                self.acceleration = self.acceleration - self.gravity/FPS*5

            if self.acceleration < 0 and self.altitude > 0:
                self.speed = self.speed + self.acceleration
            elif self.acceleration-self.gravity > 0:
                self.speed = self.speed + self.acceleration

            if self.altitude < 0: 
                print("Hit the ground a bit hard huh?")

                self.speed = 0
                self.acceleration = 0
                self.altitude = 0

                run_calculation = False 
                self.rect[0] = WIDTH/2-size[0]/2 
                self.rect[1] = HEIGHT-HEIGHT/5

        if self.speed != 0:
            print("Altitude: %d, Speed: %d, Acc: %.2f" % (self.altitude, self.speed, self.acceleration))

        # Steering constant
        constant = 1.234568

        if run_calculation: 
            y_speed = self.speed

            # Doesn't work downwards
            if self.rotation == 0:
                self.rect[1] -= self.speed 
            elif self.rotation > 0:
                #print("More than 0")
                x_speed = self.speed*int(self.rotation*(90/100)*constant)/100
                y_speed = self.speed*(1-int(self.rotation*(90/100)*constant)/100)

                self.rect[1] = self.rect[1]-y_speed
                self.rect[0] = self.rect[0]-x_speed
            else: 
                #print("Less than 0")

                x_speed = self.speed*int((self.rotation*-1)*(90/100)*constant)/100
                y_speed = self.speed*(1-int((self.rotation*-1)*(90/100)*constant)/100)

                self.rect[1] = self.rect[1]-y_speed
                self.rect[0] = self.rect[0]+x_speed

            if self.rect[1] < 0: 
                self.rect[1] = HEIGHT+self.rect[1]
            elif self.rect[1] > HEIGHT:
                self.rect[1] = self.rect[1]-HEIGHT
        
            self.altitude += y_speed 

        orange = pygame.transform.scale(orange_img, size)
        orange = pygame.transform.rotate(orange, self.rotation)

        displaysurface.blit(orange, self.rect)

    def accelerate(self):
        # Should be based on mass

        if self.fuel <= 0:
            self.step(False)
            return

        # Newtons doesn't work too well here huh...
        # Rocket equation pls
        # Use self.mass as well

        #0.1 = 100% mass
        #1.0 = 0% mass

        # This is some bad math only :)
        acc_modifier = (100-(100/self.start_mass)*self.mass)/10
        mass_acceleration = self.acceleration_constant*acc_modifier
        print("Mass acc: ", mass_acceleration, "Mass: ", acc_modifier)
        print()

        self.acceleration = self.acceleration + mass_acceleration

        # 20% fuel just to take off?
        # Acc should again be based on mass
        #print(self.speed+self.acceleration-self.gravity)
        if self.speed+self.acceleration-self.gravity > 0:
            self.speed = self.speed + self.acceleration - self.gravity
        else:
            self.speed = self.speed 

        self.fuel = self.fuel - self.fuel_consumption
        self.fuel_mass = self.fuel_mass - self.fuel_mass_consumption 
        self.mass = self.fuel_mass+self.base_mass   # Total mass (kg)

        # For steering
        if self.rotational_friction > 0:
            self.rotational_friction -= 1

        #print()
        #print("ACC: ", self.acceleration, "SPD: ", self.speed, "ROT: ", self.rotation)

        #rotation_calc = self.speed/1.7

        # Figure out X & Y calcs
        # 45 degrees rigt, 1 speed = x+0.5, y+0.5
        # 45 degrees right, 2 speed = x+1, y+1
        # 20 deg
        # straigt up, 2 speed = x+0, y+2
        # x & y should be divided by speed based on rotation
        # 0 = straight = total
        # max = 180, -90 -> 90 
        # 100/rotation = 90/100 = 0.9

        # -drag (aerodynamics), -gravity
        # 45 = speed/2 = 1/2 = speed*0.5 for y, speed*0.5 for x
        # 45 = speedj
        # 55 = speed/100/(55*(90/100)) = speed*0.495*1.11 for y, speed*(0.9-0.495*0.11) for x
        # int(45*(90/100)*1.234568)

        # Currently based on 180 degrees it seems like
        # We want to do -90->90 instead of 0->180

        # Should be general, as it's based on current direction as well
        # Instant changes make no sense
        self.step(True)


    def reset(self):
        global orange_img

        self.rotation = 0 
        self.altitude = 0
        self.speed = 0
        self.acceleration = 0
        self.max_speed = 500


        charRect = pygame.Rect((0,0),(10, 10))
        charRect[0] = WIDTH/2-size[0]/2 
        charRect[1] = HEIGHT-HEIGHT/5

        self.rect[0] = WIDTH/2-size[0]/2 
        self.rect[1] = HEIGHT-HEIGHT/5

        orange = pygame.transform.scale(orange_img, size)
        self.surf.blit(orange, self.rect)
        displaysurface.blit(orange, charRect)

    def rotate(self, direction):
        global orange_img
        global size
        global all_sprites

        # Doesn't work if no self.speed

        if self.speed == 0:
            return

        #rotation = 1*(100-self.rotational_friction)
        rotation = 1
        #print((100/100-self.rotational_friction))
        new_rotation = self.rotation
        if direction == "left":
            self.rotation += rotation 
            new_rotation = self.rotation
        elif direction == "right":
            self.rotation = self.rotation-rotation
            new_rotation = self.rotation

        #self.rect.x = self.rect[0]+50 
        #self.rect.y = self.rect[1]+50 
        #orange = pygame.transform.scale(orange_img, size)
        #orange = pygame.transform.rotate(orange, self.rotation)

        #displaysurface.blit(orange, self.rect)


rocket = Block()
all_sprites.add(rocket)

while True:
    keys = pygame.key.get_pressed()  
    if keys[pygame.K_UP]:
        rocket.accelerate()
    elif keys[pygame.K_DOWN]:
        rocket.reset()
    elif keys[pygame.K_LEFT]:
        rocket.rotate("left")
    elif keys[pygame.K_RIGHT]:
        rocket.rotate("right")
    else:
        rocket.step(False)

    for event in pygame.event.get():
        event = event.__dict__
        if "key" in event and not "unicode" in event:
            key = event["key"]
     
            surf = pygame.Surface((WIDTH, HEIGHT))
            surf.fill((0,0,0))
            displaysurface.blit(surf,(0,0))
        
        #if key == 32:
        #    rocket.step(False)
        #    continue
        #if key == 276:
        #    rocket.rotate("left")
        #    rocket.step(True)
        #if key == 275:
        #    rocket.rotate("right")
        #    rocket.step(True)
        #if key == 274:
        #    print("Down")
        #    rocket.reset()
        #
        #if key == 273:
        #    rocket.accelerate()

    alt = my_font.render('Altitude: %d' % rocket.altitude, False, (128, 128, 128))
    displaysurface.blit(alt, (10,10))

    speed = my_font.render('Speed: %d, Acc: %.2f' % (rocket.speed, rocket.acceleration), False, (128, 128, 128))
    displaysurface.blit(speed, (10, 40))

    #math = my_font.render('f = m*a = %d = %.2f*%d' % (rocket.acceleration*rocket.mass, rocket.acceleration, rocket.mass), False, (128, 128, 128))
    #displaysurface.blit(math, (10, 70))

    fuel = my_font.render('Fuel: %d, Mass: %d' % (rocket.fuel, rocket.mass), False, (128, 128, 128))
    displaysurface.blit(fuel, (10, 70))

    pygame.display.update()
    FramePerSec.tick(FPS)
    #all_sprites.empty() 
