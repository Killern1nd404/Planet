import bpy
from first import gen
from bpy.props import IntProperty


class GeneratePlanet(bpy.types.Operator):
    bl_label = "Сгенерировать планету"
    bl_idname = "planet.generate"

    def execute(self, context):
        gen(bpy.context.scene.regions_number_coefficient_slider)
        return {'FINISHED'}


class GenerationPlanetMenu(bpy.types.Panel):
    bl_label = "Параметры планеты"
    bl_idname = "TOOL_PT_GENERATION_PLANET_MENU"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = ""

    def draw(self, context):
        self.layout.prop(context.scene, 'regions_number_coefficient_slider')
        self.layout.operator("planet.generate")


classes = (
    GeneratePlanet,
    GenerationPlanetMenu,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.regions_number_coefficient_slider = bpy.props.IntProperty(
        name='Коэффициент количества секторов',
        default=21,
        soft_min=12,
        soft_max=50
    )


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()