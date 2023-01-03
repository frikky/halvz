import sys
import time
import random
import math
import uuid
import copy

world = []
should_add = True

# Quadrant for now
maxlen = 16 
xlen = maxlen 
ylen = maxlen 

distance_check = 6
score = 0
iterations = 0
# 0 = 0 degrees, 1 = 90, 2 = 180, 3 = 240/-90
added = 0

# Gravity
#swap_check = 0.6
swap_check = 1.1
current_gravity = 0
prev_gravity_swap = 0
gravity_swaps = 0

deletes = []

def init():
    global world
    world = []
    x = []

    # add stuff pls
    for i in range(0, maxlen):
        x.append(None)

    for i in range(0, maxlen):
        world.append(x.copy())

def rewrite_pixel(value):
    if value == None:
        return (" 0 ", "")

    #print(value)
    if value["flag"] == 1:
        return ("%s%d%s" % (value["source_loc"], value["flag"], value["dest_loc"]), "\033[1;31m")
    elif value["flag"] == 2:
        return ("%s%d%s" % (value["source_loc"], value["flag"], value["dest_loc"]), "\033[0;32m")
    elif value["flag"] == 5:
        return (" %d " % value["flag"], "")

    return ("eRRORR", "")

def print_world():
    #for i in range(maxlen*maxlen):
    #    sys.stdout.write(f"\b \b")
    return (world, deletes, score)

    for line in world:
        for pixel in line:
            #print("Pixel: ", pixel)
            pixelvalue = rewrite_pixel(pixel)
            sys.stdout.write(f"{pixelvalue[1]}{pixelvalue[0]}\033[0m")
            
        sys.stdout.write(f"\n")

    #return world

def gravitypls():
    global world
    global distance_check 
    global score
    global deletes

    
    #world = copy.deepcopy(world)

    #100% = maxlen*maxlen
    #80% = maxlen*maxlen*0.8

    added = 0
    start = time.time_ns()
    totals = []
    for ypos in range(len(world)-1, -1, -1):
        startgrav = time.time_ns()
        for xpos in range(len(world[ypos])): 

            skipGravity = False
            if not world[ypos][xpos]:
                skipGravity = True 
                #continue
            else:
                added += 1

            if ypos >= maxlen-1 and not skipGravity:
                skipGravity = True
                #world[ypos][xpos]["source_loc"] = " "
                #world[ypos][xpos]["dest_loc"] = " "
                #world[line-2][cnt] = None
                #continue

            # Check line's X below if empty?
            # 1. Check if below first
            # 2. Is it on something? What is it?
            skipMove = False
            if not skipGravity:
                if world[ypos+1][xpos]:
                    skipMove = True

                    option = random.randint(0,2) 
                    #print(xpos+1, maxlen-1)
                    if option == 0:
                        # stay
                        #world[ypos+1][xpos]["source_loc"] = " "
                        #world[ypos+1][xpos]["dest_loc"] = " "
                        pass

                    elif option == 1 and xpos+1 <= maxlen-1 and not world[ypos+1][xpos+1]:  
                        # move to right down
                        world[ypos+1][xpos+1] = world[ypos][xpos]
                        #world[ypos+1][xpos+1]["dest_loc"] = " "
                        #world[ypos+1][xpos+1]["source_loc"] = "\\"
                        world[ypos+1][xpos+1]["y"] = ypos+1
                        world[ypos+1][xpos+1]["x"] = xpos+1
                        world[ypos][xpos] = None

                    elif option == 2  and xpos-1 >= 0 and not world[ypos+1][xpos-1]:
                        # move to left down
                        world[ypos+1][xpos-1] = world[ypos][xpos]
                        #world[ypos+1][xpos-1]["dest_loc"] = "/"
                        #world[ypos+1][xpos-1]["source_loc"] = " "
                        world[ypos+1][xpos-1]["y"] = ypos+1
                        world[ypos+1][xpos-1]["x"] = xpos-1
                        world[ypos][xpos] = None

                if not skipMove:

                    world[ypos+1][xpos] = world[ypos][xpos]
                    world[ypos+1][xpos]["y"] = ypos+1
                    #world[ypos+1][xpos]["source_loc"] = " "
                    #world[ypos+1][xpos]["dest_loc"] = " "

                    world[ypos][xpos] = None
    

            # every time we change a pixel something, we calculate the entire line again
            # 1 = bortover
            # 2 = oppover
            # lende = 4

            # Almost all calculations are here
            # How do we optimize?
            
            # Check if they actually hit something?
            # No point in checking their lines in the air
            if not skipGravity:

                # Only checking currentline?
                for xpos2 in range(xpos, len(world[ypos])): 
                    # None
                    if not world[ypos][xpos2]:
                        continue

        
                    if world[ypos][xpos2]["flag"] <= 0: 
                        continue

                    # check xpos + 3
                    flag = world[ypos][xpos2]["flag"] 
                    if xpos2+distance_check < maxlen:
                        found = 0

                        for i in range(distance_check):
                            if not world[ypos][xpos2+i]:
                                break

                            if world[ypos][xpos2+i]["flag"] == flag:
                                found += 1

                                if found == distance_check:
                                    #print("Same X!!")

                                    for i in range(distance_check):
                                        deletes.append((ypos, xpos2+i, world[ypos][xpos2+i]["uuid"]))
                                        world[ypos][xpos2+i] = None

                                    world[ypos][xpos2] = None

                                    score += distance_check
                                    break

                    # check ypos + 3
                    if ypos+distance_check < maxlen:
                        found = 0
                        for i in range(distance_check):
                            if not world[ypos+i][xpos2]:
                                break

                            if world[ypos+i][xpos2]["flag"] == flag:
                                found += 1
                        
                                if found == distance_check:
                                    for i in range(distance_check):
                                        deletes.append((ypos+i, xpos2, world[ypos+i][xpos2]["uuid"]))
                                        world[ypos+i][xpos2] = None

                                    world[ypos][xpos2] = None
                                    score += distance_check
                                    break

                    # check ypos - 3
                    if ypos-distance_check > 0:
                        found = 0
                        for i in range(distance_check):
                            if not world[ypos-i][xpos2]:
                                break

                            if world[ypos-i][xpos2]["flag"] == flag:
                                found += 1

                                if found == distance_check:
                                    for i in range(distance_check):
                                        deletes.append((ypos-i, xpos2, world[ypos-i][xpos2]["uuid"]))
                                        world[ypos-i][xpos2] = None

                                    world[ypos][xpos2] = None
                                    score += distance_check
                                    break

        endgrav = time.time_ns()
        totals.append(endgrav-startgrav)

    #time.sleep(1)
    # 60 fps = how many ns in a frame?
    # Per line = 30.000-50.000~ for 16x16
    # If data in line, goes up to 1.200.000
    # 

    # 32x32: 400.000~ ns by default for calc
    # 400.000 ns * 1.0^-9 = 0.000400000s = 4ms?
    # 4/1000 = max fps = 250@400.000ns 
    # end num is ~ 5.000.000/iter @ 32 lines
    # 0.005000000ns = 50ms. 1000/50 = 20 fps max 
    # Need 3x speed somehow?
    # 1.750.000 = max/iter@60fps!

    # 8x8: topping out at 450.000~
    # 16x16: 2.750.000
    # 32x32: 5.500.000~

    end = time.time_ns()
    total = end-start
    #print(total, totals)
    #print()
    return added

