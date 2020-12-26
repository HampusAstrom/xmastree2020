import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

def point_dist(a, b):
    return np.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2)

def in_tree(point, top, bot, rad):
    z = point[2]
    dist_to_center = np.sqrt(point[0]**2 + point[1]**2)
    return dist_to_center < (top - z) * rad/(top - bot) and z >= bot

def visualize_without_board(pixels, coords, xmin, xmax, ymin, ymax, zmin, zmax):
    #temporary to show me what i am doing without haing a board

    # use same scaling for all dimensions
    mn = min([xmin, ymin, zmin])
    mx = max([xmax, ymax, zmax])
    ax.set_xlim3d(mn, mx)
    ax.set_ylim3d(mn, mx)
    ax.set_zlim3d(mn, mx)

    pixels_rgb = pixels[:, [1, 0, 2]]
    x, y, z = np.array([(x, y, z) for (x, y, z) in coords]).T
    ax.scatter(xs=x, ys=y, zs=z, c=pixels_rgb/255)
    #ax.plot([-237, 0, 237], [0, 0, 0], zs=[-430, 430, -430])
    #ax.plot([0, 0, 0], [-237, 0, 237], zs=[-430, 430, -430])
    plt.pause(0.05)
    plt.show(block=False)

def xmaslight():
    # This is the code from my

    #NOTE THE LEDS ARE GRB COLOUR (NOT RGB)

    # Here are the libraries I am currently using:
    import time
    import board
    #import neopixel #UNCOMMENT
    import re
    import math

    # You are welcome to add any of these:
    # import random as rnd
    import numpy as np
    # import scipy
    # import sys

    # If you want to have user changable values, they need to be entered from the command line
    # so import sys sys and use sys.argv[0] etc
    # some_value = int(sys.argv[0])

    # IMPORT THE COORDINATES (please don't break this bit)

    #coordfilename = "Python/coords.txt" #UNCOMMENT
    coordfilename = "./coords.txt" #COMMENT


    fin = open(coordfilename,'r')
    coords_raw = fin.readlines()

    coords_bits = [i.split(",") for i in coords_raw]

    coords = []

    for slab in coords_bits:
        new_coord = []
        for i in slab:
            new_coord.append(int(re.sub(r'[^-\d]','', i)))
        coords.append(new_coord)

    #set up the pixels (AKA 'LEDs')
    PIXEL_COUNT = len(coords) # this should be 500

    #pixels = neopixel.NeoPixel(board.D18, PIXEL_COUNT, auto_write=False) #UNCOMMENT
    pixels = np.zeros((PIXEL_COUNT,3), dtype=np.uint8) #COMMENT


    # YOU CAN EDIT FROM HERE DOWN

    x, y, z = np.array([(x, y, z) for (x, y, z) in coords]).T

    xmin = min(x)
    xmax = max(x)
    ymin = min(y)
    ymax = max(y)
    zmin = min(z)
    zmax = max(z)

    # VARIOUS SETTINGS

    # number of fairies in the tree, max 6 for now
    num_fairies = 3

    # pause between cycles (normally zero as it is already quite slow)
    slow = 0

    # buffer factor to keep the fey within the tree, as they whimper out outside :P
    buffer_factor = 1.0

    # how quickly the fairies change their momentum in 3d
    momentum_shift_multiplier = 10.0

    # fairy glow size, currently diminishing linearly
    glow_size = 200

    # INITIALISE SOME VALUES

    # calculate approximate cone for the tree to make sure the fairies stay within the tree
    # cone is set to be slightly smaller than the tree using buffer factor
    diam = min([xmax - xmin, ymax - ymin]) * buffer_factor
    rad = diam/2
    height = (zmax - zmin) * buffer_factor
    top = height/2
    bot = -height/2

    fey_colours = [[0, 100, 100], [100, 0, 100], [100, 100, 0], [150, 25, 25], [25, 150, 25], [25, 25, 150]]

    fairies = []

    # initialize fairies
    for i in range(num_fairies):
        fairies.append({'colour': fey_colours[i], 'position': [0, 0, 0], 'momentum': [0, 0, 0]})

    while(True):
        time.sleep(slow)

        # constrained brownian motion with momentum
        for f in fairies:
            f['momentum'] += (np.random.random(3) * 2 - 1) * momentum_shift_multiplier
            if in_tree(f['position'] + f['momentum'], top, bot, rad):
                f['position'] += f['momentum']
            elif in_tree(f['position'] - f['momentum'], top, bot, rad):
                f['momentum'] = - f['momentum']
                f['position'] += f['momentum']
            else:
                f['momentum'] = [0, 0, 0]

        # update pixels based on fey gaussians?
        for i in range(PIXEL_COUNT):
            if in_tree(coords[i], top, bot, rad):
                colour = np.array([0, 0, 0])
                for f in fairies:
                    dist = point_dist(coords[i], f['position'])
                    np.add(colour, np.multiply(max(1 - dist/glow_size, 0), f['colour']), out=colour, casting="unsafe")

                colour = np.minimum(colour, [255, 255, 255])
                pixels[i] = colour.astype(int)

        visualize_without_board(pixels, coords, xmin, xmax, ymin, ymax, zmin, zmax)





    #####################################################################
    # leaving old code down here if I need to test anything on it for now

    # I get a list of the heights which is not overly useful here other than to set the max and min altitudes
    heights = []
    for i in coords:
        heights.append(i[2])

    min_alt = min(heights)
    max_alt = max(heights)

    # VARIOUS SETTINGS

    # how much the rotation points moves each time
    dinc = 1

    # a buffer so it does not hit to extreme top or bottom of the tree
    buffer = 200

    # pause between cycles (normally zero as it is already quite slow)
    slow = 0

    # startin angle (in radians)
    angle = 0

    # how much the angle changes per cycle
    inc = 0.1

    # the two colours in GRB order
    # if you are turning a lot of them on at once, keep their brightness down please
    colourA = [0,50,50] # purple
    colourB = [50,50,0] # yellow


    # INITIALISE SOME VALUES

    swap01 = 0
    swap02 = 0

    # direct it move in
    direction = -1

    # the starting point on the vertical axis
    c = 100

    # yes, I just run which run is true
    run = 1
    while run == 1:

        time.sleep(slow)

        LED = 0
        while LED < len(coords):
            if math.tan(angle)*coords[LED][1] <= coords[LED][2]+c:
                pixels[LED] = colourA
            else:
                pixels[LED] = colourB
            LED += 1

        # use the show() option as rarely as possible as it takes ages
        # do not use show() each time you change a LED but rather wait until you have changed them all
        #pixels.show() #UNCOMMENT
        visualize_without_board(pixels, coords, xmin, xmax, ymin, ymax, zmin, zmax)

        # now we get ready for the next cycle

        angle += inc
        if angle > 2*math.pi:
            angle -= 2*math.pi
            swap01 = 0
            swap02 = 0

        # this is all to keep track of which colour is 'on top'

        if angle >= 0.5*math.pi:
            if swap01 == 0:
                colour_hold = [i for i in colourA]
                colourA =[i for i in colourB]
                colourB = [i for i in colour_hold]
                swap01 = 1

        if angle >= 1.5*math.pi:
            if swap02 == 0:
                colour_hold = [i for i in colourA]
                colourA =[i for i in colourB]
                colourB = [i for i in colour_hold]
                swap02 = 1

        # and we move the rotation point
        c += direction*dinc

        if c <= min_alt+buffer:
            direction = 1
        if c >= max_alt-buffer:
            direction = -1

    return 'DONE'


# yes, I just put this at the bottom so it auto runs
xmaslight()
