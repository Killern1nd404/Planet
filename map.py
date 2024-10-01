from math import pi, sqrt, acos, atan2, sin, cos
import numpy as np
from scipy.spatial import SphericalVoronoi, geometric_slerp
import random

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


class Region:

    def __init__(self, id, edges, face):
        self.id = id
        self.face = face
        self.edges = edges
        self.neighbors = set()
        self.area = None

    def add_neighbor(self, neighbor):
        self.neighbors.add(neighbor.id)
        neighbor.neighbors.add(self.id)

    def __and__(self, other):
        return self.edges & other.edges


class Map(SphericalVoronoi):

    def __init__(self, angle, epochs, radius=1, center=np.array([0, 0, 0])):
        self.points1 = []
        self.generate_points(angle)
        self.generate(self.points1, radius, center)
        self.lloyds_relaxation(epochs)
        self.regions_as_obj = []
        self.create_regions()
        self.areas = list()

    def generate(self, points, radius, center):
        super().__init__(points, radius, center)
        self.sort_vertices_of_regions()

    def create_regions(self):
        counter_reg = 0
        for region in self.regions:
            self.regions_as_obj.append(Region
                                       (counter_reg,
                                        {
                                            frozenset([region[i-1], region[i]]) #frozenset из индексов вершин
                                            for i in range(len(region))
                                        },
                                        region
                                        )
                                       )
            counter_reg += 1
        for id in range(len(self.regions_as_obj)):
            for i in range(id+1, len(self.regions_as_obj)):
                if self.regions_as_obj[id] & self.regions_as_obj[i]:
                    self.regions_as_obj[id].add_neighbor(self.regions_as_obj[i])

    def generate_points(self, angle_c):
        angle_c = angle_c - 1 if angle_c % 2 == 0 else angle_c
        angle = pi / angle_c  # любое нечетное число.
        theta = 0
        phi = 0
        first = Direction([0, 0])
        set_of_point = set()
        set_of_point.add(tuple(first.point))
        while theta <= pi / 2 - angle:
            theta += angle
            sin_t = sin(theta)
            while phi <= 2 * pi:
                pair = [Direction([theta, phi]), Direction([pi - theta, phi])]
                for point in pair:
                    if theta <= pi / 2: set_of_point.add(tuple(point.point))
                phi += angle / sin_t
            phi = 0
        for i in range(angle_c*50):
            a = Direction([np.random.normal(pi/2, 0.55), random.uniform(0, pi*2)])
            set_of_point.add(tuple(a.point))

        self.points1 = np.array([point for point in set_of_point])

    def lloyds_relaxation(self, epochs, center=np.array([0, 0, 0]), radius=1):
        for i in range(epochs):
            points = []
            for region in self.regions:
                sum = np.array([0., 0., 0.])
                for j in region:
                    sum += self.vertices[j]
                point = Direction((sum / len(region)).tolist())
                points.append(point.point)
            self.generate(points, radius, center)

    def create_areas(self, num_of_centers, seed = None, type_areas="T"):
        seed = seed if seed else random.random()
        random.seed(seed)
        set_of_free_region = {id for id in range(len(self.regions_as_obj))}
        centers = []
        for i in range(num_of_centers):
            a = random.choice(list(set_of_free_region))
            centers.append(a)
            set_of_free_region.remove(a)
        areas = [[center,] for center in centers]
        counter_neighbours = [[1 for center in centers], [1 for center in centers]]

        while True:
            counter_neighbours = [counter_neighbours[1], [0 for center in centers]]

            for i in range(num_of_centers):
                counter = 0

                for k in range(counter_neighbours[0][i]):
                    region = self.regions_as_obj[areas[i][-k-1-counter]]
                    new_regions = region.neighbors & set_of_free_region

                    for nr in new_regions:
                        self.regions_as_obj[nr].area = i

                    set_of_free_region = set_of_free_region - new_regions
                    areas[i].extend(new_regions)
                    counter += len(new_regions)
                    if set_of_free_region == set(): break
                counter_neighbours[1][i] += counter
                if set_of_free_region == set(): break
            if set_of_free_region == set(): break

        self.areas.extend(areas)




