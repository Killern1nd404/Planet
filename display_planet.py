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


def initialize_scene(map_data):
    # Извлечение массивов вершин и граней
    vertexes = map_data.vertices
    faces = []
    for region in map_data.regions:
        faces.append(region)
    # Очистка сцены
    clear_scene()
    # Создание объектов
    make_object(vertexes, faces)
    # Покраска секторов
    paint_regions(faces)


# bpy.data.objects["Куб"].data.vertices[0].co.x += 1.0
