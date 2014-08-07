#! /usr/bin/python

"""
    John Drogo, 2014
    BVE Visualizer
    
    A simple visualizer for voxels exported with the Blender Voxelizer Exporter.
"""

import pickle
from cube import *

filename = ""
volume = []
queue = []

try:
    filename = sys.argv[1]

except:
    filename = raw_input("Filename: ")

with open(filename, "rb") as file:
    volume = pickle.load(file)

for x in range(len(volume)):
    for y in range(len(volume[x])):
        for z in range(len(volume[x][y])):
            if (volume[x][y][z] != 0):
                queue.append((x, y, z, volume[x][y][z]))

window = Render()
window.pointqueue = queue
window.setup(500)
