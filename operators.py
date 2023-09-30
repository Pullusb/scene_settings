import bpy
import os
from pathlib import Path
from .functions.functions import *
from .functions.utils import show_message_box

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

'''
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
        
        out_file_path = Path(outfile)
        if not out_file_path.exists() or not out_file_path.is_file():
            self.report({'ERROR'}, "No file to load")
            return {'CANCELLED'}

        diff = compareSettings(outfile, stamping = bpy.types.Scene.settingsStamp)
        if diff:
            self.report({'INFO'}, f"{len(diff)} Changes (see console)")
            prop_list = [f'{k} : {v}' for k, v in diff.items()]            
            show_message_box(prop_list, 'Changes')
        else:
            self.report({'INFO'}, "No changes")

        return {"FINISHED"}
'''


class SST_OT_diff_settings(bpy.types.Operator):
    bl_idname = "settings.diff"
    bl_label = "compare Settings"
    bl_description = "Print differences between saved and current settings"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def invoke(self, context, event):
        if bpy.context.scene.settingsFilePath:
            outfile = bpy.context.scene.settingsFilePath
        else:
            outfile = os.path.join(bpy.path.abspath('//'), 'SceneSettings.json')
        
        out_file_path = Path(outfile)
        if not out_file_path.exists() or not out_file_path.is_file():
            self.report({'ERROR'}, "No file to load")
            return {'CANCELLED'}

        self.diff = compareSettings(outfile, stamping = bpy.types.Scene.settingsStamp)
        if self.diff:
            self.report({'INFO'}, f"{len(self.diff)} Changes (see console)")
            # prop_list = [f'{k} : {v[1]} -> {v[0]}}' for k, v in diff.items()]            
            # show_message_box(prop_list, 'Changes')
            return context.window_manager.invoke_props_dialog(self, width=1000)
        else:
            self.report({'INFO'}, "No changes")
        
        return {"FINISHED"}

    def draw(self, context):
        # t0 = time.time()
        layout = self.layout
        # layout.use_property_split = True
        col = layout.column()
        
        col.label(text=f'{len(self.diff)} differences')

        for k, v in self.diff.items():
            scene_val = v[0]
            source_val = v[1]

            row = col.row()
            
            ## Source value
            data_path_box = row.box()
            data_path_box.label(text=str(k))

            ## separate prop name (data_path tail)
            src_val_box = row.box()
            src_val_box.label(text=str(source_val))

            prop_path, prop_name = k.rsplit('.', 1)
            # source_val = eval(k)
            is_equal = eval(k) == source_val
            
            ## Set col
            # set_cell = set_col.box()
            if is_equal:
                ## Revert to scene value
                icon = 'FRAME_PREV'
                val_to_set = json.dumps(scene_val)
            else:
                ## Set source value
                icon = 'RIGHTARROW'
                val_to_set = json.dumps(source_val)

            op = row.operator('settings.set_value', text='', icon=icon) # ARROW_LEFTRIGHT
            op.prop_path = prop_path
            op.prop_name = prop_name
            op.value = val_to_set

            ## Show current value as text (useful ? we have already the prop at the end)
            # current_value_cell = current_value_col.box()
            # current_value_cell = row.box()
            # current_value_cell.label(text=str(scene_val))

            # prop_cell = row.box()
            row.prop(eval(prop_path), prop_name)
            
            # ok_cell = row.box()
            ## Show when equal
            if is_equal:
                row.label(text='', icon='CHECKMARK')
            else:
                row.label(text='', icon='BLANK1')

    def execute(self, context):
        return {"FINISHED"}

class SST_OT_set_value(bpy.types.Operator):
    bl_idname = "settings.set_value"
    bl_label = "Set Property Value"
    bl_description = "Set the value of passed attribute"
    bl_options = {'REGISTER', 'INTERNAL'}

    prop_path : bpy.props.StringProperty(options={'SKIP_SAVE'})
    prop_name : bpy.props.StringProperty(options={'SKIP_SAVE'})
    value : bpy.props.StringProperty(options={'SKIP_SAVE'})

    def execute(self, context):
        setattr(eval(self.prop_path), self.prop_name, json.loads(self.value))
        return {"FINISHED"}

classes = (
    SST_OT_set_value,
    SST_OT_dump_settings,
    SST_OT_load_settings,
    SST_OT_diff_settings,
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    bpy.types.Scene.settingsFilePath = bpy.props.StringProperty(
        name = "Settings", 
        description = "location for the settings save/load\n", 
        subtype='FILE_PATH') #, default = '%s/SceneSettings.json'%(bpy.path.abspath('//')))
    
    bpy.types.Scene.settingsStamp = bpy.props.BoolProperty(
        name = "Stamp changes", 
        description = "add differences between captured settings and current settings to Stamp note (usefull for comparing render)\n",
    default = False)
    
    bpy.types.Scene.backup_lamps = bpy.props.BoolProperty(
        name = "Backup Lamps", 
        description = "Backup the lamps object of the scene",
    default = False)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

    del bpy.types.Scene.settingsFilePath
    del bpy.types.Scene.settingsStamp
    del bpy.types.Scene.backup_lamps