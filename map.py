from math import pi, sqrt, acos, atan2, sin, cos
import numpy as np
from scipy.spatial import SphericalVoronoi, geometric_slerp
import random
from copy import *

#from test_console import region

#00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000

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

#00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000

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

#00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000

class Area:

    id = 0

    def __init__(self, map, center_id=None, regions_id=None):
        self.map = map
        self.id = Area.id
        Area.id += 1
        self.regions_id = []
        #self.neighbors_area = set()
        self.perimeter = {"external": set(), "internal": set()}
        if center_id==None and regions_id==None: pass
        else:
            self.sub_init(center_id, regions_id)
        self.condition = 0


    def sub_init(self, center_id=None, regions_id=None):
        #if center_id == None and regions_id == None: raise
        if not self.regions_id: self.regions_id = self.regions_id + regions_id if regions_id is not None else [center_id,]
        for region in self.regions_id:
            self.map.regions_as_obj[region].area = self.id
        self.update_perimeter()

    def update_perimeter(self):
        set_reg = set(self.regions_id)
        in_area = set()
        not_in_area = set()
        for reg in set_reg:
            neighbors = self.map.regions_as_obj[reg].neighbors
            if neighbors.issubset(set_reg): in_area.add(reg)
            not_in_area = not_in_area.union(neighbors - set_reg)
        self.perimeter["internal"] = set_reg - in_area
        free_external_reg = not_in_area & self.map.free_regions
        self.perimeter["external"] = free_external_reg
        if not free_external_reg: self.condition = 1

    def capture_external_perimeter(self, percent=1):   #percent float{0, ... , 1}
        print(f"enter in capture_external_perimeter in area {self.id}, state {self.condition}")
        if not self.condition:
            print(self.perimeter["external"])
            new_regions = set()
            counter = int(len(self.perimeter["external"]) * percent) + 1
            print(counter)
            for reg in self.perimeter["external"]:
                if counter <= 0: break
                region = self.map.regions_as_obj[reg]
                if reg in self.map.free_regions:
                    region.area = self.id
                    new_regions.add(reg)
                    self.map.free_regions.remove(reg)
                counter -= 1
            self.regions_id += list(new_regions)
            print(self.regions_id)
            self.update_perimeter()

#00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000

class LithosphericPlate(Area):

    id_lp = 0

    def __init__(self, map, type, center_id, limit_c_c=0.5):
        #TYPE = 1: Континетальная
        #TYPE = 0: Океаническая
        self.map = map
        self.limit_c_c = [type, limit_c_c]
        self.type = type
        self.id_lp = LithosphericPlate.id_lp
        LithosphericPlate.id_lp += 1
        self.epoch = 0
        self.areas = [Area(map, center_id=center_id), Area(map)]
        self.regions_id = [center_id,]
        self.condition = 0

    def next_epoch(self):
        if self.type and self.limit_c_c[0] < self.limit_c_c[1]:
            self.create_continental_crust()
        else:
            if not self.areas[1].regions_id: self.areas[1].sub_init(regions_id=list(self.areas[0].perimeter["external"]))
            else: self.create_continental_crust()
        if self.areas[0].condition and self.areas[1].condition:
            self.init_as_area()
        self.epoch += 1
        print(f"epoch {self.epoch} for plate {self.id_lp} completed")

    def get_regions(self, condition=1):
        if condition == 1:
            return self.regions_id
        else:
            regions = self.areas[0].regions_id + self.areas[1].regions_id
            return regions

    def init_as_area(self): #в планах инит в конце
        super().__init__(map=self.map, regions_id=self.get_regions(0))
        print(f"________________________AREA {self.id_lp} INIT______________________________")
        self.update_perimeter()

    def create_continental_crust(self):
        print(f"create_continental_crust")
        self.areas[0].capture_external_perimeter(1 if self.epoch % 2 == 0 else np.random.normal(0.6, 0.25))

    def create_ocean_crust(self):
        print(f"create_ocean_crust")
        self.areas[1].capture_external_perimeter(1 if self.epoch % 3 == 0 else np.random.normal(0.6, 0.25))

#00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000

class Map(SphericalVoronoi):

    def __init__(self, angle, epochs, radius=1, center=np.array([0, 0, 0]), random_points=50):
        self.points1 = []
        self.random_points = random_points
        self.generate_points(angle)
        self.generate(self.points1, radius, center)
        self.lloyds_relaxation(epochs)
        self.regions_as_obj = []
        self.free_regions = {i for i in range(len(self.regions))}
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
        for i in range(angle_c*self.random_points):
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

    """def create_areas(self, num_of_centers, seed = None, type_areas="T"):
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

        self.areas.extend(areas)"""

    def create_lit_plates(self, quantity=10):
        conditions_areas = []
        for i in range(quantity):
            center = random.choice(list(self.free_regions))
            self.free_regions.remove(center)
            self.areas.append(
                LithosphericPlate(
                    self,
                    type=1 if i < quantity - quantity//10 else 0,
                    center_id=center,
                    limit_c_c=np.random.normal(0.5, 0.15)
                )
            )
            conditions_areas.append(0)
        o = 0
        while True:
            o += 1
            for plate in self.areas:
                if plate.condition:
                    conditions_areas[self.areas.index(plate)] = 1
                    continue
                plate.next_epoch()
            for state in conditions_areas:
                if not state: break
            else: break
            if len(self.free_regions) == 0:
                for plate in self.areas:
                    plate.init_as_area()
                break
            if o == 1000: break
            print(len(self.free_regions))
