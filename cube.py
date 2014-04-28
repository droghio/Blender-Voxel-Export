#! /usr/bin/python

# This is statement is required by the build system to query build info
if __name__ == '__build__':
	raise Exception

"""
        This code builds on a couple examples included in the PyOpenGL
        Package, original licenses are shown below.
"""



'''
    
    cube.py
    Converted to Python by Jason Petrone 6/00
    
    /*
    * Copyright (c) 1993-1997, Silicon Graphics, Inc.
    * ALL RIGHTS RESERVED
    * Permission to use, copy, modify, and distribute this software for
    * any purpose and without fee is hereby granted, provided that the above
    * copyright notice appear in all copies and that both the copyright notice
    * and this permission notice appear in supporting documentation, and that
    * the name of Silicon Graphics, Inc. not be used in advertising
    * or publicity pertaining to distribution of the software without specific,
    * written prior permission.
    *
    * THE MATERIAL EMBODIED ON THIS SOFTWARE IS PROVIDED TO YOU "AS-IS"
    * AND WITHOUT WARRANTY OF ANY KIND, EXPRESS, IMPLIED OR OTHERWISE,
    * INCLUDING WITHOUT LIMITATION, ANY WARRANTY OF MERCHANTABILITY OR
    * FITNESS FOR A PARTICULAR PURPOSE.  IN NO EVENT SHALL SILICON
    * GRAPHICS, INC.  BE LIABLE TO YOU OR ANYONE ELSE FOR ANY DIRECT,
    * SPECIAL, INCIDENTAL, INDIRECT OR CONSEQUENTIAL DAMAGES OF ANY
    * KIND, OR ANY DAMAGES WHATSOEVER, INCLUDING WITHOUT LIMITATION,
    * LOSS OF PROFIT, LOSS OF USE, SAVINGS OR REVENUE, OR THE CLAIMS OF
    * THIRD PARTIES, WHETHER OR NOT SILICON GRAPHICS, INC.  HAS BEEN
    * ADVISED OF THE POSSIBILITY OF SUCH LOSS, HOWEVER CAUSED AND ON
    * ANY THEORY OF LIABILITY, ARISING OUT OF OR IN CONNECTION WITH THE
    * POSSESSION, USE OR PERFORMANCE OF THIS SOFTWARE.
    *
    * US Government Users Restricted Rights
    * Use, duplication, or disclosure by the Government is subject to
    * restrictions set forth in FAR 52.227.19(c)(2) or subparagraph
    * (c)(1)(ii) of the Rights in Technical Data and Computer Software
    * clause at DFARS 252.227-7013 and/or in similar or successor
    * clauses in the FAR or the DOD or NASA FAR Supplement.
    * Unpublished-- rights reserved under the copyright laws of the
    * United States.  Contractor/manufacturer is Silicon Graphics,
    * Inc., 2011 N.  Shoreline Blvd., Mountain View, CA 94039-7311.
    *
    * OpenGL(R) is a registered trademark of Silicon Graphics, Inc.
    */
    
    '''

#  cube.c
#  This program demonstrates a single modeling transformation,
#  glScalef() and a single viewing transformation, gluLookAt().
#  A wireframe cube is rendered.

import sys
import math

try:
    from OpenGL.GLUT import *
    from OpenGL.GL import *
    from OpenGL.GLU import *
except:
    print '''
        ERROR: PyOpenGL not installed properly.
        '''

