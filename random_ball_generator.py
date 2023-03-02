#!/usr/bin/env python

import rhino3dm as rs
from random import random
import sys
from scipy import ndimage
import numpy as np
import matplotlib.pyplot as plt

space_size = 500.0
# com_z_offset is the distance below the centre point that the COM should be
com_z_offset = 100.0
# number of balls to create
ball_count = 5

class Ball:
    def __init__(self, mass, location):
        self.mass = mass
        self.location = location

def get_random_ball():
    # we're a bit particular about z because we can't make balls in the
    # centre easily
    return Ball(104.0, rs.Point3d(random() * space_size, random() * space_size, random() * space_size))

def centre_of_mass(balls):
    total_mass = 0
    total_x = 0
    total_y = 0
    total_z = 0
    for ball in balls:
        print("ball mass: " + str(ball.mass))
        print("ball location X: " + str(ball.location.X))
        print("ball location Y: " + str(ball.location.Y))
        print("ball location Z: " + str(ball.location.Z))
        total_mass += ball.mass
        total_x += ball.mass * ball.location.X
        total_y += ball.mass * ball.location.Y
        total_z += ball.mass * ball.location.Z
    print("total mass: " + str(total_mass))
    return rs.Point3d(total_x / total_mass, total_y / total_mass, total_z / total_mass)

centre_point = rs.Point3d(250, 250, 250)

balls = []

for i in range(0, ball_count):
    balls.append(get_random_ball())

com = centre_of_mass(balls)
print("Centre of mass: %s" % com)

iterations = 0
neededVector = rs.Line(com, centre_point)
print("Need this vector to correct COM: %s" % neededVector.Direction)
print("Looping...")
while abs(neededVector.Direction.X) > 0.1 or abs(neededVector.Direction.Y) > 0.1:
    iterations += 1
    for i, ball in enumerate(balls):
        balls[i].location.X += neededVector.Direction.X
        balls[i].location.Y += neededVector.Direction.Y
        com = centre_of_mass(balls)
        print("Centre of mass: %s" % com)

        neededVector = rs.Line(com, centre_point)
        print("Need this vector to correct COM: %s" % neededVector.Direction)

print("Iterations: %d" % iterations)

if com.Z > centre_point.Z:
    print("Correcting for Z to be %d below the centre point" % com_z_offset)
    for i, ball in enumerate(balls):
        z_move = com.Z - centre_point.Z - com_z_offset
        balls[i].location.Z -= z_move
    print("Moved balls down by %f" % (z_move))


balls.append(Ball(104.0, centre_point))

plt.rcParams["figure.figsize"] = [7.00, 3.50]
plt.rcParams["figure.autolayout"] = True
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
z = [ i.location.Z for i in balls ]
x = [ i.location.X for i in balls ]
y = [ i.location.Y for i in balls ]
ax.scatter(x, y, z, c=z, alpha=1)
#ax.stem(x,y,z)
plt.show()