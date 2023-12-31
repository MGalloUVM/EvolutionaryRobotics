import pyrosim.pyrosim as pyrosim

# Create our world
def Create_World():
    # Set output file's name
    pyrosim.Start_SDF("world.sdf")
    # Define cube dimensions (L, W, H)
    cube_dim = (1, 1, 1)
    # Define cube positions (X, Y, Z)
    cube_pos = (-5, 5, cube_dim[2]/2)
    # Write to output
    pyrosim.Send_Cube(
        name="Obstacle",
        pos=[cube_pos[0], cube_pos[1], cube_pos[2]],
        size=[cube_dim[0], cube_dim[1], cube_dim[2]])
    # Close file
    pyrosim.End()


# Create our Robot
def Create_Robot():
    # Define output file for URDF writing
    pyrosim.Start_URDF("body.urdf")

    # Define dimensions (L, W, H)
    dim = (1, 1, 1)
    # Define positions (X, Y, Z) ABSOLUTE
    pos = (0, 0, 1.5)
    # Write to output
    pyrosim.Send_Cube(
        name="Torso",
        pos=[pos[0], pos[1], pos[2]],
        size=[dim[0], dim[1], dim[2]])
    # Define dimensions (L, W, H)
    dim = (1, 1, 1)
    # Define positions (X, Y, Z) RELATIVE
    pos = (0.5, 0, -0.5)
    # Write to output
    pyrosim.Send_Cube(
        name="FrontLeg",
        pos=[pos[0], pos[1], pos[2]],
        size=[dim[0], dim[1], dim[2]])
    
    # Define dimensions (L, W, H)
    dim = (1, 1, 1)
    # Define positions (X, Y, Z) RELATIVE
    pos = (-0.5, 0, -0.5)
    # Write to output
    pyrosim.Send_Cube(
        name="BackLeg",
        pos=[pos[0], pos[1], pos[2]],
        size=[dim[0], dim[1], dim[2]])

    # Define our Joints
    pyrosim.Send_Joint(
        name = "Torso_FrontLeg",
        parent = "Torso", child = "FrontLeg",
        type = "revolute",
        position = [0.5, 0, 1])
    pyrosim.Send_Joint(
        name = "Torso_BackLeg",
        parent = "Torso", child = "BackLeg",
        type = "revolute",
        position = [-0.5, 0, 1])

    # Close file
    pyrosim.End()


Create_World()
Create_Robot()