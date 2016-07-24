bl_info = {
    "name": "Scene Settings",
    "description": "Backup scene and lights settings to a json file to load/compare later",
    "author": "Samuel Bernou, Manuel Rais",
    "version": (0, 0, 1),
    "blender": (2, 77, 0),
    "location": "properties > scene",
    "warning": "This addon is still in development.",
    "wiki_url": "",
    "category": "Object" }

import bpy

##import
from . import operators 
from . import pannel

###----REGISTER---

def register():
    ###properties
    bpy.types.Scene.settingsFilePath = bpy.props.StringProperty(name = "Settings", description = "location for the settings save/load\n", subtype='FILE_PATH')#, default = '%s/SceneSettings.json'%(bpy.path.abspath('//')))
    bpy.types.Scene.settingsStamp = bpy.props.BoolProperty(name = "Stamp changes", description = "add differences between captured settings and current settings to Stamp note (usefull for comparing render)\n", default = False)
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)
    ###properties
    del bpy.types.Scene.settingsFilePath
    del bpy.types.Scene.settingsStamp

if __name__ == "__main__":
    register()