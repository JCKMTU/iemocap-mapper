"""

    Script to map IEMOCAP motion capture data to Hanson Robotics Sophia Model

"""

import numpy as np
from collections import OrderedDict
import bpy

def initializeBlender():
    #Delete all drivers, so that we have control over SKeys
    ob = bpy.data.objects["head_geo"].data.shape_keys
    drivers_data = ob.animation_data.drivers

    for dr in drivers_data:  
        ob.driver_remove(dr.data_path, -1)
        
def setShapekey(name, value):
    bpy.data.objects["head_geo"].data.shape_keys.key_blocks[name].value = value

def getMarkerPos(name):
    return bpy.data.objects[name].matrix_world.to_translation()

def evaluateShapekeys(keys):
    for key, value in keys.items():
        setShapekey(key, value)
    
    output = OrderedDict()
    
    
    for marker in markers:
        output[marker] = getMarkerPos(marker)
    
    # Normalize around noise point
    ref_vec = output["TNOSE"]
    
    output_array = []
    
    for marker in markers:
        output[marker] -= ref_vec
        output[marker] *= 280 ## Arbitrary scaling to make it more close to training data
        output_array.append(output[marker][0])
        output_array.append(output[marker][1])
        output_array.append(output[marker][2])
    
    return output, output_array
        
# Shapekeys:
shapekeys = []
ob = bpy.data.objects["head_geo"].data.shape_keys.key_blocks
for ke in ob:
   shapekeys.append(ke.name)

#Remove shapekeys we don't need.
shapekeys.remove("Basis")

#Marker positions:
markers = ["CH1", "CH2", "CH3", "FH1", "FH2", "FH3", "LC1", "LC2", "LC3", "LC4", "LC5", "LC6", "LC7", "LC8", "RC1", "RC2", "RC3", "RC4", "RC5", "RC6", "RC7", "RC8", "LLID", "RLID", "MH", "MNOSE", "LNSTRL", "TNOSE", "RNSTRL", "LBM0", "LBM1", "LBM2", "LBM3", "RBM0", "RBM1", "RBM2", "RBM3", "LBR01", "LBR02", "LBR03", "LBR04", "RBR01", "RBR02", "RBR03", "RBR04", "MOU1", "MOU2", "MOU3", "MOU4", "MOU5", "MOU6", "MOU7", "MOU8", "LHD", "RHD"]

initializeBlender()

shp = {}
for key in shapekeys:
    shp[key] = 0

print(evaluateShapekeys(shp))
