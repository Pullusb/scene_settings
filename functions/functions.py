from .utils import *
import bpy
import json

def saveSettings(outFilePath):
    '''Save scene settings as json file at given file path'''
    settings = {}
    outfile = open(outFilePath, "w")
    toSave = ['bpy.context.scene',
                'bpy.context.scene.render',
                'bpy.context.scene.cycles',
                'bpy.context.scene.eevee']
    for zone in toSave:
        settings[zone] = saveAll(Root=zone)

    if bpy.context.scene.backup_lamps:
        for light in bpy.context.scene.objects:
            if light.type == 'LAMP':
                lightPath = "bpy.data.objects['{}']".format(light.name)
                lightDataPath = "bpy.data.objects['{}'].data".format(light.name)
                print("Dump:", lightPath)
                settings[lightPath] = saveAll(lightPath)
                settings[lightDataPath] = saveAll(lightDataPath)

    outfile.write(json.dumps(settings, indent='\t')) #sort_keys=True)
    outfile.close()


def compareMatrixList(one, two):
    '''handle comparison of matrix separately due to change in precision at loading'''
    for x in range(len(one)):
        for y in range(len(one[x])):
            #print ('%.6f' % one[x][y], '%.6f' % two[x][y]) #debug-compare
            if '%.5f' % one[x][y] != '%.5f' % two[x][y]:
                return (False)
    return (True)

PROPNAME_EXCLUDE = ['name_full']

def compareSettings(outFilePath, stamping = False):
    '''Get json filepath
    print/stamp differences between captured state and current state
    Return a diff dict with data_path : (scene value, source value)'''

    with open(outFilePath, "r") as fd:
        loadedSettings = json.loads(fd.read())

    diff = {}
    
    for root, attrlist in loadedSettings.items():
        for attr, value in attrlist.items():
            if attr in PROPNAME_EXCLUDE:
                continue
            attrPath = '{}.{}'.format(root, attr)
            sceneValue = convertAttr(eval(attrPath))

            if sceneValue != value:
                if type(eval(attrPath)) == type(mathutils.Matrix()):
                    if not compareMatrixList(sceneValue, value):
                        diff[attrPath] = (sceneValue, value)
                else:
                    diff[attrPath] = (sceneValue, value)

    # Print number of properties changed
    if diff:
        print (len(diff), "properties changed:")
        
        stampstr = ''
        for k, values in diff.items():
            v = values[0]
            print (k, ":", v)
            if stampstr:
                stampstr += f' -- {k} : {v}'
            else:
                stampstr += f'TWEAK: {k} : {v}'

        ## Add pairs to stamping note
        if stamping:
            bpy.context.scene.render.stamp_note_text = stampstr # str(diff) #add dict

        return diff
    
    ## Erase note if nothing has changed
    else:
        bpy.context.scene.render.stamp_note_text = ''
        print ("Nothing changed")


def apply_from_dict(data_dic, scene=None, debug=False):
    for root, attrlist in data_dic.items():
        ## FIXME quick fix to work on multi-scene
        if scene is not None:
            root = root.replace('bpy.context.scene', f"bpy.data.scenes['{scene.name}']")
        print('\nroot: ', root)
        for attr, value in attrlist.items():
            print(f'apply {attr}, {value}')
            if type(value) == type(['list']) and len(value) == 4: # Filter for world matrix
                try:
                    setattr(eval(root), attr, mathutils.Matrix(value))
                except Exception as e:
                    print("Could not apply >>", root, attr, value)
                    if debug:
                        print(f'{e}\n')
            else:    
                try:
                    setattr(eval(root), attr, value)
                    # exec('%s.%s = value'%(root,attr))
                except Exception as e:
                    print("Could not apply >>", root, attr, value)
                    if debug:
                        print(f'{e}\n')

def applySettings(outFilePath):
    '''Get json filepath and apply every settings to current scene'''
    outfile = open(outFilePath, "r")
    loadedSettings = json.loads(outfile.read())
    outfile.close()
    apply_from_dict(loadedSettings)