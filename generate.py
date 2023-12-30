import pyrosim.pyrosim as pyrosim

# Set output file's name
pyrosim.Start_SDF("box.sdf")

# Define cube dimension variables
length = 1
width = 2
height = 3
# Define cube position variables
x = 0
y = 0
z = height/2
# Write cube to output
pyrosim.Send_Cube(name="Box", pos=[x, y, z] , size=[length, width, height])

# Close sdf file
pyrosim.End()