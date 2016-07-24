from .utils import *
import bpy
import json

def saveSettings(outFilePath):
    '''Save scene settings as json file at given file path'''
    settings = {}
    outfile = open(outFilePath, "w")
    toSave = ['bpy.context.scene', 'bpy.context.scene.render','bpy.context.scene.cycles']
    for zone in toSave:
        settings[zone] = saveAll(Root=zone)

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

def compareSettings(outFilePath, stamping = False):
    '''Get json filepath and print/stamp differences between captured state and current state return a diff dict'''
    outfile = open(outFilePath, "r")
    loadedSettings = json.loads(outfile.read())
    outfile.close()
    newState = saveAll()

    #put difference in a third dict
    diff = {}
    
    for root, attrlist in loadedSettings.items():
        for attr, value in attrlist.items():
            attrPath = '{}.{}'.format(root,attr)
            sceneValue = convertAttr(eval(attrPath))

            if sceneValue != value:
                if type(eval(attrPath)) == type(mathutils.Matrix()):
                    if not compareMatrixList(sceneValue, value):
                        diff[attrPath] = sceneValue
                else:
                    diff[attrPath] = sceneValue

    # print number of properties changed
    if diff:
        print (len(diff), "properties changed:")
        
        stampstr = ''
        for k, v in diff.items():
            print (k, ":", v)
            if stampstr:
                stampstr += ' -- {} : {}'.format(k,v)
            else:
                stampstr += 'TWEAK: {} : {}'.format(k,v)     

        ##add pairs to stamping note
        if stamping:
            # print(stampstr)
            bpy.context.scene.render.stamp_note_text = stampstr #str(diff) #add dict

        return (diff)
    
    ## erase note if nothing has changed
    else:
        print ("nothing changed")
        bpy.context.scene.render.stamp_note_text = ''


def applySettings(outFilePath):
    '''Get json filepath and apply every settings to current scene'''
    outfile = open(outFilePath, "r")
    loadedSettings = json.loads(outfile.read())
    outfile.close()
    for root, attrlist in loadedSettings.items():
        for attr, value in attrlist.items():
            if type(value) == type(['list']) and len(value) == 4: # filter for world matrix
                setattr(eval(root), attr, mathutils.Matrix(value))
            else:    
                try:
                    setattr(eval(root), attr, value)
                    # exec('%s.%s = value'%(root,attr))
                except(AttributeError):
                    print("Unchanged(readOnly)>>", root, attr, value)