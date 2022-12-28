import sys
import time
import random
import math
import uuid
import copy

world = []
should_add = True

# Quadrant for now
xlen = 8
ylen = 8
maxlen = 8 

percentAdded = 0
distance_check = 4 
score = 0
iterations = 0
gravity_swaps = 0

deletes = []

def init():
    global world
    world = []
    x = []

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
    for ypos in range(len(world)-1, -1, -1):
        for xpos in range(len(world[ypos])): 
            skipGravity = False
            if not world[ypos][xpos]:
                skipGravity = True 
                #continue
            else:
                added += 1

            if ypos >= maxlen-1 and not skipGravity:
                skipGravity = True
                world[ypos][xpos]["source_loc"] = " "
                world[ypos][xpos]["dest_loc"] = " "
                #world[line-2][cnt] = None
                #continue

            # Check line's X below if empty?
            # 1. Check if below first
            # 2. Is it on something? What is it?
            if not skipGravity:
                skipMove = False
                if world[ypos+1][xpos]:
                    skipMove = True

                    option = random.randint(0,2) 
                    #print(xpos+1, maxlen-1)
                    if option == 0:
                        # stay
                        world[ypos+1][xpos]["source_loc"] = " "
                        world[ypos+1][xpos]["dest_loc"] = " "

                    elif option == 1 and xpos+1 <= maxlen-1 and not world[ypos+1][xpos+1]:  
                        # move to right down
                        world[ypos+1][xpos+1] = world[ypos][xpos]
                        world[ypos+1][xpos+1]["dest_loc"] = " "
                        world[ypos+1][xpos+1]["source_loc"] = "\\"
                        world[ypos+1][xpos+1]["y"] = ypos+1
                        world[ypos+1][xpos+1]["x"] = xpos+1
                        world[ypos][xpos] = None

                    elif option == 2  and xpos-1 >= 0 and not world[ypos+1][xpos-1]:
                        # move to left down
                        world[ypos+1][xpos-1] = world[ypos][xpos]
                        world[ypos+1][xpos-1]["dest_loc"] = "/"
                        world[ypos+1][xpos-1]["source_loc"] = " "
                        world[ypos+1][xpos-1]["y"] = ypos+1
                        world[ypos+1][xpos-1]["x"] = xpos-1
                        world[ypos][xpos] = None

                if not skipMove:

                    world[ypos+1][xpos] = world[ypos][xpos]
                    world[ypos+1][xpos]["y"] = ypos+1
                    world[ypos+1][xpos]["source_loc"] = " "
                    world[ypos+1][xpos]["dest_loc"] = " "

                    world[ypos][xpos] = None

            # every time we change a pixel something, we calculate the entire line again
            # 1 = bortover
            # 2 = oppover
            # lende = 4
            for xpos2 in range(len(world[ypos])): 
                # None
                if not world[ypos][xpos2]:
                    continue

        
                if 5 > world[ypos][xpos2]["flag"] > 0: 
                
                    # check xpos + 3
                    flag = world[ypos][xpos2]["flag"] 
                    #if xpos2+distance_check > maxlen-1:
                    if xpos2+distance_check > maxlen:
                        pass
                    else:
                        found = 0
                        for i in range(distance_check):
                            if not world[ypos][xpos2+i]:
                                break

                            if world[ypos][xpos2+i]["flag"] == flag:
                                #print("Same!!")
                                found += 1

                        if found == distance_check:
                            #print("ALL SAMe DeL PLS0: %d, %d, flag: %d" % ( ypos, xpos2, flag))
                            for i in range(distance_check):
                                deletes.append((ypos, xpos2+i, world[ypos][xpos2+i]["uuid"]))
                                world[ypos][xpos2+i] = None

                            #deletes.append((ypos, xpos2, world[ypos][xpos2]["uuid"]))
                            world[ypos][xpos2] = None

                            score += 5

                    # check ypos + 3
                    if ypos+distance_check > maxlen:
                        pass
                    else:
                        found = 0
                        #print(ypos+distance_check, xpos2)
                        for i in range(distance_check):
                            if not world[ypos+i][xpos2]:
                                break

                            if world[ypos+i][xpos2]["flag"] == flag:
                                #print("Same!!")
                                found += 1

                        if found == distance_check:
                            #print("ALL SAMe DeL PLS1: %d, %d, flag: %d" % ( ypos, xpos2, flag))
                            for i in range(distance_check):
                                deletes.append((ypos+i, xpos2, world[ypos+i][xpos2]["uuid"]))
                                world[ypos+i][xpos2] = None

                            #deletes.append((ypos, xpos2, world[ypos][xpos2]["uuid"]))

                            world[ypos][xpos2] = None
                            score += 5

                    # check ypos - 3
                    if ypos-distance_check <= 0:
                        pass
                    else:
                        found = 0
                        for i in range(distance_check):
                            if not world[ypos-i][xpos2]:
                                break

                            if world[ypos-i][xpos2]["flag"] == flag:
                                #print("Same!!")
                                found += 1

                        if found == distance_check:
                            #print("ALL SAMe DeL PLS2: %d, %d, flag: %d" % ( ypos, xpos2, flag))
                            for i in range(distance_check):
                                deletes.append((ypos-i, xpos2, world[ypos-i][xpos2]["uuid"]))
                                world[ypos-i][xpos2] = None

                            #deletes.append((ypos, xpos2, world[ypos][xpos2]["uuid"]))

                            world[ypos][xpos2] = None
                            score += 5

    return added

def gravity_swap():
    global world
    global gravity_swaps

    newworld = []
    for i in range(maxlen):
        janus = []
        for y in range(maxlen):
            janus.append(None)

        newworld.append(janus)

    #print("\n\nGRAVITYSWAPPP WOOOOOOOOOO: \n\n")
    swap = random.randint(0, 2)

    #swap = 1
    if swap == 0:
        #print("90 clockwise")

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

def stepper(maxlen):
    global world
    global should_add
    global score

    # Calculate where it should go instead
    #if should_add == False:
    added = gravitypls()
    maxadded = int(maxlen*maxlen*0.8)
    #print("Amount: %d/%d (%d), Score: %d, Gravity Swaps: %d, Iter: %d" % (added, maxadded, maxlen*maxlen, score, gravity_swaps, iterations))

    if added >= maxadded:
        gravity_swap()
        #exit()
        return None

    #should_add = False 
    ypos = 0
    xpos = random.randint(0, maxlen-1)

    new_object = {
        "uuid": str(uuid.uuid4()),
        "x": xpos,
        "y": ypos,
        "flag": random.randint(1, 2),
        "source_loc": " ",
        "dest_loc": " ",
    }

    world[ypos][xpos] = new_object
    return world 

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