class Render:

    (view_rotx,view_roty,view_rotz)=(0.0, 0.0, 0.0)
    view_width, view_height = 500, 500;
    
    pointqueue = []

    def init(self):
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glShadeModel(GL_FLAT)
        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        #glEnable(GL_DEPTH_TEST)
        

    def drawCube(self, x, y, z, size):
        glTranslate(size+x*size, size+y*size, size+z*size)
        glutSolidCube(size)
        glTranslate(-(size+x*size), -(size+y*size), -(size+z*size))


    def drawGrid(self, size):
        glColor3f(.2, .1, .2)
        glLineWidth(.05)
        glBegin(GL_LINES)
        for x in range(self.view_width/size): #draw horizontial lines
            glVertex3f(x*size, 0.0, 0.0)
            glVertex3f(x*size, self.view_height, 0)
            
        for y in range(self.view_height/size): #draw verticle lines
            glVertex3f(0.0, y*size, 0.0)
            glVertex3f(self.view_width, y*size, 0)
        glEnd()


    def display(self):
        
        size = 6; #Universal size for grid spacing/voxel size.
        
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()             # clear the matrix
        glScalef(1.0, 1.0, 1.0)      # modeling transformation

        self.rotateView() #Rotate our reference frame based on keyboard.
        
        light_position = [ 0.0, 0.0, -1.0 ]
        GL_SPOT_CUTOFF = 500
        glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, light_position)
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, (1, 1, 1, .5))

        self.drawGrid(size) #Draw our voxel grid.
        secondaryqueue = [] #A holder for our cursor path.

        #Prepare for the path tracing based on points in the queue.
        glPointSize(3)
        glColor3f(1, .5, .5)
        
        #Move path to the center of the blocks to begin with.
        glTranslate(0, size/2, 0)
        glBegin(GL_POINTS)
        
        #Go through all points in our draw queue.
        #If the points have a size parameter move it to the secondary queue.
        #Otherwise trace our points in a nice salmon color.
        for point in self.pointqueue:
            if (len(point) == 2):
                glVertex3f(point[0]*100, point[1]*100, 0)
            else:
                secondaryqueue.append(point)
        glEnd()
        glTranslate(0, -size/2, 0)
        #Restore the original reference frame.
        
        
        #Prepare for the path tracing of our cursor.
        #Use a nice aqua color.
        glColor3f(0.0, .5, .5)

        #Place our cursor into the grid
        glTranslate(-size/2, -size/2, -size/2)

        #For all our special points (the cursor paths)
        #change the color and trace its path with cubes.
        for point in secondaryqueue:
            self.drawCube(math.floor(point[0]), math.floor(point[1]), math.floor(point[2]), size)
        glTranslate(size/2, size/2, size/2)
        #Restore original reference frame.

        glFlush()


    def rotateView(self):
        #Center our reference frame, rotate view around center
        #then move view back to original position.
        glTranslate(self.view_width/2, self.view_height/2, 0)
        glRotatef(self.view_rotx, 1.0, 0.0, 0.0)
        glRotatef(self.view_roty, 0.0, 1.0, 0.0)
        glRotatef(self.view_rotz, 0.0, 0.0, 1.0)
        glTranslate(-self.view_width/2, -self.view_height/2, 0)


    def reshape(self, w, h):
        #Handle window resizing.
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        #Use orthographic view, we don't want the cubes peaking out from
        #their grid section.
        glOrtho(0, w, 0, h, -h, h)
        glMatrixMode (GL_MODELVIEW)


    # change view angle, exit upon ESC
    def keyboard(self, k, x, y):
        global view_rotz
        
        #Secondary rotation.
        if k == 'z':
            self.view_rotz += 5.0
        elif k == 'Z':
            self.view_rotz -= 5.0
        
        elif ord(k) == 27: # Escape
            sys.exit(0)

        #Primary rotations.
        elif k == 'q':
            self.view_rotz += 5.0
        elif k == 'e':
            self.view_rotz -= 5.0
        elif k == 'w':
            self.view_rotx += 5.0
        elif k == 's':
            self.view_rotx -= 5.0
        elif k == 'a':
            self.view_roty += 5.0
        elif k == 'd':
            self.view_roty -= 5.0
        
        #Reset rotation.
        elif k == 'r':
            self.view_rotx = 0
            self.view_roty = 0
            self.view_rotz = 0
        else:
            return
        glutPostRedisplay()


    # change view angle
    def special(self, k, x, y):
        global view_rotx, view_roty, view_rotz
        
        #Secondary rotation.
        if k == GLUT_KEY_UP:
            self.view_rotx += 5.0
        elif k == GLUT_KEY_DOWN:
            self.view_rotx -= 5.0
        elif k == GLUT_KEY_LEFT:
            self.view_roty += 5.0
        elif k == GLUT_KEY_RIGHT:
            self.view_roty -= 5.0
        else:
            return
        glutPostRedisplay()


    def setup(self, size):
        #Initialize opengl window.
        glutInit(sys.argv)
        glutInitDisplayMode (GLUT_SINGLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize (size, size)
        glutInitWindowPosition (500, 500)
        glutCreateWindow ('Cube')

        #Store window size into render.
        self.view_width = size;
        self.view_height = size;

        #Initialize view and bind event handler functions.
        self.init()
        glutDisplayFunc(self.display)
        glutReshapeFunc(self.reshape)
        glutKeyboardFunc(self.keyboard)
        glutSpecialFunc(self.special)
        glutMainLoop()

