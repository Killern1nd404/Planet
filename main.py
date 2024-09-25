import bpy
from map import Map
from bpy.props import IntProperty
from display_planet import initialize_scene


class GeneratePlanet(bpy.types.Operator):
    bl_label = "Сгенерировать планету"
    bl_idname = "planet.generate"

    def execute(self, context):
        initialize_scene(Map(bpy.context.scene.regions_number_coefficient_slider,
                             bpy.context.scene.lloyd_relaxation_passes_number))
        return {'FINISHED'}


class GenerationPlanetMenu(bpy.types.Panel):
    bl_label = "Параметры планеты"
    bl_idname = "TOOL_PT_GENERATION_PLANET_MENU"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = ""

    def draw(self, context):
        self.layout.prop(context.scene, 'regions_number_coefficient_slider')
        self.layout.prop(context.scene, 'lloyd_relaxation_passes_number')
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
        default=41,
        soft_min=10,
        soft_max=199,
        min=10,
        max=199
    )

    bpy.types.Scene.lloyd_relaxation_passes_number = bpy.props.IntProperty(
        name='Кол-во проходов релаксации Ллойда',
        default=10,
        soft_min=0,
        soft_max=100,
        min=0,
        max=100
    )


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()