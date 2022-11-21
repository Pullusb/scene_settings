import bpy
import os
from .functions.functions import *

class SST_OT_apply_multi_scene(bpy.types.Operator):
    bl_idname = "settings.apply_multi_scene"
    bl_label = "Apply Settings Multi Scene"
    bl_description = "Apply settings of current scene or loaded file\
        \non selected scenes (popup ops)"
    bl_options = {"REGISTER"}

    use_current_scene : bpy.props.BoolProperty(
        name='Use active scene settings',
        description='Replicate current scene settings instead of loading from file',
        default=True)

    @classmethod
    def poll(cls, context):
        return True

    def invoke(self, context, event):
        # Clear and populate select list
        scenes_prop = context.window_manager.scene_select_list
        scenes_prop.clear()
        for s in bpy.data.scenes:
            # if s == context.scene:
            #     continue

            item = scenes_prop.add()
            item.s_name = s.name

            # if s == context.scene:
            #     item.select = False
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout=self.layout
        layout.use_property_split = True
        layout.prop(self, 'use_current_scene')
        if self.use_current_scene:
            layout.label(text=f'Source: {context.scene.name}', icon='INFO')
        else:
            layout.label(text=f'Load settings from file', icon='INFO')

        col=layout.column()
        for item in context.window_manager.scene_select_list:
            row = col.row()
            row.prop(item, 'select', text='')
            row.label(text=item.s_name)
            if self.use_current_scene and item.s_name == context.scene.name:
                row.active=False

    def execute(self, context):
        if self.use_current_scene:
            print('\n\n\nfrom scene')
            saved_datapath = [
                'bpy.context.scene',
                'bpy.context.scene.render',
                'bpy.context.scene.cycles',
                'bpy.context.scene.eevee']

            settings = {}
            for zone in saved_datapath:
                settings[zone] = saveAll(Root=zone)
        
        else:
            if bpy.context.scene.settingsFilePath:
                outfile = bpy.context.scene.settingsFilePath
            else:
                outfile = os.path.join(bpy.path.abspath('//'), 'SceneSettings.json')

            if os.path.exists(outfile) and os.path.isfile(outfile):    
                with open(outfile, "r") as fd:
                    settings = json.loads(fd.read())
            
            else:
                self.report({'ERROR'}, "No file to load")
                return {'CANCELLED'}

        for item in context.window_manager.scene_select_list:
            if self.use_current_scene and item.s_name == context.scene.name:
                # skip active scene (it's the reference)
                continue
            if item.select:
                target_scene = bpy.data.scenes.get(item.s_name)
                print('target_scene: ', target_scene)
                apply_from_dict(settings, scene=target_scene)

        return {"FINISHED"}

#--- PROPERTIES

class SST_PG_scene_list_prop(bpy.types.PropertyGroup):
    s_name : bpy.props.StringProperty()
    select : bpy.props.BoolProperty(default=True)

classes = (
    SST_PG_scene_list_prop,
    SST_OT_apply_multi_scene,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    # bpy.types.WindowManager.scene_select_list = bpy.props.PointerProperty(type=SST_PG_scene_list_prop)
    bpy.types.WindowManager.scene_select_list = bpy.props.CollectionProperty(type=SST_PG_scene_list_prop)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.WindowManager.scene_select_list