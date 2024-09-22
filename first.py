import random
import matplotlib.pyplot as plt
from math import *
#from scipy import spatial
#import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import SphericalVoronoi, geometric_slerp
from mpl_toolkits.mplot3d import proj3d
import os
import sys
import bpy


# Добавление пути директории проекта
dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)


from display_planet import initialize_scene



class Direction:


    def __init__(self, data):
        self._direction = None
        self._point = None
        if len(data) == 2: self.direction = data
        elif len(data) == 3: self.point = data
        else: raise

    def point_by_dir(self):
        theta = self._direction[0]
        phi = self._direction[1]
        self._point = [sin(theta) * cos(phi), sin(theta) * sin(phi), cos(theta)]

    def dir_by_point(self):
        x, y, z = self._point
        radius = sqrt(x * x + y * y + z * z)
        self.direction = [acos(z / radius), atan2(y, x)]

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, direction):
        theta = direction[0]
        phi = direction[1]
        theta %= pi
        phi %= (2*pi)
        self._direction = [theta, phi]
        self.point_by_dir()

    @property
    def point(self):
        return self._point

    @point.setter
    def point(self, point):
        self._point = point
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

class Map(SphericalVoronoi):

    def __int__(self, points, radius, center):
        super().__init__(points, radius, center)
        self.sort_vertices_of_regions()
        self.regions_as_obj = []

    def createRegions(self):

        for region in self.regions:
            pass

'''class Edge():

    def __init__(self, point1, point2):
        self._begin = point1
        self._end = point2

    @property
    def point1(self): return self._begin

    @point1.setter
    def point1(self, point):
        self._begin = point

    @property
    def point2(self): return self._end

    @point2.setter
    def point2(self, point): self._end = point

    def __eq__(self, other):
        return ((self.point1 == other.point1 and self.point2 == other.point2) or
                (self.point1 == other.point2 and self.point2 == other.point1))'''

class Region():

    def __init__(self, vertices):
        self.id = None
        self.vertices = vertices
        self.edges = []

angle = pi/3 # любое нечетное число.
theta = 0
phi = 0
first = Direction([0, 0])
set_of_point = set()
set_of_point.add(tuple(first.point))
while theta <= pi/2 - angle:
    theta += angle
    sin_t = sin(theta)
    while phi <= 2*pi:
        pair = [Direction([theta, phi]), Direction([pi-theta, phi])]
        for point in pair:
            if theta <= pi/2: set_of_point.add(tuple(point.point))
        phi += angle / sin_t
    phi = 0



points = np.array([list(point) for point in list(set_of_point)])
#for point in points:
 #   print(point)

radius = 1
center = np.array([0, 0, 0])
sv = SphericalVoronoi(points, radius, center) #объект типа диаграмма вороного

# sort vertices (optional, helpful for plotting)
sv.sort_vertices_of_regions()

for i in range(10):
    points = []
    for region in sv.regions:
        sum = np.array([0., 0., 0.])
        for j in region:
            sum += sv.vertices[j]
        point = Direction((sum/len(region)).tolist())
        points.append(point.point)
    sv = SphericalVoronoi(points, radius, center)
    sv.sort_vertices_of_regions()


t_vals = np.linspace(0, 1, 2000)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
# plot the unit sphere for reference (optional)
u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)
x = np.outer(np.cos(u), np.sin(v))
y = np.outer(np.sin(u), np.sin(v))
z = np.outer(np.ones(np.size(u)), np.cos(v))
ax.plot_surface(x, y, z, color='y', alpha=0.1)
# plot generator points
#ax.scatter(points[:, 0], points[:, 1], points[:, 2], c='b')
# plot Voronoi vertices
ax.scatter(sv.vertices[:, 0], sv.vertices[:, 1], sv.vertices[:, 2],
                   c='g')
# indicate Voronoi regions (as Euclidean polygons)
for region in sv.regions:

   n = len(region)
   for i in range(n):
       #print(region[i])
       start = sv.vertices[region][i]
       end = sv.vertices[region][(i + 1) % n]
       result = geometric_slerp(start, end, t_vals)
       ax.plot(result[..., 0],
               result[..., 1],
               result[..., 2],
               c='k')
   #print("\n")
ax.azim = 10
ax.elev = 40
_ = ax.set_xticks([])
_ = ax.set_yticks([])
_ = ax.set_zticks([])
fig.set_size_inches(4, 4)
plt.show()