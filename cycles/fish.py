import sys
sys.path.append('/Users/zhangjiayi/Documents/BlenderToolbox/cycles') # your path to “BlenderToolbox/cycles”
from include import *
import os
cwd = os.getcwd()

'''
MINIMUM RENDER STEPS:
1. copy "tutorial.py" to your preferred local folder
2. In "tutorial.py":
    - change meshPath and readPLY/readOBJ
    - comment out the last line "renderImage"
    - set your desired material (select one from the demo scripts)
3. run "blender --background --python tutorial.py" in terminal, this outputs a "test.blend"
4. open "test.blend" with your blender software
5. In blender UI, adjust:
    - mesh (location, rotation, scale) 
    - material parameters
6. In "tutorial.py":
    - type in the adjust parameters from UI 
    - uncomment the last line "renderImage"
    - set outputPath and increase imgRes_x, imgRes_y, numSamples
7. run "blender --background --python tutorial.py" again to output your final image
'''


# counter the number of files(frames) to render
my_dir = os.listdir('../meshes/fish/') # dir is your directory path
num_files = len(my_dir) - 1


img_idx = [180]

for i in range(len(img_idx)):

    ## initialize blender: rendering set up
    imgRes_x = 1350 # recommend > 2000 (UI: Scene > Output > Resolution X)
    imgRes_y = 990 # recommend > 2000 (UI: Scene > Output > Resolution Y)
    numSamples = 100 # recommend > 200 for paper images (UI: Scene > Render > Sampling > Render)
    exposure = 1.5 # exposure of the entire image (UI: Scene > Render > Film > Exposure)
    blenderInit(imgRes_x, imgRes_y, numSamples, exposure)

    # construct input and output paths
    meshPath = '../meshes/fish/fish'
    outputPath = './results/fish/fish'
    idx = i + 1
    idx = img_idx[i]
    int_length = len(str(idx))
    for j in range(5-int_length):
        meshPath = meshPath + '0'
        outputPath = outputPath + '0'
    meshPath = meshPath + str(idx) + '.obj'
    outputPath = outputPath + str(idx) + '.png'

    ## read mesh (choose either readPLY or readOBJ)
    # meshPath = '../meshes/spot.ply'
    # meshPath = '../meshes/elephant/elephant00001.obj'

    location = (-0.48,0.52,0.2) # (UI: click mesh > Transform > Location)
    rotation = (80, 0, 105) # (UI: click mesh > Transform > Rotation)
    scale = (0.27,0.27,0.27) # (UI: click mesh > Transform > Scale)
    # mesh = readPLY(meshPath, location, rotation, scale)
    mesh = readOBJ(meshPath, location, rotation, scale)

    ###########################################
    ## Set your material here (see other demo scripts)

    ## set shading (choose one of them)
    # bpy.ops.object.shade_smooth() # Option1: Gouraud shading
    # bpy.ops.object.shade_flat() # Option2: Flat shading
    edgeNormals(mesh, angle = 45) # Option3: Edge normal shading

    ## subdivision
    subdivision(mesh, level = 2)

    # # set material
    # colorObj(RGBA, H, S, V, Bright, Contrast)
    useless = (0,0,0,1)
    meshColor = colorObj(useless, 0.5, 1.0, 1.0, 0.0, 0.0)
    texturePath = '../meshes/golden_fish.png' 
    # using relative path gives us weired bug...
    setMat_texture(mesh, texturePath, meshColor)


    ## set invisible plane (shadow catcher): control the brightness of the shadow
    invisibleGround(shadowBrightness=0.8)

    ## set camera (recommend to change mesh instead of camera, unless you want to adjust the Elevation)
    camLocation = (2,1.85,0.32)
    lookAtLocation = (0,0,0.5)
    focalLength = 45 # (UI: click camera > Object Data > Focal Length)
    cam = setCamera(camLocation, lookAtLocation, focalLength)
    # bpy.context.object.data.type = 'ORTHO'

    ## set light
    ## Option1: Three Point Light System (recommended)
    # setLight_threePoints(radius=4, height=10, intensity=2500, softness=8, keyLoc='left')
    ## Option2: simple sun light
    lightAngle = (-45,0,-45)
    strength = 2
    shadowSoftness = 1
    sun = setLight_sun(lightAngle, strength, shadowSoftness)

    ## set ambient light
    setLight_ambient(color=(0.1,0.1,0.1,1)) # (UI: Scene > World > Surface > Color)

    ## set gray shadow to completely white with a threshold (optional)
    alphaThreshold = 0.05
    shadowThreshold(alphaThreshold, interpolationMode = 'CARDINAL')

    ## save blender file so that you can adjust parameters in the UI
    bpy.ops.wm.save_mainfile(filepath='./test.blend')

    ## save rendering
    renderImage(outputPath, cam)