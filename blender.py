"""

    Script to map IEMOCAP motion capture data to Hanson Robotics Sophia Model

"""

import numpy as np
from numpy import genfromtxt
from collections import OrderedDict
from pyswarm import pso
import bpy
from time import sleep

def sigmoid(x):
  return 1.0 / (1.0 + np.exp(-x))

def calcVecToOthers(M, m):
    refPoint = Vector((M[(m*3)], M[(m*3)+1], M[(m*3)+2]))
    
    # Get Max distance for normalization:
    maxDist = 0.0
    for i in range(int(len(M)/3)):
        if m != i:
            point = Vector((M[(i*3)], M[(i*3)+1], M[(i*3)+2]))
            dist = np.sqrt(np.power(refPoint[0] - point[0],2) + np.power(refPoint[1] - point[1],2) + np.power(refPoint[2] - point[2],2))
            if dist > maxDist:
                maxDist = dist

    # Output Vector
    outputVec = Vector((0,0,0))
    for i in range(int(len(M)/3)):
        if m != i:
            point = Vector((M[(i*3)], M[(i*3)+1], M[(i*3)+2]))
            diff = (refPoint - point) / maxDist
            diff += Vector((0.00001, 0.00001, 0.00001))
            outputVec += Vector((1/diff[0], 1/diff[1], 1/diff[2]))
    
    return outputVec


def fitness(A, B):
    # Input is lists of XYZXYZ,...
    assert(len(A) == len(B))
    
    fitness = 0
    
    for i in range(int(len(A)/3)):
        vecA = calcVecToOthers(A, i)
        vecB = calcVecToOthers(B, i)
        fitness =+ np.sqrt(np.power(vecA[0] - vecB[0],2) + np.power(vecA[1] - vecB[1],2) + np.power(vecA[2] - vecB[2],2))
        
    return fitness
    
def loadData(path):
    data = genfromtxt(path, delimiter=" ", skip_header=2)
    return data[:,2:]

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
    
    # Important: update
    bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
    bpy.context.scene.update()

    output = OrderedDict()
    
    for marker in markers:
        output[marker] = getMarkerPos(marker)
    
    # Normalize around noise point
    ref_vec = output["TNOSE"]
    
    output_array = []
    
    for marker in markers:
        #output[marker] -= ref_vec
        #output[marker] *= 100 ## Arbitrary scaling to make it more close to training data
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

data = loadData('/home/ralf/HR/IEMOCAP/IEMOCAP_full_release/Session3/dialog/MOCAP_rotated/Ses03F_impro01.txt')

data_frame = data[1]

"""
def model(data, theta):
    weights = theta.reshape([len(data), -1])
    return sigmoid(np.matmul(data, weights))

def banana(theta):
    #assert(len(theta) == len(shapekeys))
    frame = [np.nan]
    
    while np.isnan(np.sum(frame)):
        frame = data[np.random.randint(1,data.shape[0])]
    
    evaluation = model(frame, theta)
    
    shp = {}
    for i, key in enumerate(shapekeys):
        shp[key] = evaluation[i]
    
    _, output = evaluateShapekeys(shp)
    
    return fitness(output, frame)
"""    

def banana(theta):
    #assert(len(theta) == len(shapekeys))
    frame = data[170]
    
    shp = {}
    for i, key in enumerate(shapekeys):
        shp[key] = theta[i]
    
    _, output = evaluateShapekeys(shp)
    
    return -fitness(output, frame)
    
    
        
#lb = np.zeros(len(shapekeys))
#lb = np.ones(nrOfWeights) * 0.0
#ub = np.ones(nrOfWeights) * 1.0

lb = np.zeros(len(shapekeys))
ub = np.ones(len(shapekeys))

#pso(banana, lb, ub)


"""
shp = {}
for key in shapekeys:
    shp[key] = np.random.rand()
output = evaluateShapekeys(shp)[1]
print("fitness %f" % fitness(output, data[1]))
"""