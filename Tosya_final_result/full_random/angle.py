import random
import matplotlib.pyplot
import numpy as np
import smuthi.simulation
import smuthi.initial_field
import smuthi.layers
import smuthi.particles
import smuthi.postprocessing.far_field as ff

instructions = open("instructions.txt", "r")

instructions_lines = instructions.readlines()

min_radius = float(input())

spheres = []

def full_random(num_of_spheres):
    global mid_radius

    spheres.append([0., 0., 0.])

    n = num_of_spheres

    while n > 0:
        i = True
        radius = mid_radius + mid_radius * 0.05 * (1 - 2 * random.random())
        x_coord, y_coord = (radius + random.random() * (r_screen_width - 2 * radius),
                            radius + random.random() * (r_screen_height - 2 * radius))
        for sphere in spheres:
            if (sphere[0] - x_coord) ** 2 + (sphere[1] - y_coord) ** 2 < (radius + sphere[2] + 0.2) ** 2:
                i = False
                break
        if i:
            spheres.append([x_coord, y_coord, radius])
            n -= 1

    spheres.remove([0., 0., 0.])

full_random(int(input()))