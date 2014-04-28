"""
    John Drogo, 2014
    Blender Voxelization Export
    
    Built in blender mods can easily voxelize meshes,
    but few can export this data into a voxel format while
    preserving empty interior space.
    
    This add-on does just that.
    Version 0.1a
    
    Reference:
        ideasman42 -> http://blender.stackexchange.com/questions/2776/how-to-read-vertices-of-quad-faces-using-python-api
"""

import bpy
import bmesh
import math

obj = bpy.context.active_object
bm = bmesh.from_edit_mesh(obj.data) 

selectedfaces = []
cur_coord = 0
min_coord = 0
min_coord = 0

axial_coords = []
axis = 1

distance = 0

#Find the voxel levels in our search axis.
#Also find the start coord
for f in bm.faces:
    for v in f.verts:
        print(v.co)
        if (axial_coords.count(v.co[axis]) == 0):
            axial_coords.append(v.co[axis])

sort(axial_coords)
min_coord = axial_coords[0]
max_coor = axial_coords[-1]


#Find all faces in our search plane.
for coord in axial_coords:
    axial_coord = math.trunc((coord)*10**4)/10**4

    for f in bm.faces:
        f.select = False
        faceinplane = True
        #print(f.nomal())
        #Determine if all vectors are in our search plane.
        for v in f.verts:
            if (math.trunc(v.co[axis]*10**4)/10**4 != cur_coord):
                faceinplane = False         
        if (faceinplane):
            selectedfaces.append(f)

#So long as there is one face in our search plane.
if (len(selectedfaces) > 0):
    distance = math.trunc(abs(axial_coords[0] - axial_coords[1])*10**4)/10**4
    print("Distance:", distance)

    #Select all faces in our plane in the edit window.
    for face in selectedfaces:
        face.select = True

    if (distance != 1):
        bmesh.ops.scale(bm, vec=(1/distance, 1/distance, 1/distance), verts=bm.verts)
        for f in bm.faces:
            for v in f.verts:
                v.co[0] = math.ceil(v.co[0])
                v.co[1] = math.ceil(v.co[1])
                v.co[2] = math.ceil(v.co[2])
                
# if you make edits then you need to update at the end
bmesh.update_edit_mesh(obj.data)