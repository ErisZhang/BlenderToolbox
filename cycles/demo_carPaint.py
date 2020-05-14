import sys
sys.path.append('/Users/zhangjiayi/Documents/BlenderToolbox/cycles')
from include import *
import bpy

outputPath = './results/demo_carPaint.png'

# # init blender
imgRes_x = 720 
imgRes_y = 720 
numSamples = 50 
exposure = 1.0
blenderInit(imgRes_x, imgRes_y, numSamples, exposure)

# read mesh 
# meshPath = '../meshes/spot.ply'
meshPath = '../meshes/barSTVK00050.obj'
location = (-0.3, 0.6, -0.04)
rotation = (90, 0,0)
scale = (1.5,1.5,1.5)
# mesh = readPLY(meshPath, location, rotation, scale)
mesh = readOBJ(meshPath, location, rotation, scale)


# # set shading
angle = 10
edgeNormals(mesh, angle)


# # set shading
# bpy.ops.object.shade_smooth()
bpy.ops.object.shade_flat()

# # subdivision
level = 2
subdivision(mesh, level)

# # set material
# colorObj(RGBA, H, S, V, Bright, Contrast)
C1 = colorObj(derekBlue, 0.5, 1.0, 1.0, 0.0, 0.5)
C2 = colorObj(royalBlue, 0.5, 1.0, 1.0, 0.0, 0.0)
setMat_carPaint(mesh, C1, C2)

# # set invisible plane (shadow catcher)
groundCenter = (0,0,0)
shadowDarkeness = 0.7
groundSize = 20
invisibleGround(groundCenter, groundSize, shadowDarkeness)

# # set camera
camLocation = (1.9,2,2.2)
lookAtLocation = (0,0,0.5)
focalLength = 45
cam = setCamera(camLocation, lookAtLocation, focalLength)

# # set sunlight
lightAngle = (-15,-34,-155) 
strength = 2
shadowSoftness = 0.1
sun = setLight_sun(lightAngle, strength, shadowSoftness)

# # set ambient light
ambientColor = (0.2,0.2,0.2,1)
setLight_ambient(ambientColor)

# # save blender file
bpy.ops.wm.save_mainfile(filepath='./test.blend')

# # save rendering
renderImage(outputPath, cam)