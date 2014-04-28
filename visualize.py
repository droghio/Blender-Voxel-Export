#! /usr/bin/python

"""
    John Drogo, 2014
    BVE Visualizer
    
    A simple visualizer for voxels exported with the Blender Voxelizer Exporter.
"""

import pickle
from cube import *

filename = "/Users/John/Desktop/voxelout.vox"
volume = []
queue = []

with open(filename, "rb") as file:
    volume = pickle.load(file)

for x in range(len(volume)):
    for y in range(len(volume[x])):
        for z in range(len(volume[x][y])):
            if (volume[x][y][z] == 1):
                queue.append((x, y, z))

window = Render()
window.pointqueue = queue
window.setup(500)