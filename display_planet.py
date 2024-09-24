import bpy
import bmesh
import random

biomes_colors = {"Water": [0, (0, 0, 1, 1)],
                 "Land": [1, (0.09, 0.4, 0.05, 1)]}


def clear_scene():
    # Переключение режима
    if bpy.context.scene.objects:
        if bpy.context.object.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
    # Выделение всех объектов на сцене
    bpy.ops.object.select_all(action='SELECT')
    # Удаление выделенных объектов
    bpy.ops.object.delete(use_global=False, confirm=False)
    # Удаление всех материалов
    for material in bpy.data.materials:
        material.user_clear()
        bpy.data.materials.remove(material)
    # Удаление всех мэшей
    for mesh in bpy.data.meshes:
        mesh.user_clear()
        bpy.data.meshes.remove(mesh)


def make_object(vertexes, faces):
    # Инициация объекта
    mesh = bpy.data.meshes.new("Planet")
    object_ = bpy.data.objects.new("Planet", mesh)
    # Добавление объекта в коллекцию
    collection = bpy.data.collections["Collection"]
    collection.objects.link(object_)
    # Объявление объекта активным
    bpy.context.view_layer.objects.active = object_

    # Рёбра
    edges = []

    # Добавление объекта на сцену
    mesh.from_pydata(vertexes, edges, faces)


def create_material(mat_name, diffuse_color=(1, 1, 1, 1)):
    mat = bpy.data.materials.new(name=mat_name)
    mat.diffuse_color = diffuse_color
    return mat


def paint_regions(faces):
    # Создание массива материалов
    materials = []
    for key, attributes in biomes_colors.items():
        materials.append(create_material(key, attributes[1]))

    # Переменная объекта
    #obj = bpy.context.object
    obj = bpy.data.objects[0]

    # ТЕСТОВЫЙ НАБОР ДАННЫХ!!!!!!!!!!!
    # В БУДУЩЕМ УДАЛИТЬ!!!!!!!!!!!!!!!
    dataaaaaa = []
    for _ in range(len(faces)):
        dataaaaaa.append(random.choice(["Water", "Land"]))

    # Добавление материалов к объекту
    for material in materials:
        obj.data.materials.append(material)

    # Присваивание секторам цвет их биома
    for i in range(len(dataaaaaa)):
        obj.data.polygons[i].material_index = biomes_colors[dataaaaaa[i]][0]


def initialize_scene(sphere_data):
    # Создание массивов вершин и граней
    vertexes = sphere_data.vertices
    faces = sphere_data.regions
    # Очистка сцены
    clear_scene()
    # Создание объектов
    make_object(vertexes, faces)
    # Покраска секторов
    paint_regions(faces)


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