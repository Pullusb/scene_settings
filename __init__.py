bl_info = {
    "name": "Scene Settings",
    "description": "Backup scene and lights settings to a json file to load/compare later",
    "author": "Samuel Bernou, Manuel Rais",
    "version": (0, 2, 0),
    "blender": (2, 91, 0),
    "location": "properties > scene",
    "warning": "",
    "doc_url": "https://github.com/Pullusb/SceneSettings",
    "category": "Object" }

import bpy

from . import operators
from . import OP_copy_to_other_scenes
from . import panel


def register():
    operators.register()
    OP_copy_to_other_scenes.register()
    panel.register()

def unregister():
    panel.unregister()
    OP_copy_to_other_scenes.unregister()
    operators.unregister()

if __name__ == "__main__":
    register()