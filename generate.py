import pyrosim.pyrosim as pyrosim

# Set output file's name
pyrosim.Start_SDF("world.sdf")

# Define cube dimension variables
length = 1
width = 1
height = 1
# Define first cube position variables
x = 0
y = 0
z = height/2

# Write to output
pyrosim.Send_Cube(name="Box", pos=[x, y, z] , size=[length, width, height])

# Close sdf file
pyrosim.End()