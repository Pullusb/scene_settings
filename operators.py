import bpy
import os
from .functions.functions import *

class dumpSettings(bpy.types.Operator):
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

class loadSettings(bpy.types.Operator):
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

class diffSettings(bpy.types.Operator):
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