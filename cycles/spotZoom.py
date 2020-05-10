import sys
sys.path.append('/u6/b/eriszhang/BlenderToolbox/cycles')
from include import *
import bpy


for iter in range(17,90):

    frame_idx = iter + 1
    int_length = len(str(frame_idx))
    outputPath = './results/spot/spot'
    for j in range(6-int_length):
        outputPath = outputPath + '0'
    outputPath = outputPath + str(frame_idx) + '.png'


    int_length = len(str(frame_idx))
    num_suffix = ''
    for j in range(6-int_length):
        num_suffix = num_suffix + '0'
    num_suffix = num_suffix + str(frame_idx) + '.obj'


    # # init blender
    imgRes_x = 1280
    imgRes_y = 960
    numSamples = 100
    # imgRes_x = 1575
    # imgRes_y = 1050
    # numSamples = 100 
    exposure = 1.0
    blenderInit(imgRes_x, imgRes_y, numSamples, exposure)

    ###########################################################
    # read mesh: bowl
    meshPath = '../meshes/bowl.obj'
    location = (-1.53134, -0.137405, 0)
    rotation = (90,0,90.1)
    scale = (1.252,1.252,1.252)
    # mesh = readPLY(meshPath, location, rotation, scale)
    mesh = readOBJ(meshPath, location, rotation, scale)

    # # set material
    # colorObj(RGBA, H, S, V, Bright, Contrast)
    stoneRGBA = derekBlue # 255/255.0)
    meshC = colorObj(stoneRGBA, 0.5, 1.0, 1.0, 0.0, 0.0)
    subC = colorObj(stoneRGBA, 0.5, 2.0, 1.0, 0.0, 1.0)
    setMat_ceramic(mesh, meshC, subC)

    # # set shading
    # bpy.ops.object.shade_smooth()
    bpy.ops.object.shade_flat()

    # # subdivision
    level = 2
    subdivision(mesh, level)
    ###########################################################


    # don't need to render bob in the view
    # ###########################################################
    # for i in range(2):
    #     # read mesh: bob
    #     mesh_idx = i + 1
    #     meshPath = '../meshes/spot/bob' + str(mesh_idx) + '' + num_suffix
    #     # meshPath = '../meshes/spot/bob1000100.obj'
    #     location = (0.405266, -0.419702, 0)
    #     rotation = (90,0,104)
    #     scale = (0.283,0.283,0.283)
    #     # scale = (0.344,0.344,0.344) # Input
    #     # mesh = readPLY(meshPath, location, rotation, scale)
    #     mesh = readOBJ(meshPath, location, rotation, scale)

    #     useless = (0,0,0,1)
    #     meshColor = colorObj(useless, 0.5, 1.0, 1.0, 0.0, 0.0)
    #     texturePath = '../meshes/bob_diffuse.png' 
    #     # using relative path gives us weired bug...
    #     setMat_texture(mesh, texturePath, meshColor)

    #     # # set shading
    #     # bpy.ops.object.shade_smooth()
    #     bpy.ops.object.shade_flat()

    #     # # subdivision
    #     level = 2
    #     subdivision(mesh, level)
    # ###########################################################


    # only render two spots in this view
    ###########################################################
    for i in [1,5]:
        # read mesh: spot
        mesh_idx = i
        meshPath = '../meshes/spot/spot' + str(mesh_idx) + '' + num_suffix
        location = (-1.53134, -0.137405, 0)
        rotation = (90,0,90.1)
        scale = (0.783,0.783,0.783)
        # scale = (0.344,0.344,0.344) # Input
        # mesh = readPLY(meshPath, location, rotation, scale)
        mesh = readOBJ(meshPath, location, rotation, scale)

        useless = (0,0,0,1)
        meshColor = colorObj(useless, 0.5, 1.0, 1.0, 0.0, 0.0)
        texturePath = '../meshes/spot_by_keenan.png' 
        # using relative path gives us weired bug...
        setMat_texture(mesh, texturePath, meshColor)

        # # set shading
        # bpy.ops.object.shade_smooth()
        bpy.ops.object.shade_flat()

        # # subdivision
        level = 2
        subdivision(mesh, level)
    ###########################################################


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
    # lightAngle = (-15,-34,-155) 
    # strength = 2
    # shadowSoftness = 0.1
    # sun = setLight_sun(lightAngle, strength, shadowSoftness)
    setLight_threePoints(radius=4, height=10, intensity=2500, softness=8, keyLoc='left')


    # # set ambient light
    ambientColor = (0.2,0.2,0.2,1)
    setLight_ambient(ambientColor)

    # # save blender file
    bpy.ops.wm.save_mainfile(filepath='./test.blend')

    # # save rendering
    renderImage(outputPath, cam)