import bpy
import os
from .functions.functions import *

class SST_OT_dump_settings(bpy.types.Operator):
    bl_idname = "settings.save"
    bl_label = "Save Settings"
    bl_description = "Save settings to a json file"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        if bpy.context.scene.settingsFilePath:
            outfile = bpy.context.scene.settingsFilePath
        else:
            outfile = os.path.join(bpy.path.abspath('//'), 'SceneSettings.json')
            bpy.context.scene.settingsFilePath = outfile
        saveSettings(outfile)

        return {"FINISHED"}

class SST_OT_load_settings(bpy.types.Operator):
    bl_idname = "settings.load"
    bl_label = "Load Settings"
    bl_description = "Load settings from json file (overwrite current settings)"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        if bpy.context.scene.settingsFilePath:
            outfile = bpy.context.scene.settingsFilePath
        else:
            outfile = os.path.join(bpy.path.abspath('//'), 'SceneSettings.json')

        if os.path.exists(outfile) and os.path.isfile(outfile):    
            applySettings(outfile)
        else:
            self.report({'ERROR'}, "no file to load")
            return {'CANCELLED'}

        return {"FINISHED"}

class SST_OT_diff_settings(bpy.types.Operator):
    bl_idname = "settings.diff"
    bl_label = "compare Settings"
    bl_description = "Print differences between saved and current settings"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        if bpy.context.scene.settingsFilePath:
            outfile = bpy.context.scene.settingsFilePath
        else:
            outfile = os.path.join(bpy.path.abspath('//'), 'SceneSettings.json')
        if os.path.exists(outfile) and os.path.isfile(outfile):
            compareSettings(outfile, stamping = bpy.types.Scene.settingsStamp)
        else:
            self.report({'ERROR'}, "no file to load")
            return {'CANCELLED'}
        return {"FINISHED"}

classes = (
    SST_OT_dump_settings,
    SST_OT_load_settings,
    SST_OT_diff_settings,
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    bpy.types.Scene.settingsFilePath = bpy.props.StringProperty(name = "Settings", description = "location for the settings save/load\n", subtype='FILE_PATH')#, default = '%s/SceneSettings.json'%(bpy.path.abspath('//')))
    bpy.types.Scene.settingsStamp = bpy.props.BoolProperty(name = "Stamp changes", description = "add differences between captured settings and current settings to Stamp note (usefull for comparing render)\n", default = False)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

    del bpy.types.Scene.settingsFilePath
    del bpy.types.Scene.settingsStamp