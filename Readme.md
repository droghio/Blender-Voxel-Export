Blender-Voxel-Export
===============

***Minecraft schematic exporter for Blender.***


###SAMPLES

![photo 1](https://cloud.githubusercontent.com/assets/3069222/3851794/cd97339a-1e9b-11e4-8d70-db5bb01fb514.JPG)


###PREREQUISITES

You need Blender 2.68+ installed on your system.
You also need BOTH python2 and python3.

For BOTH installs you need pickle (should be installed by default), numpy, and yaml.
If you install MCEdit many of these requirements should be filled.

        sudo yum install python3-numpy

        sudo yum install numpy #Fedora
        sudo port install py-numpy #Mac
        sudo apt-get install python-numpy #Debian/Ubuntu


###SETUP

You'll need to install the module into blender.

After you download the project you'll need to compress it into a zip. (Or just download the zip from github.)

Now fireup blender, go to File > User Preferences > Add-ons, and on the bottom bar click the button that says "Load From File".
Now point blende to the zip file.

Blender should detect a module called "Object: Voxel Conversion", check it and then click "Save User Preferences" in the bottom bar.

That's it!
  
  
  
###Running

So this part is a little tricky.

There are two ways to use this program, and each way has different abilities.
```
Most people will want to quickly import their creations, so to use the simpler mode:
    1. Make your blender structure.
    2. Once you are finished go under modifiers, add a Remesh modifier (it's under the Generators column), and change its mode to "Block".
    3. Tweak the settings, this is what your structure will look like in Minecraft, then click "Appy". (THIS WILL PREMENTLY CHANGE YOUR MODEL, MAKE A COPY FIRST!)
    4. Select your structure and hit tab to go into "Edit" mode.
    5. Hit the space button and type "Save Voxelized Mesh" and hit enter. (If this didn't work make sure you installed the module correctly.)
    6. Choose an output file location, DO NOT CHANGE THE .vox FILE EXTENSION!!! We'll fix that later.
    7. Hit enter and wait, the ui will lock up for a few seconds. The larger your structure the longer the wait, but even for crazy large landscapes (1000x1000x300+) it only takes a few minutes. For a 50x50x50 structure it should only take about 10 seconds.
```
So now you should have a .vox file, well now we need to change that to a schematic.
In the project download there is a script called voxtomcedit.py, run it with a python2 interpriter, usually:
        python ./voxtomcedit.py path_to_vox.vox
        
Although it might be something like python2.7, python2, etc.

It will give a few status messages and create a .schematic of your file in the same location as the .vox.

YAY! Now you have a nice shiny schematic!
From here I would use MCEdit to import the file into the world file of your choice.

This is a cool and **pretty** quick way to get your structures into Minecraft, but it does have several shortcommings.
```
   Pros:
       +Great for monument structures or walls.
       +Easy to do!

   Cons:
       +You will not be able to save different materials.
       +Only the object's shell will be saved.

There is a more advanced method: you can build pre-voxeled structures.

    Pros:
       +Different materials will be saved as different blocks.
       +The structure will be imported EXACTLY into Minecraft.
       +Great for rapid construction of complex buildings.
       +Small details are preserved, and interior walls/passageways are also preserved.

    Cons:
       +Harder.
       +You need to build in a particular way.
 ```

###Details

This method is complex so I'll probably need to throw a youtube video together, but here are the basics...

First some background, in case you haven't realized my script doesn't actually voxelize anything... [shocked]
What it does instead is disect a voxelized mesh and record where the voxels are, and saves this as a pickled python array to the .vox file.
(That's why we needed to apply the Remesh modifier in the above steps, to actually voxelize the mesh.)

We then use the voxtomcedit script to turn that pickled array into a schematic file.

You might be asking why on earth did I split up the program into two parts, and the answer is simple: there are two pythons.

To make my life easier I used the same libraries as MCEdit to handle the schematic creation, (pymclevel for those intereseted).
Problem is this is written in Python2, Blender uses exclusively Python3.

Inshort 2 != 3, and after spending 2 hours trying to update pymclevel it just wasn't worth it.

Now with that in mind...


###Advanced Export
```
As I said above we have two options to actually voxelize our mesh:
   +Automatically (as shown above)
   +Or manually.
```
Manually modeling a voxel structure might seem like a cop out, but hey it works.

The exporter scans the structure from the top down. When it hits a face in that lies in the xy place it either starts recording a voxel, changes the voxel column's color, or stops recording voxels.

If this is the first face detected in the voxel column it will create a block with an id or 1 (Stone), or based on the Material name. If the face has a material applied to it with a name formatted as "AnythingYouWant.Blockid" then the "Blockid" will become the voxel's block id.

For example if I wanted a dirt block I would create a face that lies in the xy plane, and give it a material named "DirtFloor.3".
You can create multiple materials that all share the same "Blockid". This makes it easier to sort out parts of more complex structures.

Now it the exporter continues down the voxel column and hits a face with a different material it starts placing voxels based on that new material.
The exporter will stop placing voxels if it encounters a face in the voxel column with the same material as the voxels it is already creating, and will resume placing again once it hits the next face.

Now that I've bored you to depth time for some ascii examples!

Let's say my work of art will be a dirt block stacked on a stone brick (creative I know).

I would make a structure in Blender that looks like this.
```
z+   ----- < Has a material called "Roof.3"
|    |   | < There is no face in the xy plane here!
|    ----- < Has a material called "Mid.1".
|    |   |
|    ----- < Has a material called "Floor.1".
y---------x+
```

Notice we don't care about faces in the zy or yx planes, if you want leave them in, leave them out for a speed bump, they will be ignored in the export.

That brick is nice, but let's get something a little more complex, like a bridge.
```
z+   -------- < Has a material called "Roof.1"
|    |  __  | < Also has a material called "Roof.1"
|    | |  | |
|    --    -- < Has a material called "Floor.1".
|
y---------x+

```
Or even a valnia chocolate dounut.
```
z+   -------- < Has a material called "Roof.49"
|    |  __  | < Also has a material called "RoofRingInner.48"
|    | |  | |
|    --    -- < Has a material called "Midway.12".
|    | |  | |
|    |  __  | < Also has a material called "FloorRingInner.12"
|    |      |
|    -------- < Has a material called "Floor.12"
|
y---------x+
```

Some tips, turn on "Snap control in Blender" (Cntrl+Tab) by pressing the magnent icon in the 3d view toolbar, and set increments to grid units.
Use grids sized to 1bu per voxel.

Always extrude, or use cntrl d.

Make sure your spacing in the x y and z dimensions is all the same, this is best when you use 1bu per voxel.
Make sub-parts in different layers and merge them together at the very end.
Use different material names, the material select/deselect is very handy.

Work on ortho mode with block transperancy on, it makes the process a lot easier.

This is a lot, but it is wayyyy easier then placing each block one by one in survival.
I'll update the guide once I make the tutorials, and I'll throw in some examples at some point.

Have fun!

