bl_info = {
    "name": "Scene Settings",
    "description": "Backup scene and lights settings to a json file to load/compare later",
    "author": "Samuel Bernou, Manuel Rais",
    "version": (0, 1, 0),
    "blender": (2, 91, 0),
    "location": "properties > scene",
    "warning": "",
    "doc_url": "https://github.com/Pullusb/SceneSettings",
    "category": "Object" }

import bpy

from . import operators
from . import panel


def register():
    operators.register()
    panel.register()

def unregister():
    panel.unregister()
    operators.unregister()

if __name__ == "__main__":
    register()