def gravity_swap(direction):
    global world
    global gravity_swaps
    global current_gravity

    newworld = []
    for i in range(maxlen):
        janus = []
        for y in range(maxlen):
            janus.append(None)

        newworld.append(janus)

    if direction == current_gravity:
        return 

    swap = random.randint(0, 2)
    if direction >= 0:
        # Based on current gravity
        if direction == 1:
            #print("SWAP: RIGHT")
            if current_gravity == 0:
                swap = 0
            elif current_gravity == 2:
                swap = 1
            elif current_gravity == 3:
                swap = 2
        elif direction == 2:
            #print("SWAP: UP")
            if current_gravity == 0:
                swap = 2 
            elif current_gravity == 1:
                swap = 0
            elif current_gravity == 3:
                swap = 1
        elif direction == 3:
            #print("SWAP: LEFT")
            if current_gravity == 0:
                swap = 1
            elif current_gravity == 1:
                swap = 2
            elif current_gravity == 2:
                swap = 0
        elif direction == 0:
            #print("SWAP: DOWN")
            if current_gravity == 1:
                swap = 1
            elif current_gravity == 2:
                swap = 2
            elif current_gravity == 3:
                swap = 0
        else:
            print("NO handler for direction %d" % direction)
            exit()

    #print("\n\nGRAVITYSWAPPP WOOOOOOOOOO: %d \n\n" % swap)

    if swap == 0:
        #print("90 clockwise")

        current_gravity = (current_gravity + 1) % 4

        # 90 grader counter:
        for ypos in range(len(world)):
            for xpos in range(len(world[ypos])):
                newypos = xpos
                newxpos = maxlen-1-ypos

                newworld[newypos][newxpos] = world[ypos][xpos]

                if not newworld[newypos][newxpos]:
                    continue

                newworld[newypos][newxpos]["x"] = newxpos
                newworld[newypos][newxpos]["y"] = newypos

                newworld[newypos][newxpos]["source_loc"] = " "
                newworld[newypos][newxpos]["dest_loc"] = " "
    elif swap == 1:
        #print("90 counter-clockwise")

        current_gravity = (current_gravity - 1) % 4


        # 90 grader counter:
        for ypos in range(len(world)):
            for xpos in range(len(world[ypos])):
                newypos = maxlen-1-xpos
                newxpos = ypos

                newworld[newypos][newxpos] = world[ypos][xpos]

                if not newworld[newypos][newxpos]:
                    continue

                newworld[newypos][newxpos]["x"] = newxpos
                newworld[newypos][newxpos]["y"] = newypos

                newworld[newypos][newxpos]["source_loc"] = " "
                newworld[newypos][newxpos]["dest_loc"] = " "

    elif swap == 2:
        #print("180 swap")

        current_gravity = (current_gravity + 2) % 4


        for ypos in range(len(world)):
            for xpos in range(len(world[ypos])):
                newypos = maxlen-1-ypos 
                newxpos = maxlen-1-xpos 

                newworld[newypos][newxpos] = world[ypos][xpos]

                if not newworld[newypos][newxpos]:
                    continue

                newworld[newypos][newxpos]["x"] = newxpos
                newworld[newypos][newxpos]["y"] = newypos

                newworld[newypos][newxpos]["source_loc"] = " "
                newworld[newypos][newxpos]["dest_loc"] = " "

    #180 grader = ypos:
    #max-curpos = newpos?
    #8-6 = 2

    # 90 grader clockwise:
    # 0:0 = 0:3
    # 0:3 = 3:0
    # 1:2 = 1:3
    # 2:1 = 1:1

    #print_world()
    world = newworld
    gravity_swaps += 1 
    #print()
    #print_world()

