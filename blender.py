"""

    Script to map IEMOCAP motion capture data to Hanson Robotics Sophia Model

"""

def initializeBlender():
    #Delete all drivers, so that we have control over SKeys
    ob = bpy.data.objects["Sophia"].data.shape_keys
    drivers_data = ob.animation_data.drivers

    for dr in drivers_data:  
        ob.driver_remove(dr.data_path, -1)
        
def setShapekey(name, value):
    bpy.data.objects["Sophia"].data.shape_keys.key_blocks[name].value = value

def getMarkerPos(name):
    bpy.data.objects[name].matrix_world.to_translation()

def evaluateShapekeys(keys):
    for key, value in keys:
        setShapekey(key, value)
    
    output = {}
    
    for marker in markers:
        output[marker] = getMarkerPos(marker)
        
    return output
        
# Shapekeys:
shapekeys = []
ob = bpy.data.objects["Sophia"].data.shape_keys.key_blocks
for ke in ob:
   shapekeys.append(ke.name)

#Remove shapekeys we don't need.
shapekeys.remove("Basis")
shapekeys.remove("Shrinkwrap")
shapekeys.remove("adjustments")

#Marker positions:
markers = ["CH1", "CH2", "CH3", "FH1", "FH2", "FH3", "LC1", "LC2", "LC3", "LC4", "LC5", "LC6", "LC7", "LC8", "RC1", "RC2", "RC3", "RC4", "RC5", "RC6", "RC7", "RC8", "LLID", "RLID", "MH", "MNOSE", "LNSTRL", "TNOSE", "RNSTRL", "LBM0", "LBM1", "LBM2", "LBM3", "RBM0", "RBM1", "RBM2", "RBM3", "LBRO1", "LBRO2", "LBRO3", "LBRO4", "RBRO1", "RBRO2", "RBRO3", "RBRO4", "Mou1", "Mou2", "Mou3", "Mou4", "Mou5", "Mou6", "Mou7", "Mou8", "LHD ", "RHD"]


