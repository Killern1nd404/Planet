import random
import matplotlib.pyplot as plt
from math import *
#import math

####

class Direction:

    def point_by_dir(self):
        theta, phi = self.direction
        self.point = (sin(theta) * cos(phi), sin(theta) * sin(phi), cos(theta))

    def dir_by_point(self):
        self.direction = (acos(self.point[2]),
                          atan2(self.point[1],
                                self.point[0]))

    def __init__(self, direc):
        self.direction = direc
        self.point = None
        self.point_by_dir()

    def set_dir(self, direc):
        self.diretion = direc
        self.point_by_direction()

    def set_point(self, point):
        self.point = point
        self.dir_by_point()

class Relations:

    def scalar_(self):
        x1, y1, z1 = self.dir_1.point
        x2, y2, z2 = self.dir_2.point
        self.scalar = x1*x2 + y1*y2 + z1*z2

    def distance(self):
        return acos(self.scalar)

    def __init__(self, dir_1, dir_2):
        self.dir_1 = dir_1
        self.dir_2 = dir_2
        self.scalar = None
        self.scalar_()

    
        
    
        