def reverse_gravity(x,y):

    global current_gravity
    global world

    GRAVITY_0 = 0
    GRAVITY_90 = 1
    GRAVITY_180 = 2
    GRAVITY_240 = 3

    if current_gravity == GRAVITY_90:
        newypos = maxlen-1-x
        newxpos = y
        return (newxpos, newypos)
    elif current_gravity == GRAVITY_240:
        #print("90 clockwise")

        # 90 grader clockwise:

        newypos = x
        newxpos = maxlen-1-y

        return (newxpos, newypos)
    elif current_gravity == GRAVITY_180:

        # newypos = maxlen-1-x 
        # newxpos = maxlen-1-y 

        # newypos_temp = maxlen-1-x
        # newxpos_temp = y

        newypos = maxlen-1-y
        newxpos = maxlen-1-x

        return (newxpos, newypos)
    else:
        return (x,y)



def stabelize_world():
    global current_gravity
    global world


    newworld = []
    for i in range(maxlen):
        janus = []
        for y in range(maxlen):
            janus.append(None)

        newworld.append(janus)


    for ypos in range(len(world)):
        for xpos in range(len(world[ypos])):
            (newxpos, newypos) = reverse_gravity(xpos, ypos)

            newworld[newypos][newxpos] = world[ypos][xpos]

            if not newworld[newypos][newxpos]:
                continue

            newworld[newypos][newxpos]["x"] = newxpos
            newworld[newypos][newxpos]["y"] = newypos

            newworld[newypos][newxpos]["source_loc"] = " "
            newworld[newypos][newxpos]["dest_loc"] = " "
    return newworld


def stepper(maxlen):
    global world
    global should_add
    global score
    global swap_check
    global added
    global prev_gravity_swap

    # Calculate where it should go instead
    #if should_add == False:
    added = gravitypls()
    maxadded = int(maxlen*maxlen*swap_check)
    #print("Amount: %d/%d (%d), Score: %d, Gravity Swaps: %d, Iter: %d" % (added, maxadded, maxlen*maxlen, score, gravity_swaps, iterations))

    if added >= maxadded:
        if iterations-prev_gravity_swap > 20:
            gravity_swap(-1)
            prev_gravity_swap = iterations

        return stabelize_world() 

    #should_add = False 
    ypos = 0
    maxcnt = maxlen

    xpos = random.randint(0, maxlen-1)
    #if added >= maxlen*maxlen-maxlen: 
    #    while True:
    #        print("In while true")

    #        if world[ypos][xpos] != None:
    #            print("BAD - it has stuff!")
    #            continue

    #        xpos = random.randint(0, maxlen-1)
    #        break

    new_object = {
        "uuid": str(uuid.uuid4()),
        "x": xpos,
        "y": ypos,
        "flag": random.randint(1, 2),
        "source_loc": " ",
        "dest_loc": " ",
    }

    world[ypos][xpos] = new_object
    return stabelize_world() 

if __name__ == "__main__":
    print()
    init()

    while True:
        value = input()
        if value == "c":
            init()
            print()

        stepper(maxlen)
        print_world()
        iterations += 1
        #time.sleep(10)

    print()
