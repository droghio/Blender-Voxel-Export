#! /usr/bin/python

print "Loading libraries, this will take a second..."

import pickle
import sys
from pymclevel.schematic import *

volume = []
filename = ""

print "Loading vox file..."

try:
    filename = sys.argv[1]

except:
    filename = raw_input("Filename: ")

with open(filename, "rb") as file:
    volume = pickle.load(file)

creeper = MCSchematic(shape=(100,100,100))

print "Scanning input file..."

try:
	print "  Volume is {0} by {1} by {2} blocks.".format( len(volume), len(volume[0]), len(volume[0][0]) )
except:
	print "WARNING: File was invalid. Try running the exporter again and check your settings."
	exit()

for x in range(len(volume)):
    print "  {0:.2%} completed".format( float(x)/len(volume) )
    for y in range(len(volume[x])):
        for z in range(len(volume[x][y])):
            creeper._Blocks[x][y][z] = volume[x][y][z]

print "  100% complete"

creeper.saveToFile(filename=filename.split(".")[0]+".schematic");
print "File saved to: {0}".format(filename.split(".")[0]+".schematic")
