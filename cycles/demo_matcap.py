import sys
sys.path.append('/Users/hsuehtil/Dropbox/BlenderToolbox/cycles')
from include import *
import bpy

outputPath = './results/demo_matcap.png'

# # init blender
imgRes_x = 720 
imgRes_y = 720 
numSamples = 50 
exposure = 1.0
blenderInit(imgRes_x, imgRes_y, numSamples, exposure)
# read mesh 
meshPath = '../meshes/spot.ply'
location = (-0.3, 0.6, -0.04)
rotation = (90, 0,0)
scale = (1.5,1.5,1.5)
mesh = readPLY(meshPath, location, rotation, scale)

# # set shading
bpy.ops.object.shade_smooth()
# bpy.ops.object.shade_flat()

# # subdivision
level = 2
subdivision(mesh, level)

# this matcap file you will need to install in blender first
# see the render engine "workbench" or "studio_light"
matcapFile = 'clay_brown.exr'
setMat_matcap(matcapFile)

# # set studio light (for the entire scene)
# colorObj(RGBA, H, S, V, Bright, Contrast)
meshColor = colorObj(derekBlue, 0.5, 1.0, 1.0, 0.0, 2.0)
AOStrength = 0.5
setMat_singleColor(mesh, meshColor, AOStrength)

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