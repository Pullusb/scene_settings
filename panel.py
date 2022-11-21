import bpy

###----PANNEL---

class SST_PT_sceneSettingsPanel(bpy.types.Panel):
    bl_label = "Scene Settings"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"
    
    def draw(self, context):
        layout = self.layout
        
        row = layout.row(align=False)
        row.prop(bpy.context.scene, "settingsFilePath")

        row = layout.row()
        row.operator("settings.save")
        row = layout.row()
        row.operator("settings.load")
        row.operator("settings.apply_multi_scene")

        row = layout.row()
        row.operator("settings.diff")
        row.split().prop(bpy.context.scene, "settingsStamp")
        row = layout.row()
        row.prop(bpy.context.scene, "backup_lamps")


def register():
    bpy.utils.register_class(SST_PT_sceneSettingsPanel)

def unregister():
    bpy.utils.unregister_class(SST_PT_sceneSettingsPanel)
