"""
    John Drogo, 2014
    Blender Voxelization Export
    
    Built in blender mods can easily voxelize meshes,
    but few can export this data into a voxel format while
    preserving empty interior space.
    
    This add-on does just that. (Or will soon.)
    Version 0.2a
    
    Reference:
        ideasman42 -> http://blender.stackexchange.com/questions/2776/how-to-read-vertices-of-quad-faces-using-python-api
        blazingsentinal -> http://forums.blockaderunnergame.com/index.php?topic=1411.0
"""

import bpy
import bmesh
import math
import pickle
from bpy.props import StringProperty

bl_info = {
    "name": "Voxel Conversion",
    "category": "Object",
}


class VoxelizeOutput(bpy.types.Operator):
    """Quick Output to Voxel Format"""      # blender will use this as a tooltip for menu items and buttons.
    bl_idname = "object.voxelize"        # unique identifier for buttons and menu items to reference.
    bl_label = "Save Voxelized Mesh"         # display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # enable undo for the operator.
    executionAttempts = 0;
    
    filepath = bpy.props.StringProperty(name="Save Location", description="Where to save the file.", subtype="FILE_PATH")
    #filepath = subtype(StringProperty='FILE_PATH')

    def invoke(self, context, event):
        wm = context.window_manager
        
        if not self.filepath:
            self.filepath = bpy.path.ensure_ext(bpy.data.filepath, ".vox")
            
        wm.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):        # execute() is called by blender when running the operator.

        # The original script
        obj = context.active_object
        bm = bmesh.from_edit_mesh(obj.data)
        
        selectedfaces = []
        cur_coord = 0
        min_coord = [0, 0, 0]
        max_coord = [0, 0, 0]
        sizes = [0, 0, 0]
        
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
            sizes[axis] = max_coord[axis] - min_coord[axis]

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

                if (distance):
                    print( "Mesh not the right size, each voxel should be 1 bu, rescaling to {0}x.".format(1/distance) )
                    bmesh.ops.scale(bm, vec=(1/distance, 1/distance, 1/distance), verts=bm.verts)

                else:
                    #If this fails chances are our distance is zero due to rounding error.
                    #We'll try scalling by a hundred and hope this is enough to resize it on the next run through.

                    print("Mesh is way too small, each voxel should be 1 bu, attempting to scale by to 100x.")
                    bmesh.ops.scale(bm, vec=(100, 100, 100), verts=bm.verts)

                for f in bm.faces:
                    for v in f.verts:
                        #Snap each coord to the nearest voxel corner (integer blender unit).
                        v.co[0] = math.ceil(v.co[0])
                        v.co[1] = math.ceil(v.co[1])
                        v.co[2] = math.ceil(v.co[2])

                #Now let's try that again.
                #First let's clean up this mess.

                #obj = 0 That one is important.
                bm = 0

                selectedfaces = []
                cur_coord = 0
                min_coord = []
                max_coord = []
                sizes = []
        
                volume = {}
                outputvolume = []
        
                axial_coords = []
                axis = 0
        
                distance = 0

                if (self.executionAttempts < 5):
                    self.executionAttempts+=1;
                    return self.execute(context)

                else:
                    #We failed way too many times, something might be wrong.
                    raise Exception("Too many mesh resizes attempted."+\
                        "Try running the command again, check your mesh voxel size"+\
                        " (each voxel should be 1 blender unit), and if that fails please file an issue report on github.")
        
            #Determine where there are voxels.
            else:
                for f in selectedfaces:
                    v = f.calc_center_median_weighted()
                    try:
                        volume[math.floor(v[0])][math.floor(v[1])][math.floor(v[2])] = f.material_index+1
                            
                    except:
                        try:
                            volume[math.floor(v[0])][math.floor(v[1])] = {}
                            volume[math.floor(v[0])][math.floor(v[1])][math.floor(v[2])] = f.material_index+1
                        except:
                            volume[math.floor(v[0])] = {}
                            volume[math.floor(v[0])][math.floor(v[1])] = {}
                            volume[math.floor(v[0])][math.floor(v[1])][math.floor(v[2])] = f.material_index+1
        
        
                print(volume)
                for x in range(int(max_coord[0])-int(min_coord[0])):
                    plane = []
                    for y in range(int(max_coord[1])-int(min_coord[1])):
                        strip = []
                        tracingblock = 0
                        for z in range(int(max_coord[2])-int(min_coord[2])):
                            print(x+min_coord[0], y+min_coord[1], z+min_coord[2])
                            try:
                                if (volume[x+min_coord[0]][y+min_coord[1]][z+min_coord[2]]):
                                    tracingblock = not tracingblock
                            except:
                                pass
        
                            if (tracingblock == 1):
                                try:
                                    strip.append(volume[x+min_coord[0]][y+min_coord[1]][z+min_coord[2]])
                                except:
                                    strip.append(1)
                            else:
                                strip.append(0)
                        plane.append(strip)
                    outputvolume.append(plane)
        
        #Save output.
        with open(self.filepath, "wb") as file:
            pickle.dump(outputvolume, file, 0)
        
        # if you make edits then you need to update at the end
        bmesh.update_edit_mesh(obj.data)

        return {'FINISHED'}            # this lets blender know the operator finished successfully.

def register():
    bpy.utils.register_class(VoxelizeOutput)


def unregister():
    bpy.utils.unregister_class(VoxelizeOutput)


# This allows you to run the script directly from blenders text editor
# to test the addon without having to install it.
if __name__ == "__main__":
    register()
