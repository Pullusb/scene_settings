# SPDX-License-Identifier: GPL-2.0-or-later

import bpy

def get_addon_prefs():
    '''function to read current addon preferences properties'''
    import os 
    addon_name = os.path.splitext(__name__)[0]
    preferences = bpy.context.preferences
    addon_prefs = preferences.addons[addon_name].preferences
    return (addon_prefs)


class scene_settings_addon_prefs(bpy.types.AddonPreferences):
    bl_idname = __name__.split('.')[0]

    debug : bpy.props.BoolProperty(
        name='Debug',
        description="Print debug messages in console",
        default=False)

    def draw(self, context):
            layout = self.layout
            layout.prop(self, "debug")

### --- REGISTER ---

classes=(
scene_settings_addon_prefs,
)

def register(): 
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)