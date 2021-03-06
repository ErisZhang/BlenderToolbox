import sys
sys.path.append('/Users/hsuehtil/Dropbox/BlenderToolbox/cycles')
from include import *
import bpy

outputPath = './results/demo_vertexArrowSubset.png'

# # init blender
imgRes_x = 720 
imgRes_y = 720 
numSamples = 50 
exposure = 1.0
blenderInit(imgRes_x, imgRes_y, numSamples, exposure)

# # read mesh 
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

# # set mesh material
meshColor = colorObj((1,1,1,1), 0.5, 1.0, 2.0, 0.5, 0.0)
AOStrength = 0.0
setMat_singleColor(mesh, meshColor, AOStrength)

# creat template arrow mesh
length = 2
location = (1e10, 1e10, 1e10)
rotation = (0,0,0)
scale = (.015,.015,.015)
templateObj = createArrow(length,location,rotation,scale)

# material for the template
meshColor = colorObj(derekBlue, 0.5, 1.0, 1.0, 0.0, 2.0)
AOStrength = 0.0
setMat_singleColor(templateObj, meshColor, AOStrength)

# draw arrows
VIdx = np.arange(100)
VNs = np.zeros((100,3))
for ii in range(VNs.shape[0]):
    VNs[ii,:] = mesh.matrix_world @ mesh.data.vertices[VIdx[ii]].normal
copyArrowToVertex(mesh, templateObj, VIdx, VNs)

# # set invisible plane (shadow catcher)
groundCenter = (0,0,0)
shadowDarkeness = 0.8
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
ambientColor = (0.1,0.1,0.1,1)
setLight_ambient(ambientColor)

# # save blender file
bpy.ops.wm.save_mainfile(filepath='./test.blend')

# # save rendering
renderImage(outputPath, cam)