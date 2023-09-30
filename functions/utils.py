import bpy
import mathutils
import numpy as np

def convertAttr(Attr):
    '''Convert given value to a Json serializable format'''
    if type(Attr) in [type(mathutils.Vector()),type(mathutils.Color())]:
        if len(Attr) == 3:
            return([Attr[0],Attr[1],Attr[2]])
        elif len(Attr) == 1:
            return([Attr[0]])
        elif len(Attr) == 4:
            return([Attr[0],Attr[1],Attr[2],Attr[3]])
    elif type(Attr) == type(mathutils.Matrix()):
        return (np.matrix(Attr).tolist())
    else:
        return(Attr)

def compareMatrixList(one, two):
    '''handle comparison of matrix separately due to change in precision at loading'''
    for x in range(len(one)):
        for y in range(len(one[x])):
            #print ('%.6f' % one[x][y], '%.6f' % two[x][y]) #debug-compare
            if '%.5f' % one[x][y] != '%.5f' % two[x][y]:
                return (False)
    return (True)

EXCLUDES = [
    'name',
    'bl_rna','identifier','name_property',
    'rna_type','properties', 'stamp_note_text','use_stamp_note',
    'settingsFilePath', 'settingsStamp', 'select',
    'matrix_local', 'matrix_parent_inverse', 'matrix_basis', 
    'location',
    'rotation_euler', 'rotation_quaternion', 'rotation_axis_angle',
    'scale']

def saveAll(Root="bpy.context.scene"):
    '''iterate over given destination and return a dict containing every attribute'''

    print(f'\n\n{Root}\n')
    Dic={}
    for attr in dir(eval(Root)):
        if not attr.startswith('__')  and attr not in EXCLUDES:
            try:
                value = getattr(eval(Root),attr)
            except AttributeError:
                value = None
            if value != None:
                if not callable(value):
                    if type(value) in [type(0),type(0.0),type(True),type('str'),type(mathutils.Vector()),type(mathutils.Color()), type(mathutils.Matrix())]:
                        print(attr)
                        Dic[attr] = convertAttr(value)
                    #else:
                    #    print(attr,value,type(value))
                    #    Dic[attr] = saveAll(Root='%s.%s'%(Root,attr),Dic=Dic)
    return(Dic)

    ## scan loop over scene objects
#    for i in bpy.context.scene.objects:
#        print(json.dumps(saveAll(Root='bpy.context.scene.objects["%s"]'%i.name),indent='\t'))


def show_message_box(_message = "", _title = "Message Box", _icon = 'INFO'):
    '''Show message box with element passed as string or list
    if _message if a list of lists:
        if sublist have 2 element:
            considered a label [text, icon]
        if sublist have 3 element:
            considered as an operator [ops_id_name, text, icon]
        if sublist have 4 element:
            considered as a property [object, propname, text, icon]
    '''

    def draw(self, context):
        layout = self.layout
        for l in _message:
            if isinstance(l, str):
                layout.label(text=l)
            elif len(l) == 2: # label with icon
                layout.label(text=l[0], icon=l[1])
            elif len(l) == 3: # ops
                layout.operator_context = "INVOKE_DEFAULT"
                layout.operator(l[0], text=l[1], icon=l[2], emboss=False) # <- highligh the entry
            elif len(l) == 4: # prop
                row = layout.row(align=True)
                row.label(text=l[2], icon=l[3])
                row.prop(l[0], l[1], text='') 
    
    if isinstance(_message, str):
        _message = [_message]
    bpy.context.window_manager.popup_menu(draw, title = _title, icon = _icon)