import pyrosim.pyrosim as pyrosim

# Give pyrosim location of world data
pyrosim.Start_SDF("box.sdf")
# Stores cube in box file with specifications:
#   x=0, y=0, z=0.5
#   L=1m, W=1m, H=1m
pyrosim.Send_Cube(name="Box", pos=[0,0,0.5] , size=[1,1,1])
# Close sdf file
pyrosim.End()