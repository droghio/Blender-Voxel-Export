"""
    John Drogo, 2014
    Blender Voxelization Export
    
    Built in blender mods can easily voxelize meshes,
    but few can export this data into a voxel format while
    preserving empty interior space.
    
    This add-on does just that. (Or will soon.)
    Version 0.1a
    
    Reference:
        ideasman42 -> http://blender.stackexchange.com/questions/2776/how-to-read-vertices-of-quad-faces-using-python-api
        blazingsentinal -> http://forums.blockaderunnergame.com/index.php?topic=1411.0
"""

import bpy
import bmesh
import math
import pickle

obj = bpy.context.active_object
bm = bmesh.from_edit_mesh(obj.data) 

selectedfaces = []
cur_coord = 0
min_coord = [0, 0, 0]
max_coord = [0, 0, 0]

volume = {}
outputvolume = []

axial_coords = []
axis = 1

distance = 0

for axis in range(3):

    #Find the voxel levels in our search axis.
    #Also find the start coord
    for f in bm.faces:
        for v in f.verts:
            #print(v.co)
            if (axial_coords.count(v.co[axis]) == 0):
                axial_coords.append(v.co[axis])

    axial_coords.sort()

    min_coord[axis] = axial_coords[0]
    max_coord[axis] = axial_coords[-1]
    print(min_coord[axis])

    #Find all planes down our search axis.
    for coord in axial_coords:
        if (axis != 2):
            break

        cur_coord = math.trunc((coord)*10**4)/10**4

        #For all faces in our current search plane.
        for f in bm.faces:
            f.select = False
            faceinplane = True
            #print(f.nomal())
            
            #Determine if all verticies are in our search plane.
            for v in f.verts:
                if (math.trunc(v.co[axis]*10**4)/10**4 != cur_coord):
                    faceinplane = False

            #If so add the face to our list of faces to select.
            if (faceinplane):
                selectedfaces.append(f)


#So long as there is one face along our search axis.
if (len(selectedfaces) > 0):
    distance = math.trunc(abs(axial_coords[0] - axial_coords[1])*10**4)/10**4
    print("Distance:", distance)

    #Select all faces in our axis in the edit window.
    for face in selectedfaces:
        face.select = True

    #If the voxels are not square and properly sized, resize them.
    print(len(selectedfaces))
    if (distance != 1):
        bmesh.ops.scale(bm, vec=(1/distance, 1/distance, 1/distance), verts=bm.verts)
        for f in bm.faces:
            for v in f.verts:
                v.co[0] = math.ceil(v.co[0])
                v.co[1] = math.ceil(v.co[1])
                v.co[2] = math.ceil(v.co[2])

    #Determine where there are voxels.
    else:
        for f in selectedfaces:
            v = f.calc_center_median_weighted()
            try:
                volume[math.floor(v[0])][math.floor(v[1])][math.floor(v[2])] = 1
                    
            except:
                try:
                    volume[math.floor(v[0])][math.floor(v[1])] = {}
                    volume[math.floor(v[0])][math.floor(v[1])][math.floor(v[2])] = 1
                except:
                    volume[math.floor(v[0])] = {}
                    volume[math.floor(v[0])][math.floor(v[1])] = {}
                    volume[math.floor(v[0])][math.floor(v[1])][math.floor(v[2])] = 1


        print(volume)
        for x in range(int(max_coord[0])-int(min_coord[0])):
            plane = []
            for y in range(int(max_coord[1])-int(min_coord[1])):
                strip = []
                tracingblock = 0
                for z in range(int(max_coord[2])-int(min_coord[2])):
                    print(x+min_coord[0], y+min_coord[1], z+min_coord[2])
                    try:
                        if (volume[x+min_coord[0]][y+min_coord[1]][z+min_coord[2]] == 1):
                            tracingblock = not tracingblock
                    except:
                        pass

                    if (tracingblock == 1):
                        strip.append(1)
                    else:
                        strip.append(0)
                plane.append(strip)
            outputvolume.append(plane)

with open("/Users/John/Desktop/voxelout.vox", "wb") as file:
    pickle.dump(outputvolume, file, 0)


# if you make edits then you need to update at the end
bmesh.update_edit_mesh(obj.data)