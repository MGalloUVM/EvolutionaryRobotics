import pyrosim.pyrosim as pyrosim

# Set output file's name
pyrosim.Start_SDF("boxes.sdf")

# Create tower of cubes
for x in range(5):
    for y in range(5):
        # Define cube dimension variables
        length = 1
        width = 1
        height = 1
        # Define first cube position variables
        z = height/2
        for _ in range(10):
            # Write to output
            pyrosim.Send_Cube(name="Box", pos=[x, y, z] , size=[length, width, height])
            # Set our 'ground level' for next cube to the top of the next cube
            z += height/2

            # Multiply scale by 0.9
            length *= .9
            width *= .9
            height *= .9

            # Add half of our new height to place the cube directly in the correct position
            z += height/2

# Close sdf file
pyrosim.End()