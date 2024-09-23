from bpy.props import (StringProperty, BoolProperty, IntProperty, FloatProperty)
import bpy


my_bool: BoolProperty(
    name="Enable or Disable",
    description="Bool property",
    default = False
    )

class HelloWorldPanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_hello_world"
    bl_label = "Hello World"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw(self, context):
        self.layout.label(text="Hello World")


class MyCustomMenu(bpy.types.Panel):
    bl_label = "Simple Custom Menu"
    bl_idname = "OBJECT_PT_hello_world"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw(self, context):
        layout = self.layout

        layout.operator("wm.open_mainfile")
        layout.operator("wm.save_as_mainfile")


def start():
    bpy.utils.register_class(MyCustomMenu)