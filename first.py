import random
import matplotlib.pyplot as plt
from math import *
#from scipy import spatial
#import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import SphericalVoronoi, geometric_slerp
from mpl_toolkits.mplot3d import proj3d



class Direction:


    def __init__(self, direction):
        self._direction = direction
        self._point = None
        self.point_by_dir()

    def point_by_dir(self):
        theta = self._direction[0]
        phi = self._direction[1]
        self._point = [sin(theta) * cos(phi), sin(theta) * sin(phi), cos(theta)]

    def dir_by_point(self):
        self.direction = [acos(self.point[2]),
                          atan2(self.point[1],
                                self.point[0])]

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, direction):
        theta = direction[0]
        phi = direction[1]
        theta %= pi
        phi %= (2*pi)
        print((theta, phi))
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

vertices = list()
for vertice in sv.vertices:
    vertices.append(vertice.tolist())



#print(sv.regions)



"""t_vals = np.linspace(0, 1, 2000)
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
ax.scatter(points[:, 0], points[:, 1], points[:, 2], c='b')
# plot Voronoi vertices
ax.scatter(sv.vertices[:, 0], sv.vertices[:, 1], sv.vertices[:, 2],
                   c='g')
# indicate Voronoi regions (as Euclidean polygons)
for region in sv.regions:

   n = len(region)
   for i in range(n):
       print(region[i])
       start = sv.vertices[region][i]
       end = sv.vertices[region][(i + 1) % n]
       result = geometric_slerp(start, end, t_vals)
       ax.plot(result[..., 0],
               result[..., 1],
               result[..., 2],
               c='k')
   print("\n")
ax.azim = 10
ax.elev = 40
_ = ax.set_xticks([])
_ = ax.set_yticks([])
_ = ax.set_zticks([])
fig.set_size_inches(4, 4)
plt.show()"""