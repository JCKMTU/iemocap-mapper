import bpy
import time
import numpy as np
import pyswarm as ps

from numpy import genfromtxt
from collections import OrderedDict

# Path to mocap data files.
PATH = '/home/masa/Programming/my_repo/iemocap-mapper/IEMOCAP_full_release/Session3/dialog/MOCAP_rotated/Ses03F_impro01.txt'

# There are 55 markers in IEMOCAP data set.
MARKERS = ["MO_CH1", "MO_CH2", "MO_CH3",
           "MO_FH1", "MO_FH2", "MO_FH3",
           "MO_LC1", "MO_LC2", "MO_LC3", "MO_LC4", "MO_LC5", "MO_LC6", "MO_LC7", "MO_LC8",
           "MO_RC1", "MO_RC2", "MO_RC3", "MO_RC4", "MO_RC5", "MO_RC6", "MO_RC7", "MO_RC8",
           "MO_LLID",
           "MO_RLID",
           "MO_MH", "MO_MNOSE", "MO_LNSTRL", "MO_TNOSE", "MO_RNSTRL",
           "MO_LBM0", "MO_LBM1", "MO_LBM2", "MO_LBM3",
           "MO_RBM0", "MO_RBM1", "MO_RBM2", "MO_RBM3",
           "MO_LBR01", "MO_LBR02", "MO_LBR03", "MO_LBR04",
           "MO_RBR01", "MO_RBR02", "MO_RBR03", "MO_RBR04",
           "MO_MOU1", "MO_MOU2", "MO_MOU3", "MO_MOU4", "MO_MOU5", "MO_MOU6", "MO_MOU7", "MO_MOU8",
           "MO_LHD",
           "MO_RHD"]

ORIG_MARKERS = ["CH1", "CH2", "CH3", "FH1", "FH2", "FH3", "LC1", "LC2", "LC3", "LC4", "LC5", "LC6", "LC7", "LC8", "RC1", "RC2", "RC3", "RC4", "RC5", "RC6", "RC7", "RC8", "LLID", "RLID", "MH", "MNOSE", "LNSTRL", "TNOSE", "RNSTRL", "LBM0", "LBM1", "LBM2", "LBM3", "RBM0", "RBM1", "RBM2", "RBM3", "LBR01", "LBR02", "LBR03", "LBR04", "RBR01", "RBR02", "RBR03", "RBR04", "MOU1", "MOU2", "MOU3", "MOU4", "MOU5", "MOU6", "MOU7", "MOU8", "LHD", "RHD"]


FRAME = 0

# Take mocap data per frame and store in ordered dictionary 'pos'
def load_data(path):
    data = genfromtxt(path, delimiter=" ", skip_header=2)
    return data[:,2:]

def get_pos(data, index):
    pos = OrderedDict()
    i = 0
    for marker in MARKERS:
        one = data[index][i]
        two = data[index][i+1]
        thr = data[index][i+2]
        pos[marker] = Vector((one, two, thr))
        i += 3
    return pos

def get_sophia_marker_pos_at(name):
    return bpy.data.objects[name].matrix_world.to_translation()

def display_sophia_markers_pos():
    for marker in ORIG_MARKERS:
        print(marker, ":", bpy.data.objects[marker].matrix_world.to_translation())

def create_marker_obj(size, name, coord):
    tnose_coord = bpy.data.objects['TNOSE'].matrix_world.to_translation()
    coord = coord + tnose_coord

    bpy.ops.mesh.primitive_ico_sphere_add(
        subdivisions=2,
        size=size,
        view_align=False,
        enter_editmode=False,
        location=coord,
        rotation=(0,0,0))

    ob = bpy.context.active_object
    ob.name = name
    ob.scale = Vector((0.1, 0.1, 0.1))
    me = ob.data
    me.name = name

    return ob

def create_markers(data):
    pos = get_pos(data, 0)
    for marker in MARKERS:
        pos[marker] = pos[marker] / 100
        create_marker_obj(.15, marker, pos[marker])
    global FRAME
    FRAME += 1

def remove_markers():
    bpy.ops.object.select_all(action='DESELECT')
    for marker in MARKERS:
        bpy.data.objects[marker].select = True
        bpy.ops.object.delete()

def move_markers_x(num):
    for marker in MARKERS:
        ob = bpy.data.objects[marker]
        ob.location = Vector((ob.location.x, ob.location.y - num, ob.location.z))
    bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
    bpy.context.scene.update()


# Get to 5 frame ahead and update location of markers
def forward():
    global FRAME
    print("curent fame is %d", FRAME)
    data = load_data(PATH, FRAME)
    for marker in MARKERS:
        ob = bpy.data.objects[marker]
        ob.location = (data[marker])
    FRAME += 5

def play(data):
    rows = data.shape

    for _ in range(rows[0]):
        print("Frame: %d", _)
        i = 0
        for marker in MARKERS:
            tnose_coord = bpy.data.objects['TNOSE'].matrix_world.to_translation()
            ob = bpy.data.objects[marker]
            ob.location = Vector((data[_][i], data[_][i+1], data[_][i+2])) / 100 + tnose_coord
            i += 3
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
        bpy.context.scene.update()

# Get max pos of axis.
def get_max(data):
    x_high = 0
    y_high = 0
    z_high = 0
    pos = data
    for marker in MARKERS:
        if x_high < abs(pos.x): x_high = pos[marker].x
        if y_high < abs(pos.y): y_high = pos[marker].y
        if z_high < abs(pos.z): z_high = pos[marker].z
    return x_high, y_high, z_high

#def create_circle_obj():
#    bpy.ops.mesh.primitive_ico_sphere_add(
#        subdivisions=1,
#        size=.25,
#        view_align=False,
#        enter_editmode=False,
#        location=Vector((-.75, 0, 0.6512970924377441)),
#        rotation=(0,0,0))
#    ob = bpy.context.active_object
#    ob.name = 'Circle'
#    ob.show_name = True
#    me = ob.data
#    me.name = 'Circle mesh'
#    return ob
