import bpy

###----PANNEL---

class sceneSettingsPannel(bpy.types.Panel):
    bl_label = "scene settings"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"
    
    def draw(self, context):
        layout = self.layout
        
        row = layout.row(align=False)#layout.column()
        row.prop(bpy.context.scene, "settingsFilePath")

        row = layout.row()
        row.operator("settings.save")
        row = layout.row() #comment this line to but save and load on same line
        row.operator("settings.load")

        row = layout.row()
        row.operator("settings.diff")
        row.split().prop(bpy.context.scene, "settingsStamp")