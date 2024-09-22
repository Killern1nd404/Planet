import bpy
import bmesh
#from math import pi, cos, sin

"""
# Объявление файла как модуля для открытия в Blender
my_module = bpy.data.texts["my_module"].as_module()
"""


def clear_scene():
    # Выделение всех объектов на сцене
    bpy.ops.object.select_all(action='SELECT')
    # Удаление выделенных объектов
    bpy.ops.object.delete(use_global=False, confirm=False)


"""
def move_vertex():
    bpy.data.objects["Basic_Sphere.002"].data.vertices[0].co.x += 0.02
    bpy.data.objects["Basic_Sphere.002"].data.vertices[0].co.y -= 0.02
    bpy.data.objects["Basic_Sphere.002"].data.vertices[0].co.z += 0.03


def create_sphere():
    # Create an empty mesh and the object.
    mesh = bpy.data.meshes.new('Basic_Sphere')
    basic_sphere = bpy.data.objects.new("Basic_Sphere", mesh)

    # Add the object into the scene.
    bpy.context.collection.objects.link(basic_sphere)

    # Select the newly created object
    bpy.context.view_layer.objects.active = basic_sphere
    basic_sphere.select_set(True)

    # Construct the bmesh sphere and assign it to the blender mesh.
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, radius=1)
    bm.to_mesh(mesh)
    bm.free()
"""


def make_object_by_points(vertexes):
    # Инициация объекта
    mesh = bpy.data.meshes.new("Planet")
    object_ = bpy.data.objects.new("Planet", mesh)
    # Добавление объекта в коллекцию
    collection = bpy.data.collections["Collection"]
    collection.objects.link(object_)
    # Объявление объекта активным
    bpy.context.view_layer.objects.active = object_

    # Рёбра и грани
    edges = []
    faces = []

    # Добавление объекта на сцену
    mesh.from_pydata(vertexes, edges, faces)
    

"""
def make_object_by_points():
    mesh = bpy.data.meshes.new("myBeautifulMesh")  # add the new mesh
    obj = bpy.data.objects.new(mesh.name, mesh)
    col = bpy.data.collections["Collection"]
    col.objects.link(obj)
    bpy.context.view_layer.objects.active = obj

    vertexes = [[0.5,  1.0,  0.0], (1.0, -1.0,  0.0), (-1.0, -1.0,  0.0), (-1.0,  1.0,  0.0), (1, 2, 3)]

    verts = [( 1.0,  1.0,  0.0),
             ( 1.0, -1.0,  0.0),
             (-1.0, -1.0,  0.0),
             (-1.0,  1.0,  0.0)
             ]  # 4 verts made with XYZ coords
    edges = []
    faces = [[0, 1, 2, 3], [0, 1, 4], [0, 3, 4], [2, 3, 4], [1, 2, 4]]

    mesh.from_pydata(vertexes, edges, faces)
"""


def initialize_scene(vertexes):
    clear_scene()
    make_object_by_points(vertexes)


#vertexes_ = [[0.5, 1.0, 0.0], (1.0, -1.0, 0.0), (-1.0, -1.0, 0.0), (-1.0, 1.0, 0.0), (1, 2, 3)]
#initialize_scene(vertexes_)


"""mesh = bpy.data.meshes.new('Basic_Sphere')
basic_sphere = bpy.data.objects.new("Basic_Sphere", mesh)
# Add the object into the scene.
bpy.context.collection.objects.link(basic_sphere)
# Select the newly created object
bpy.context.view_layer.objects.active = basic_sphere
basic_sphere.select_set(True)
# Construct the bmesh sphere and assign it to the blender mesh.
bm = bmesh.new()
bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, diameter=1)
bm.to_mesh(mesh)
bm.free()
bpy.ops.object.modifier_add(type='SUBSURF')
bpy.ops.object.shade_smooth()"""


"""# create curve
bpy.ops.curve.primitive_nurbs_path_add(radius=1, enter_editmode=False)
obj = bpy.context.object

#bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
#bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
#bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
#bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))

try:
    objs = bpy.data.objects
    objs.remove(objs["Куб"], do_unlink=True)
except:
    pass"""


# bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
# bpy.data.objects["Куб"].data.vertices[0].co.x += 1.0
"""Obj = bpy.context.active_object
mod = Obj.modifiers.new("Bevel", 'BEVEL')
mod.segments = 3
bpy.ops.object.shade_smooth()
mod1 = Obj.modifiers.new("Array", 'ARRAY')
mod1.count=20
mod2 = Obj.modifiers.new("Array", 'ARRAY')
mod2.relative_offset_displace[0]=0
mod2.relative_offset_displace[1]=1
mod2.count=20
bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Array.001")
bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Array")
bpy.ops.object.editmode_toggle()
bpy.ops.mesh.separate(type="LOOSE")
bpy.ops.object.editmode_toggle()
bpy.ops.object.randomize_transform(loc=(0, 0, 1))"""