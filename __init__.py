# SPDX-License-Identifier: GPL-2.0-or-later

bl_info = {
    "name": "Scene Settings",
    "description": "Backup scene and lights settings to a json file to load/compare later",
    "author": "Samuel Bernou, Manuel Rais",
    "version": (0, 3, 0),
    "blender": (3, 0, 0),
    "location": "properties > scene",
    "warning": "",
    "doc_url": "https://github.com/Pullusb/SceneSettings",
    "category": "Object" }

import bpy

from . import preferences
from . import operators
from . import OP_copy_to_other_scenes
from . import panel

mods = (
    preferences,
    operators,
    OP_copy_to_other_scenes,
    panel,
)

def register():
    for mod in mods:
        mod.register()

def unregister():
    for mod in reversed(mods):
        mod.unregister()

if __name__ == "__main__":
    register()